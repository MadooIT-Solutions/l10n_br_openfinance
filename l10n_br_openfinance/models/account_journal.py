from odoo import models, fields


class AccountJournal(models.Model):
    _inherit = 'account.journal'

    open_finance_config_ids = fields.Many2many(
        'open.finance.config', string='Configurações Open Finance')

    open_finance_bank_code = fields.Char(
        string='Código do Banco',
        help='Código do banco para cobrança (ex: 001, 341, 237)')
    open_finance_wallet = fields.Char(
        string='Carteira de Cobrança')
    open_finance_agency = fields.Char(string='Agência')
    open_finance_account = fields.Char(string='Conta Corrente')

    open_finance_pix_key = fields.Char(string='Chave Pix')
    open_finance_pix_key_type = fields.Selection([
        ('cpf', 'CPF'),
        ('cnpj', 'CNPJ'),
        ('email', 'E-mail'),
        ('phone', 'Telefone'),
        ('evp', 'Chave Aleatória'),
    ], string='Tipo de Chave Pix')
