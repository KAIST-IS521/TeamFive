import sys
import random
import string
import time
from selenium import webdriver
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

POSTING_XPATH = '/html/body/div/table/tbody/tr/td/a'
FLAG_FILE = '/tmp/IS521GovFlag'
#Below two variables are temporary for test
ADMIN_ID = 'kwon'
ADMIN_PW = 'kwon1234'
SITE = "127.0.0.1:12345"
DOMAIN_NAME = "bank.com"
LOGIN_URI = '/bbs/login/'

def read_posting(driver):
    # Get post's links by inspecting html
    links = driver.find_elements_by_xpath(POSTING_XPATH)
    link_num = len(links)

    if(link_num == 0):
        print "Caanot read any post."

    else:
        # Read each post and go back to bbs list page 
        for i in range(len(links)):
            try:
                WebDriverWait(driver, 5).until(EC.title_contains('list'))
                links[i].click()
                WebDriverWait(driver, 5).until(EC.title_contains('Read'))
                # Wait 1 second after closing all alert boxes
                while WebDriverWait(driver, 1).until(EC.alert_is_present()):
                    alert = driver.switch_to_alert()
                    alert.accept()
            except:
                driver.execute_script('window.history.go(-1)')
 

def bbs_login(driver):
    visit_website(driver, SITE + LOGIN_URI)
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
        print "[Fail] Cannot login"
        driver.close()
        exit(1)
   

def set_cookie(driver, domain):
    # Get a flag from the file which a flag updater is generated
    try:
        f = open(FLAG_FILE, 'r')
        flag = f.readline()
        f.close()
    except:
        print "[Fail] Cannot read a flag file, " + FLAG_FILE
        driver.close()
        exit(1)

    # Check flag size
    flag = flag.strip()
    if len(flag) != 16:
        print "[Fail] Invalid length of the flag value, %d" % len(flag)
        driver.close()
        exit(1)

    # Set a cookie with the flag value
    try:   
        driver.add_cookie({'name': 'flag', 'value': flag, 'domain': domain})
        print "Set-cookie: Flag=" + flag
    except:
        print "Cannot set a cookie."


def get_url(argv):
    if len(argv) != 2:
        print "Usage: " + argv[0] + " [goverment homepage URL]:[PORT]"
        #exit(1)
        #TODO: Uncomment an above line and Remove a below line which are for test
        return '127.0.0.1:12345/bbs/login/'
    else:
        return argv[1]

def visit_website(driver, domain):
    driver.get('http://' + domain)
    time.sleep(2)


def set_driver(driver):
    driver.implicitly_wait(3)
    driver.set_window_size(1000, 600)
   

if __name__ == '__main__':
    site = get_url(sys.argv)

    driver = webdriver.Firefox()
    set_driver(driver)

    visit_website(driver, DOMAIN_NAME)
    set_cookie(driver, DOMAIN_NAME)

    visit_website(driver, SITE)
    bbs_login(driver)
    read_posting(driver)

    #driver.close()
