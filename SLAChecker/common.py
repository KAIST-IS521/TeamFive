import re
import requests

ID = 'admin'
PW = 'asdf1234'

def get_csrf_token(r):
    m = re.search('name=.csrfmiddlewaretoken. value=.([^\'\"]+)', r.content)
    return m.group(1)

def test_connection(domain):
    r = requests.get(domain)
    return r.status_code
