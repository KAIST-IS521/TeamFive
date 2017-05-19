import sys
import random
import string
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def read_posting(driver):
    # Get post's links by inspecting html
    links = driver.find_elements_by_xpath('/html/body/div/table/tbody/tr/td/a')
    link_num = len(links)

    if(link_num == 0):
        print "Caanot read any post."

    else:
        # Read each post and go back to bbs list page 
        for i in range(len(links)):
            links[i].click()
            WebDriverWait(driver, 5).until(EC.title_contains('Read'))
            driver.execute_script('window.history.go(-1)')

def bbs_login(driver):
    # Login with admin user for TEST
    login_id = driver.find_element_by_id('username')
    login_id.send_keys('kwon')

    login_pw = driver.find_element_by_id('password')
    login_pw.send_keys('kwon1234')

    login_form = driver.find_element_by_class_name('form-inline')
    login_form.submit()
    try:
        element = WebDriverWait(driver, 5).until(EC.title_contains('list'))
    except:
        print "Cannot login"
    finally:
        print "Login finished"
   

def set_cookie(driver):
    #rand_str = lambda n: ''.join([random.choice(string.lowercase) for i in range(n)])
    # Get a flag from the file which a flag updater is generated
    f = open('/tmp/IS521GovFlag', 'r')
    flag = f.read()
    f.close()

    if len(flag) != 16:
        print "Invalid flag"
        #driver.close()
        #return

    driver.add_cookie({'name': 'flag', 'value': flag})
    #driver.add_cookie({'name': 'flag', 'value': flag, 'domain': '.bank.com'})
    print "Flag: " + flag

if __name__ == '__main__':
    driver = webdriver.Firefox()
    site = 'http://127.0.0.1:12345/bbs/login/'
    driver.implicitly_wait(3)

    driver.get(site)
    set_cookie(driver)

    bbs_login(driver)
    read_posting(driver)

    #driver.close()
