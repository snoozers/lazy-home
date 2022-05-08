from datetime import datetime, timedelta

def lambda_handler(event, context) -> dict:
    # TODO: twitterから明日の起床時刻を取得
    now = datetime.utcnow()
    open_curtains_at = now + timedelta(seconds=60)

    return {
        'open_curtains_at': open_curtains_at.strftime('%Y-%m-%dT%H:%M:%SZ')
    }