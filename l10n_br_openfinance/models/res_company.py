from odoo import models, fields


class ResCompany(models.Model):
    _inherit = 'res.company'

    open_finance_config_ids = fields.One2many(
        'open.finance.config', 'company_id',
        string='Configurações Open Finance')

    open_finance_consent_ids = fields.One2many(
        'open.finance.consent', 'company_id',
        string='Consentimentos Open Finance')
