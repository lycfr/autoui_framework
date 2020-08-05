#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''=================================================
@Project -> File   ：autoui_base -> __init__.py
@IDE    ：PyCharm
@Author ：GAI
@Date   ：2020/7/17 3:01 下午
@Desc   ：
=================================================='''

from atf.drivers.appium.driver_appium import AndroidDriver, iOSDriver
from atf.drivers.chrome.driver_chrome import Chrome_Driver


__all__ = ['AndroidDriver','iOSDriver','Chrome_Driver']
