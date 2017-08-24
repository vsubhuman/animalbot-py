import requests


class Bot:
    token = None

    def __init__(self, token):
        self.token = token

    def send(self, method, body):
        print("Posting '%s' with data: %s" % (method, body))
        r = requests.post("https://api.telegram.org/bot%s/%s" % (self.token, method), data=body)
        print("Response from '%s' is {code=%s, reason=%s}: %s" % (method, r.status_code, r.reason, r.text))
        return r

    def send_message(self, chat_id, text):
        return self.send('sendMessage', {'chat_id': chat_id, 'text': text})

    def send_photo(self, chat_id, photo, text=None):
        return self.send('sendPhoto', {'chat_id': chat_id, 'photo': photo, 'caption': text})

    def send_video(self, chat_id, video, text=None):
        return self.send('sendPhoto', {'chat_id': chat_id, 'video': video, 'caption': text})

    def leave_chat(self, chat_id):
        return self.send('leaveChat', {'chat_id': chat_id})


def bot(token):
    return Bot(token)
