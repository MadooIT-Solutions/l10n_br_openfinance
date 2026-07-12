from odoo import models, fields, api, _
from odoo.exceptions import UserError


class OpenFinanceStatement(models.Model):
    _name = 'open.finance.statement'
    _description = 'Extrato Bancário Open Finance'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc'
    _rec_name = 'display_name'

    display_name = fields.Char(compute='_compute_display_name', store=True)
    config_id = fields.Many2one(
        'open.finance.config', string='Configuração',
        required=True, ondelete='cascade')
    company_id = fields.Many2one(
        'res.company', string='Empresa',
        related='config_id.company_id', store=True)

    consent_id = fields.Many2one(
        'open.finance.consent', string='Consentimento',
        required=True, domain=[('status', 'in', ('authorized', 'active'))])

    state = fields.Selection([
        ('draft', 'Rascunho'),
        ('fetching', 'Buscando...'),
        ('imported', 'Importado'),
        ('error', 'Erro'),
    ], string='Estado', default='draft', required=True, tracking=True)

    journal_ids = fields.Many2many(
        'account.journal', string='Diários',
        domain=[('type', '=', 'bank')],
        help='Diários para criar os extratos')
    bank_statement_id = fields.Many2one(
        'account.bank.statement', string='Extrato Gerado',
        readonly=True)

    date_from = fields.Date(string='Data Início', required=True)
    date_to = fields.Date(string='Data Fim', required=True)

    total_transactions = fields.Integer(
        string='Total Transações', readonly=True)
    total_debit = fields.Monetary(
        string='Total Débitos', readonly=True)
    total_credit = fields.Monetary(
        string='Total Créditos', readonly=True)
    currency_id = fields.Many2one(
        'res.currency', string='Moeda',
        default=lambda self: self.env.company.currency_id)

    raw_response = fields.Text(
        string='Resposta da API (JSON)', readonly=True)
    error_message = fields.Text(
        string='Mensagem de Erro', readonly=True)

    statement_line_ids = fields.One2many(
        'open.finance.statement.line', 'statement_id',
        string='Linhas do Extrato')

    fetch_count = fields.Integer(
        string='Tentativas de Busca', default=0)

    api_log_ids = fields.One2many(
        'open.finance.api.log', 'statement_id',
        string='Logs de API')

    @api.depends('config_id.institution_name', 'date_from', 'date_to', 'state')
    def _compute_display_name(self):
        for r in self:
            state_label = dict(r._fields['state'].selection).get(r.state, r.state)
            r.display_name = (
                f'{r.config_id.institution_name} - '
                f'{r.date_from} a {r.date_to} [{state_label}]'
            )

    @api.constrains('date_from', 'date_to')
    def _check_dates(self):
        for r in self:
            if r.date_from and r.date_to and r.date_from > r.date_to:
                raise UserError(_('Data início não pode ser posterior à data fim.'))

    @api.model
    def _cron_sync_all(self):
        consents = self.env['open.finance.consent'].search([
            ('status', 'in', ('authorized', 'active')),
            ('scope', 'in', (
                'read_extrato_pf', 'read_extrato_pj',
                'read_extrato_pix', 'read_extrato_payment_pix',
                'read_all_pf', 'read_all_pj',
            )),
        ])
        for consent in consents:
            for journal in consent.journal_ids:
                self.create({
                    'config_id': consent.config_id.id,
                    'consent_id': consent.id,
                    'journal_ids': [(4, journal.id)],
                    'date_from': fields.Date.today(),
                    'date_to': fields.Date.today(),
                }).with_context(async_exec=False)._do_fetch()

    def action_fetch_statement(self):
        self.ensure_one()
        if self.state not in ('draft', 'error'):
            raise UserError(_('Este extrato já foi processado ou está em andamento.'))
        async_exec = self.env.context.get('async_exec', True)
        if async_exec:
            self.write({'state': 'fetching'})
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': _('Processando'),
                    'message': _('A busca do extrato foi agendada em segundo plano.'),
                    'sticky': False,
                    'type': 'info',
                }
            }
        return self._do_fetch()

    def _do_fetch(self):
        self.ensure_one()
        self.write({'state': 'fetching', 'fetch_count': self.fetch_count + 1})
        try:
            api = self.config_id._get_api_client()
            result = api.fetch_transactions(self)
            self.write({
                'raw_response': result.get('raw_response'),
                'state': 'imported',
            })
            self._process_api_result(result)
        except Exception as e:
            self.write({
                'state': 'error',
                'error_message': str(e),
            })

    def _process_api_result(self, result):
        self.ensure_one()
        transactions = result.get('transactions', [])
        self.write({
            'total_transactions': len(transactions),
            'total_debit': sum(t.get('amount', 0) for t in transactions if t.get('amount', 0) < 0),
            'total_credit': sum(t.get('amount', 0) for t in transactions if t.get('amount', 0) > 0),
        })
        for txn in transactions:
            self.env['open.finance.statement.line'].create({
                'statement_id': self.id,
                'transaction_id': txn.get('transaction_id'),
                'end_to_end_id': txn.get('end_to_end_id'),
                'date': txn.get('date'),
                'description': txn.get('description', ''),
                'amount': txn.get('amount', 0.0),
                'partner_name': txn.get('partner_name'),
                'partner_document': txn.get('partner_document'),
                'payment_type': txn.get('payment_type', 'other'),
                'category': txn.get('category', 'other'),
                'raw_data': txn.get('raw_data'),
            })

    def action_import_to_accounting(self):
        self.ensure_one()
        if self.state != 'imported':
            raise UserError(_('O extrato precisa ser importado primeiro.'))
        if self.bank_statement_id:
            raise UserError(_('Extrato já foi importado para a contabilidade.'))
        if not self.journal_ids:
            raise UserError(_('Selecione pelo menos um diário bancário.'))

        for journal in self.journal_ids:
            statement = self.env['account.bank.statement'].create({
                'journal_id': journal.id,
                'name': f'OF {self.date_from} a {self.date_to}',
            })
            line_commands = []
            for line in self.statement_line_ids:
                if line.imported:
                    continue
                line_commands.append((0, 0, {
                    'date': line.date,
                    'payment_ref': line.description or line.transaction_id or '',
                    'amount': abs(line.amount) if line.amount else 0.0,
                    'partner_name': line.partner_name or '',
                    'partner_id': line.partner_id.id if line.partner_id else False,
                }))
            if line_commands:
                statement.write({'line_ids': line_commands})
            self.bank_statement_id = statement
            self.statement_line_ids.write({'imported': True})

    def action_view_bank_statement(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'account.bank.statement',
            'res_id': self.bank_statement_id.id,
            'view_mode': 'form',
        }


