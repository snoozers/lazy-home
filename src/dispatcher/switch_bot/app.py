from http import HTTPStatus
import json

def lambda_handler(event:dict, context:dict) -> dict:
    print(json.loads(event['body']))

    return {
        'statusCode': HTTPStatus.OK
    }
