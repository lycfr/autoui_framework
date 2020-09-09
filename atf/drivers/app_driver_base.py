#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
import time
from concurrent import futures

from atf.commons.logging import *
from atf.commons.variable_global import Var
from atf.utils.commom_utils import *


class AppDriverBase(object):


    @staticmethod
    def init():
        try:
            global appdriver
            if Var.appdriver.lower() == 'appium':
                from atf.drivers.appium.driver_appium import AndroidDriver, iOSDriver

            else:
                # from drivers.macaca import AndroidDriver, iOSDriver
                print("else==")
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

        appdriver.adb_shell(cmd)

    @staticmethod
    def install_app(app_path):
        '''
        install app
        :param app_path:
        :return:
        '''
        appdriver.install_app(app_path)

    @staticmethod
    def uninstall_app(package_info):
        '''
        uninstall app
        :param package_info: Android(package) or iOS(bundleId)
        :return:
        '''
        appdriver.uninstall_app(package_info)

    @staticmethod
    def launch_app(package_info):
        '''
        launch app
        :param package_info: Android(package/activity) or iOS(bundleId)
        :return:
        '''
        print("lauch_app")
        appdriver.launch_app(package_info)
        time.sleep(3)

    @staticmethod
    def close_app(package_info):
        '''
        close app
        :param package_info: Android(package) or iOS(bundleId)
        :return:
        '''
        appdriver.close_app(package_info)

    @staticmethod
    def screenshot():
        '''
        only appium
        :return:
        '''
        tempimage = "temp_pic_{}.png".format(int(time.time()))
        image_name = os.path.join(Var.snapshot_dir, tempimage)
        # image_name = Var.ROOT + '/temp/pic_{}.png'.format(int(time.time()))
        appdriver.get_screenshot_as_file(image_name)
        return image_name

    @staticmethod
    def seekBar():
        '''
        only appium
        :return:
        '''
        log_info("滑动进度条")
        appdriver.seekBar()

    @staticmethod
    def tapSeekBar(x):
        '''
        only appium
        :return:
        '''
        log_info("点击到进度条某一位置")
        appdriver.tapSeekBar(x)

    @staticmethod
    def swipeSeekBar(x):
        '''
        only appium
        :return:
        '''
        appdriver.swipeSeekBar(x)
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
    def pressElement(element, duration=2):
        '''
        :param element:
        :param duration:
        :return:
        '''
        appdriver.pressElement(element, duration)

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
    def swipe1(from_x, from_y, to_x, to_y, duration=2):
        '''
        :param from_x:
        :param from_y:
        :param to_x:
        :param to_y:
        :param duration:
        :return:
        '''
        appdriver.swipe1(from_x, from_y, to_x, to_y, duration)

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
        element = AppDriverBase.find_elements_by_key(key=key, timeout=timeout, interval=interval, index=index)
        if not element:
            raise Exception("Can't find element {}".format(key))
        log_info("click:{},{}".format(key,index))
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
        elements = AppDriverBase.get_eles(key=key, timeout=timeout, interval=interval)
        if not elements:
            raise Exception("Can't find element {}".format(key))
        textlist = appdriver.get_texts(elements)
        return textlist

    @staticmethod
    def get_eles(key, timeout=10, interval=1):
        '''
        :param key:
        :param timeout:
        :param interval:
        :param index:
        :return:
        '''
        elements = AppDriverBase.find_elements_by_key(key=key, timeout=timeout, interval=interval, index=None)
        if not elements:
            raise Exception("Can't find element {}".format(key))
        return elements

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
    def find_elements_by_key(key, timeout=10, interval=1, index=None):
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
        if Var.platformName.lower() == 'android':
            if re.match(r'[a-zA-Z]+\.[a-zA-Z]+[\.\w]+:id/\S+', key):
                dict['element_type'] = 'id'
            elif re.match(r'android\.[a-zA-Z]+[\.(a-zA-Z)]+', key) or re.match(r'[a-zA-Z]+\.[a-zA-Z]+[\.(a-zA-Z)]+', key):
                dict['element_type'] = 'classname'
            elif re.match('//\*\[@\S+=\S+\]', key) or re.match('//[a-zA-Z]+\.[a-zA-Z]+[\.(a-zA-Z)]+\[\d+\]', key) or re.match('//*[contains(@\S,)]', key):
                dict['element_type'] = 'xpath'
            else:
                dict['element_type'] = 'name'
        else:
            if re.match(r'XCUIElementType', key):
                dict['element_type'] = 'classname'
            elif re.match(r'//XCUIElementType', key):
                dict['element_type'] = 'xpath'
            elif re.match(r'//\*\[@\S+=\S+\]', key):
                dict['element_type'] = 'xpath'
            else:
                dict['element_type'] = 'name'
        return AppDriverBase.wait_for_elements_by_key(dict)

    @staticmethod
    def wait_for_elements_by_key(elements_info):
        '''
        :param elements_info:
        :return:
        '''
        print("elements_info",elements_info)
        _error_max = 10
        _error_count = 0
        element_type = elements_info['element_type']
        element = elements_info['element']
        timeout = elements_info['timeout']
        interval = elements_info['interval']
        index = elements_info['index']

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

        # log_info('查找到对应元素列表为: {}'.format(elements))

        try:
            # if len(elements) <= int(index):
            #     log_error('elements exists, but cannot find index({}) position'.format(index), False)
            #     raise Exception('list index out of range, index:{}'.format(index))
            # 如果成功，清空错误计数
            _error_count = 0
            if elements_info['index'] != None:
                # 进行截图Var.file
                if Var.ocrimg is not None:
                    cv2.imwrite(Var.file, Var.ocrimg)
                    Var.ocrimg = None
                else:
                    # Var.instance.save_screenshot(Var.file)app_screenshot_eles_steps
                    print("截图时：elements[index]",elements[index])
                    app_screenshot_steps(elements[index], Var.tmp_file, Var.file, zoom=1.0)
                return elements[index]
            else:
                # 截图
                if Var.ocrimg is not None:
                    cv2.imwrite(Var.file, Var.ocrimg)
                    Var.ocrimg = None
                else:
                    app_screenshot_eles_steps(elements, Var.tmp_file, Var.file, zoom=1.0)
                return elements
        except Exception as e:
            # 如果次数太多，就退出异常逻辑，直接报错
            if _error_count > _error_max:
                raise e
            # 记录一直异常的次数
            _error_count += 1
            # 对黑名单里的弹框进行处理
            if Var.black_list:
                for i in Var.black_list:
                    # w = re.split('[(,)]', i)
                    inBrackets = i[12:-1]
                    douIndex = inBrackets.find(",")
                    byBlack = inBrackets[:douIndex]
                    eleBlack = inBrackets[(douIndex + 1):]
                    elements = appdriver.black_for_elements(byBlack,eleBlack)
                    if len(elements) > 0:
                        elements[0].click()
                        time.sleep(1)
                        # 继续寻找原来的正常控件
                        return AppDriverBase.wait_for_elements_by_key(elements_info)
            app_screenshot_eles_steps(None, Var.tmp_file, Var.file, zoom=1.0)
            # 如果黑名单也没有，就报错
            log_info("black list no one found")
            return None