{
    'name': 'Open Finance Brasil - Pagamentos',
    'version': '18.0.1.0.0',
    'category': 'Accounting/Localizations',
    'summary': 'Pagamentos Open Finance - Pix e Boleto',
    'description': """
Iniciação de pagamentos via Open Finance Brasil.
Suporte a Pix e boletos de cobrança com registro, consulta e conciliação contábil.
    """,
    'author': 'MadooIT',
    'website': 'https://www.madooit.com.br',
    'depends': [
        'l10n_br_openfinance',
        'l10n_br_openfinance_consent',
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/ir_cron_data.xml',
        'views/open_finance_pix_views.xml',
        'views/open_finance_boleto_views.xml',
        'views/open_finance_config_views.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'AGPL-3',
}
