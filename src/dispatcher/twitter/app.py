from datetime import datetime, timezone, timedelta
from http import HTTPStatus
import json
import os
import re
import boto3
from switchbot import LivingAirConditioner, LivingLight

def lambda_handler(event:dict, context:dict) -> dict:
    tweet = json.loads(event['body'])['tweet_create_events'][0]
    hashtags = [hashtag['text'] for hashtag in tweet['entities']['hashtags']]

    if '就寝' in hashtags:
        execute_open_curtains_state_machine(get_utc_open_curtains_at(tweet))
    elif '入眠' in hashtags:
        turn_off_all()

    return {
        'statusCode': HTTPStatus.OK
    }

def get_utc_open_curtains_at(tweet:dict) -> datetime:
    # 設定した起床時刻のfromを取得する
    jst_time = re.search(r'アラーム設定 (\d{1,2}:\d{2}) - \d{1,2}:\d{2}', tweet['text']).groups()[0]
    jst_now = datetime.now(timezone(timedelta(hours=9)))
    # 就寝時刻が午前の場合、起床日が同日になる
    jst_date = jst_now.strftime('%Y-%m-%d') if jst_now.strftime('%p') == 'AM' else (jst_now + timedelta(days=1)).strftime('%Y-%m-%d')
    jst_datetime = datetime.strptime(jst_date + ' ' + jst_time + '+0900', '%Y-%m-%d %H:%M%z', )

    # アラームが鳴る1分前にカーテンを開けたい
    jst_open_curtains_at= jst_datetime + timedelta(minutes=-1)

    return jst_open_curtains_at.astimezone(timezone.utc)

def execute_open_curtains_state_machine(open_curtains_at: datetime) -> None:
    client = boto3.client('stepfunctions')
    # 実行中のOpenCurtainsステートマシーンがある場合停止して新たに実行
    running = client.list_executions(
        stateMachineArn=os.environ['OPEN_CURTAINS_STATE_MACHINE_ARN'],
        statusFilter='RUNNING'
    )
    for execution in running['executions']:
        client.stop_execution(executionArn=execution['executionArn'])
    client.start_execution(
        stateMachineArn=os.environ['OPEN_CURTAINS_STATE_MACHINE_ARN'],
        # StepFunctionsのWaitに指定可能なフォーマットに変更
        input=json.dumps({
            'open_curtains_at': open_curtains_at.strftime('%Y-%m-%dT%H:%M:%SZ')
        })
    )

def turn_off_all() -> None:
    LivingAirConditioner().turn_off()
    LivingLight().turn_off()
