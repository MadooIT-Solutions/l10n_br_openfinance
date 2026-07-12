import json
import logging
import requests
from odoo import models, fields, api, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class OpenFinanceAPI(models.Model):
    _name = 'open.finance.api'
    _description = 'API Client Open Finance (técnico)'

    config_id = fields.Many2one(
        'open.finance.config', string='Configuração',
        required=True, ondelete='cascade')

    def _get_headers(self, access_token=None):
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        }
        if access_token:
            headers['Authorization'] = f'Bearer {access_token}'
        return headers

    def _request(self, method, endpoint, data=None, access_token=None):
        self.ensure_one()
        config = self.config_id
        url = f'{config.api_base_url.rstrip("/")}/{endpoint.lstrip("/")}'
        headers = self._get_headers(access_token)
        log_vals = {
            'config_id': config.id,
            'method': method.upper(),
            'endpoint': endpoint,
            'request_data': json.dumps(data) if data else '',
            'state': 'requested',
        }
        log = self.env['open.finance.api.log'].create(log_vals)
        try:
            cert_data = self._get_cert_for_request()
            response = requests.request(
                method=method.upper(),
                url=url,
                headers=headers,
                json=data,
                cert=cert_data,
                timeout=30,
            )
            log.write({
                'response_status': response.status_code,
                'response_data': response.text,
                'state': 'success' if response.ok else 'error',
            })
            if not response.ok:
                _logger.error('OpenFinance API error %s: %s', response.status_code, response.text)
                response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            error_msg = str(e)
            log.write({'response_data': error_msg, 'state': 'error'})
            raise UserError(_('Erro na comunicação com Open Finance: %s') % error_msg)

    def _get_cert_for_request(self):
        self.ensure_one()
        try:
            import tempfile
            import os
            cert = self.config_id.certificate_id
            tmp_dir = tempfile.mkdtemp()
            p12_path = os.path.join(tmp_dir, 'cert.p12')
            with open(p12_path, 'wb') as f:
                f.write(bytes(cert.file, 'ascii') if isinstance(cert.file, str) else cert.file)
            return p12_path
        except Exception as e:
            raise UserError(_('Erro ao processar certificado: %s') % str(e))

    def health_check(self):
        endpoint = '/discovery/v1/status'
        return self._request('GET', endpoint)

    def request_consent(self, consent):
        self.ensure_one()
        config = self.config_id
        logged_user_doc = consent.cpf_cnpj or ''
        is_pf = consent.person_type == 'pf'

        consent_data = {
            'loggedUser': {
                'document': {
                    'identification': logged_user_doc,
                    'rel': 'CPF',
                }
            },
            'permissions': self._map_scope_to_permissions(consent.scope),
        }

        if is_pf:
            if logged_user_doc:
                consent_data['businessEntity'] = {
                    'document': {
                        'identification': logged_user_doc,
                        'rel': 'CPF',
                    }
                }
        else:
            consent_data['businessEntity'] = {
                'document': {
                    'identification': config.company_id.vat or logged_user_doc,
                    'rel': 'CNPJ',
                }
            }

        endpoint = '/consents/v2/consents'
        result = self._request('POST', endpoint, consent_data)
        return {
            'consent_id': result.get('data', {}).get('consentId'),
            'qr_code_url': result.get('data', {}).get('qrCodeUrl'),
            'qr_code_text': result.get('data', {}).get('qrCodeText'),
            'expiration_date': result.get('data', {}).get('expirationDateTime'),
        }

    def _map_scope_to_permissions(self, scope):
        mapping = {
            'read_extrato_pf': [
                'ACCOUNTS_READ', 'ACCOUNTS_BALANCES_READ',
                'ACCOUNTS_TRANSACTIONS_READ', 'RESOURCES_READ',
            ],
            'read_extrato_pj': [
                'ACCOUNTS_READ', 'ACCOUNTS_BALANCES_READ',
                'ACCOUNTS_TRANSACTIONS_READ', 'RESOURCES_READ',
            ],
            'read_extrato_pix': [
                'ACCOUNTS_READ', 'ACCOUNTS_BALANCES_READ',
                'ACCOUNTS_TRANSACTIONS_READ', 'RESOURCES_READ',
            ],
            'read_cadastro_pf': [
                'CUSTOMERS_PERSONAL_IDENTIFICATIONS_READ',
                'CUSTOMERS_PERSONAL_ADITTIONALINFO_READ',
                'RESOURCES_READ',
            ],
            'read_cadastro_pj': [
                'CUSTOMERS_BUSINESS_IDENTIFICATIONS_READ',
                'CUSTOMERS_BUSINESS_ADITTIONALINFO_READ',
                'RESOURCES_READ',
            ],
            'payment_pix': ['PAYMENTS_PAY'],
            'payment_boleto': ['PAYMENTS_PAY'],
            'read_extrato_payment_pix': [
                'ACCOUNTS_READ', 'ACCOUNTS_BALANCES_READ',
                'ACCOUNTS_TRANSACTIONS_READ',
                'RESOURCES_READ', 'PAYMENTS_PAY',
            ],
            'read_all_pf': [
                'ACCOUNTS_READ', 'ACCOUNTS_BALANCES_READ',
                'ACCOUNTS_TRANSACTIONS_READ', 'ACCOUNTS_OVERDRAFT_LIMITS_READ',
                'CREDIT_CARDS_ACCOUNTS_READ', 'CREDIT_CARDS_ACCOUNTS_LIMITS_READ',
                'CREDIT_CARDS_ACCOUNTS_TRANSACTIONS_READ',
                'CREDIT_CARDS_ACCOUNTS_BILLS_READ',
                'CREDIT_CARDS_ACCOUNTS_BILLS_TRANSACTIONS_READ',
                'CUSTOMERS_PERSONAL_IDENTIFICATIONS_READ',
                'CUSTOMERS_PERSONAL_ADITTIONALINFO_READ',
                'LOANS_READ', 'LOANS_SCHEDULED_INSTALMENTS_READ',
                'LOANS_PAYMENTS_READ', 'LOANS_WARRANTIES_READ',
                'FINANCINGS_READ', 'FINANCINGS_SCHEDULED_INSTALMENTS_READ',
                'FINANCINGS_PAYMENTS_READ', 'FINANCINGS_WARRANTIES_READ',
                'UNARRANGED_ACCOUNTS_OVERDRAFT_READ',
                'UNARRANGED_ACCOUNTS_OVERDRAFT_SCHEDULED_INSTALMENTS_READ',
                'UNARRANGED_ACCOUNTS_OVERDRAFT_PAYMENTS_READ',
                'UNARRANGED_ACCOUNTS_OVERDRAFT_WARRANTIES_READ',
                'INVOICE_FINANCINGS_READ',
                'INVOICE_FINANCINGS_SCHEDULED_INSTALMENTS_READ',
                'INVOICE_FINANCINGS_PAYMENTS_READ',
                'INVOICE_FINANCINGS_WARRANTIES_READ',
                'RESOURCES_READ',
            ],
            'read_all_pj': [
                'ACCOUNTS_READ', 'ACCOUNTS_BALANCES_READ',
                'ACCOUNTS_TRANSACTIONS_READ', 'ACCOUNTS_OVERDRAFT_LIMITS_READ',
                'CREDIT_CARDS_ACCOUNTS_READ', 'CREDIT_CARDS_ACCOUNTS_LIMITS_READ',
                'CREDIT_CARDS_ACCOUNTS_TRANSACTIONS_READ',
                'CREDIT_CARDS_ACCOUNTS_BILLS_READ',
                'CREDIT_CARDS_ACCOUNTS_BILLS_TRANSACTIONS_READ',
                'CUSTOMERS_BUSINESS_IDENTIFICATIONS_READ',
                'CUSTOMERS_BUSINESS_ADITTIONALINFO_READ',
                'LOANS_READ', 'LOANS_SCHEDULED_INSTALMENTS_READ',
                'LOANS_PAYMENTS_READ', 'LOANS_WARRANTIES_READ',
                'FINANCINGS_READ', 'FINANCINGS_SCHEDULED_INSTALMENTS_READ',
                'FINANCINGS_PAYMENTS_READ', 'FINANCINGS_WARRANTIES_READ',
                'UNARRANGED_ACCOUNTS_OVERDRAFT_READ',
                'UNARRANGED_ACCOUNTS_OVERDRAFT_SCHEDULED_INSTALMENTS_READ',
                'UNARRANGED_ACCOUNTS_OVERDRAFT_PAYMENTS_READ',
                'UNARRANGED_ACCOUNTS_OVERDRAFT_WARRANTIES_READ',
                'INVOICE_FINANCINGS_READ',
                'INVOICE_FINANCINGS_SCHEDULED_INSTALMENTS_READ',
                'INVOICE_FINANCINGS_PAYMENTS_READ',
                'INVOICE_FINANCINGS_WARRANTIES_READ',
                'RESOURCES_READ',
            ],
        }
        return mapping.get(scope, [])

    def check_consent_status(self, consent_id):
        endpoint = f'/consents/v2/consents/{consent_id}'
        result = self._request('GET', endpoint)
        data = result.get('data', {})
        return {
            'status': self._map_status(data.get('status')),
            'access_token': data.get('accessToken'),
            'refresh_token': data.get('refreshToken'),
            'token_expiry': data.get('tokenExpiry'),
        }

    def _map_status(self, status):
        mapping = {
            'AWAITING': 'requested',
            'AWAITING_AUTHORISATION': 'requested',
            'AUTHORISED': 'authorized',
            'REJECTED': 'rejected',
            'REVOKED': 'revoked',
            'EXPIRED': 'expired',
        }
        return mapping.get(status, status)

    def revoke_consent(self, consent_id):
        endpoint = f'/consents/v2/consents/{consent_id}'
        self._request('DELETE', endpoint)

    def refresh_access_token(self, refresh_token):
        config = self.config_id
        data = {
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token,
            'client_id': config.client_id,
            'client_secret': config.client_secret,
        }
        result = self._request('POST', '/token', data)
        return {
            'access_token': result.get('access_token'),
            'refresh_token': result.get('refresh_token', refresh_token),
            'token_expiry': result.get('expires_in'),
        }

    def fetch_transactions(self, statement):
        self.ensure_one()
        consent = statement.consent_id
        if not consent.access_token:
            raise UserError(_('Consentimento sem access token. Verifique se foi autorizado.'))
        date_from = statement.date_from.strftime('%Y-%m-%d')
        date_to = statement.date_to.strftime('%Y-%m-%d')
        endpoint = f'/accounts/v1/accounts/transactions?from={date_from}&to={date_to}'
        raw_result = self._request('GET', endpoint, access_token=consent.access_token)
        transactions = []
        accounts = raw_result.get('data', [])
        for account in accounts:
            account_id = account.get('accountId')
            txn_endpoint = f'/accounts/v1/accounts/{account_id}/transactions?from={date_from}&to={date_to}'
            try:
                txn_result = self._request('GET', txn_endpoint, access_token=consent.access_token)
                for txn in txn_result.get('data', []):
                    transactions.append(self._parse_transaction(txn))
            except Exception as e:
                _logger.warning('Erro ao buscar transações da conta %s: %s', account_id, str(e))
        return {
            'transactions': transactions,
            'raw_response': json.dumps(raw_result, indent=2),
        }

    def _parse_transaction(self, txn):
        amount = float(txn.get('amount', 0))
        txn_type = txn.get('creditDebitType', '')
        if txn_type == 'CREDIT':
            amount = abs(amount)
        else:
            amount = -abs(amount)
        return {
            'transaction_id': txn.get('transactionId'),
            'end_to_end_id': txn.get('endToEndId'),
            'date': txn.get('transactionDate'),
            'description': txn.get('description', ''),
            'amount': amount,
            'partner_name': txn.get('partnerName'),
            'partner_document': txn.get('partnerDocument'),
            'payment_type': self._map_payment_type(txn.get('type')),
            'category': self._map_category(txn.get('category')),
            'raw_data': json.dumps(txn, indent=2),
        }

    def _map_payment_type(self, ptype):
        mapping = {
            'PIX': 'pix', 'TED': 'ted', 'DOC': 'doc',
            'BOLETO': 'boleto', 'TRANSFERENCIA': 'transfer',
        }
        return mapping.get(ptype, 'other')

    def _map_category(self, category):
        mapping = {
            'RECEITA': 'receita', 'DESPESA': 'despesa',
            'TRANSFERENCIA': 'transferencia',
        }
        return mapping.get(category, 'outros')

    def send_pix(self, pix):
        self.ensure_one()
        consent = pix.consent_id
        if not consent or not consent.access_token:
            raise UserError(_('Consentimento com token de acesso é necessário.'))
        data = {
            'pixKey': pix.pix_key or '',
            'pixKeyType': (pix.pix_key_type or 'evp').upper(),
            'amount': str(pix.amount),
            'description': pix.description or '',
            'recipient': {
                'name': pix.partner_name or pix.partner_id.display_name or '',
                'document': pix.partner_document or pix.partner_id.vat or '',
            },
        }
        endpoint = '/payments/v2/pix/payments'
        result = self._request('POST', endpoint, data, access_token=consent.access_token)
        return {
            'txid': result.get('data', {}).get('txid'),
            'end_to_end_id': result.get('data', {}).get('endToEndId'),
            'settlement_date': result.get('data', {}).get('settlementDate'),
        }

    def check_pix_status(self, pix):
        self.ensure_one()
        endpoint_id = pix.end_to_end_id or pix.txid
        if not endpoint_id:
            raise UserError(_('ID da transação Pix não disponível.'))
        endpoint = f'/payments/v2/pix/payments/{endpoint_id}'
        result = self._request('GET', endpoint)
        data = result.get('data', {})
        status_map = {
            'SCHEDULED': 'pending', 'SETTLED': 'completed',
            'REJECTED': 'failed', 'CANCELLED': 'cancelled',
            'REFUNDED': 'refunded',
        }
        return {'status': status_map.get(data.get('status'), data.get('status'))}

    def register_boleto(self, boleto):
        self.ensure_one()
        data = {
            'amount': str(boleto.amount),
            'dueDate': boleto.date_due.strftime('%Y-%m-%d'),
            'payer': {
                'name': boleto.partner_name or '',
                'document': boleto.partner_document or '',
                'email': boleto.partner_email or '',
            },
            'description': boleto.description or '',
            'instructions': boleto.instructions or '',
        }
        if boleto.wallet:
            data['wallet'] = boleto.wallet
        if boleto.interest_rate:
            data['interestRate'] = boleto.interest_rate
        if boleto.fine_rate:
            data['fineRate'] = boleto.fine_rate
        endpoint = '/cobranca/v2/boletos'
        result = self._request('POST', endpoint, data)
        return {
            'nosso_numero': result.get('data', {}).get('nossoNumero'),
            'nosso_numero_formatado': result.get('data', {}).get('nossoNumeroFormatado'),
            'linha_digitavel': result.get('data', {}).get('linhaDigitavel'),
            'codigo_barras': result.get('data', {}).get('codigoBarras'),
            'barcode_data': result.get('data', {}).get('barcodeData'),
            'pdf_base64': result.get('data', {}).get('pdf'),
        }

    def check_boleto_status(self, boleto):
        if not boleto.nosso_numero:
            raise UserError(_('Boleto sem nosso número.'))
        endpoint = f'/cobranca/v2/boletos/{boleto.nosso_numero}'
        result = self._request('GET', endpoint)
        data = result.get('data', {})
        status_map = {
            'REGISTERED': 'registered', 'PAID': 'paid',
            'CANCELLED': 'cancelled', 'OVERDUE': 'overdue',
        }
        return {
            'state': status_map.get(data.get('status'), boleto.state),
            'date_paid': data.get('paymentDate'),
        }

    def cancel_boleto(self, boleto):
        if not boleto.nosso_numero:
            raise UserError(_('Boleto sem nosso número.'))
        endpoint = f'/cobranca/v2/boletos/{boleto.nosso_numero}/cancel'
        self._request('POST', endpoint)
