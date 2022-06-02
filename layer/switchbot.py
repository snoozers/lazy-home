import json
import os
import requests

BASE_END_POINT = 'https://api.switch-bot.com'
devices = requests.get(
    url=BASE_END_POINT + '/v1.0/devices',
    headers={
        'Authorization': os.environ['SWITCH_BOT_OPEN_TOKEN']
    }
).json()['body']

class LivingCurtains():
    def __init__(self):
        for k, v in enumerate(devices['deviceList']):
            if v['deviceName'] == 'カーテン':
                key = k
                break
        self.__devices_ids = devices['deviceList'][key]['curtainDevicesIds']

    def open(self):
        for device_id in self.__devices_ids:
            requests.post(
                url='%s/v1.0/devices/%s/commands' % (BASE_END_POINT, device_id),
                headers={
                    'Authorization': os.environ['SWITCH_BOT_OPEN_TOKEN'],
                    'Content-Type': 'application/json; charset=utf8',
                },
                data=json.dumps({
                    'command': 'turnOn',
                    'parameter': 'default',
                    'commandType': 'command'
                })
            )
