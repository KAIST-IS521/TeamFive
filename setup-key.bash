#!/bin/bash

if [ "$#" -lt 1 ];
then
    echo "Usage: setup-key.bash KEY_ROOT"
    exit 1
fi

set -ex
KEY_ROOT="$1"

# Copy key files
sudo mkdir -p $KEY_ROOT/pub $KEY_ROOT/priv $KEY_ROOT/student
sudo cp ./key/*.pub $KEY_ROOT/pub/
sudo cp ./key/student/*.pub $KEY_ROOT/student/
if [ -f ./key/service.key ]; then
    sudo cp ./key/service.key $KEY_ROOT/priv/
fi

# Setup web config
echo "from .prod import *" > ./web/gov/settings/local.py
echo "" >> ./web/gov/settings/local.py
echo "SECRET_KEY='`head /dev/urandom | base64 | head -n1`'" >> ./web/gov/settings/local.py
sudo echo "NOTARY_PUBKEY='$KEY_ROOT/pub/notary.pub'" >> ./web/gov/settings/local.py
sudo echo "STUDENT_PUBKEY_DIR='$KEY_ROOT/student'" >> ./web/gov/settings/local.py
sudo echo "SERVICE_PUBKEY='$KEY_ROOT/pub/service.pub'" >> ./web/gov/settings/local.py
sudo echo "SERVICE_PRIVKEY='$KEY_ROOT/priv/service.key'" >> ./web/gov/settings/local.py
echo "ALLOWED_HOSTS = ['*']" >> ./web/gov/settings/local.py
