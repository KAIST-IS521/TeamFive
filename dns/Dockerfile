FROM ubuntu:16.04

EXPOSE 53
RUN apt-get update
RUN apt-get install -y sudo
RUN apt-get install -y dnsmasq 
RUN apt-get install -y vim
RUN echo "user=root" >> /etc/dnsmasq.conf
RUN sudo dnsmasq

