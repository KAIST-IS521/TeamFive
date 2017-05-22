import sys
import random
import string
from selenium import webdriver
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

POSTING_XPATH = '/html/body/div/table/tbody/tr/td/a'
FLAG_FILE = '/tmp/IS521GovFlag'
#Below two variables are temporary for test
ADMIN_ID = 'kwon'
ADMIN_PW = 'kwon1234'

def read_posting(driver):
    # Get post's links by inspecting html
    links = driver.find_elements_by_xpath(POSTING_XPATH)
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
    #TODO: Change login procee. Login with admin user for TEST
    login_id = driver.find_element_by_id('username')
    login_id.send_keys(ADMIN_ID)

    login_pw = driver.find_element_by_id('password')
    login_pw.send_keys(ADMIN_PW)

    login_form = driver.find_element_by_class_name('form-inline')
    login_form.submit()
    try:
        element = WebDriverWait(driver, 5).until(EC.title_contains('list'))
    except:
        print "Cannot login"
    finally:
        print "Login finished"
   

def set_cookie(driver):
    # Get a flag from the file which a flag updater is generated
    #TODO: Error handling 
    f = open(FLAG_FILE, 'r')
    flag = f.read()
    f.close()

    # Check flag size
    if len(flag) != 16:
        print "Invalid flag"
        driver.close()
        exit(1)
    
    #TODO: Set cross domain cookie
    driver.add_cookie({'name': 'flag', 'value': flag})
    #driver.add_cookie({'name': 'flag', 'value': flag, 'domain': 'bank.com'})
    print "Flag: " + flag


def get_url(argv):
    if len(argv) != 2:
        print "Usage: " + argv[0] + " [goverment homepage URL]:[PORT]"
        #exit(1)
        #TODO: Uncomment an above line and Remove a below line which are for test
        return 'http://127.0.0.1:12345/bbs/login/'
    else:
        return argv[1]


if __name__ == '__main__':
    site = get_url(sys.argv)

    profile = FirefoxProfile()
    #profile.set_preference('security.fileuri.strict_origin_policy', False)

    driver = webdriver.Firefox(profile)
    driver.implicitly_wait(3)

    driver.get(site)
    set_cookie(driver)

    bbs_login(driver)
    read_posting(driver)

    #driver.close()
