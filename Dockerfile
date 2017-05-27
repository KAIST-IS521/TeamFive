FROM ioft/i386-ubuntu:16.04

# Change apt repository since we will run it in the CTF server.
RUN sed -i 's/archive.ubuntu.com/ftp.kaist.ac.kr/g' /etc/apt/sources.list

# TODO: minimize size
RUN apt-get update
RUN apt-get install -y curl git

RUN apt-get install -y python-minimal python3 python2.7-dev python3-dev
RUN curl https://bootstrap.pypa.io/get-pip.py -o /tmp/get-pip.py \
    && python2 /tmp/get-pip.py \
    && python3 /tmp/get-pip.py \
    && rm /tmp/get-pip.py
RUN pip2 install requests python-gnupg
RUN pip3 install requests python-gnupg
RUN apt-get install -y sqlite3 gnupg

RUN apt-get install -y build-essential
RUN apt-get install -y nginx

COPY bot /bot
COPY web /web
COPY update_flag /update_flag

RUN pip3 install -r /web/requirements.txt
RUN pip2 install -r /update_flag/requirement.txt
RUN pip2 install -r /bot/requirement.txt

COPY key /key
RUN echo 'from .prod import *' >> /tmp/local.py \
    && echo "SECRET_KEY='`head /dev/urandom | base64 | head -n1`'" >> /tmp/local.py \
    && echo "NOTARY_PUBKEY='/key/notary.pub'" >> /tmp/local.py \
    && echo "STUDENT_PUBKEY_DIR='/key/student'" >> /tmp/local.py \
    && echo "SERVICE_PUBKEY='/key/service.pub'" >> /tmp/local.py \
    && echo "SERVICE_PRIVKEY='/key/service.key'" >> /tmp/local.py \
    && echo "SERVICE_PRIVKEY_PASSPHRASE=None" >> /tmp/local.py \
    && echo "ALLOWED_HOSTS = ['*']" >> /tmp/local.py \
    && mv /tmp/local.py /web/gov/settings/local.py

RUN cd web && python3 manage.py migrate

COPY nginx.conf /etc/nginx/conf.d/
RUN ln -sf /dev/stdout /var/log/nginx/access.log \
    && ln -sf /dev/stderr /var/log/nginx/error.log
RUN rm -f /etc/nginx/sites-enabled/*
RUN echo "daemon off;" >> /etc/nginx/nginx.conf
