import json
import requests
import base64
import datetime
import os
from Crypto.Hash import CMAC
from Crypto.Cipher import AES
from http import HTTPStatus
from aws import FrontDoor

BASE_END_POINT = 'https://app.candyhouse.co/api/sesame2'
API_KEY = os.environ['SESAME_API_KEY']
DEVICE_UUID = os.environ['SESAME_DEVICE_UUID']
DEVICE_SECRET = os.environ['SESAME_DEVICE_SECRET']

class Key():
    def lock(self) -> bool:
        # lock
        return self.executeCommand(82) == HTTPStatus.OK

    def unlock(self) -> bool:
        # unlock
        succeeded = self.executeCommand(83) == HTTPStatus.OK
        if succeeded:
            FrontDoor().put_unlock_message()

        return succeeded

    def status(self) -> str:
        self.fetch()
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