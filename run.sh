#!/bin/sh
set -e
sudo docker build -t five .
sudo docker run --rm --name five \
    -e "FLAG_DOMAIN=naver.com" \
    -p 80:80 -p 42:42 \
    -it five \
    $@
