import requests
from requests.auth import HTTPBasicAuth
from datetime import datetime
import base64

# Get from your Safaricom developer app
CONSUMER_KEY = 'v2rvXxZsmA3YYgy6LdAfNpljglxb8mI0X5pdXuIqLlgcLvBa'
CONSUMER_SECRET = 'k64PXd8rVYiIzmcfXg9J7jtdEl3pXf2y8OlRpx4fTkVb84nSgAzHnWjuhiSXGg6p'
BUSINESS_SHORTCODE = '174379'  # Test shortcode
PASSKEY = 'bfb279f9aa9bdbcf113b1e3c4b3e7d72'
CALLBACK_URL = 'https://e8072e81c2e0.ngrok-free.app'  # Must be public

def get_access_token():
    url = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
    response = requests.get(url, auth=HTTPBasicAuth(CONSUMER_KEY, CONSUMER_SECRET))
    return response.json().get('access_token')

def lipa_na_mpesa(phone, amount, account_reference='SPRINTUP', transaction_desc='Booking Payment'):
    access_token = get_access_token()
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    password = base64.b64encode((BUSINESS_SHORTCODE + PASSKEY + timestamp).encode()).decode()

    payload = {
        "BusinessShortCode": 174379,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": 1,
        "PartyA": 254708374149,
        "PartyB": 174379,
        "PhoneNumber": 254708374149,
        "CallBackURL": 'https://e8072e81c2e0.ngrok-free.app',
        "AccountReference": account_reference,
        "TransactionDesc": transaction_desc
    }

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    response = requests.post(url, json=payload, headers=headers)
    return response.json()
