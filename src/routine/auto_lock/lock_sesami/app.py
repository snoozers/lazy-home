from sesami import Key

def lambda_handler(event, context):
    linebot.post_message('自動施錠しました') if Key().lock() else linebot.post_message('鍵の施錠に失敗しました')
