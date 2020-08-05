#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
import time
from concurrent import futures

from atf.commons.logging import *
from atf.commons.variable_global import Var



class AppDriverBase(object):


    @staticmethod
    def init():
        print("AppDriverBase--init")
        try:
            global appdriver
            print(Var.appdriver)
            if Var.appdriver.lower() == 'appium':
                from atf.drivers.appium.driver_appium import AndroidDriver, iOSDriver

            else:
                # from drivers.macaca import AndroidDriver, iOSDriver
                print("else==")
            print(Var.platformName)

            if Var.platformName.lower() == "ios":
                appdriver = iOSDriver
            elif Var.platformName.lower() == "android":
                appdriver = AndroidDriver
            Var.driver_instance = appdriver
        except Exception as e:
            raise e

    @staticmethod
    def adb_shell(cmd):
        """onlu Android
        Args:
            command
        Usage:
            adbshell 'adb devices'
        Returns:
            None
        """
        print("DriverBase--adbshell")

        appdriver.adb_shell(cmd)

    @staticmethod
    def install_app(app_path):
        '''
        install app
        :param app_path:
        :return:
        '''
        print("DriverBase--installapp")

        appdriver.install_app(app_path)

    @staticmethod
    def uninstall_app(package_info):
        '''
        uninstall app
        :param package_info: Android(package) or iOS(bundleId)
        :return:
        '''
        print("DriverBase--uninstallapp")

        appdriver.uninstall_app(package_info)

    @staticmethod
    def launch_app(package_info):
        '''
        launch app
        :param package_info: Android(package/activity) or iOS(bundleId)
        :return:
        '''
        print("AppDriverBase--lauchapp",package_info)
        appdriver.launch_app(package_info)

    @staticmethod
    def close_app(package_info):
        '''
        close app
        :param package_info: Android(package) or iOS(bundleId)
        :return:
        '''
        print("DriverBase--closeapp")
        appdriver.close_app(package_info)

    @staticmethod
    def screenshot():
        '''
        only appium
        :return:
        '''
        print('进入截图',Var.snapshot_dir)
        tempimage = "temp_pic_{}.png".format(int(time.time()))
        print(tempimage)
        image_name = os.path.join(Var.snapshot_dir, tempimage)
        # image_name = Var.ROOT + '/temp/pic_{}.png'.format(int(time.time()))
        print('截图路径 ==> {}',image_name)
        appdriver.get_screenshot_as_file(image_name)
        return image_name

    @staticmethod
    def background_app():
        '''
        only appium
        :return:
        '''
        appdriver.background_app()

    @staticmethod
    def tap(x, y):
        '''
        :param x:
        :param y:
        :return:
        '''
        appdriver.tap(x, y)

    @staticmethod
    def double_tap(x, y):
        '''
        :param x:
        :param y:
        :return:
        '''
        appdriver.double_tap(x, y)

    @staticmethod
    def press(x, y, duration=2):
        '''
        :param x:
        :param y:
        :param duration:
        :return:
        '''
        appdriver.press(x, y, duration)

    @staticmethod
    def press(element, duration=2):
        '''
        :param element:
        :param duration:
        :return:
        '''
        appdriver.press(element, duration)

    @staticmethod
    def swipe_up(duration=2):
        '''
        :param duration:
        :return:
        '''
        appdriver.swipe_up(duration)

    @staticmethod
    def swipe_down(duration=2):
        '''
        :param duration:
        :return:
        '''
        appdriver.swipe_down(duration)

    @staticmethod
    def swipe_left(duration=2):
        '''
        :param duration:
        :return:
        '''
        appdriver.swipe_left(duration)

    @staticmethod
    def swipe_right(duration=2):
        '''
        :param duration:
        :return:
        '''
        appdriver.swipe_right(duration)

    @staticmethod
    def swipe(from_x, from_y, to_x, to_y, duration=2):
        '''
        :param from_x:
        :param from_y:
        :param to_x:
        :param to_y:
        :param duration:
        :return:
        '''
        appdriver.swipe(from_x, from_y, to_x, to_y, duration)

    @staticmethod
    def move_to(x, y):
        '''
        :param x:
        :param y:
        :return:
        '''
        appdriver.move_to(x, y)


    @staticmethod
    def click(key, timeout=10, interval=1, index=0):
        '''
        :param element:
        :param timeout:
        :param interval:
        :param index:
        :return:
        '''
        print("click:",key)
        element = AppDriverBase.find_elements_by_key(key=key, timeout=timeout, interval=interval, index=index)
        print("click----element",element)
        if not element:
            raise Exception("Can't find element {}".format(key))
        element.click()

    @staticmethod
    def check(key, timeout=10, interval=1, index=0):
        '''
        :param key:
        :param timeout:
        :param interval:
        :param index:
        :return:
        '''
        element = AppDriverBase.find_elements_by_key(key=key, timeout=timeout, interval=interval, index=index)
        if not element:
            return False
        return True


    @staticmethod
    def input(key, text='', timeout=10, interval=1, index=0, clear=True):
        '''
        :param text:
        :param timeout:
        :param interval:
        :param index:
        :param clear:
        :return:
        '''
        element = AppDriverBase.find_elements_by_key(key=key, timeout=timeout, interval=interval, index=index)
        if not element:
            raise Exception("Can't find element {}".format(key))
        appdriver.input(element, text)

    @staticmethod
    def get_text(key, timeout=10, interval=1, index=0):
        '''
        :param key:
        :param timeout:
        :param interval:
        :param index:
        :return:
        '''
        element = AppDriverBase.find_elements_by_key(key=key, timeout=timeout, interval=interval, index=index)
        if not element:
            raise Exception("Can't find element {}".format(key))
        text = appdriver.get_text(element)
        return text

    @staticmethod
    def get_texts(key, timeout=10, interval=1):
        '''
        :param key:
        :param timeout:
        :param interval:
        :param index:
        :return:
        '''
        elements = AppDriverBase.find_elements_by_key(key=key, timeout=timeout, interval=interval)
        if not elements:
            raise Exception("Can't find element {}".format(key))
        print("elements--热土人结果：",elements)
        textlist = appdriver.get_texts(elements)
        return textlist

    @staticmethod
    def get_page_source():
        '''
        :param key:
        :param timeout:
        :param interval:
        :param index:
        :return:
        '''
        pagesource = appdriver.get_page_source()
        return pagesource


    @staticmethod
    def find_elements_by_key(key, timeout=10, interval=1, index=0):
        print("find_elements_by_key-----",key)
        '''
        :param key:
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
            'element': key,
            'timeout': timeout,
            'interval': interval,
            'index': index
        }
        print("dict^^^^^^^",dict)
        if Var.platformName.lower() == 'android':
            if re.match(r'[a-zA-Z]+\.[a-zA-Z]+[\.\w]+:id/\S+', key):
                dict['element_type'] = 'id'
            elif re.match(r'android\.[a-zA-Z]+[\.(a-zA-Z)]+', key) or re.match(r'[a-zA-Z]+\.[a-zA-Z]+[\.(a-zA-Z)]+', key):
                dict['element_type'] = 'classname'
            elif re.match('//\*\[@\S+=\S+\]', key) or re.match('//[a-zA-Z]+\.[a-zA-Z]+[\.(a-zA-Z)]+\[\d+\]', key):
                dict['element_type'] = 'xpath'
            else:
                dict['element_type'] = 'name'
            print("dict^^^^^^^element_type", dict['element_type'])

        else:
            if re.match(r'XCUIElementType', key):
                dict['element_type'] = 'classname'
            elif re.match(r'//XCUIElementType', key):
                dict['element_type'] = 'xpath'
            elif re.match(r'//\*\[@\S+=\S+\]', key):
                dict['element_type'] = 'xpath'
            else:
                dict['element_type'] = 'name'
            print("dict^^^5555^^^^element_type", dict['element_type'])


        return AppDriverBase.wait_for_elements_by_key(dict)

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
        if element_type == 'name':
            elements = appdriver.wait_for_elements_by_name(name=element, timeout=timeout, interval=interval)
        elif element_type == 'id':
            elements = appdriver.wait_for_elements_by_id(id=element, timeout=timeout, interval=interval)
        elif element_type == 'xpath':

            elements = appdriver.wait_for_elements_by_xpath(xpath=element, timeout=timeout, interval=interval)
        elif element_type == 'classname':
            elements = appdriver.wait_for_elements_by_classname(classname=element, timeout=timeout, interval=interval)
        else:
            elements = None

        log_info('return elements: {}'.format(elements))
        if elements:
            if len(elements) <= int(index):
                log_error('elements exists, but cannot find index({}) position'.format(index), False)
                raise Exception('list index out of range, index:{}'.format(index))
            return elements[index]
        else:
            print("meiyou elements")
            return None
