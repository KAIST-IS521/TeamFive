import os
import sys
import requests
import re
from common import ID, PW, get_csrf_token, test_connection
from login import test_login
from bs4 import BeautifulSoup

def get_a_post(domain, session):
    r = session.get(domain + '/bbs/list')
    soup = BeautifulSoup(r.content, 'html.parser')

    for link in soup.find_all('a'):
        rpage = link.get('href')
        if "/bbs/read/" in rpage:
            return rpage.split('/')[-1]
    return -1

def test_read(domain, session):
    post_id = get_a_post(domain, session)

    r = session.get(domain + '/bbs/read/' + str(post_id))

    if r.status_code == requests.codes.ok:
        if post_id == -1: # fail test case
            if 'error' in r.url:
                return True
        else:
            if '/read/' + str(post_id) in r.url:
                return True

    return False

def run(domain, session):
    if test_login(domain, session):
        if test_read(domain, session):
            return 0
    return 1

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: {} <ip> <port>".format(sys.argv[0]))
        exit(1)

    session = requests.Session()
    domain = 'http://{}:{}'.format(sys.argv[1], sys.argv[2])

    # check if connection can establish
    if not test_connection(domain):
        exit(2)

    exit_code = run(domain, session)
    exit(exit_code)
