#!/usr/bin/env bash

pip3.8 uninstall atf -y

python3.8 setup.py bdist_egg

cd dist && easy_install *.egg