import linebot

def lambda_handler(event, context):
    # TODO: カーテンを開く処理
    linebot.post_message('カーテンを開きました')
    print(event)
    print(context)
