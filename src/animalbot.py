import os

import telegram

version = '1.0-SNAPSHOT'
bot = telegram.bot(os.environ['bot_token'])
environment = os.environ.get('environment', 'test')


def handler(evt, ctx):
    print("Event: %s" % evt)
    msg = evt.get('message')
    if msg:
        print('Processing message')
        chat = msg['chat']
        user = msg['from']
        text = msg.get('text')
        if environment == 'test':
            if chat['type'] != 'private':
                bot.leave_chat(chat['id'])
                return
            elif user['username'] != 'vsubhuman':
                return
        if text:
            bot.send_message(chat['id'], "Echo> %s" % text)