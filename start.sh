#!/bin/sh
set -e

# Auto-generate admin password
admin_pass="`head /dev/urandom | base64 | head -n1 | cut -b -10`"

# Setup web service
echo "SECRET_KEY='`head /dev/urandom | base64 | head -n1`'" >> /web/gov/settings/local.py
cd /web && python3 manage.py migrate
cd /web && echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', '', '$admin_pass')" | python3 manage.py shell

# Setup bot
echo "[government]" > /bot/config.conf
echo "admin_id = admin" >> /bot/config.conf
echo "admin_pw = $admin_pass" >> /bot/config.conf
echo "site = localhost" >> /bot/config.conf
echo "domain_name = naver.com" >> /bot/config.conf

echo "--------- Starting TeamFive ---------"
echo "admin_pass = $admin_pass"

# Run superdaemon.
/usr/bin/supervisord
