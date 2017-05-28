#!/bin/sh
set -e
sudo docker build -t dns3 .
sudo docker run --rm --name dns3 \
    -p 10.0.105.42:53:53 --dns=192.168.127.15 \
    -it dns \
