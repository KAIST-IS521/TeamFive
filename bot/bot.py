import sys
import random
import string
from selenium import webdriver


def read_posting(driver):
    driver.get('http://127.0.0.1:12345/bbs/list')

    continue_link = driver.find_element_by_partial_link_text('/bbs/read/')

    print(continue_link)


def bbs_login(driver):
    login_id = driver.find_element_by_id('username')
    login_id.send_keys('kwon')

    login_pw = driver.find_element_by_id('password')
    login_pw.send_keys('kwon1234')

    login_form = driver.find_element_by_class_name('form-inline')
    login_form.submit()


def set_cookie(driver):
    rand_str = lambda n: ''.join([random.choice(string.lowercase) for i in range(n)])
    flag = rand_str(32)
    domain = '.bank.com'

    driver.add_cookie({'name': 'flag', 'value': flag})
    #driver.add_cookie({'name': 'flag', 'value': flag, 'domain': domain}) 
    print(flag)

if __name__ == '__main__':
    driver = webdriver.Firefox()
    site = 'http://127.0.0.1:12345/bbs/login/'

    driver.get(site)
    set_cookie(driver)

    bbs_login(driver)
    #read_posting(driver)

    #driver.close()
