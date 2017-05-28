import os
import sys
import requests
from common import ID, PW, get_csrf_token, test_connection
from login import test_login

def test_write(domain, session):
    r = session.get(domain + '/bbs/write')
    token = get_csrf_token(r)

    payload = {'title': 'test_sla',
               'content': 'test_sla',
               'csrfmiddlewaretoken': token}

    r = session.post(domain + '/bbs/write/', data = payload )

    if r.status_code == requests.codes.ok:
        if 'list' in r.url:
            return True

    return False

def run(domain, session):
    if test_login(domain, session):
        if test_write(domain, session):
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
