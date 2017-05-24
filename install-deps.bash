#!/bin/bash
set -e

msg () {
    echo -e "\033[1;32m$1\033[0;m"
}

doit () {
    msg "$*"
    $*
}

doit sudo apt-get update

# Install python
doit sudo apt-get install -y python-minimal python2.7 python3 python-dev python3-dev

# Install python for both 2 and 3
if [type "pip2" &> /dev/null] and [type "pip3" &> /dev/null]; then
    msg "pip is already installed"
else
    doit curl https://bootstrap.pypa.io/get-pip.py -o /tmp/get-pip.py
    doit sudo -H python2 /tmp/get-pip.py
    doit sudo -H python3 /tmp/get-pip.py
fi

sudo -H pip2 install virtualenv
sudo -H pip3 install virtualenv
