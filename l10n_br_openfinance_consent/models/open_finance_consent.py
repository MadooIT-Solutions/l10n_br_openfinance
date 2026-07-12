import base64
from odoo import models, fields, api, _
from odoo.exceptions import UserError


class OpenFinanceConsent(models.Model):
    _name = 'open.finance.consent'
    _description = 'Consentimento Open Finance'
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

    person_type = fields.Selection([
        ('pf', 'Pessoa Física'),
        ('pj', 'Pessoa Jurídica'),
    ], string='Tipo de Pessoa', default='pf', required=True,
        help='Define se o consentimento é para pessoa física (PF) ou jurídica (PJ)')

    consent_id = fields.Char(
        string='ID do Consentimento',
        help='Identificador único do consentimento no Open Finance')
    status = fields.Selection([
        ('draft', 'Rascunho'),
        ('requested', 'Solicitado'),
        ('authorized', 'Autorizado'),
        ('active', 'Ativo'),
        ('expired', 'Expirado'),
        ('revoked', 'Revogado'),
        ('rejected', 'Rejeitado'),
    ], string='Status', default='draft', required=True, tracking=True)

    scope = fields.Selection([
        ('read_extrato_pf', 'Leitura de Extrato (PF)'),
        ('read_extrato_pj', 'Leitura de Extrato (PJ)'),
        ('read_extrato_pix', 'Leitura de Extrato Pix'),
        ('read_cadastro_pf', 'Leitura de Dados Cadastrais (PF)'),
        ('read_cadastro_pj', 'Leitura de Dados Cadastrais (PJ)'),
        ('payment_pix', 'Pagamento Pix'),
        ('payment_boleto', 'Pagamento Boleto'),
        ('read_extrato_payment_pix', 'Extrato + Pagamento Pix'),
        ('read_all_pf', 'Leitura Completa (PF)'),
        ('read_all_pj', 'Leitura Completa (PJ)'),
    ], string='Escopo de Permissão', required=True, default='read_extrato_pf')

    permissions = fields.Text(
        string='Permissões (JSON)',
        help='Detalhes das permissões em formato JSON')

    journal_ids = fields.Many2many(
        'account.journal', string='Diários',
        domain=[('type', 'in', ('bank', 'cash'))],
        help='Diários financeiros cobertos por este consentimento')

    partner_id = fields.Many2one(
        'res.partner', string='Cliente/Titular',
        help='Titular da conta que autorizou o compartilhamento')

    cpf_cnpj = fields.Char(
        string='CPF/CNPJ do Titular',
        help='CPF (PF) ou CNPJ (PJ) do titular da conta')

    qr_code = fields.Binary(
        string='QR Code', readonly=True,
        help='QR Code para autorização via app do banco')
    qr_code_text = fields.Text(
        string='Conteúdo do QR Code', readonly=True,
        help='Payload para gerar o QR Code de autorização')
    qr_code_url = fields.Char(
        string='URL de Autorização', readonly=True,
        help='URL para autorização (pode ser convertida em QR Code)')

    date_requested = fields.Datetime(string='Data da Solicitação')
    date_authorized = fields.Datetime(string='Data da Autorização')
    date_expiration = fields.Datetime(
        string='Data de Expiração',
        help='Data em que o consentimento expira')
    date_revoked = fields.Datetime(string='Data de Revogação')

    access_token = fields.Text(
        string='Access Token', readonly=True,
        groups='base.group_system')
    refresh_token = fields.Text(
        string='Refresh Token', readonly=True,
        groups='base.group_system')
    token_expiry = fields.Datetime(
        string='Expiração do Token', readonly=True)

    api_log_ids = fields.One2many(
        'open.finance.api.log', 'consent_id',
        string='Logs de API')

    notes = fields.Text(string='Observações')

    @api.depends('config_id.institution_name', 'person_type', 'scope', 'status')
    def _compute_display_name(self):
        for r in self:
            person_label = dict(r._fields['person_type'].selection).get(r.person_type, r.person_type)
            scope_label = dict(r._fields['scope'].selection).get(r.scope, r.scope)
            status_label = dict(r._fields['status'].selection).get(r.status, r.status)
            r.display_name = (
                f'{r.config_id.institution_name} - {scope_label}'
                f' ({person_label}) [{status_label}]'
            )

    def action_request_consent(self):
        self.ensure_one()
        api = self.config_id._get_api_client()
        try:
            result = api.request_consent(self)
            self.write({
                'consent_id': result.get('consent_id'),
                'status': 'requested',
                'qr_code_url': result.get('qr_code_url'),
                'qr_code_text': result.get('qr_code_text'),
                'date_requested': fields.Datetime.now(),
                'date_expiration': result.get('expiration_date'),
            })
            if result.get('qr_code_text'):
                self._generate_qr_code()
        except Exception as e:
            raise UserError(_('Erro ao solicitar consentimento: %s') % str(e))

    def _generate_qr_code(self):
        self.ensure_one()
        try:
            import qrcode
            from io import BytesIO
            qr = qrcode.QRCode(version=1, box_size=10, border=4)
            qr.add_data(self.qr_code_text)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")
            buffer = BytesIO()
            img.save(buffer, format='PNG')
            self.qr_code = base64.b64encode(buffer.getvalue())
        except ImportError:
            self.qr_code = base64.b64encode(
                self.qr_code_text.encode()
            )
        except Exception:
            pass

    def action_check_status(self):
        self.ensure_one()
        if not self.consent_id:
            raise UserError(_('Consentimento ainda não foi solicitado.'))
        api = self.config_id._get_api_client()
        try:
            result = api.check_consent_status(self.consent_id)
            new_status = result.get('status')
            if new_status and new_status != self.status:
                self.write({'status': new_status})
                if new_status == 'authorized':
                    self.date_authorized = fields.Datetime.now()
            if result.get('access_token'):
                self.write({
                    'access_token': result['access_token'],
                    'refresh_token': result.get('refresh_token'),
                    'token_expiry': result.get('token_expiry'),
                })
        except Exception as e:
            raise UserError(_('Erro ao verificar status: %s') % str(e))

    def action_revoke(self):
        self.ensure_one()
        if self.status not in ('authorized', 'active'):
            raise UserError(_('Apenas consentimentos ativos podem ser revogados.'))
        api = self.config_id._get_api_client()
        try:
            api.revoke_consent(self.consent_id)
            self.write({
                'status': 'revoked',
                'date_revoked': fields.Datetime.now(),
            })
        except Exception as e:
            raise UserError(_('Erro ao revogar consentimento: %s') % str(e))

    def action_refresh_token(self):
        self.ensure_one()
        if not self.refresh_token:
            raise UserError(_('Não há refresh token disponível.'))
        api = self.config_id._get_api_client()
        try:
            result = api.refresh_access_token(self.refresh_token)
            self.write({
                'access_token': result.get('access_token'),
                'refresh_token': result.get('refresh_token', self.refresh_token),
                'token_expiry': result.get('token_expiry'),
            })
        except Exception as e:
            raise UserError(_('Erro ao renovar token: %s') % str(e))


