import linebot
from switchbot import LivingCurtains

def lambda_handler(event, context):
    LivingCurtains().open()
    linebot.post_message('カーテンを開きました')
