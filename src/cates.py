import xml.etree.ElementTree as ET

import requests


def get_cates(type, num=3):
    url = "http://thecatapi.com/api/images/get?format=xml&size=full&results_per_page=%s&type=%s" % (num, type)
    r = requests.get(url)
    if r.status_code == 200:
        root = ET.fromstring(r.text)
        return list(map(_el2dict, root.find('./data/images')))


def _el2dict(el):
    res = {}
    for c in el.getchildren():
        res[c.tag] = c.text
    return res
