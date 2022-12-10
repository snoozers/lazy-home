import json
import time
import boto3

class FrontDoor():
    def __init__(self):
        self.__input_name = 'front_door_input'

    def put_message(self, message:dict) -> dict:
        return boto3.client('iotevents-data').batch_put_message(
            messages=[{
                'messageId': str(int(time.time())),
                'inputName': self.__input_name,
                'payload': bytes(json.dumps(message), 'utf-8')
            }]
        )

    def put_unlock_message(self) -> dict:
        return self.put_message({'key': {'event': 'unlock'}})

    def put_open_message(self) -> dict:
        return self.put_message({'door': {'event': 'open'}})

    def put_close_message(self) -> dict:
        return self.put_message({'door': {'event': 'close'}})
