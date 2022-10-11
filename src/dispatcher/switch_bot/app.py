from http import HTTPStatus
import json
import linebot

def lambda_handler(event:dict, context:dict) -> dict:
    # open | close | timeOutNotClose"
    openState = json.loads(event['body'])['context']['openState']
    if openState == 'open':
        linebot.post_message('ドアが開きました')
    elif openState == 'close':
        linebot.post_message('ドアが閉まりました')


    return {
        'statusCode': HTTPStatus.OK
    }
