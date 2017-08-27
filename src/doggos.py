import os
import random

from requests_futures import sessions

from vutil import *


def get_basset_chance(default):
    str_value = os.environ.get('basset_chance')
    if str_value:
        try:
            return float(str_value)
        except Exception as e:
            print("Failed to parse \"basset_chance\" '%s'! %s" % (str_value, e))
    print("Using default \"basset_chance\": %s" % default)
    return default


basset_chance = get_basset_chance(0.5)


def get_doggos(num=3, is_basset_lover=False):
    print("Acquiring doggos")
    is_basset = is_basset_lover and random.random() < basset_chance
    if is_basset:
        print("Basset lover mode")
    img_url = basset_url() if is_basset else dog_url(num)
    r1, r2 = get_async(img_url, "https://dog-api.kinduff.com/api/facts")
    images = get_bassets(r1, num) if is_basset else r1.json().get('data')
    return {
        'images': images,
        'text': head(r2.json().get('facts'))
    }


def dog_url(num):
    return "https://api.thedogapi.co.uk/v2/dog.php?limit=%s" % num


def basset_url():
    return "https://dog.ceo/api/breed/hound/basset/images"


def get_bassets(r, num):
    all_urls = r.json().get('message', [])
    url = random.sample(all_urls, num)
    return list({'url': x} for x in url)


def get_async(*urls):
    session = sessions.FuturesSession()
    futures = map(session.get, urls)
    return list(x.result() for x in futures)