class OpenFinanceStatementLine(models.Model):
    _name = 'open.finance.statement.line'
    _description = 'Linha do Extrato Open Finance'
    _order = 'date desc, id'

    statement_id = fields.Many2one(
        'open.finance.statement', string='Extrato',
        required=True, ondelete='cascade')
    company_id = fields.Many2one(
        'res.company', string='Empresa',
        related='statement_id.company_id', store=True)

    transaction_id = fields.Char(
        string='ID Transação',
        help='Identificador único da transação no Open Finance')
    end_to_end_id = fields.Char(
        string='End-to-End ID',
        help='Identificador único da transação no arranjo Pix')
    date = fields.Date(string='Data', required=True)
    description = fields.Char(string='Descrição')
    amount = fields.Monetary(string='Valor', required=True)
    currency_id = fields.Many2one(
        'res.currency', string='Moeda',
        related='statement_id.currency_id', store=True)

    partner_name = fields.Char(string='Nome do Contraparte')
    partner_document = fields.Char(string='CPF/CNPJ do Contraparte')
    partner_id = fields.Many2one(
        'res.partner', string='Parceiro',
        help='Parceiro vinculado automaticamente')
    payment_type = fields.Selection([
        ('pix', 'Pix'),
        ('ted', 'TED'),
        ('doc', 'DOC'),
        ('boleto', 'Boleto'),
        ('transfer', 'Transferência'),
        ('other', 'Outro'),
    ], string='Tipo de Pagamento', default='other')

    category = fields.Selection([
        ('receita', 'Receita'),
        ('despesa', 'Despesa'),
        ('transferencia', 'Transferência'),
        ('outros', 'Outros'),
    ], string='Categoria', default='outros')

    imported = fields.Boolean(string='Importado?', default=False)
    raw_data = fields.Text(string='Dados Brutos')
