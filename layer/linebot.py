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
