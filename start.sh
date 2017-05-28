#!/bin/sh

echo "SECRET_KEY='`head /dev/urandom | base64 | head -n1`'" >> /web/gov/settings/local.py
cd /web && python3 manage.py migrate

# Setup admin_pass to both web and bot.
admin_pass="`head /dev/urandom | base64 | head -n1 | cut -b -10`"
cd /web && echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', '', '$admin_pass')" | python3 manage.py shell
echo "admin_pass = $admin_pass" >> /bot/config.conf

echo "--------- Starting TeamFive ---------"
echo "admin_pass = $admin_pass"

# Run superdaemon.
/usr/bin/supervisord
