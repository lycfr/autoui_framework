#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time

from atf import driver
from atf.driver import appdriver


def appProfile():
    '''
    Safari 打开url
    :param url:
    :return:
    '''
    #短信验证码登录
    other_login = appdriver.element_by_name('其他方式登录')
    if other_login:
        other_login.click()
    #appdriver.element_by_name('com.dedao.juvenile:id/etMobile').clear().send_keys(account)
#
# if self.find(self._display_time, *self._other_login_btn):
#     self.find(self._display_time, *self._other_login_btn).click()
#     logger_info("点击其他方式登录")
#
# self.find(self._display_time, *self._sms_phone_login).clear().send_keys(account)
# logger_info("输入账号:【{}】".format(account))
# self.find(self._display_time, *self._send_sms_btn).click()
# logger_info("点击【发送验证码】")
# self.find(self._display_time, *self._sms_phone_text).clear().send_keys(smscode)
# logger_info("输入短信验证码: 【{}】".format(smscode))
# return self