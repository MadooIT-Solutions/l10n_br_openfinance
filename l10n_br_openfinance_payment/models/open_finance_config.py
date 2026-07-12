from odoo import models, fields, api, _


class OpenFinanceConfig(models.Model):
    _inherit = 'open.finance.config'

    pix_ids = fields.One2many(
        'open.finance.pix', 'config_id',
        string='Transações Pix')

    total_pix = fields.Integer(
        compute='_compute_total_pix', string='Total Pix')

    @api.depends('pix_ids')
    def _compute_total_pix(self):
        for r in self:
            r.total_pix = len(r.pix_ids)

    def action_open_pix(self):
        return {
            'type': 'ir.actions.act_window',
            'name': _('Transações Pix'),
            'res_model': 'open.finance.pix',
            'domain': [('config_id', '=', self.id)],
            'context': {'default_config_id': self.id},
            'view_mode': 'list,form',
        }
