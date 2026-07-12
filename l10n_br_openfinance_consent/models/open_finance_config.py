from odoo import models, fields, api, _


class OpenFinanceConfig(models.Model):
    _inherit = 'open.finance.config'

    consent_ids = fields.One2many(
        'open.finance.consent', 'config_id',
        string='Consentimentos')

    active_consent_count = fields.Integer(
        compute='_compute_active_consent_count', string='Consentimentos Ativos')

    @api.depends('consent_ids.status')
    def _compute_active_consent_count(self):
        for r in self:
            r.active_consent_count = len(r.consent_ids.filtered(lambda c: c.status == 'authorized'))

    def action_open_consents(self):
        return {
            'type': 'ir.actions.act_window',
            'name': _('Consentimentos'),
            'res_model': 'open.finance.consent',
            'domain': [('config_id', '=', self.id)],
            'context': {'default_config_id': self.id},
            'view_mode': 'list,form',
        }
