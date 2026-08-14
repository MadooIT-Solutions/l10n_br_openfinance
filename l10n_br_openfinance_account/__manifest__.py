{
    'name': 'Open Finance Brasil - Extratos',
    'version': '16.0.1.0.0',
    'category': 'Accounting/Localizations',
    'summary': 'Importação de extratos bancários via Open Finance',
    'description': """
Importação e sincronização de extratos bancários via Open Finance Brasil.
Suporte a contas correntes, cartões de crédito e conciliação contábil automática.
    """,
    'author': 'MadooIT',
    'website': 'https://www.madooit.com',
    'depends': [
        'l10n_br_openfinance',
        'l10n_br_openfinance_consent',
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/ir_cron_data.xml',
        'views/open_finance_statement_views.xml',
        'views/open_finance_import_views.xml',
        'views/open_finance_config_views.xml',
        'views/open_finance_consent_views.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'AGPL-3',
}
