import os
import random
import re

import gnupg
from django.conf import settings


def _sanitize_id(auth_id):
    return re.match(r'^[a-zA-Z0-9\-_]+$', auth_id) is not None

def generate_challenge(auth_id):
    '''
    Given auth_id, generates a random nonce and
    the nonce value encrypted with the public key of auth_id.
    Returns a 2-tuple (nonce as string, encrypted_nonce as string).
    Returns None on error.
    '''
    # Block directory traversal attack.
    if not _sanitize_id(auth_id):
        return None

    # Load student's public key
    gpg = gnupg.GPG()
    key_name = '{}.pub'.format(auth_id)
    key_path = os.path.join(settings.STUDENT_PUBKEY_DIR, key_name)
    try:
        with open(key_path, "r") as f:
            gpg.import_keys(f.read())
    except FileNotFoundError:
        return None

    # Generate nonce
    nonce = str(random.randint(0, 2**64))

    # Encrypt nonce
    keyid = gpg.list_keys()[0]['keyid'] # There should be only one key.
    enc_nonce = gpg.encrypt(nonce, keyid) # Returns ascii-armored encrypted messsage.

    return (nonce, enc_nonce)

def get_service_pubkey():
    key_path = settings.SERVICE_PUBKEY
    with open(key_path, 'r') as f:
        pubkey = f.read()
    return pubkey
