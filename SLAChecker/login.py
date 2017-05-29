import os
import sys
import requests
import gnupg
from common import ID, PW, get_csrf_token, test_connection


def test_login(domain, session):
    r = session.get(domain + '/bbs/login')
    token = get_csrf_token(r)

    payload = {'username': ID, 'password': PW, 'csrfmiddlewaretoken': token}
    r = session.post(domain + '/bbs/login/', data = payload )

    if r.status_code == requests.codes.ok:
        if 'list' in r.url:
            return True

    return False

def test_logout(domain, session):
    r = session.get(domain + '/bbs/logout')

    if r.status_code == requests.codes.ok:
        if 'login' in r.url:
            return False

    return True

def run(domain, session):
    if test_login(domain, session) and test_logout(domain, session):
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
