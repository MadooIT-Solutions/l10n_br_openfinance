import base64
import json
from odoo import models, fields, api, _
from odoo.exceptions import UserError


class OpenFinanceImport(models.TransientModel):
    _name = 'open.finance.import.wizard'
    _description = 'Importar Extrato Open Finance (manual)'

    file = fields.Binary(string='Arquivo JSON/OFX', required=True)
    filename = fields.Char(string='Nome do Arquivo')
    config_id = fields.Many2one(
        'open.finance.config', string='Configuração',
        required=True)
    journal_ids = fields.Many2many(
        'account.journal', string='Diários',
        domain=[('type', '=', 'bank')], required=True)

    def action_import_file(self):
        if not self.file or not self.filename:
            raise UserError(_('Selecione um arquivo para importar.'))
        file_data = base64.b64decode(self.file)
        content = file_data.decode('utf-8')
        try:
            data = json.loads(content)
        except json.JSONDecodeError:
            raise UserError(_('Formato de arquivo não suportado. Use JSON.'))

        statement = self.env['open.finance.statement'].create({
            'config_id': self.config_id.id,
            'journal_ids': [(6, 0, self.journal_ids.ids)],
            'date_from': fields.Date.today(),
            'date_to': fields.Date.today(),
            'state': 'imported',
            'raw_response': content,
        })

        transactions = data.get('transactions', data.get('data', []))
        for txn in transactions:
            self.env['open.finance.statement.line'].create({
                'statement_id': statement.id,
                'transaction_id': txn.get('transactionId') or txn.get('id'),
                'end_to_end_id': txn.get('endToEndId'),
                'date': txn.get('date') or txn.get('transactionDate'),
                'description': txn.get('description', ''),
                'amount': float(txn.get('amount', 0)),
                'partner_name': txn.get('partnerName'),
                'partner_document': txn.get('partnerDocument'),
            })

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'open.finance.statement',
            'res_id': statement.id,
            'view_mode': 'form',
        }
