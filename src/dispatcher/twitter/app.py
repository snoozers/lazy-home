from http import HTTPStatus
import json

def lambda_handler(event, context):
    # TODO: ステートマシーンの実行を開始する処理など...
    action = 'test'

    return {
        'statusCode': HTTPStatus.OK,
        'body': json.dumps({
            'message': f'{action} was dispatched'
        }),
    }
