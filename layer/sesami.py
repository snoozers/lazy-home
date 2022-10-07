import json
import requests
import base64
import datetime
import os
from Crypto.Hash import CMAC
from Crypto.Cipher import AES
from http import HTTPStatus

BASE_END_POINT = 'https://app.candyhouse.co/api/sesame2'

def unlock() -> bool:
    api_key = os.environ['SESAMI_API_KEY']
    device_uuid = os.environ['SESAMI_DEVICE_UUID']
    device_secret = os.environ['SESAMI_DEVICE_SECRET']

    base64_history = base64.b64encode('IFTTT button'.encode('utf-8')).decode()

    timestamp = int(datetime.datetime.now().timestamp())
    message = timestamp.to_bytes(4, byteorder='little').hex()[2:8]
    cmac = CMAC.new(bytes.fromhex(device_secret), ciphermod=AES).update(bytes.fromhex(message))
    sign = cmac.hexdigest()

    res = requests.post(
        url=f'{BASE_END_POINT}/{device_uuid}/cmd',
        data=json.dumps({
            'cmd': 83, # lock
            'history': base64_history,
            'sign': sign
        }),
        headers={'x-api-key': api_key}
    )

    return res.status_code == HTTPStatus.OK
