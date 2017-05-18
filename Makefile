all: deps flag web

deps:
	sudo bash install-deps.bash

flag:
	make -C flag

web:
	make -C web

.PHONY: deps flag web
