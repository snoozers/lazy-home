import linebot

def lambda_handler(event, context):
    linebot.post_message('ドアが開きっぱなしになっています')
