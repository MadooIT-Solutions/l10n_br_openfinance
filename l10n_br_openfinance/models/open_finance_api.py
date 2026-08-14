import base64
import json
import logging
import os
import tempfile
import time
import uuid
from datetime import datetime, timedelta, timezone

import requests
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.primitives.serialization import (
    Encoding,
    NoEncryption,
    PrivateFormat,
    load_pem_private_key,
    pkcs12,
)

from odoo import _, fields, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class OpenFinanceAPI(models.Model):
    _name = 'open.finance.api'
    _description = 'API Client Open Finance (técnico)'

    _JWT_ALGORITHM = 'RS256'
    _CLIENT_ASSERTION_TYPE = 'urn:ietf:params:oauth:client-assertion-type:jwt-bearer'
    _CERT_CREDENTIALS_CACHE = {}

    config_id = fields.Many2one(
        'open.finance.config', string='Configuração',
        required=True, ondelete='cascade')

    def _get_headers(self, access_token=None, form=False):
        headers = {
            'Accept': 'application/json',
            'x-fapi-interaction-id': str(uuid.uuid4()),
        }
        if form:
            headers['Content-Type'] = 'application/x-www-form-urlencoded'
        else:
            headers['Content-Type'] = 'application/json'
        if access_token:
            headers['Authorization'] = 'Bearer %s' % access_token
        return headers

    def _request(self, method, endpoint, data=None, access_token=None,
                 form=False, is_full_url=False):
        self.ensure_one()
        config = self.config_id
        if is_full_url:
            url = endpoint
        else:
            url = '%s/%s' % (config.api_base_url.rstrip('/'), endpoint.lstrip('/'))
        headers = self._get_headers(access_token, form=form)
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
            if form:
                response = requests.request(
                    method=method.upper(),
                    url=url,
                    headers=headers,
                    data=data,
                    cert=cert_data,
                    timeout=30,
                )
            else:
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
        """Return the (cert, key) PEM file paths used as mTLS client certificate."""
        creds = self._get_cert_credentials()
        return (creds['cert_pem'], creds['key_pem'])

    def _get_cert_credentials(self):
        """Load the e-CNPJ A1 certificate (.p12) and expose it as PEM files,
        private key and certificate thumbprint for mTLS and JWT signing.

        The result is cached per configuration in a module-level dict because
        Odoo model records do not allow arbitrary instance attributes.
        """
        cert = self.config_id.certificate_id
        if not cert or not cert.file:
            raise UserError(_(
                'Certificado não configurado. Configure um certificado válido '
                'na configuração do Open Finance.'))
        raw = cert.file
        if isinstance(raw, str):
            raw = raw.encode('ascii')
        password = (cert.password or '').encode('utf-8')

        cache_key = (cert.id, raw, password)
        cached = self._CERT_CREDENTIALS_CACHE.get(cache_key)
        if cached:
            return cached

        key = cert_obj = extra_certs = None
        for candidate in (base64.b64decode(raw), raw):
            try:
                key, cert_obj, extra_certs = pkcs12.load_key_and_certificates(
                    candidate, password)
                break
            except Exception:
                continue
        if key is None or cert_obj is None:
            raise UserError(_(
                'Não foi possível ler o certificado .p12. Verifique o arquivo '
                'e a senha cadastrados no certificado fiscal.'))

        tmp_dir = tempfile.mkdtemp(prefix='open_finance_cert_')
        cert_pem = os.path.join(tmp_dir, 'cert.pem')
        key_pem = os.path.join(tmp_dir, 'key.pem')
        cert_pem_content = cert_obj.public_bytes(Encoding.PEM)
        for extra in extra_certs or []:
            cert_pem_content += extra.public_bytes(Encoding.PEM)
        key_pem_content = key.private_bytes(
            Encoding.PEM, PrivateFormat.PKCS8, NoEncryption())
        with open(cert_pem, 'wb') as f:
            f.write(cert_pem_content)
        with open(key_pem, 'wb') as f:
            f.write(key_pem_content)

        creds = {
            'cert_pem': cert_pem,
            'key_pem': key_pem,
            'key_pem_data': key_pem_content,
            'thumbprint': cert_obj.fingerprint(hashes.SHA256()).hex(),
            'cert_der': cert_obj.public_bytes(Encoding.DER),
        }
        self._CERT_CREDENTIALS_CACHE[cache_key] = creds
        return creds

    def _get_token_url(self):
        config = self.config_id
        if config.token_url:
            return config.token_url
        return '%s/token' % config.api_base_url.rstrip('/')

    def _b64url_json(self, data):
        encoded = json.dumps(data, separators=(',', ':')).encode('utf-8')
        return base64.urlsafe_b64encode(encoded).rstrip(b'=').decode('ascii')

    def _get_client_assertion(self):
        """Build the private_key_jwt client assertion required by FAPI,
        signing the JWT with the certificate private key (RS256).
        """
        config = self.config_id
        creds = self._get_cert_credentials()
        now = int(time.time())
        header = {
            'alg': self._JWT_ALGORITHM,
            'typ': 'JWT',
            'kid': creds['thumbprint'],
            'x5c': [base64.b64encode(creds['cert_der']).decode('ascii')],
        }
        payload = {
            'iss': config.client_id,
            'sub': config.client_id,
            'aud': self._get_token_url(),
            'exp': now + 300,
            'iat': now,
            'jti': str(uuid.uuid4()),
        }
        private_key = load_pem_private_key(creds['key_pem_data'], password=None)
        if not isinstance(private_key, rsa.RSAPrivateKey):
            raise UserError(_(
                'O certificado precisa conter uma chave RSA (padrão e-CNPJ A1) '
                'para assinar a autenticação JWT.'))
        signing_input = '%s.%s' % (
            self._b64url_json(header), self._b64url_json(payload))
        signature = private_key.sign(
            signing_input.encode('ascii'), padding.PKCS1v15(), hashes.SHA256())
        signature_b64 = base64.urlsafe_b64encode(signature).rstrip(b'=').decode('ascii')
        return '.'.join((signing_input, signature_b64))

    def _get_client_token(self):
        """Obtain an OAuth2 client_credentials token from the token endpoint."""
        config = self.config_id
        data = {
            'grant_type': 'client_credentials',
            'client_id': config.client_id,
            'client_assertion_type': self._CLIENT_ASSERTION_TYPE,
            'client_assertion': self._get_client_assertion(),
        }
        result = self._request(
            'POST', self._get_token_url(), data=data,
            form=True, is_full_url=True)
        return result.get('access_token')

    def _only_digits(self, value):
        if not value:
            return value
        return ''.join(ch for ch in str(value) if ch.isdigit())

    def _consent_expiration(self, consent):
        if consent.date_expiration:
            exp = consent.date_expiration
            if exp.tzinfo is None:
                exp = exp.replace(tzinfo=timezone.utc)
            return exp.astimezone(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
        return (datetime.now(timezone.utc) + timedelta(days=30)).strftime(
            '%Y-%m-%dT%H:%M:%SZ')

    def _get_paginated(self, endpoint, access_token):
        """Fetch all pages of a paginated Open Finance endpoint."""
        page = 1
        all_data = []
        while True:
            separator = '&' if '?' in endpoint else '?'
            url = '%s%s%s' % (endpoint, separator, 'page=%d&page-size=100' % page)
            result = self._request('GET', url, access_token=access_token)
            all_data += result.get('data', [])
            meta = result.get('meta') or {}
            if page >= meta.get('totalPages', 1):
                break
            page += 1
        return all_data

    def health_check(self):
        endpoint = '/open-banking/discovery/v1/status'
        return self._request('GET', endpoint)

    def request_consent(self, consent):
        self.ensure_one()
        config = self.config_id
        is_pf = consent.person_type == 'pf'
        logged_user_cpf = consent.cpf_cnpj if is_pf else (
            consent.logged_user_cpf or consent.cpf_cnpj)
        consent_data = {
            'data': {
                'loggedUser': {
                    'document': {
                        'identification': self._only_digits(logged_user_cpf),
                        'rel': 'CPF',
                    },
                },
                'permissions': self._map_scope_to_permissions(consent.scope),
                'expirationDateTime': self._consent_expiration(consent),
            },
        }
        if not is_pf:
            consent_data['data']['businessEntity'] = {
                'document': {
                    'identification': self._only_digits(
                        config.company_id.vat or consent.cpf_cnpj),
                    'rel': 'CNPJ',
                },
            }
        client_token = self._get_client_token()
        endpoint = '/open-banking/consents/v2/consents'
        result = self._request(
            'POST', endpoint, consent_data, access_token=client_token)
        data = result.get('data', {})
        return {
            'consent_id': data.get('consentId'),
            'qr_code_url': data.get('qrCodeUrl'),
            'qr_code_text': data.get('qrCodeText'),
            'expiration_date': data.get('expirationDateTime'),
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
        client_token = self._get_client_token()
        endpoint = '/open-banking/consents/v2/consents/%s' % consent_id
        result = self._request('GET', endpoint, access_token=client_token)
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
        client_token = self._get_client_token()
        endpoint = '/open-banking/consents/v2/consents/%s' % consent_id
        self._request('DELETE', endpoint, access_token=client_token)

    def refresh_access_token(self, refresh_token):
        config = self.config_id
        data = {
            'grant_type': 'refresh_token',
            'client_id': config.client_id,
            'refresh_token': refresh_token,
            'client_assertion_type': self._CLIENT_ASSERTION_TYPE,
            'client_assertion': self._get_client_assertion(),
        }
        result = self._request(
            'POST', self._get_token_url(), data=data,
            form=True, is_full_url=True)
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
        accounts = self._get_paginated(
            '/open-banking/accounts/v1/accounts', consent.access_token)
        transactions = []
        for account in accounts:
            account_id = account.get('accountId')
            txn_endpoint = (
                '/open-banking/accounts/v1/accounts/%s/transactions'
                '?fromBookingDate=%s&toBookingDate=%s'
                % (account_id, date_from, date_to))
            try:
                txn_result = self._get_paginated(
                    txn_endpoint, consent.access_token)
                for txn in txn_result:
                    transactions.append(self._parse_transaction(txn))
            except Exception as e:
                _logger.warning('Erro ao buscar transações da conta %s: %s', account_id, str(e))
        return {
            'transactions': transactions,
            'raw_response': json.dumps(accounts, indent=2),
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
        endpoint = '/open-banking/payments/v1/pix/payments'
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
        endpoint = '/open-banking/payments/v1/pix/payments/%s' % endpoint_id
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
        endpoint = '/cobranca/v2/boletos/%s' % boleto.nosso_numero
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
        endpoint = '/cobranca/v2/boletos/%s/cancel' % boleto.nosso_numero
        self._request('POST', endpoint)
