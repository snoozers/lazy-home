import base64
import hashlib
import hmac
import json
from http import HTTPStatus
import os

def lambda_handler(event, context):
    sha256_hash_digest = hmac.new(
        os.environ['TWITTER_CONSUMER_SECRET'].encode(),
        msg=event['queryStringParameters']['crc_token'].encode(),
        digestmod=hashlib.sha256
    ).digest()

    return {
        'statusCode': HTTPStatus.OK,
        'body': json.dumps({
            'response_token': 'sha256=' + base64.b64encode(sha256_hash_digest).decode()
        }),
    }
