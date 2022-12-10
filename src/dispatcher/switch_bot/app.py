import json
import linebot
from aws import FrontDoor

def lambda_handler(event:dict, context:dict) -> None:
    body = json.loads(event['body'])['context']
    if 'openState' not in body:
        return

    # open | close | timeOutNotClose
    openState = body['openState']
    if openState == 'open':
        FrontDoor().put_open_message()
    elif openState == 'close':
        FrontDoor().put_close_message()
    else:
        linebot.post_message('ドアが開きっぱなしになっています')
