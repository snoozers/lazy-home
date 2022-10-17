from http import HTTPStatus
import json
import time
import boto3
import linebot

def lambda_handler(event:dict, context:dict) -> None:
    body = json.loads(event['body'])['context']
    if 'openState' not in body:
        return

    # open | close | timeOutNotClose"
    openState = body['openState']
    if openState in ['open', 'close']:
        res = boto3.client('iotevents-data').batch_put_message(
            messages=[{
                'messageId': str(int(time.time())),
                'inputName': 'front_door_input',
                'payload': bytes(json.dumps({"door": {"event": openState}}), 'utf-8')
            }]
        )
        if res.status_code != HTTPStatus.OK:
            linebot.post_message('batch_put_messageの操作に失敗')
