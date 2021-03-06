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
                pass
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
        log_info("启动app")
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
    def SeekBar000(ele1,ele2):
        '''
        only appium
        :return:
        '''
        element1 = AppDriverBase.find_elements_by_key(key=ele1,timeout=10, interval=1, index=0,flag=False)
        if not element1:
            raise Exception("Can't find element {}".format(ele1))

        element2 = AppDriverBase.find_elements_by_key(key=ele2, timeout=10, interval=1, index=0,flag=False)
        if not element2:
            raise Exception("Can't find element {}".format(ele2))
        fromX = element1.location.get('x')
        fromY = element1.location.get('y')
        toX = element2.location.get('x')
        toY = element2.location.get('y')
        log_info("SeekBar000:{},{}".format(ele1, ele2))

        appdriver.SeekBar000(fromX,fromY,toX,toY)


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
    def click(key, timeout=10, interval=1, index=0,flag=False):
        '''
        :param element:
        :param timeout:
        :param interval:
        :param index:
        :return:
        '''
        element = AppDriverBase.find_elements_by_key(key=key, timeout=timeout, interval=interval, index=index,flag=flag)
        if not element:
            raise Exception("Can't find element {}".format(key))
        log_info("click:{},{}".format(key, index))
        element.click()


    @staticmethod
    def click1(key, timeout=10, interval=1, index=0, flag=False):
        '''
        :param element:
        :param timeout:
        :param interval:
        :param index:
        :return:
        '''
        element = AppDriverBase.find_element_by_key1_click(key=key, timeout=timeout, interval=interval, index=0,
                                                      flag=flag)
        element.click()
        log_info("click:{},{}".format(key, index))
        # 进行截图Var.file
        if Var.ocrimg is None:
            app_screenshot_steps(element, Var.tmp_file, Var.file, zoom=1.0, flag=False)
        else:
            cv2.imwrite(Var.file, Var.ocrimg)
            Var.ocrimg = None

    @staticmethod
    def executeScript(direction, ele):
        '''
        :param element:
        :param timeout:
        :param interval:
        :param index:
        :return:
        '''
        if not ele:
            raise Exception("Can't find element {}".format(ele))
        appdriver.executeScript(direction, ele)

    @staticmethod
    def executeTap(x,y):
        '''
        :param element:
        :param timeout:
        :param interval:
        :param index:
        :return:
        '''
        appdriver.executeTap(x,y)

    @staticmethod
    def XYclick(x, y):
        '''
        :param element:
        :param timeout:
        :param interval:
        :param index:
        :return:
        '''
        app_screenshot_eles_steps(None, Var.tmp_file, Var.file, zoom=1.0)
        appdriver.XYclick(x, y)


    @staticmethod
    def check(key, timeout=10, interval=1, index=0):
        '''
        :param key:
        :param timeout:
        :param interval:
        :param index:
        :return:
        '''
        element = AppDriverBase.find_elements_by_key(key=key, timeout=timeout, interval=interval, index=index,flag=False)
        # if Var.ocrimg == None:
        #     app_screenshot_steps(element, Var.tmp_file, Var.file, zoom=1.0, flag=False)
        # else:
        #     cv2.imwrite(Var.file, Var.ocrimg)
        #     Var.ocrimg = None
        if not element:
            return False
        return True

    @staticmethod
    def getOneAttribute(key, timeout=10, interval=1, index=0, name='class'):
        '''
        key=list_params[0], timeout=Var.timeout, interval=Var.interval,
                                            index=int(list_params[1]),name=list_params[2]
        :param key:
        :param timeout:
        :param interval:
        :param index:
        :return:
        '''
        element = AppDriverBase.find_elements_by_key(key=key, timeout=timeout, interval=interval, index=index,flag=False)
        getOneAttribute = appdriver.getOneAttribute(element,name)
        # 进行截图Var.file
        # if Var.ocrimg is None:
        #     app_screenshot_steps(element, Var.tmp_file, Var.file, zoom=1.0, flag=False)
        # else:
        #     cv2.imwrite(Var.file, Var.ocrimg)
        #     Var.ocrimg = None
        return getOneAttribute

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
        element = AppDriverBase.find_elements_by_key(key=key, timeout=timeout, interval=interval, index=index,flag=False)
        if not element:
            raise Exception("Can't find element {}".format(key))
        appdriver.input(element, text)

    @staticmethod
    def numInput(text):
        '''
        :param text:
        :param timeout:
        :param interval:
        :param index:
        :param clear:
        :return:
        '''
        appdriver.numInput(text)

    @staticmethod
    def get_text(key, timeout=10, interval=1, index=0):
        '''
        :param key:
        :param timeout:
        :param interval:
        :param index:
        :return:
        '''
        element = AppDriverBase.find_elements_by_key(key=key, timeout=timeout, interval=interval, index=index,flag=False)
        if not element:
            raise Exception("Can't find element {}".format(key))
        text = appdriver.get_text(element)
        # 进行截图Var.file
        # if Var.ocrimg is None:
        #     app_screenshot_steps(element, Var.tmp_file, Var.file, zoom=1.0, flag=False)
        # else:
        #     cv2.imwrite(Var.file, Var.ocrimg)
        #     Var.ocrimg = None
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
        # 进行截图Var.file
        # if Var.ocrimg is None:
        #     app_screenshot_steps(elements, Var.tmp_file, Var.file, zoom=1.0, flag=False)
        # else:
        #     cv2.imwrite(Var.file, Var.ocrimg)
        #     Var.ocrimg = None
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
        elements = AppDriverBase.find_elements_by_key(key=key, timeout=timeout, interval=interval, index=None,flag=False)
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
    def find_elements_by_key(key, timeout=10, interval=1, index=None,flag=False):
        '''
        :param key:
        :param timeout:
        :param interval:
        :param index:list对应下标
        :param flag:False；不标记元素截图
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
            'index': index,
            'flag':flag
        }

        if Var.platformName.lower() == 'android':
            # pagesource = appdriver.get_page_source()
            # oneelement_list = ['com.dedao.juvenile:id/iv_close','com.dedao.juvenile:id/upgrade_button']
            # for one in oneelement_list:
            #     if one in pagesource:
            #         ele = appdriver.wait_for_element_by_id(one, timeout=timeout, interval=interval)
            #         ele.click()
            # oneeleXpath_list = ['允许', '始终允许', '稍后', '关闭']
            #
            # for oneXpath in oneeleXpath_list:
            #     if oneXpath in pagesource:
            #         oneXpath_text = "//*[@text='" + oneXpath + "']"
            #         print(oneXpath_text)
            #         ele = appdriver.wait_for_element_by_xpath(oneXpath_text, timeout=timeout, interval=interval)
            #         ele.click()
            print(key)
            if re.match(r'[a-zA-Z]+\.[a-zA-Z]+[\.\w]+:id/\S+', key):
                dict['element_type'] = 'id'
            elif re.match(r'android\.[a-zA-Z]+[\.(a-zA-Z)]+', key) or re.match(r'[a-zA-Z]+\.[a-zA-Z]+[\.(a-zA-Z)]+', key):
                dict['element_type'] = 'classname'
            elif re.match('//\*\[@\S+=\S+\]', key) or re.match('//[a-zA-Z]+\.[a-zA-Z]+[\.(a-zA-Z)]+\[\d+\]', key) or re.match('//*[contains(@\S,)]', key):
                dict['element_type'] = 'xpath'
            else:
                dict['element_type'] = 'name'
            print(dict['element_type'])
        else:
            pagesource = appdriver.get_page_source()
            oneelement_list = ['tc icon certificate close','listen icon sheet close','close AD','以后再说']
            for one in oneelement_list:
                if one in pagesource:
                    eles = appdriver.wait_for_elements_by_name(name=one, timeout=timeout, interval=interval)
                    eles[0].click()
                    time.sleep(2)

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
        print(elements_info)
        _error_max = 10
        _error_count = 0
        element_type = elements_info['element_type']
        element = elements_info['element']
        timeout = elements_info['timeout']
        interval = elements_info['interval']
        index = elements_info['index']
        if elements_info['flag'] == None:
            flag = False
        else:
            flag = elements_info['flag']
        print(element_type)
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
                if Var.ocrimg == None:
                    app_screenshot_steps(elements, Var.tmp_file, Var.file, zoom=1.0, flag=flag)
                else:
                    cv2.imwrite(Var.file, Var.ocrimg)
                    Var.ocrimg = None
                return elements[index]
            else:
                log_info('index==None时进行操作')
                #截图
                if Var.ocrimg is not None:
                    cv2.imwrite(Var.file, Var.ocrimg)
                    Var.ocrimg = None
                else:
                    app_screenshot_eles_steps(elements, Var.tmp_file, Var.file, zoom=1.0,flag=flag)
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
            app_screenshot_eles_steps(None, Var.tmp_file, Var.file, zoom=1.0,flag=flag)
            # 如果黑名单也没有，就报错
            log_info("black list no one found")
            return None

    @staticmethod
    def find_element_by_key1_click(key, timeout=10, interval=1, index=0, flag=False):
        '''
        :param key:
        :param timeout:
        :param interval:
        :param index:list对应下标
        :param flag:False；不标记元素截图
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
            'index': index,
            'flag': flag
        }

        if Var.platformName.lower() == 'android':
            if re.match(r'[a-zA-Z]+\.[a-zA-Z]+[\.\w]+:id/\S+', key):
                dict['element_type'] = 'id'
            elif re.match(r'android\.[a-zA-Z]+[\.(a-zA-Z)]+', key) or re.match(r'[a-zA-Z]+\.[a-zA-Z]+[\.(a-zA-Z)]+',
                                                                               key):
                dict['element_type'] = 'classname'
            elif re.match('//\*\[@\S+=\S+\]', key) or re.match('//[a-zA-Z]+\.[a-zA-Z]+[\.(a-zA-Z)]+\[\d+\]',
                                                               key) or re.match('//*[contains(@\S,)]', key):
                dict['element_type'] = 'xpath'
            else:
                dict['element_type'] = 'name'
        log_info("dict:{}".format(dict))
        return AppDriverBase.wait_for_element_by_key1_click(dict)

    @staticmethod
    def wait_for_element_by_key1_click(elements_info):
        '''
        :param elements_info:
        :return:
        '''
        _error_max = 10
        _error_count = 0
        element_type = elements_info['element_type']
        element = elements_info['element']
        timeout = elements_info['timeout']
        interval = elements_info['interval']
        index = elements_info['index']
        # if elements_info['flag'] == None:
        #     flag = False
        # else:
        #     flag = elements_info['flag']
        flag = False
        if element_type == 'name':
            element = appdriver.wait_for_element_by_name(name=element, timeout=timeout, interval=interval)
        elif element_type == 'id':
            element = appdriver.wait_for_element_by_id(id=element, timeout=timeout, interval=interval)
        elif element_type == 'xpath':
            element = appdriver.wait_for_element_by_xpath(xpath=element, timeout=timeout, interval=interval)
        elif element_type == 'classname':
            element = appdriver.wait_for_element_by_classname(classname=element, timeout=timeout, interval=interval)
        else:
            element = None

        try:
            print("tryyyyyy")
            # 如果成功，清空错误计数
            _error_count = 0
            return element
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
            app_screenshot_eles_steps(None, Var.tmp_file, Var.file, zoom=1.0,flag=flag)
            # 如果黑名单也没有，就报错
            log_info("black list no one found")
            return None