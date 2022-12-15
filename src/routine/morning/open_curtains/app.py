from switchbot import LivingCurtains

def lambda_handler(event, context):
    LivingCurtains().open()
