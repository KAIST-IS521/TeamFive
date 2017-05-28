import re
import requests

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
