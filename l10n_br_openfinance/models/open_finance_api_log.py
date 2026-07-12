from odoo import models, fields, api


class OpenFinanceApiLog(models.Model):
    _name = 'open.finance.api.log'
    _description = 'Log de Requisições Open Finance'
    _order = 'create_date desc'
    _rec_name = 'display_name'

    display_name = fields.Char(compute='_compute_display_name', store=True)
    config_id = fields.Many2one(
        'open.finance.config', string='Configuração',
        required=True, ondelete='cascade')

    consent_id = fields.Many2one(
        'open.finance.consent', string='Consentimento',
        ondelete='set null')
    statement_id = fields.Many2one(
        'open.finance.statement', string='Extrato',
        ondelete='set null')
    pix_id = fields.Many2one(
        'open.finance.pix', string='Pix',
        ondelete='set null')
    boleto_id = fields.Many2one(
        'open.finance.boleto', string='Boleto',
        ondelete='set null')

    method = fields.Char(string='Método HTTP', required=True)
    endpoint = fields.Char(string='Endpoint', required=True)
    request_data = fields.Text(string='Dados da Requisição')
    response_status = fields.Integer(string='Status HTTP')
    response_data = fields.Text(string='Resposta')
    state = fields.Selection([
        ('requested', 'Requisição Enviada'),
        ('success', 'Sucesso'),
        ('error', 'Erro'),
    ], string='Estado', default='requested', required=True)

    @api.depends('method', 'endpoint', 'response_status', 'state')
    def _compute_display_name(self):
        for r in self:
            r.display_name = (
                f'{r.method} {r.endpoint} '
                f'- {r.response_status or "..."} [{r.state}]'
            )
