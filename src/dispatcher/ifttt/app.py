from http import HTTPStatus
import json
from sesame import Key

def lambda_handler(event, context):
    action = get_action(event)
    execution = get_execution()

    execution[action]()

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
    Key().unlock()
