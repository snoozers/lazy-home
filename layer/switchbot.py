import json
import os
import requests
import time
import hashlib
import hmac
import base64

BASE_END_POINT = 'https://api.switch-bot.com/v1.1'

def headers() -> dict:
    # open token
    token = os.environ['SWITCH_BOT_OPEN_TOKEN']
    # secret key
    secret = os.environ['SWITCH_BOT_CLIENT_SECRET']
    nonce = ''
    t = int(round(time.time() * 1000))
    string_to_sign = '{}{}{}'.format(token, t, nonce)

    string_to_sign = bytes(string_to_sign, 'utf-8')
    secret = bytes(secret, 'utf-8')

    sign = base64.b64encode(hmac.new(secret, msg=string_to_sign, digestmod=hashlib.sha256).digest())

    return {
        'Authorization': token,
        't': str(t),
        'sign': str(sign, 'utf-8'),
        'nonce': nonce
    }

devices = requests.get(
    url=BASE_END_POINT + '/devices',
    headers=headers()
).json()['body']

class LivingCurtains():
    def __init__(self):
        for k, v in enumerate(devices['deviceList']):
            if v['deviceName'] == 'カーテン':
                key = k
                break
        self.__devices_ids = devices['deviceList'][key]['curtainDevicesIds']

    def open(self) -> None:
        for device_id in self.__devices_ids:
            requests.post(
                url=f'{BASE_END_POINT}/devices/{device_id}/commands',
                headers=headers(),
                data=json.dumps({
                    'command': 'turnOn',
                    'parameter': 'default',
                    'commandType': 'command'
                })
            )

class InfraredRemoteDevice():
    def __init__(self, deviceName:str):
        for k, v in enumerate(devices['infraredRemoteList']):
            if v['deviceName'] == deviceName:
                key = k
                break
        self.__devices_id = devices['infraredRemoteList'][key]['deviceId']

    def turn_off(self) -> None:
        requests.post(
            url=f'{BASE_END_POINT}/devices/{self.__devices_id}/commands',
            headers=headers(),
            data=json.dumps({
                'command': 'turnOff',
                'parameter': 'default',
                'commandType': ''
            })
        )

class LivingAirConditioner(InfraredRemoteDevice):
    def __init__(self):
        super().__init__('エアコン')

class LivingLight(InfraredRemoteDevice):
    def __init__(self):
        super().__init__('ライト')
