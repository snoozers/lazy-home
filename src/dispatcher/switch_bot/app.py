from http import HTTPStatus
import json
import time
import boto3
import linebot

def lambda_handler(event:dict, context:dict) -> None:
    # open | close | timeOutNotClose"
    openState = json.loads(event['body'])['context']['openState']
    client = boto3.client('iotevents-data')
    if openState in ['open', 'close']:
        res = client.batch_put_message(
            messages=[{
                'messageId': str(int(time.time())),
                'inputName': 'front_door_input',
                'payload': bytes(json.dumps({"door": {"event": openState}}), 'utf-8'),
                'timestamp': {'timeInMillis': int(time.time())}
            }]
        )
        if res.status_code != HTTPStatus.OK:
            linebot.post_message('batch_put_messageの操作に失敗')
