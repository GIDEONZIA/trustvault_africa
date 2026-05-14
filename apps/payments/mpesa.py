"""M-Pesa Daraja API integration service."""

import base64
import logging
from datetime import datetime

import requests
from django.conf import settings

logger = logging.getLogger(__name__)


class MpesaService:
    def __init__(self):
        self.environment = settings.MPESA_ENVIRONMENT
        if self.environment == 'sandbox':
            self.base_url = 'https://sandbox.safaricom.co.ke'
        else:
            self.base_url = 'https://api.safaricom.co.ke'
        self.consumer_key = settings.MPESA_CONSUMER_KEY
        self.consumer_secret = settings.MPESA_CONSUMER_SECRET
        self.passkey = settings.MPESA_PASSKEY
        self.shortcode = settings.MPESA_SHORTCODE
        self.callback_url = settings.MPESA_CALLBACK_URL

    def get_access_token(self):
        url = f'{self.base_url}/oauth/v1/generate?grant_type=client_credentials'
        credentials = base64.b64encode(
            f'{self.consumer_key}:{self.consumer_secret}'.encode()
        ).decode()
        headers = {'Authorization': f'Basic {credentials}'}

        try:
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            return response.json().get('access_token')
        except requests.RequestException as e:
            logger.error(f'M-Pesa token error: {e}')
            return None

    def generate_password(self):
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        data = f'{self.shortcode}{self.passkey}{timestamp}'
        password = base64.b64encode(data.encode()).decode()
        return password, timestamp

    def stk_push(self, phone_number, amount, account_reference, description):
        access_token = self.get_access_token()
        if not access_token:
            return {'success': False, 'error': 'Failed to get access token'}

        password, timestamp = self.generate_password()

        url = f'{self.base_url}/mpesa/stkpush/v1/processrequest'
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json',
        }
        payload = {
            'BusinessShortCode': self.shortcode,
            'Password': password,
            'Timestamp': timestamp,
            'TransactionType': 'CustomerPayBillOnline',
            'Amount': int(amount),
            'PartyA': phone_number,
            'PartyB': self.shortcode,
            'PhoneNumber': phone_number,
            'CallBackURL': self.callback_url,
            'AccountReference': account_reference,
            'TransactionDesc': description,
        }

        try:
            response = requests.post(url, json=payload, headers=headers, timeout=30)
            data = response.json()
            if data.get('ResponseCode') == '0':
                return {
                    'success': True,
                    'checkout_request_id': data.get('CheckoutRequestID'),
                    'merchant_request_id': data.get('MerchantRequestID'),
                    'message': data.get('CustomerMessage'),
                }
            return {
                'success': False,
                'error': data.get('errorMessage', data.get('ResponseDescription', 'Unknown error')),
            }
        except requests.RequestException as e:
            logger.error(f'M-Pesa STK push error: {e}')
            return {'success': False, 'error': str(e)}

    def query_stk_status(self, checkout_request_id):
        access_token = self.get_access_token()
        if not access_token:
            return {'success': False, 'error': 'Failed to get access token'}

        password, timestamp = self.generate_password()
        url = f'{self.base_url}/mpesa/stkpushquery/v1/query'
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json',
        }
        payload = {
            'BusinessShortCode': self.shortcode,
            'Password': password,
            'Timestamp': timestamp,
            'CheckoutRequestID': checkout_request_id,
        }

        try:
            response = requests.post(url, json=payload, headers=headers, timeout=30)
            return response.json()
        except requests.RequestException as e:
            logger.error(f'M-Pesa query error: {e}')
            return {'success': False, 'error': str(e)}

    @staticmethod
    def process_callback(callback_data):
        stk_callback = callback_data.get('Body', {}).get('stkCallback', {})
        result_code = stk_callback.get('ResultCode')
        result_desc = stk_callback.get('ResultDesc')
        checkout_request_id = stk_callback.get('CheckoutRequestID')
        merchant_request_id = stk_callback.get('MerchantRequestID')

        result = {
            'result_code': result_code,
            'result_desc': result_desc,
            'checkout_request_id': checkout_request_id,
            'merchant_request_id': merchant_request_id,
        }

        if result_code == 0:
            metadata = stk_callback.get('CallbackMetadata', {}).get('Item', [])
            for item in metadata:
                name = item.get('Name')
                value = item.get('Value')
                if name == 'Amount':
                    result['amount'] = value
                elif name == 'MpesaReceiptNumber':
                    result['mpesa_receipt'] = value
                elif name == 'TransactionDate':
                    result['transaction_date'] = value
                elif name == 'PhoneNumber':
                    result['phone_number'] = str(value)
            result['success'] = True
        else:
            result['success'] = False

        return result


mpesa_service = MpesaService()
