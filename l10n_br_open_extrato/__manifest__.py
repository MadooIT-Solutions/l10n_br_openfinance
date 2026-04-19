# Copyright (C) 2026 - TODAY Rodrigo Abrão Madureira - MadooIT
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

{
    'name': 'Integração Open Finance Brasil para Extratos Bancários',
    'version': '1.0',
    'category': 'Accounting',
    'summary': 'Módulo para importar extratos bancários via Open Finance Brasil',
    'description': 'Integração com APIs do Open Finance Brasil para sincronização automática de extratos bancários.',
    'author': 'MadooIT',
    'depends': ['account'],  # Dependências: account para statements, assumindo l10n_br_bank_statement se existir, mas para CE básico
    'data': [
        'data/ir_cron_data.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}