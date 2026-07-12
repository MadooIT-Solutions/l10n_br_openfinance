from odoo import models, fields


class ResCompany(models.Model):
    _inherit = 'res.company'

    open_finance_config_ids = fields.One2many(
        'open.finance.config', 'company_id',
        string='Configurações Open Finance')
