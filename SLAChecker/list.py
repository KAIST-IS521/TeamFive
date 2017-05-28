import os
import sys
import requests
from common import ID, PW, get_csrf_token, test_connection
from login import test_login

def test_list(domain, session):
    r = session.get(domain + '/bbs/list')

    if r.status_code == requests.codes.ok:
        if 'login' in r.url:
            return False

    return True

def run(domain, session):
    if test_login(domain, session):
        if test_list(domain, session):
            return 0
    return 1

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: {} <ip> <port>".format(sys.argv[0]))
        exit(1)

    session = requests.Session()
    domain = 'http://{}:{}'.format(sys.argv[1], sys.argv[2])

    # check if connection can establish
    if test_connection(domain) != requests.codes.ok:
        exit(2)

    exit_code = run(domain, session)
    exit(exit_code)
