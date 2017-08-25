from requests_futures import sessions

from vutil import *


def get_doggos(num=3):
    r1, r2 = get_async(
        "https://api.thedogapi.co.uk/v2/dog.php?limit=%s" % num,
        "https://dog-api.kinduff.com/api/facts")
    return {
        'images': r1.json().get('data'),
        'text': head(r2.json().get('facts'))
    }


def get_async(*urls):
    session = sessions.FuturesSession()
    futures = map(session.get, urls)
    return list(x.result() for x in futures)
