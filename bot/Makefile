all: setup deps

deps:
	sudo bash install-deps.bash

setup: env
	. env/bin/activate && pip install -r requirement.txt

env:
	virtualenv --python=`which python2.7` env

clean:
	rm -rf env geckodriver.log

.PHONY: all setup clean
