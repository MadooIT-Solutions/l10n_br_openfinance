import base64

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class OpenFinancePix(models.Model):
    _name = 'open.finance.pix'
    _description = 'Transação Pix Open Finance'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc'
    _rec_name = 'display_name'

    display_name = fields.Char(compute='_compute_display_name', store=True)
    config_id = fields.Many2one(
        'open.finance.config', string='Configuração',
        required=True, ondelete='cascade')
    company_id = fields.Many2one(
        'res.company', string='Empresa',
        related='config_id.company_id', store=True)

    consent_id = fields.Many2one(
        'open.finance.consent', string='Consentimento',
        domain=[('scope', 'in', ('payment_pix', 'read_extrato_payment_pix', 'read_all_pf', 'read_all_pj')),
                ('status', 'in', ('authorized', 'active'))])

    type = fields.Selection([
        ('recebido', 'Recebido'),
        ('enviado', 'Enviado'),
        ('devolucao', 'Devolução'),
    ], string='Tipo', default='recebido', required=True)

    direction = fields.Selection([
        ('in', 'Entrada'),
        ('out', 'Saída'),
    ], string='Direção', compute='_compute_direction', store=True)

    state = fields.Selection([
        ('draft', 'Rascunho'),
        ('pending', 'Pendente'),
        ('completed', 'Concluído'),
        ('failed', 'Falhou'),
        ('cancelled', 'Cancelado'),
        ('refunded', 'Devolvido'),
    ], string='Estado', default='draft', required=True, tracking=True)

    pix_key = fields.Char(string='Chave Pix')
    pix_key_type = fields.Selection([
        ('cpf', 'CPF'),
        ('cnpj', 'CNPJ'),
        ('email', 'E-mail'),
        ('phone', 'Telefone'),
        ('evp', 'Chave Aleatória'),
    ], string='Tipo de Chave')

    txid = fields.Char(string='TxID', readonly=True)
    end_to_end_id = fields.Char(
        string='End-to-End ID', readonly=True)

    emv = fields.Text(string='EMV / QR Code Payload')
    qr_code_image = fields.Binary(
        string='QR Code', readonly=True,
        help='QR Code para pagamento')
    qr_code_text = fields.Text(
        string='Conteúdo do QR Code', readonly=True)

    amount = fields.Monetary(
        string='Valor', required=True, tracking=True)
    currency_id = fields.Many2one(
        'res.currency', string='Moeda',
        default=lambda self: self.env.company.currency_id)

    description = fields.Char(string='Descrição')

    partner_id = fields.Many2one(
        'res.partner', string='Contraparte')
    partner_name = fields.Char(string='Nome do Contraparte')
    partner_document = fields.Char(string='CPF/CNPJ')
    partner_bank_id = fields.Many2one(
        'res.partner.bank', string='Conta Bancária')

    date_requested = fields.Datetime(string='Data da Solicitação')
    date_confirmed = fields.Datetime(string='Data da Confirmação')
    date_settlement = fields.Datetime(string='Data da Liquidação')

    payment_id = fields.Many2one(
        'account.payment', string='Pagamento Odoo')
    invoice_id = fields.Many2one(
        'account.move', string='Fatura',
        domain=[('move_type', 'in', ('out_invoice', 'out_receipt', 'in_invoice', 'in_receipt'))])

    api_log_ids = fields.One2many(
        'open.finance.api.log', 'pix_id',
        string='Logs de API')

    notes = fields.Text(string='Observações')

    @api.depends('partner_name', 'amount', 'state')
    def _compute_display_name(self):
        for r in self:
            partner = r.partner_name or r.partner_id.display_name or 'N/D'
            r.display_name = f'Pix {partner} - R$ {r.amount:.2f} [{r.state}]'

    @api.depends('type')
    def _compute_direction(self):
        for r in self:
            r.direction = 'in' if r.type in ('recebido', 'devolucao') else 'out'

    def action_generate_qr_code(self):
        self.ensure_one()
        if not self.emv:
            raise UserError(_('Gere o payload EMV primeiro.'))
        try:
            import qrcode
            from io import BytesIO
            qr = qrcode.QRCode(version=1, box_size=10, border=4)
            qr.add_data(self.emv)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")
            buffer = BytesIO()
            img.save(buffer, format='PNG')
            self.qr_code_image = base64.b64encode(buffer.getvalue())
        except ImportError:
            raise UserError(_('Biblioteca qrcode não instalada. Execute: pip install qrcode[pil]'))

    def action_send_pix(self):
        self.ensure_one()
        if self.state != 'draft':
            raise UserError(_('Apenas rascunhos podem ser enviados.'))
        if not self.consent_id:
            raise UserError(_('Selecione um consentimento com permissão Pix.'))
        self.write({'state': 'pending', 'date_requested': fields.Datetime.now()})
        try:
            api = self.config_id._get_api_client()
            result = api.send_pix(self)
            self.write({
                'state': 'completed',
                'txid': result.get('txid'),
                'end_to_end_id': result.get('end_to_end_id'),
                'date_confirmed': fields.Datetime.now(),
                'date_settlement': result.get('settlement_date'),
            })
        except Exception as e:
            self.write({'state': 'failed'})
            raise UserError(_('Erro ao enviar Pix: %s') % str(e))

    def action_check_status(self):
        self.ensure_one()
        if not self.end_to_end_id and not self.txid:
            raise UserError(_('Transação ainda não possui identificador.'))
        api = self.config_id._get_api_client()
        try:
            result = api.check_pix_status(self)
            if result.get('status'):
                self.write({'state': result['status']})
        except Exception as e:
            raise UserError(_('Erro ao verificar status: %s') % str(e))

    def action_create_account_payment(self):
        self.ensure_one()
        if self.payment_id:
            raise UserError(_('Pagamento já foi criado.'))
        if self.state != 'completed':
            raise UserError(_('Apenas transações concluídas podem gerar pagamentos.'))
        payment_vals = {
            'payment_type': 'inbound' if self.direction == 'in' else 'outbound',
            'partner_id': self.partner_id.id or self._find_or_create_partner(),
            'amount': abs(self.amount),
            'currency_id': self.currency_id.id,
            'ref': self.end_to_end_id or self.txid or '',
        }
        payment = self.env['account.payment'].create(payment_vals)
        payment.action_post()
        self.payment_id = payment
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'account.payment',
            'res_id': payment.id,
            'view_mode': 'form',
        }

    def _find_or_create_partner(self):
        if self.partner_id:
            return self.partner_id.id
        if self.partner_document:
            partner = self.env['res.partner'].search([
                ('vat', '=', self.partner_document)
            ], limit=1)
            if partner:
                self.partner_id = partner
                return partner.id
        if self.partner_name:
            partner = self.env['res.partner'].create({
                'name': self.partner_name,
                'vat': self.partner_document or '',
                'is_company': len(self.partner_document or '') > 11 if self.partner_document else False,
            })
            self.partner_id = partner
            return partner.id
        return False

