import datetime
import os
import random

import cates
import telegram
from vutil import *

version = '1.1-SNAPSHOT'
bot_username = os.environ['bot_username'].lower()
bot = telegram.bot(os.environ['bot_token'])
environment = os.environ.get('environment', 'test')

def handler(evt, ctx):
    print("Event: %s" % evt)
    with_(evt.get('message'), handle_message)

def handle_message(msg):
    msg['date'] = datetime.datetime.fromtimestamp(msg['date'])
    print("Processing message from %s" % msg['date'].strftime('%Y-%m-%d %H:%M:%S'))
    chat, user, text = destruct(msg, 'chat', 'from', 'text')
    text, is_personal = destruct(fix_text(text), 'text', 'personal')
    chat_id, chat_type = destruct(chat, 'id', 'type')
    uname, fname = destruct(user, 'username', 'first_name')
    if environment == 'test':
        if chat_type != 'private':
            bot.leave_chat(chat_id)
            return
        elif uname != 'vsubhuman':
            return
    case(lower(text), {
        '/animal': lambda: send_animal_help(chat_id),
        '/cate': lambda: send_cate(chat_id, fname),
        '/start': lambda: send_hello(chat_id, fname),
        '/version': lambda: bot.send_message(chat_id, "Version: %s" % version),
        DEFAULT: lambda: send_help(chat_id, fname),
        None: lambda: None
    })


def fix_text(text):
    if lower(text).endswith("@%s" % bot_username):
        return {'text': text[0:len(text) - len(bot_username) - 1], 'personal': True}
    else:
        return {'text': text, 'personal': True}


def send_help(chat_id, fname):
    text = "Sorry, %s, the proper command is: `/cate`" % fname
    return bot.send_message(chat_id, text)


def send_animal_help(chat_id):
    text = "The only supported animal for now is `/cate` =)"
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
            r = case(type, {
                'jpg': lambda: bot.send_photo(chat_id, url, text),
                'gif': lambda: bot.send_video(chat_id, url, text)
            })
            if r.status_code == 200:
                print("Successfully sent a cate! (%s)" % r)
                return r
            else:
                print("Failed to send cate with reason: %s" % r.reason)
                if len(imgs) - i <= 1:
                    raise BaseException("Giving up on sending cate: %s" % r)
        except Exception as e:
            print("Failed to send cate with exception: %s" % e)
            if len(imgs) - i <= 1:
                raise
