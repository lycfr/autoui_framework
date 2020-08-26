#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#############################################
# File Name: setup.py
# Author: IMJIE
# Email: imjie@outlook.com
# Created Time: 2020-1-29
#############################################

import setuptools

with open("README.MD", "r", encoding='UTF-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="atf", # 软件包发行名称
    version="0.0.1", # 软件包版本
    author="igetcool_qa", # 作者
    author_email="qa@igetcool.com", # 邮件
    keywords=('macaca', 'appium', 'UI自动化', '关键字驱动'),
    description="A keyword based UI testing framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="http://gitlab.igetcool.com/qa/autoui_framework",
    packages=setuptools.find_packages(),
    include_package_data=True,
    package_data={'atf/result':['resource/*']},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires='>=3.6',
)