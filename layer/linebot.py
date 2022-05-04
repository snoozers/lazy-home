import os
import json
from urllib import request

def postMessage(message:str) -> None:
    endpoint = 'https://api.line.me/v2/bot/message/push'
    body = {
        'to': os.environ['ADMIN_LINE_USER_ID'],
        'messages': [{
            'type': 'text',
            'text': message
        }]
    }
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + os.environ['CHANNEL_ACCESS_TOKEN']
    }

    try:
        req = request.Request(endpoint, json.dumps(body).encode(), headers)
        request.urlopen(req)
    except Exception as e:
        print(e)
