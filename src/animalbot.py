import requests


def req():
    requests.post("https://api.telegram.org/bot379978390:AAHk9QTeogqdUp3waYPSMCMV6ApKYiGR5_4/sendMessage",
                  data={'chat_id': 256295697, 'text': 'Python test'})


def handler(evt, ctx):
    print(evt)

