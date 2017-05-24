#!/bin/bash
set -e

msg () {
    echo -e "\033[1;32m$1\033[0;m"
}

doit () {
    msg "$*"
    $*
}

doit sudo apt-get install -y firefox
doit sudo apt-get install xvfb

if [ ! -f /usr/local/bin/geckodriver ]; then
    doit sudo chmod +x driver/geckodriver
    doit sudo cp -f driver/geckodriver /usr/local/bin/geckodriver
fi
