import os
import random
import datetime

import cates
import telegram
from vutil import *

version = '1.0-SNAPSHOT'
bot = telegram.bot(os.environ['bot_token'])
environment = os.environ.get('environment', 'test')


def handler(evt, ctx):
    print("Event: %s" % evt)
    with_(evt.get('message'), handle_message)


def handle_message(msg):
    msg['date'] = datetime.datetime.fromtimestamp(msg['date'])
    print("Processing message from %s" % msg['date'].strftime('%Y-%m-%d %H:%M:%S'))
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
        '/cate': lambda: send_cate(chat_id, user['first_name']),
        '/version': send_version,
        DEFAULT: send_echo,
        None: lambda: None
    })


def send_cate(chat_id, fname):
    type = random.choice(['jpg', 'gif'])
    imgs = cates.get_cates(type)
    for i in range(0, len(imgs)):
        try:
            url = imgs[i]['url']
            type_str = 'pic' if type == 'jpg' else 'gif'
            text = "Here's your awesome cat %s, %s!" % (type_str, fname)
            return case(type, {
                'jpg': lambda: bot.send_photo(chat_id, url, text),
                'gif': lambda: bot.send_video(chat_id, url, text)
            })
        except Exception as e:
            print("Failed to send cate! %s" % e)
            if len(imgs) - i <= 1:
                raise e
