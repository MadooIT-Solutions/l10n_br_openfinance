from odoo import models, fields, api
import requests
import json
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
import base64

class AccountBankStatement(models.Model):
    _inherit = 'account.bank.statement'

    # Campos adicionais para Open Finance
    open_finance_token = fields.Char(string='Token de Acesso Open Finance', help='Token JWT para autenticação na API')
    open_finance_refresh_token = fields.Char(string='Refresh Token', help='Token para renovar o acesso')
    open_finance_consent_id = fields.Char(string='ID do Consentimento', help='ID do consentimento autorizado')
    open_finance_client_id = fields.Char(string='Client ID', help='ID do cliente registrado no Open Finance')
    open_finance_client_secret = fields.Char(string='Client Secret', help='Segredo do cliente')
    open_finance_sandbox = fields.Boolean(string='Modo Sandbox', default=True, help='Usar ambiente de sandbox para testes')

    # Método para obter token via OAuth2
    def _get_access_token(self):
        # Implementar fluxo OAuth2 para obter token inicial
        # Para sandbox, usar endpoints de teste
        url = 'https://auth.sandbox.openfinancebrasil.org.br/token' if self.open_finance_sandbox else 'https://auth.openfinancebrasil.org.br/token'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        data = {
            'grant_type': 'client_credentials',
            'client_id': self.open_finance_client_id,
            'client_secret': self.open_finance_client_secret,
            'scope': 'accounts balances transactions',
        }
        response = requests.post(url, headers=headers, data=data)
        if response.status_code == 200:
            token_data = response.json()
            self.open_finance_token = token_data.get('access_token')
            self.open_finance_refresh_token = token_data.get('refresh_token')
        else:
            raise Exception('Erro ao obter token: ' + response.text)

    # Método para renovar token
    def _refresh_access_token(self):
        url = 'https://auth.sandbox.openfinancebrasil.org.br/token' if self.open_finance_sandbox else 'https://auth.openfinancebrasil.org.br/token'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        data = {
            'grant_type': 'refresh_token',
            'refresh_token': self.open_finance_refresh_token,
            'client_id': self.open_finance_client_id,
            'client_secret': self.open_finance_client_secret,
        }
        response = requests.post(url, headers=headers, data=data)
        if response.status_code == 200:
            token_data = response.json()
            self.open_finance_token = token_data.get('access_token')
            self.open_finance_refresh_token = token_data.get('refresh_token')
        else:
            raise Exception('Erro ao renovar token: ' + response.text)

    # Método para buscar extratos via API
    def fetch_bank_statements(self):
        if not self.open_finance_token:
            self._get_access_token()

        # Endpoint para transações (exemplo para contas)
        base_url = 'https://api.sandbox.openfinancebrasil.org.br' if self.open_finance_sandbox else 'https://api.openfinancebrasil.org.br'
        url = f'{base_url}/accounts/v1/accounts/{self.journal_id.bank_account_id.acc_number}/transactions'
        headers = {
            'Authorization': f'Bearer {self.open_finance_token}',
            'Content-Type': 'application/json',
        }
        params = {
            'fromDateTime': '2023-01-01T00:00:00Z',  # Exemplo, ajustar
            'toDateTime': '2023-12-31T23:59:59Z',
        }

        # Lidar com paginação
        all_transactions = []
        while url:
            response = requests.get(url, headers=headers, params=params)
            if response.status_code == 200:
                data = response.json()
                all_transactions.extend(data.get('data', []))
                url = data.get('links', {}).get('next')  # Próxima página
                params = {}  # Limpar params para próximas páginas
            elif response.status_code == 401:
                self._refresh_access_token()
                headers['Authorization'] = f'Bearer {self.open_finance_token}'
                continue
            else:
                raise Exception('Erro ao buscar transações: ' + response.text)

        # Importar transações para account.bank.statement.line
        for transaction in all_transactions:
            # Criar linha de extrato
            self.env['account.bank.statement.line'].create({
                'statement_id': self.id,
                'date': transaction['transactionDate'],
                'name': transaction['description'],
                'amount': transaction['amount']['value'],
                'ref': transaction['transactionId'],
                # Outros campos conforme necessário
            })