from http import HTTPStatus
import json
import linebot

def lambda_handler(event, context):
    action = get_action_type(event)
    execute = {
        'unlock': lambda: unlock(),
        'nop': lambda: None
    }
    execute[action]()

    return {
        'statusCode': HTTPStatus.OK,
        'body': json.dumps({
            'message': f'{action} was executed'
        }),
    }

def get_action_type(event) -> str:
    # IFTTTから実行された場合
    if 'action_type' in json.loads(event['body']):
        return json.loads(event['body'])['action_type']

    print(event)

    # LineのWebhockで実行された場合
    return 'nop'

def unlock() -> None:
    # TODO: 解錠
    linebot.post_message('解錠しました。')
