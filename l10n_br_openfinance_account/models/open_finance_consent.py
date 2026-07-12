from odoo import models, fields, api, _
from odoo.exceptions import UserError


class OpenFinanceConsent(models.Model):
    _inherit = 'open.finance.consent'

    def action_sync_statement(self):
        self.ensure_one()
        if self.scope not in (
            'read_extrato_pf', 'read_extrato_pj',
            'read_extrato_pix', 'read_extrato_payment_pix',
            'read_all_pf', 'read_all_pj',
        ):
            raise UserError(_(
                'Este consentimento não possui permissão para leitura de extratos.'))
        statement = self.env['open.finance.statement'].create({
            'config_id': self.config_id.id,
            'consent_id': self.id,
            'journal_ids': [(6, 0, self.journal_ids.ids)],
            'date_from': fields.Date.today(),
            'date_to': fields.Date.today(),
        })
        statement.with_context(async_exec=False).action_fetch_statement()
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'open.finance.statement',
            'res_id': statement.id,
            'view_mode': 'form',
        }
