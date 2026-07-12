{
    'name': 'Open Finance Brasil - Base',
    'version': '18.0.1.0.0',
    'category': 'Accounting/Localizations',
    'summary': 'Base do Open Finance Brasil - Configuração, API e Logs',
    'description': """
Módulo base do Open Finance Brasil.
Gerencia configurações de instituições financeiras, cliente de API e logs de requisições.
    """,
    'author': 'MadooIT',
    'website': 'https://www.madooit.com.br',
    'depends': [
        'account',
        'l10n_br_fiscal_certificate',
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/sequence_data.xml',
        'data/institution_data.xml',
        'views/open_finance_config_views.xml',
        'views/open_finance_api_log_views.xml',
        'views/account_journal_views.xml',
        'views/res_company_views.xml',
        'views/menu_views.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'AGPL-3',
}
