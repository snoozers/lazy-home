import json
import os
import requests

def postMessage(message:str) -> None:
    requests.post(
        url='https://api.line.me/v2/bot/message/push',
        data=json.dumps({
            'to': os.environ['ADMIN_LINE_USER_ID'],
            'messages': [{
                'type': 'text',
                'text': message
            }]
        }),
        headers={
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + os.environ['CHANNEL_ACCESS_TOKEN']
        }
    )

def  post_unlocking_stamp() -> None:
    _post_sticker(6359, 11069867)

def _post_sticker(package_id:str, sticker_id:str) -> None:
    """
    See below for available parameters
    https://developers.line.biz/ja/docs/messaging-api/sticker-list/
    """
    requests.post(
        url='https://api.line.me/v2/bot/message/push',
        data=json.dumps({
            'to': os.environ['ADMIN_LINE_USER_ID'],
            'messages': [{
                'type': 'sticker',
                'packageId': package_id,
                'stickerId': sticker_id
            }]
        }),
        headers={
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + os.environ['CHANNEL_ACCESS_TOKEN']
        }
    )