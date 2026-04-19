from odoo import models, fields, api
import qrcode
import base64
from io import BytesIO

class ConsentAuthorizationWizard(models.TransientModel):
    _name = 'consent.authorization.wizard'
    _description = 'Wizard para Autorização de Consentimento Open Finance'

    statement_id = fields.Many2one('account.bank.statement', string='Extrato Bancário')
    consent_url = fields.Char(string='URL de Consentimento', readonly=True)
    qr_code = fields.Binary(string='QR Code', readonly=True)

    @api.model
    def default_get(self, fields):
        res = super().default_get(fields)
        statement = self.env['account.bank.statement'].browse(self.env.context.get('active_id'))
        # Gerar URL para consentimento (exemplo, ajustar para Open Finance)
        res['consent_url'] = f'https://consent.sandbox.openfinancebrasil.org.br?client_id={statement.open_finance_client_id}&scope=accounts'
        # Gerar QR Code
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(res['consent_url'])
        qr.make(fit=True)
        img = qr.make_image(fill='black', back_color='white')
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        res['qr_code'] = base64.b64encode(buffer.getvalue()).decode()
        return res

    def authorize_consent(self):
        # Após autorização, o usuário deve fornecer o consent_id manualmente ou via callback
        # Para simplificação, assumir que o consent_id é inserido
        pass
