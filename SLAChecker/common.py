import re
import requests
from bs4 import BeautifulSoup

ID = 'admin'
PW = 'asdf1234'

def get_csrf_token(r):
    m = re.search('name=.csrfmiddlewaretoken. value=.([^\'\"]+)', r.content)
    return m.group(1)

def test_connection(domain):
    try:
        r = requests.get(domain)
        if r.status_code == requests.codes.ok:
            return True
        return False
    except:
        return False

def get_a_post(domain, session):
    r = session.get(domain + '/bbs/list')
    soup = BeautifulSoup(r.content, 'html.parser')

    for link in soup.find_all('a'):
        rpage = link.get('href')
        if "/bbs/read/" in rpage:
            return rpage.split('/')[-1]
    return -1

