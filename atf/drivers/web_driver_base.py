#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''=================================================
@Project -> File   ：autoui_base -> web_driver_base
@IDE    ：PyCharm
@Author ：GAI
@Date   ：2020/7/18 4:38 下午
@Desc   ：
=================================================='''
import re

from atf.common.logging import log_info, log_error
from atf.common.variable_global import Var


class WebDriverBase(object):

    @staticmethod
    def init():
        print("WebDriverBase--init")
        try:
            global web_driver
            print('Var.web_driver',Var.web_driver)
            if Var.web_driver.lower() == 'chrome':
                from atf.drivers.chrome import Chrome_Driver
                web_driver = Chrome_Driver

            else:
                # from drivers.macaca import AndroidDriver, iOSDriver
                print("else==")
        except Exception as e:
            raise e



    @staticmethod
    def launch_web(package_info):
        '''
        launch app
        :param package_info: Android(package/activity) or iOS(bundleId)
        :return:
        '''
        print("web_driverBase--launch_web",package_info)
        web_driver.launch_web(package_info)

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
        element.click()

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



    @staticmethod
    def  find_elements_by_key(key1, key2, timeout=10, interval=1, index=0):
        print("find_elements_by_key--web---",key1,key2)
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
        print("dict^^^^^^^",dict)
        dict['element_type'] = dict['by']

        print("dict^^^5555^^^^element_type", dict['element_type'])

        return WebDriverBase.wait_for_elements_by_key(dict)


    @staticmethod
    def wait_for_elements_by_key(elements_info):
        '''
        :param elements_info:
        :return:
        '''
        print("wait_for_elements_by_key")
        print("elements_info:::",elements_info)
        element_type = elements_info['element_type']
        element = elements_info['element']
        timeout = elements_info['timeout']
        interval = elements_info['interval']
        index = elements_info['index']
        # 2020-07-20 19:18:32,488 INFO :find elements: Body: {'using': 'id', 'value': 'com.dedao.juvenile:id/notificationBtn', 'index': 0}
        log_info("find elements: Body: {'using': '%s', 'value': '%s', 'index': %s}" % (element_type, element, index))

        '''
        ID = "id"
        XPATH = "xpath"
        LINK_TEXT = "link text"
        PARTIAL_LINK_TEXT = "partial link text"
        NAME = "name"
        TAG_NAME = "tag_name"
        CLASS_NAME = "class name"
        CSS_SELECTOR = "css selector"
        '''

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


