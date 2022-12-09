from http import HTTPStatus
import json
import linebot
from sesame import Key

def lambda_handler(event, context):
    action = get_action(event)
    execute = get_execution()

    execute[action]()

    return {
        'statusCode': HTTPStatus.OK,
        'body': json.dumps({
            'message': f'{action} was executed'
        }),
    }

def get_action(event) -> str:
    body = json.loads(event['body'])

    if body['action_type'] in get_execution().keys():
        return body['action_type']

    return 'nop'

def get_execution() -> dict:
    return {
        'unlock': lambda: unlock(),
        'nop': lambda: None
    }

def unlock() -> None:
    linebot.post_message('解錠しました') if Key().unlock() else linebot.post_message('鍵の解錠に失敗しました')
