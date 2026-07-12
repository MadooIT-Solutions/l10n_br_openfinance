from odoo import models, fields


class AccountJournal(models.Model):
    _inherit = 'account.journal'

    open_finance_consent_ids = fields.Many2many(
        'open.finance.consent', string='Consentimentos')
