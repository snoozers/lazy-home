from http import HTTPStatus
import json
import linebot

def lambda_handler(event, context):
    action = get_action_type(event)
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

def get_action_type(event) -> str:
    if 'action_type' in json.loads(event['body']):
        return json.loads(event['body'])['action_type']

    # TODO: linebot用のアクション
    return 'nop'

def unlock() -> None:
    # TODO: 解錠
    linebot.post_message('解錠しました。')
