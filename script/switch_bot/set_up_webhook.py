import json
import requests
import time
import hashlib
import hmac
import base64

BASE_END_POINT = 'https://api.switch-bot.com/v1.1'

url = input('webhook_url:')
token = input('switch_bot_open_token:')
secret = input('switch_bot_client_secret:')
nonce = ''
t = int(round(time.time() * 1000))
string_to_sign = '{}{}{}'.format(token, t, nonce)

string_to_sign = bytes(string_to_sign, 'utf-8')
secret = bytes(secret, 'utf-8')

sign = base64.b64encode(hmac.new(secret, msg=string_to_sign, digestmod=hashlib.sha256).digest())

res = requests.post(
    url=f'{BASE_END_POINT}/webhook/setupWebhook',
    headers={
        'Authorization': token,
        't': str(t),
        'sign': str(sign, 'utf-8'),
        'nonce': nonce
    },
    data=json.dumps({
        'action': 'setupWebhook',
        'url': url,
        'deviceList': 'ALL'
    })
)

if res.status_code == 200:
    print('success')
else:
    print('failed')