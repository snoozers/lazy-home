import linebot
from sesami import Key

def lambda_handler(event, context):
    linebot.post_message('セサミの開閉状態: ' + Key().fetch().status())
