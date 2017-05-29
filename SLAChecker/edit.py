import os
import sys
import requests
import re
from common import ID, PW, get_csrf_token, test_connection, get_a_post
from login import test_login

def test_edit(domain, session):
    post_id = get_a_post(domain, session)

    r = session.get(domain + '/bbs/edit/' + str(post_id))
    token = get_csrf_token(r)

    payload = {'title': 'edit_sla',
               'content': 'edit_sla',
               'csrfmiddlewaretoken': token}

    r = session.post(domain + '/bbs/edit/' + str(post_id), data = payload )

    if r.status_code == requests.codes.ok:
        # TODO: test more
        return True

    return False

def run(domain, session):
    if test_login(domain, session):
        if test_edit(domain, session):
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
    print (exit_code)
    exit(exit_code)
