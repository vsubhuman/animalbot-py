import os

import telegram
from vutil import *

version = '1.0-SNAPSHOT'
bot = telegram.bot(os.environ['bot_token'])
environment = os.environ.get('environment', 'test')


def handler(evt, ctx):
    print("Event: %s" % evt)
    with_(evt.get('message'), handle_message)


def handle_message(msg):
    print('Processing message')
    chat, user, text = destruct(msg, 'chat', 'from', 'text')
    chat_id, chat_type = destruct(chat, 'id', 'type')
    if environment == 'test':
        if chat_type != 'private':
            bot.leave_chat(chat_id)
            return
        elif user['username'] != 'vsubhuman':
            return
    send_version = lambda: bot.send_message(chat_id, "Version: %s" % version)
    send_echo = lambda: bot.send_message(chat_id, "Echo> %s" % text)
    case(lower(text), {
        '/version': send_version,
        DEFAULT: send_echo,
        None: lambda: None
    })
