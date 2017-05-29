import os
import sys
import requests
import gnupg
from common import ID, get_csrf_token, test_connection
import re

def carve_chal(r):
    data = r.content
    pat = '-----BEGIN PGP MESSAGE-----[^\-]+-----END PGP MESSAGE-----'
    m = re.search(pat, data)
    enc_nonce = m.group(0)

    pat = '-----BEGIN PGP PUBLIC KEY BLOCK-----[^\-]+'
    pat += '-----END PGP PUBLIC KEY BLOCK-----'
    m = re.search(pat, data)
    service_pubkey = m.group(0)
    return enc_nonce, service_pubkey

def test_register(domain, session):
    r = session.get(domain + '/bbs/auth/')
    token = get_csrf_token(r)

    ID = 'mikkang' # for test
    # Get challenge
    r = session.post(domain + '/bbs/auth/chal/',
                     {'csrfmiddlewaretoken': token, 'id': ID})

    if r.url == domain + '/bbs/auth/':
        return False

    enc_nonce, service_pubkey = carve_chal(r)
    token = get_csrf_token(r)

    # Decrypt nonce
    with open('/tmp/nonce.gpg', 'w') as f:
        f.write(enc_nonce)
    os.system('rm -f /tmp/nonce.txt')
    os.system('gpg --decrypt --output /tmp/nonce.txt /tmp/nonce.gpg')
    with open('/tmp/nonce.txt', 'r') as f:
        nonce = f.read()
    nonce = nonce.splitlines()[3].strip()
    #print('nonce = {}'.format(nonce))

    # Encrypt nonce
    gpg = gnupg.GPG()
    service_gpg = gpg.import_keys(service_pubkey)
    #service_keyid = gpg.list_keys()[0]['keyid']
    resp = gpg.encrypt(nonce, service_gpg.fingerprints[0], always_trust=True)

    # Set password
    r = session.post(domain + '/bbs/auth/resp/',
                     {'csrfmiddlewaretoken': token, 'auth_resp': resp})
    token = get_csrf_token(r)

    pw = '1234'
    #print('Setting your pw to "{}"'.format(pw))
    r = session.post(domain + '/bbs/auth/success/',
                     {'csrfmiddlewaretoken': token,
                      'password': pw,
                      'password_check': pw })

    if 'login' in r.url:
        return True

    return False

def run(domain, session):
    if test_register(domain, session):
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
