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
from telnetlib import EC

from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver.common import by
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from atf.commons.logging import *
from atf.commons.variable_global import Var

class Chrome_Driver(object):




    @staticmethod
    def launch_web():
        '''

        :return:
        '''
        print("WebDriverBase--launch_web")
        # Var.webinstance.launch_web()

    @staticmethod
    def wait_for(timeout=10 ,*loc):
        elements = WebDriverWait(Var.webinstance, timeout).until(expected_conditions.visibility_of_any_elements_located(*loc))
        return elements

    @staticmethod
    def wait_for_elements_by_id(id, timeout=10, interval=1):
        '''
        :param id:
        :return:
        '''
        try:
            # elements = Var.webinstance.find_elements_by_id(id)
            elements = WebDriverWait(Var.webinstance, timeout).until(expected_conditions.visibility_of_any_elements_located((By.ID,id)))
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
            elements = WebDriverWait(Var.webinstance, timeout).until(expected_conditions.visibility_of_any_elements_located((By.XPATH, xpath)))
            # elements = Var.webinstance.find_elements_by_xpath(xpath)
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
            elements = WebDriverWait(Var.webinstance, timeout).until(expected_conditions.visibility_of_any_elements_located((By.LINK_TEXT, linktext)))

            # elements = Var.webinstance.find_elements_by_link_text(linktext)
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
            # elements = Var.webinstance.find_elements_by_partial_link_text(partiallinktext)
            elements = WebDriverWait(Var.webinstance, timeout).until(expected_conditions.visibility_of_any_elements_located((By.PARTIAL_LINK_TEXT, partiallinktext)))
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
            # elements = Var.webinstance.find_elements_by_name(name)
            elements = WebDriverWait(Var.webinstance, timeout).until(expected_conditions.visibility_of_any_elements_located((By.NAME, name)))

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
            # elements = Var.webinstance.find_elements_by_tag_name(tag_name)
            elements = WebDriverWait(Var.webinstance, timeout).until(expected_conditions.visibility_of_any_elements_located((By.TAG_NAME, tag_name)))
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
            # elements = Var.webinstance.find_elements_by_class_name(classname)
            elements = WebDriverWait(Var.webinstance, timeout).until(expected_conditions.visibility_of_any_elements_located((By.CLASS_NAME, classname)))

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
            # elements = Var.webinstance.find_elements_by_css_selector(cssselector)
            elements = WebDriverWait(Var.webinstance, timeout).until(expected_conditions.visibility_of_any_elements_located((By.CSS_SELECTOR, cssselector)))

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