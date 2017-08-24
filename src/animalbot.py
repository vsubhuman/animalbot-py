import requests
import os

TOKEN = os.environ['bot_token']


def post(method, body):
    print("Posting '%s' with data: %s" % (method, body))
    r=requests.post("https://api.telegram.org/bot%s/%s" % (TOKEN, method), data=body)
    print("Response from '%s' is {code=%s, reason=%s}: %s" % (method, r.status_code, r.reason, r.text))


def send_message(chat_id, text):
    post('sendMessage', {'chat_id': chat_id, 'text': text})


def handler(evt, ctx):
    print("Event: %s" % evt)
    msg=evt['message']
    if msg:
        print('Processing message')
        chat=msg['chat']
        text=msg['text']
        user=msg['from']
        if text and (chat['type'] == 'private') and (user['username'] == 'vsubhuman'):
            send_message(chat['id'], "Echo> %s" % text)
