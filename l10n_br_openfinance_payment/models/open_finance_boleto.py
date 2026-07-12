from odoo import models, fields, api, _
from odoo.exceptions import UserError


class OpenFinanceBoleto(models.Model):
    _name = 'open.finance.boleto'
    _description = 'Boleto Bancário Open Finance'
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

    state = fields.Selection([
        ('draft', 'Rascunho'),
        ('registered', 'Registrado'),
        ('paid', 'Pago'),
        ('cancelled', 'Cancelado'),
        ('overdue', 'Vencido'),
        ('failed', 'Falhou'),
    ], string='Estado', default='draft', required=True, tracking=True)

    nosso_numero = fields.Char(string='Nosso Número', readonly=True)
    nosso_numero_formatado = fields.Char(string='Nosso Número Formatado', readonly=True)
    linha_digitavel = fields.Char(string='Linha Digitável', readonly=True)
    codigo_barras = fields.Char(string='Código de Barras', readonly=True)
    barcode_data = fields.Char(string='Dados do Código de Barras', readonly=True)

    amount = fields.Monetary(string='Valor', required=True, tracking=True)
    currency_id = fields.Many2one(
        'res.currency', string='Moeda',
        default=lambda self: self.env.company.currency_id)

    partner_id = fields.Many2one(
        'res.partner', string='Pagador', required=True,
        domain=[('active', '=', True)])
    partner_name = fields.Char(string='Nome do Pagador', related='partner_id.display_name')
    partner_document = fields.Char(string='CPF/CNPJ', related='partner_id.vat')
    partner_email = fields.Char(string='E-mail', related='partner_id.email')

    invoice_id = fields.Many2one(
        'account.move', string='Fatura',
        domain=[('move_type', 'in', ('out_invoice', 'out_receipt'))])
    payment_id = fields.Many2one('account.payment', string='Pagamento')

    date_issue = fields.Date(string='Data de Emissão', default=fields.Date.today, required=True)
    date_due = fields.Date(string='Data de Vencimento', required=True)
    date_discount = fields.Date(string='Data Limite para Desconto')
    date_paid = fields.Datetime(string='Data do Pagamento', readonly=True)
    interest_rate = fields.Float(string='Taxa de Juros %', default=0.0)
    fine_rate = fields.Float(string='Taxa de Multa %', default=0.0)

    description = fields.Text(string='Descrição')

    instructions = fields.Text(
        string='Instruções de Pagamento',
        default='Não receber após o vencimento.')

    boleto_pdf = fields.Binary(string='Boleto PDF', readonly=True)
    boleto_pdf_filename = fields.Char(string='Nome do Arquivo', readonly=True)

    recipient_account = fields.Char(string='Conta do Beneficiário')
    recipient_agency = fields.Char(string='Agência do Beneficiário')

    bank_code = fields.Char(string='Código do Banco')
    bank_name = fields.Char(string='Nome do Banco')

    wallet = fields.Char(string='Carteira')

    api_log_ids = fields.One2many(
        'open.finance.api.log', 'boleto_id',
        string='Logs de API')

    @api.depends('partner_name', 'amount', 'state')
    def _compute_display_name(self):
        for r in self:
            r.display_name = f'Boleto {r.partner_name or "N/D"} - R$ {r.amount:.2f} [{r.state}]'

    @api.constrains('amount')
    def _check_amount(self):
        for r in self:
            if r.amount <= 0:
                raise UserError(_('O valor do boleto deve ser positivo.'))

    @api.model
    def _cron_check_pending_boletos(self):
        boletos = self.search([('state', 'in', ('registered', 'overdue'))])
        for boleto in boletos:
            try:
                api = boleto.config_id._get_api_client()
                result = api.check_boleto_status(boleto)
                new_state = result.get('state')
                if new_state and new_state != boleto.state:
                    boleto.write({'state': new_state})
            except Exception:
                continue

    def action_register_boleto(self):
        self.ensure_one()
        if self.state != 'draft':
            raise UserError(_('Apenas rascunhos podem ser registrados.'))
        self.write({'state': 'registered'})
        try:
            api = self.config_id._get_api_client()
            result = api.register_boleto(self)
            self.write({
                'nosso_numero': result.get('nosso_numero'),
                'nosso_numero_formatado': result.get('nosso_numero_formatado'),
                'linha_digitavel': result.get('linha_digitavel'),
                'codigo_barras': result.get('codigo_barras'),
                'barcode_data': result.get('barcode_data'),
                'state': 'registered',
            })
            if result.get('pdf_base64'):
                self.write({
                    'boleto_pdf': result.get('pdf_base64'),
                    'boleto_pdf_filename': f'boleto_{self.nosso_numero or self.id}.pdf',
                })
        except Exception as e:
            self.write({'state': 'failed'})
            raise UserError(_('Erro ao registrar boleto: %s') % str(e))

    def action_print_boleto(self):
        self.ensure_one()
        if not self.boleto_pdf:
            raise UserError(_('Boleto ainda não foi registrado ou PDF não disponível.'))
        return {
            'type': 'ir.actions.act_url',
            'url': f'/web/content/{self._name}/{self.id}/boleto_pdf/{self.boleto_pdf_filename}',
            'target': 'new',
        }

    def action_check_payment_status(self):
        self.ensure_one()
        if self.state not in ('registered', 'overdue'):
            raise UserError(_('Boleto não está pendente de pagamento.'))
        api = self.config_id._get_api_client()
        try:
            result = api.check_boleto_status(self)
            new_state = result.get('state')
            if new_state:
                self.write({
                    'state': new_state,
                    'date_paid': result.get('date_paid') or fields.Datetime.now() if new_state == 'paid' else False,
                })
        except Exception as e:
            raise UserError(_('Erro ao verificar status: %s') % str(e))

    def action_cancel(self):
        self.ensure_one()
        if self.state not in ('draft', 'registered'):
            raise UserError(_('Boleto não pode ser cancelado neste estado.'))
        api = self.config_id._get_api_client()
        try:
            api.cancel_boleto(self)
            self.write({'state': 'cancelled'})
        except Exception as e:
            raise UserError(_('Erro ao cancelar boleto: %s') % str(e))

    def action_create_from_invoice(self):
        invoice = self.env['account.move'].browse(self.env.context.get('active_id'))
        if invoice and invoice.move_type in ('out_invoice', 'out_receipt'):
            vals = {
                'partner_id': invoice.partner_id.id,
                'amount': invoice.amount_residual or invoice.amount_total,
                'invoice_id': invoice.id,
                'date_due': invoice.invoice_date_due or fields.Date.today(),
                'description': invoice.name or invoice.ref or '',
            }
            if invoice.partner_id.bank_ids:
                bank = invoice.partner_id.bank_ids[0]
                vals.update({
                    'recipient_account': bank.acc_number,
                })
            return {
                'type': 'ir.actions.act_window',
                'res_model': 'open.finance.boleto',
                'view_mode': 'form',
                'context': {'default_%s' % k: v for k, v in vals.items()},
            }
