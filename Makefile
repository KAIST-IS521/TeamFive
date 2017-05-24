all: deps flag web bot key

key:
	sudo bash setup-key.bash /opt

deps:
	sudo bash install-deps.bash

flag:
	make -C update_flag

web:
	make -C web

bot:
	make -C bot

.PHONY: deps flag web bot key
