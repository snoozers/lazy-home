from http import HTTPStatus
import json
from aws import FrontDoor

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
        'unlock': lambda: FrontDoor().put_unlock_message(),
        'nop': lambda: None
    }
