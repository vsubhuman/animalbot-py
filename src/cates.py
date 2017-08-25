import xml.etree.ElementTree as ET

import requests


def get_cates(type, num=3):
    url = "http://thecatapi.com/api/images/get?format=xml&size=full&results_per_page=%s&type=%s" % (num, type)
    r = requests.get(url)
    if r.status_code == 200:
        root = ET.fromstring(r.text)
        el2dict = lambda el: dict((c.tag, c.text) for c in el.getchildren())
        return list(map(el2dict, root.find('./data/images')))

