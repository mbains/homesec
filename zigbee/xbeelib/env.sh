#!/bin/bash
sudo apt-get install python-dev python-setuptools postfix
sudo easy_install pip
sudo pip install virtualenv

virtualenv env
. env/bin/activate
pip install pyserial
pip install twisted
pip install scapy
