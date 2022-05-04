import json
import linebot
from http import HTTPStatus

def lambda_handler(event, context):
    action = getActionType(event)
    execute = {
        'unlock': unlock(),
        'nop': ''
    }
    execute[action]

    return {
        'statusCode': HTTPStatus.OK,
        'body': json.dumps({
            'message': f'{action} was executed'
        }),
    }

def getActionType(event) -> str:
    if 'action_type' in json.loads(event['body']):
        return json.loads(event['body'])['action_type']

    # TODO: linebot用のアクション
    return 'nop'

def unlock() -> None:
    # TODO: 解錠
    linebot.postMessage('解錠しました。')
