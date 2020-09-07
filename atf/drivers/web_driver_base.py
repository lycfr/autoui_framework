#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''=================================================
@Project -> File   ：autoui_base -> web_driver_base
@IDE    ：PyCharm
@Author ：GAI
@Date   ：2020/7/18 4:38 下午
@Desc   ：
=================================================='''
import os
import re
import time

from atf.commons.logging import *
from atf.commons.variable_global import Var


class WebDriverBase(object):

    @staticmethod
    def init():
        log_info("WebDriverBase--init")
        try:
            global web_driver
            print('Var.web_driver',Var.web_driver)
            if Var.web_driver.lower() == 'chrome':
                from atf.drivers.chrome.driver_chrome import Chrome_Driver

                #删除Chrome进程
                log_info('========> 杀死chrome进程')
                info = os.popen("pgrep -l Chrome")
                _processes = info.readlines()
                for pid in _processes:
                    values = pid.split()[0]
                    os.system("kill -9 " + values)

                web_driver = Chrome_Driver

            else:
                # from drivers.macaca import AndroidDriver, iOSDriver
                log_info("else==")
        except Exception as e:
            raise e

    @staticmethod
    def launch_web(package_info):
        '''
        launch app
        :param package_info: Android(package/activity) or iOS(bundleId)
        :return:
        '''
        web_driver.launch_web(package_info)

    @staticmethod
    def getAttribute(key1, key2,name, timeout=10, interval=1, index=0):
        '''

        :param key1:
        :param key2:
        :param timeout:
        :param interval:
        :param index:
        :return:
        '''
        element = WebDriverBase.find_elements_by_key(key1=key1, key2=key2, timeout=timeout, interval=interval,
                                                     index=index)
        if not element:
            raise Exception("Can't find element {}".format(key1, key2))
        element.get_attribute(name)



    @staticmethod
    def click(key1, key2, timeout=10, interval=1, index=0):
        '''
        :param element:
        :param timeout:
        :param interval:
        :param index:
        :return:
        '''
        element = WebDriverBase.find_elements_by_key(key1=key1, key2=key2, timeout=timeout, interval=interval, index=index)
        if not element:
            raise Exception("Can't find element {}".format(key1,key2))
        log_info("click:{}".format(element))
        element.click()
        time.sleep(2)


    @staticmethod
    def input(key1, key2, text='', timeout=10, interval=1, index=0, clear=True):
        '''
        :param text:
        :param timeout:
        :param interval:
        :param index:
        :param clear:
        :return:
        '''
        element = WebDriverBase.find_elements_by_key(key1=key1, key2=key2, timeout=timeout, interval=interval, index=index)
        if not element:
            raise Exception("webCan't find element {}".format(key1,key2))
        web_driver.input(element, text)
        time.sleep(2)



    @staticmethod
    def  find_elements_by_key(key1, key2, timeout=10, interval=1, index=0):
        '''
        :param key1:
        :param key2:
        :param timeout:
        :param interval:
        :param index:
        :return:
        '''
        if not timeout:
            timeout = 10
        if not interval:
            interval = 1
        dict = {
            'by':key1,
            'element': key2,
            'timeout': timeout,
            'interval': interval,
            'index': index
        }
        dict['element_type'] = dict['by']
        return WebDriverBase.wait_for_elements_by_key(dict)


    @staticmethod
    def wait_for_elements_by_key(elements_info):
        '''
        :param elements_info:
        :return:
        '''
        element_type = elements_info['element_type']
        element = elements_info['element']
        timeout = elements_info['timeout']
        interval = elements_info['interval']
        index = elements_info['index']

        if element_type == 'id':
            elements = web_driver.wait_for_elements_by_id(id=element, timeout=timeout, interval=interval)
        elif element_type == 'xpath':
            elements = web_driver.wait_for_elements_by_xpath(xpath=element, timeout=timeout, interval=interval)
        elif element_type == 'linktext':
            elements = web_driver.wait_for_elements_by_link_text(linktext=element, timeout=timeout, interval=interval)
        elif element_type == 'partiallinktext':
            elements = web_driver.wait_for_elements_by_partial_link_text(partiallinktext=element, timeout=timeout, interval=interval)
        elif element_type == 'name':
            elements = web_driver.wait_for_elements_by_name(name=element, timeout=timeout, interval=interval)
        elif element_type == 'tag_name':
            elements = web_driver.wait_for_elements_by_tag_name(tag_name=element, timeout=timeout, interval=interval)
        elif element_type == 'classname':
            elements = web_driver.wait_for_elements_by_classname(classname=element, timeout=timeout, interval=interval)
        elif element_type == 'cssselector':
            elements = web_driver.wait_for_elements_by_cssselector(cssselector=element, timeout=timeout, interval=interval)
        else:
            elements = None

        log_info('return elements: {}'.format(elements))
        if elements:
            if len(elements) <= int(index):
                log_error('elements exists, but cannot find index({}) position'.format(index), False)
                raise Exception('list index out of range, index:{}'.format(index))
            return elements[index]
        return None


