import json
import requests
import base64
import datetime
import time
import os
from Crypto.Hash import CMAC
from Crypto.Cipher import AES
from http import HTTPStatus
import boto3

BASE_END_POINT = 'https://app.candyhouse.co/api/sesame2'
API_KEY = os.environ['SESAMI_API_KEY']
DEVICE_UUID = os.environ['SESAMI_DEVICE_UUID']
DEVICE_SECRET = os.environ['SESAMI_DEVICE_SECRET']

class Key():
    def lock(self) -> bool:
        # lock
        return self.executeCommand(82) == HTTPStatus.OK

    def unlock(self) -> bool:
        # unlock
        success = self.executeCommand(83) == HTTPStatus.OK
        if success:
            boto3.client('iotevents-data').batch_put_message(
                messages=[{
                    'messageId': str(int(time.time())),
                    'inputName': 'front_door_input',
                    'payload': bytes(json.dumps({'key': {'event': 'unlock'}}), 'utf-8')
                }]
            )

        return success

    def status(self) -> str:
        # locked | unlocked | moved
        return self.__status

    def fetch(self):
        res = requests.get(
            url=f'{BASE_END_POINT}/{DEVICE_UUID}',
            headers={'x-api-key': API_KEY}
        )
        self.__status = res.CHSesame2Status

        return self

    def executeCommand(self, cmd:int) -> int:
        base64_history = base64.b64encode('IFTTT button'.encode('utf-8')).decode()

        timestamp = int(datetime.datetime.now().timestamp())
        message = timestamp.to_bytes(4, byteorder='little').hex()[2:8]
        cmac = CMAC.new(bytes.fromhex(DEVICE_SECRET), ciphermod=AES).update(bytes.fromhex(message))
        sign = cmac.hexdigest()

        res = requests.post(
            url=f'{BASE_END_POINT}/{DEVICE_UUID}/cmd',
            data=json.dumps({
                'cmd': cmd,
                'history': base64_history,
                'sign': sign
            }),
            headers={'x-api-key': API_KEY}
        )

        return res.status_code