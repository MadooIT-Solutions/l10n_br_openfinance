from odoo import models, fields, api, _


class OpenFinanceConfig(models.Model):
    _inherit = 'open.finance.config'

    statement_ids = fields.One2many(
        'open.finance.statement', 'config_id',
        string='Extratos Importados')

    total_statements = fields.Integer(
        compute='_compute_total_statements', string='Total Extratos')

    @api.depends('statement_ids')
    def _compute_total_statements(self):
        for r in self:
            r.total_statements = len(r.statement_ids)

    def action_open_statements(self):
        return {
            'type': 'ir.actions.act_window',
            'name': _('Extratos'),
            'res_model': 'open.finance.statement',
            'domain': [('config_id', '=', self.id)],
            'context': {'default_config_id': self.id},
            'view_mode': 'list,form',
        }
