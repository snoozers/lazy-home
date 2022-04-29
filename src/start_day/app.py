import json

def lambda_handler(event, context):
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "一日の始まり！！！",
            # "location": ip.text.replace("\n", "")
        }),
    }
