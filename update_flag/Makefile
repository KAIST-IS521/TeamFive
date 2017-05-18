all: setup

setup: env
	. env/bin/activate && pip install -r requirement.txt

env:
	virtualenv --python=`which python2.7` env

clean:
	rm -rf env

.PHONY: all setup clean
