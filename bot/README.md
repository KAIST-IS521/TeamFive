# TeamFive/bot

The bot lauches Firefox and read every posting from Goverment homepage BBS. 

Written in Python 2.7 and python-selenium.


## Requirements

- Python 2.7
- python-selenium
- Firefox
- Geckodriver


## Caution

- config.conf
  At the beginning of the program, it reads a config file, "config.conf". If the file is not exist, then it will make a file with your STDIN inputs. When it creates a config file, 4 variable are needed: ADMIN\_ID, ADMIN\_PW, SITE, DOMAIN\_NAME. ADMIN\_ID/ADMIN\_PW means the admin account of government web application. You probably set the value when install the web application. Otherwise, just set an account which can read all posting of govrnment website's BBS postings. SITE means the address of the government website. It may have the value, "127.0.0.1:12345". DOMAIN\_NAME is a domain name of a virtual web site which is described as "bank.com" in class activity requirement file, "engineering.tex". The domain name of each team is supposed to be notified later.
  If you miss-configured, remove "config.conf" and launch bot.py. 

	pc@lab:~/TeamFive/bot$ python bot.py 
	Config file is not exist.
	Making config file...
	Enter government website admin ID: kwon
	Enter government website admin PW: password1234
	Enter government website address: http://127.0.0.1:12345
	Enter domain of bank.com: http://bank.team1.com


- webdriver
  The program is specialized for reading BBS postings of government web page. It will stop, if it encounter unexpected situation such as human interrupt, javascript redirection, and so on. Therefore, you should watch out when it reads a javascript inserted BBS posting.


## Run

	python bot.py

