{
    'name': 'Open Finance Brasil - Consentimento',
    'version': '18.0.1.0.0',
    'category': 'Accounting/Localizations',
    'summary': 'Gerenciamento de consentimentos Open Finance',
    'description': """
Gerencia consentimentos para integração Open Finance.
Suporte a pessoa física (PF) e jurídica (PJ), autorização via QR Code e renovação de tokens.
    """,
    'author': 'MadooIT',
    'website': 'https://www.madooit.com.br',
    'depends': [
        'l10n_br_openfinance',
        'l10n_br_openfinance_account',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/open_finance_consent_views.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'AGPL-3',
}
