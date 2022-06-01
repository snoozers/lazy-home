from datetime import datetime, timezone, timedelta
from http import HTTPStatus
import json
import os
import re
from time import strftime
import boto3

def lambda_handler(event, context):
    tweet = json.loads(event['body'])['tweet_create_events'][0]
    print(tweet)

    hashtags = [hashtag['text'] for hashtag in tweet['entities']['hashtags']]
    if '就寝' in hashtags:
        # 設定した起床時刻のfromを取得する
        jst_time = re.search(r'アラーム設定 (\d{1,2}:\d{2}) - \d{1,2}:\d{2}', tweet['text']).groups()[0]
        jst_now = datetime.now(timezone(timedelta(hours=9)))
        # 就寝時刻が午前の場合、起床日が同日になる
        jst_date = jst_now.strftime('%Y-%m-%d') if jst_now.strftime('%p') == 'AM' else (jst_now + timedelta(days=1)).strftime('%Y-%m-%d')
        jst_datetime = datetime.strptime(jst_date + ' ' + jst_time + '+0900', '%Y-%m-%d %H:%M%z', )
        # アラームが鳴る1分前にカーテンを開けたい
        jst_open_curtains_at= jst_datetime + timedelta(minutes=-1)
        utc_open_curtains_at = jst_open_curtains_at.astimezone(timezone.utc)

        print(jst_open_curtains_at)
        print(utc_open_curtains_at)

        client = boto3.client('stepfunctions')
        client.start_execution(
            stateMachineArn=os.environ['OPEN_CURTAINS_STATE_MACHINE_ARN'],
            name=utc_open_curtains_at.strftime('%Y-%m-%d'),
            # StepFunctionsのWaitに指定可能なフォーマットに変更
            input=json.dumps(utc_open_curtains_at.strftime('%Y-%m-%dT%H:%M:%SZ'))
        )


    action = 'test'

    return {
        'statusCode': HTTPStatus.OK,
        'body': json.dumps({
            'message': f'{action} was dispatched'
        }),
    }
