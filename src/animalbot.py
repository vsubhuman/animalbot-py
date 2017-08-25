import datetime
import os
import random

import cates
import telegram
from vutil import *

version = '1.0'
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
    uname, fname = destruct(user, 'username', 'first_name')
    if environment == 'test':
        if chat_type != 'private':
            bot.leave_chat(chat_id)
            return
        elif uname != 'vsubhuman':
            return
    case(lower(text), {
        '/cate': lambda: send_cate(chat_id, fname),
        '/start': lambda: send_hello(chat_id, fname),
        '/version': lambda: bot.send_message(chat_id, "Version: %s" % version),
        DEFAULT: lambda: send_help(chat_id, fname),
        None: lambda: None
    })


def send_help(chat_id, fname):
    text = "Sorry, %s, the proper command is: `/cate`" % fname
    return bot.send_message(chat_id, text)


def send_hello(chat_id, fname):
    text = "Hello, %s! Current command is `/cate` =)" % fname
    return bot.send_message(chat_id, text)


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
