#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''=================================================
@Project -> File   ：autoui_base -> driver_chrome
@IDE    ：PyCharm
@Author ：GAI
@Date   ：2020/7/18 4:38 下午
@Desc   ：
=================================================='''
import time
import traceback
import subprocess
from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver.support.wait import WebDriverWait

from atf.common.logging import *
from atf.common.variable_global import Var

class Chrome_Driver(object):

    @staticmethod
    def launch_web():
        '''

        :return:
        '''
        print("WebDriverBase--launch_web")
        # Var.webinstance.launch_web()


    @staticmethod
    def wait_for_elements_by_id(id, timeout=10, interval=1):
        '''
        :param id:
        :return:
        '''
        try:
            elements = Var.webinstance.find_elements_by_id(id)
            return elements
        except Exception as e:
            raise e

    @staticmethod
    def wait_for_elements_by_xpath(xpath, timeout=10, interval=1):
        '''
        :param xpath:
        :return:
        '''
        try:
            elements = Var.webinstance.find_elements_by_xpath(xpath)
            return elements
        except Exception as e:
            raise e

    @staticmethod
    def wait_for_elements_by_link_text(linktext, timeout=10, interval=1):
        '''
        :param xpath:
        :return:
        '''
        try:
            elements = Var.webinstance.find_elements_by_link_text(linktext)
            return elements
        except Exception as e:
            raise e



    @staticmethod
    def wait_for_elements_by_partial_link_text(partiallinktext, timeout=10, interval=1):
        '''
        :param xpath:
        :return:
        '''
        try:
            elements = Var.webinstance.find_elements_by_partial_link_text(partiallinktext)
            return elements
        except Exception as e:
            raise e

    @staticmethod
    def wait_for_elements_by_name(name, timeout=10, interval=1):
        '''
        :param classname:
        :return:
        '''
        try:
            elements = Var.webinstance.find_elements_by_name(name)
            return elements
        except Exception as e:
            raise e

    @staticmethod
    def wait_for_elements_by_tag_name(tag_name, timeout=10, interval=1):
        '''
        :param classname:
        :return:
        '''
        try:
            elements = Var.webinstance.find_elements_by_tag_name(tag_name)
            return elements
        except Exception as e:
            raise e

    @staticmethod
    def wait_for_elements_by_classname(classname, timeout=10, interval=1):
        '''
        :param classname:
        :return:
        '''
        try:
            elements = Var.webinstance.find_elements_by_class_name(classname)
            return elements
        except Exception as e:
            raise e

    @staticmethod
    def wait_for_elements_by_cssselector(cssselector, timeout=10, interval=1):
        '''
        :param classname:
        :return:
        '''
        try:
            elements = Var.webinstance.find_elements_by_css_selector(cssselector)
            return elements
        except Exception as e:
            raise e

    @staticmethod
    def input(element, text, clear=True, hide_keyboard=True):
        '''
        :param element:
        :param text:
        :param clear:
        :param hide_keyboard:
        :return:
        '''
        try:
            element.clear()
            time.sleep(1)
            element.send_keys(text)
        except Exception as e:
            raise e