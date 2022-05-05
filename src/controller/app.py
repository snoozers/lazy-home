from http import HTTPStatus
import json
import linebot

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

    # IFTTTから実行された場合
    if 'action_type' in body:
        return body['action_type']

    # LineのWebhockで実行された場合
    if ('events' in body
            and body['events'][0]['message']['type'] == 'text'
            and body['events'][0]['message']['text'] in get_execution().keys()):
        return body['events'][0]['message']['text']

    return 'nop'

def get_execution() -> dict:
    return {
        'unlock': lambda: unlock(),
        'lock': lambda: lock(),
        'nop': lambda: None
    }

def unlock() -> None:
    # TODO: 解錠
    linebot.post_message('解錠しました。')

def lock() -> None:
    # TODO: 施錠
    linebot.post_message('施錠しました。')
