from sesame import Key

def lambda_handler(event, context):
    Key().lock()
