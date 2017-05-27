#!/bin/sh
set -e
sudo docker build -t five .
sudo docker run --rm --name five \
    -p 80:80 \
    -it five
