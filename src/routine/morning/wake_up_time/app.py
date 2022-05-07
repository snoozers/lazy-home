from datetime import datetime

def lambda_handler(event, context) -> dict:
    # TODO: twitterから明日の起床時刻を取得
    now = datetime.utcnow()
    print(now)
    open_curtains_at = now.strftime('%Y-%m-%dT%H:%M:%SZ')
    print(event)
    print(context)

    return {
        'open_curtains_at': open_curtains_at
    }