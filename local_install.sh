#!/usr/bin/env bash

pip3 uninstall atf -y

python3 setup.py bdist_egg

cd dist && easy_install *.egg