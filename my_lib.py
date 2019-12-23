import requests
from fake_useragent import UserAgent
import os

def get_html(url, coding):
    ua = UserAgent()
    headers = {'user-agent': f'{ua.opera}'}
    r = requests.get(url, auth=('sanoto', 'mazyakidze652'), headers=headers)
    r.encoding = coding
    return r.text


def save_file(url, name):
    r = requests.get(url, stream=True)
    if os.path.exists('img'):
        with open(name, 'bw') as f:
            f.write(r.content)
    else:
        os.mkdir('img')
        with open(name, 'bw') as f:
            f.write(r.content)