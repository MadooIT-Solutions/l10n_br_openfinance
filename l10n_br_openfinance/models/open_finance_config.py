from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class OpenFinanceConfig(models.Model):
    _name = 'open.finance.config'
    _description = 'Configuração Open Finance por Instituição'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'display_name'
    _order = 'company_id, institution_name'

    display_name = fields.Char(compute='_compute_display_name', store=True)
    company_id = fields.Many2one(
        'res.company', string='Empresa',
        default=lambda self: self.env.company, required=True)
    active = fields.Boolean(default=True)

    institution_name = fields.Char(
        string='Instituição Financeira', required=True,
        help='Nome da instituição (ex: Banco do Brasil, Itaú, Bradesco)')
    institution_cnpj = fields.Char(string='CNPJ da Instituição')

    environment = fields.Selection([
        ('sandbox', 'Sandbox (Homologação)'),
        ('production', 'Produção'),
    ], string='Ambiente', default='sandbox', required=True)

    certificate_id = fields.Many2one(
        'l10n_br_fiscal.certificate', string='Certificado A1/A3',
        tracking=True)

    client_id = fields.Char(
        string='Client ID', tracking=True,
        help='Client ID fornecido pela instituição para autenticação OAuth2')
    client_secret = fields.Char(
        string='Client Secret', tracking=True)

    api_base_url = fields.Char(
        string='URL Base API',
        default='https://api.sandbox.openfinance.com.br',
        help='URL base da API Open Finance da instituição')
    auth_url = fields.Char(
        string='URL de Autorização',
        help='URL para autorização OAuth2/consentimento')
    token_url = fields.Char(
        string='URL do Token',
        help='URL para obtenção do token OAuth2')

    color = fields.Integer(string='Color Index')

    @api.depends('institution_name', 'environment')
    def _compute_display_name(self):
        for r in self:
            env_label = dict(r._fields['environment'].selection).get(r.environment, r.environment)
            r.display_name = f'{r.institution_name} [{env_label}]'

    @api.constrains('api_base_url')
    def _check_api_url(self):
        for r in self:
            if r.api_base_url and not r.api_base_url.startswith('https://'):
                raise ValidationError(_('A URL base da API deve usar HTTPS.'))

    def test_connection(self):
        self.ensure_one()
        api = self._get_api_client()
        try:
            result = api.health_check()
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': _('Sucesso'),
                    'message': _('Conexão com Open Finance estabelecida com sucesso!'),
                    'sticky': False,
                    'type': 'success',
                }
            }
        except Exception as e:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': _('Erro na Conexão'),
                    'message': str(e),
                    'sticky': True,
                    'type': 'danger',
                }
            }

    def _get_api_client(self):
        self.ensure_one()
        return self.env['open.finance.api'].create({'config_id': self.id})
