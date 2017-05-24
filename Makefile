all: deps flag web bot pub

KEY_ROOT?=/opt

pub:
	sudo mkdir -p $(KEY_ROOT)/pub $(KEY_ROOT)/priv $(KEY_ROOT)/student
	sudo cp ./key/*.pub $(KEY_ROOT)/pub/
	sudo cp ./key/student/*.pub $(KEY_ROOT)/student/ 
	sudo cp ./key/*.key $(KEY_ROOT)/priv/
	echo "from .prod import *" > ./web/gov/settings/local.py
	echo "" >> ./web/gov/settings/local.py
	echo "SECRET_KEY='`head /dev/urandom | base64 | head -n1`'" >> ./web/gov/settings/local.py
	sudo echo "NOTARY_PUBKEY='$(KEY_ROOT)/pub/notary.pub'" >> ./web/gov/settings/local.py
	sudo echo "STUDENT_PUBKEY_DIR='$(KEY_ROOT)/student'" >> ./web/gov/settings/local.py
	sudo echo "SERVICE_PUBKEY='$(KEY_ROOT)/pub/service.pub'" >> ./web/gov/settings/local.py
	sudo echo "SERVICE_PRIVKEY='$(KEY_ROOT)/priv/service.key'" >> ./web/gov/settings/local.py
	echo "ALLOWED_HOSTS = ['*']" >> ./web/gov/settings/local.py

deps:
	sudo bash install-deps.bash

flag:
	make -C update_flag

web:
	make -C web

bot:
	make -C bot

.PHONY: deps flag web bot
