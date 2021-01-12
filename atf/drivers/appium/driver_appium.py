#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time
import traceback
import subprocess

import cv2
from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver.support.wait import WebDriverWait

from atf.commons.logging import *
from atf.commons.variable_global import Var


class AndroidDriver(object):
    _current_context = "NATIVE_APP"


    @staticmethod
    def adb_shell(cmd):
        '''
        :param cmd:
        :return:
        '''
        try:
            log_info('adb对应命令为: {}'.format(cmd))
            if cmd.startswith('shell'):
                cmd = ["adb", "-s", Var.udid, "shell", "{}".format(cmd.lstrip('shell').strip())]
                pipe = subprocess.Popen(cmd, stdin=subprocess.PIPE,
                                        stdout=subprocess.PIPE)
                out = pipe.communicate()
            else:
                cmd = ["adb", "-s", Var.udid, "{}".format(cmd)]
                os.system(' '.join(cmd))
        except:
            raise Exception(traceback.format_exc())



    @staticmethod
    def install_app(app_path):
        '''
        install app
        :param app_path:
        :return:
        '''
        try:
            Var.appinstance.install_app(app_path)
        except Exception as e:
            raise e

    @staticmethod
    def uninstall_app(package_info):
        '''
        uninstall app
        :param package_info: Android(package) or iOS(bundleId)
        :return:
        '''
        try:
            Var.appinstance.remove_app(package_info)
        except Exception as e:
            raise e

    @staticmethod
    def launch_app(package_info):
        '''
        launch app
        :param package_info: Android(package/activity) or iOS(bundleId)
        :return:
        '''
        try:
            if not package_info:
                Var.appinstance.launch_app()
            else:
                AndroidDriver.adb_shell('shell am start -W {}'.format(package_info))

        except Exception as e:
            raise e

    @staticmethod
    def close_app(package_info):
        '''
        close app
        :param package_info: Android(package) or iOS(bundleId)
        :return:
        '''
        try:
            if not package_info:
                Var.appinstance.close_app()
            else:
                AndroidDriver.adb_shell('shell am force-stop {}'.format(package_info))
        except Exception as e:
            raise e

    @staticmethod
    def black_for_elements(by, ele):
        '''
        :param name:
        :return:
        '''
        if by == 'name':
            elements = Var.appinstance.find_elements_by_accessibility_id(ele)

        elif by == 'id':
            elements = Var.appinstance.find_elements_by_id(ele)
        elif by == 'xpath':
            elements = Var.appinstance.find_elements_by_xpath(ele)
        elif by == 'classname':
            elements = Var.appinstance.find_elements_by_class_name(ele)
        else:
            elements = None
        return elements



    @staticmethod
    def get_screenshot_as_file(image_name):
        '''
        app端进行截图
        :param image_name:
        :return:
        '''
        try:
            Var.appinstance.get_screenshot_as_file(image_name)
        except Exception as e:
            raise e

    @staticmethod
    def seekBar(index = ''):
        try:
            e = Var.appinstance.find_element_by_android_uiautomator('new UiSelector().className("android.widget.SeekBar")')  # 使用uiautomator搭配class属性方法定位控制条
            ex = e.location.get('x')  # 获取元素初始横坐标
            ey = e.location.get('y')  # 获取元素初始纵坐标
            if index == '':
                Var.appinstance.tap([(ex,ey)],500)         #用tap方法点击拖动按钮的最左侧起始位置
            elif 'x' in index:
                # Var.appinstance.tap([(ex+400,ey)],500)      #用tap方法横向点击某按钮，ex+400,ey不变
                Var.appinstance.tap([(index,ey)],500)      #用tap方法横向点击某按钮，ex+400,ey不变
            elif 'y' in index:
                # driver.swipe(ex, ey, ex + 400, ey, 500)  # 用swipe方法横向拖动某按钮， ey纵坐标不变
                Var.appinstance.swipe1(ex, ey, ex + 400, ey, 500)  # 用swipe方法横向拖动某按钮， ey纵坐标不变

        except Exception as e:
            raise e

    @staticmethod
    def tapSeekBar(index=''):
        try:
            e = Var.appinstance.find_element_by_android_uiautomator(
                'new UiSelector().className("android.widget.SeekBar")')  # 使用uiautomator搭配class属性方法定位控制条
            ex = e.location.get('x')  # 获取元素初始横坐标
            ey = e.location.get('y')  # 获取元素初始纵坐标

            # Var.appinstance.tap([(ex+400,ey)],500)      #用tap方法横向点击某按钮，ex+400,ey不变
            Var.appinstance.tap([(ex+int(index), ey)], 500)  # 用tap方法横向点击某按钮，ex+400,ey不变

        except Exception as e:
            raise e

    @staticmethod
    def swipeSeekBar(index=''):
        try:
            e = Var.appinstance.find_element_by_android_uiautomator(
                'new UiSelector().className("android.widget.SeekBar")')  # 使用uiautomator搭配class属性方法定位控制条
            ex = e.location.get('x')  # 获取元素初始横坐标
            ey = e.location.get('y')  # 获取元素初始纵坐标
            # driver.swipe(ex, ey, ex + 400, ey, 500)  # 用swipe方法横向拖动某按钮， ey纵坐标不变
            Var.appinstance.swipe1(ex, ey, ex + int(index), ey, 500)  # 用swipe方法横向拖动某按钮， ey纵坐标不变
        except Exception as e:
            raise e


    @staticmethod
    def background_app():
        '''
        only appium
        :return:
        '''
        try:
            Var.appinstance.background_app()
        except Exception as e:
            raise e

    @staticmethod
    def tap(x, y):
        '''
        :param x:
        :param y:
        :return:
        '''
        try:
            width = Var.appinstance.get_window_size()['width']
            height = Var.appinstance.get_window_size()['height']
            if x <= 1.0:
                x = x * width
            if y <= 1.0:
                y = y * height
            Var.appinstance.tap([(int(x), int(y))])
            time.sleep(1)
            Var.appinstance.save_screenshot(Var.file)
        except Exception as e:
            raise e

    @staticmethod
    def executeScript(direction, ele):
        try:
            Var.appinstance.execute_script("mobile:swipe", {"direction": direction, 'element': ele, "duration": 1})
        except Exception as e:
            raise e

    @staticmethod
    def double_tap(x, y):
        '''
        :param x:
        :param y:
        :return:
        '''
        try:
            width = Var.appinstance.get_window_size()['width']
            height = Var.appinstance.get_window_size()['height']
            if x <= 1.0:
                x = x * width
            if y <= 1.0:
                y = y * height
            TouchAction(Var.appinstance).press(x=int(x), y=int(y), pressure=0.25).release().perform().wait(110). \
                press(x=int(x), y=int(y), pressure=0.25).release().perform()
        except Exception as e:
            raise e

    @staticmethod
    def getUrl(url):
        '''
        :param x:
        :param y:
        :param duration:
        :return:
        '''

        Var.appinstance.get(url)


    @staticmethod
    def press(x, y, duration=2):
        '''
        :param x:
        :param y:
        :param duration:
        :return:
        '''
        try:
            width = Var.appinstance.get_window_size()['width']
            height = Var.appinstance.get_window_size()['height']
            if x <= 1.0:
                x = x * width
            if y <= 1.0:
                y = y * height
            Var.appinstance.long_press(x=int(x), y=int(y), duration=duration)
        except Exception as e:
            raise e

    @staticmethod
    def pressElement(element, duration=2):
        '''
        :param element:
        :param duration:
        :return:
        '''
        try:
            # Var.appinstance.long_press(element=element, duration=duration)
            TouchAction(Var.appinstance).long_press(el=element,duration=duration).perform()
        except Exception as e:
            raise e

    @staticmethod
    def swipe_up(duration=2):
        '''
        :param duration:
        :return:
        '''
        try:
            width = Var.appinstance.get_window_size()['width']
            height = Var.appinstance.get_window_size()['height']
            AndroidDriver.swipe1(width / 2, height * 3 / 4, width / 2, height / 4, duration)
        except Exception as e:
            raise e

    @staticmethod
    def swipe_down(duration=2):
        '''
        :param duration:
        :return:
        '''
        try:
            width = Var.appinstance.get_window_size()['width']
            height = Var.appinstance.get_window_size()['height']
            AndroidDriver.swipe1(width / 2, height / 4, width / 2, height * 3 / 4, duration)

        except Exception as e:
            raise e

    @staticmethod
    def swipe_left(duration=2):
        '''
        :param duration:
        :return:
        '''
        try:
            width = Var.appinstance.get_window_size()['width']
            height = Var.appinstance.get_window_size()['height']
            AndroidDriver.swipe1(width * 3 / 4, height / 2, width / 4, height / 2, duration)
        except Exception as e:
            raise e

    @staticmethod
    def swipe_right(duration=2):
        '''
        :param duration:
        :return:
        '''
        try:
            width = Var.appinstance.get_window_size()['width']
            height = Var.appinstance.get_window_size()['height']
            AndroidDriver.swipe1(width / 4, height / 2, width * 3 / 4, height / 2, duration)
        except Exception as e:
            raise e

    @staticmethod
    def swipe1(from_x, from_y, to_x, to_y, duration=3):
        '''
        :param from_x:
        :param from_y:
        :param to_x:
        :param to_y:
        :param duration:
        :return:
        '''
        try:
            width = Var.appinstance.get_window_size()['width']
            height = Var.appinstance.get_window_size()['height']
            if from_x <= 1.0:
                from_x = from_x * width
            if from_y <= 1.0:
                from_y = from_y * height
            if to_x <= 1.0:
                to_x = to_x * width
            if to_y <= 1.0:
                to_y = to_y * height
            AndroidDriver.adb_shell(
                'shell input swipe {} {} {} {} {}'.format(from_x, from_y, to_x, to_y, duration * 100))

            time.sleep(1)
            Var.appinstance.save_screenshot(Var.file)
        except Exception as e:
            raise e

    @staticmethod
    def input(element, text, hide_keyboard=True):
        '''
        :param element:
        :param text:
        :param clear:
        :param hide_keyboard:
        :return:
        '''
        try:
            log_info("输入对应的文本")
            element.send_keys(text)
            # for i in str(text):
            #     time.sleep(1)
            #     cmd = 'adb -s {} shell input text {}'.format(Var.udid, i)
            #     print("input cmd {}".format(cmd))
            #     subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=1,
            #                      close_fds=True)
        except Exception as e:
            raise e

    @staticmethod
    def numInput(num):
        '''
        :param element:
        :param text:
        :param clear:
        :param hide_keyboard:
        :return:
        '''
        try:
            log_info("输入对应的num")
            for i in str(num):
                time.sleep(1)
                cmd = 'adb -s {} shell input text {}'.format(Var.udid, i)
                log_info("input cmd {}".format(cmd))
                subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=1,
                                 close_fds=True)
                time.sleep(1)
        except Exception as e:
            raise e

    @staticmethod
    def get_text(element):
        '''
        :param element:
        :return:
        '''
        try:
            text = element.text
            return text
        except Exception as e:
            raise e

    @staticmethod
    def getOneAttribute(element,name):
        '''
        :param element:
        :return:
        '''
        try:
            getOneAttribute = element.get_attribute(name)
            return getOneAttribute
        except Exception as e:
            raise e

    @staticmethod
    def get_texts(elements):
        '''
        android
        :param element:
        :return:
        '''
        texts = list()
        try:
            for ele in elements:
                text = ele.text
                texts.append(text)
            return texts
        except Exception as e:
            raise e

    @staticmethod
    def get_page_source():
        try:
            page_source = Var.appinstance.page_source
            return page_source
        except Exception as e:
            raise e


    @staticmethod
    def wait_for_elements_by_id(id, timeout=10, interval=1):
        '''
        :param id:
        :return:
        '''
        try:
            elements = Var.appinstance.find_elements_by_id(id)
            return elements
        except Exception as e:
            raise e

    @staticmethod
    def wait_for_elements_by_name(name, timeout=10, interval=1):
        '''
        :param name:
        :return:
        '''
        try:
            Var.appinstance.implicitly_wait(int(timeout)/2)
            elements = Var.appinstance.find_elements_by_accessibility_id(name)
            if not elements:
                elements = Var.appinstance.find_elements_by_android_uiautomator('new UiSelector().text("{}")'.format(name))
            Var.appinstance.implicitly_wait(timeout)
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
            elements = Var.appinstance.find_elements_by_xpath(xpath)
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
            elements = Var.appinstance.find_elements_by_class_name(classname)
            return elements
        except Exception as e:
            raise e

    @staticmethod
    def wait_for_element_by_id(id, timeout=10, interval=1):
        '''
        :param id:
        :return:
        '''
        try:
            t1 = time.time()
            element = Var.appinstance.find_element_by_id(id)
            t2 = time.time()
            print(t2 - t1)
            return element
        except Exception as e:
            tempimage = "temp_by_xpath_{}.png".format(int(time.time()))
            image_name = os.path.join(Var.snapshot_dir, tempimage)
            Var.appinstance.get_screenshot_as_file(image_name)
            raise e

    @staticmethod
    def wait_for_element_by_name(name, timeout=10, interval=1):
        '''
        :param name:
        :return:
        '''
        try:
            Var.appinstance.implicitly_wait(int(timeout) / 2)
            element = Var.appinstance.find_element_by_accessibility_id(name)
            if not element:
                element = Var.appinstance.find_element_by_android_uiautomator(
                    'new UiSelector().text("{}")'.format(name))
            Var.appinstance.implicitly_wait(timeout)
            return element

        except Exception as e:
            tempimage = "temp_by_xpath_{}.png".format(int(time.time()))
            image_name = os.path.join(Var.snapshot_dir, tempimage)
            Var.appinstance.get_screenshot_as_file(image_name)
            raise e

    @staticmethod
    def wait_for_element_by_xpath(xpath, timeout=10, interval=1):
        '''
        :param xpath:
        :return:
        '''
        try:
            t1 = time.time()
            element = Var.appinstance.find_element_by_xpath(xpath)
            t2 = time.time()
            print(t2 - t1)
            return element
        except Exception as e:
            tempimage = "temp_by_xpath_{}.png".format(int(time.time()))
            image_name = os.path.join(Var.snapshot_dir, tempimage)
            Var.appinstance.get_screenshot_as_file(image_name)
            raise e

    @staticmethod
    def wait_for_element_by_classname(classname, timeout=10, interval=1):
        '''
        :param classname:
        :return:
        '''
        try:
            element = Var.appinstance.find_element_by_class_name(classname)
            return element
        except Exception as e:
            tempimage = "temp_by_xpath_{}.png".format(int(time.time()))
            image_name = os.path.join(Var.snapshot_dir, tempimage)
            Var.appinstance.get_screenshot_as_file(image_name)
            raise e


    @staticmethod
    def save_context(self):
        _current_context = Var.appinstance.context
        if "WEBVIEW" in _current_context:
            _current_window = Var.appinstance.current_window_handle

    @staticmethod
    def restore_context(self):
        if self._current_context != Var.appinstance.context:
            Var.appinstance.switch_to.context(self._current_context)

        if "WEBVIEW" in self._current_context:
            Var.appinstance.switch_to.window(self._current_window)
            logging.info(Var.appinstance.page_source)



class iOSDriver(object):

    @staticmethod
    def install_app(app_path):
        '''
        install app
        :param app_path:
        :return:
        '''
        try:
            Var.appinstance.install_app(app_path)
        except Exception as e:
            raise e

    @staticmethod
    def uninstall_app(package_info):
        '''
        uninstall app
        :param package_info: Android(package) or iOS(bundleId)
        :return:
        '''
        try:
            Var.appinstance.remove_app(package_info)
        except Exception as e:
            raise e

    @staticmethod
    def launch_app(package_info):
        '''
        launch app
        :param package_info: Android(package/activity) or iOS(bundleId)
        :return:
        '''
        try:
            if not package_info:
                Var.appinstance.launch_app()
            else:
                pass  # todo 待补充
        except Exception as e:
            raise e

    @staticmethod
    def close_app(package_info):
        '''
        close app
        :param package_info: Android(package) or iOS(bundleId)
        :return:
        '''
        try:
            if not package_info:
                Var.appinstance.close_app()
            else:
                pass # todo 待补充
        except Exception as e:
            raise e

    @staticmethod
    def get_screenshot_as_file(image_name):
        '''
        app端进行截图
        :param image_name:
        :return:
        '''
        try:
            Var.appinstance.get_screenshot_as_file(image_name)
        except Exception as e:
            raise e


    @staticmethod
    def background_app():
        '''
        only appium
        :return:
        '''
        try:
            Var.appinstance.background_app()
        except Exception as e:
            raise e

    @staticmethod
    def tap(x, y):
        '''
        :param x:
        :param y:
        :return:
        '''
        try:
            width = Var.appinstance.get_window_size()['width']
            height = Var.appinstance.get_window_size()['height']
            if x <= 1.0:
                x = x * width
            if y <= 1.0:
                y = y * height
            Var.appinstance.tap([(int(x), int(y))])
        except Exception as e:
            raise e

    @staticmethod
    def double_tap(x, y):
        '''
        :param x:
        :param y:
        :return:
        '''
        try:
            width = Var.appinstance.get_window_size()['width']
            height = Var.appinstance.get_window_size()['height']
            if x <= 1.0:
                x = x * width
            if y <= 1.0:
                y = y * height
            TouchAction(Var.appinstance).press(x=int(x), y=int(y), pressure=0.25).release().perform().wait(110). \
                press(x=int(x), y=int(y), pressure=0.25).release().perform()
        except Exception as e:
            raise e

    @staticmethod
    def press(el=None, x=None, y=None, duration=2):
        '''
        :param x:
        :param y:
        :param duration:
        :return:
        '''
        try:
            width = Var.appinstance.get_window_size()['width']
            height = Var.appinstance.get_window_size()['height']
            if x <= 1.0:
                x = x * width
            if y <= 1.0:
                y = y * height
            # Var.appinstance.long_press(x=int(x), y=int(y), duration=duration)

            TouchAction(Var.appinstance).long_press(el=el,x=int(x), y=int(y),duration=duration).perform()

        except Exception as e:
            raise e

    @staticmethod
    def pressElement(element, duration=2):
        '''
        :param element:
        :param duration:
        :return:
        '''
        try:
            # Var.appinstance.long_press(element=element, duration=duration)
            TouchAction(Var.appinstance).long_press(el=element,duration=duration).perform()
        except Exception as e:
            raise e

    @staticmethod
    def swipe_up(duration=200):
        '''
        :param duration:
        :return:
        '''
        try:
            width = Var.appinstance.get_window_size()['width']
            height = Var.appinstance.get_window_size()['height']
            iOSDriver.swipe1(width / 2, height * 3 / 4, width / 2, height / 4, duration)
        except Exception as e:
            raise e

    @staticmethod
    def swipe_down(duration=2):
        '''
        :param duration:
        :return:
        '''
        try:
            width = Var.appinstance.get_window_size()['width']
            height = Var.appinstance.get_window_size()['height']
            iOSDriver.swipe1(width / 2, height / 4, width / 2, height * 3 / 4, duration)
            # TouchAction(Var.appinstance).press(width / 2, height / 4).move_to(width / 2, height * 3 / 4).release().perform()
        except Exception as e:
            raise e

    @staticmethod
    def swipe_left(duration=2):
        '''
        :param duration:
        :return:
        '''
        try:
            width = Var.appinstance.get_window_size()['width']
            height = Var.appinstance.get_window_size()['height']
            iOSDriver.swipe1(width * 3 / 4, height / 2, width / 4, height / 2, duration)
        except Exception as e:
            raise e

    @staticmethod
    def swipe_right(duration=2):
        '''
        :param duration:
        :return:
        '''
        try:
            width = Var.appinstance.get_window_size()['width']
            height = Var.appinstance.get_window_size()['height']
            iOSDriver.swipe1(width / 4, height / 2, width * 3 / 4, height / 2, duration)
        except Exception as e:
            raise e

    @staticmethod
    def swipe1(from_x, from_y, to_x, to_y, duration=3):
        '''
        :param from_x:
        :param from_y:
        :param to_x:
        :param to_y:
        :param duration:
        :return:
        '''
        try:
            width = Var.appinstance.get_window_size()['width']
            height = Var.appinstance.get_window_size()['height']
            if from_x <= 1.0:
                from_x = from_x * width
            if from_y <= 1.0:
                from_y = from_y * height
            if to_x <= 1.0:
                to_x = to_x * width
            if to_y <= 1.0:
                to_y = to_y * height
            print(Var.appinstance)
            Var.appinstance.swipe(int(from_x), int(from_y), int(to_x), int(to_y), 200)
            if Var.ocrimg is not None:
                cv2.imwrite(Var.file, Var.ocrimg)
                Var.ocrimg = None
            else:
                return Var.appinstance.save_screenshot(Var.file)

        except Exception as e:
            raise e

    @staticmethod
    def input(element, text, hide_keyboard=True):
        '''
        :param element:
        :param text:
        :param clear:
        :param hide_keyboard:
        :return:
        '''
        try:
            # if hide_keyboard:
            #     iOSDriver.hide_keyboard1()
            # element.clear()
            element.send_keys(text)

        except Exception as e:
            raise e

    @staticmethod
    def get_text(element):
        '''
        :param element:
        :return:
        '''
        try:
            text = element.text
            return text
        except Exception as e:
            raise e

    @staticmethod
    def getOneAttribute(element,name):
        '''
        :param element:
        :return:
        '''
        try:
            getOneAttribute = element.get_attribute(name)
            return getOneAttribute
        except Exception as e:
            raise e

    @staticmethod
    def get_texts(elements):
        '''
        android
        :param element:
        :return:
        '''
        texts = list()
        try:
            for ele in elements:
                text = ele.text
                texts.append(text)
            return texts
        except Exception as e:
            raise e

    @staticmethod
    def wait_for_elements_by_id(id, timeout=10, interval=1):
        '''
        :param id:
        :return:
        '''
        try:
            elements = Var.appinstance.find_elements_by_id(id)
            return elements

        except Exception as e:
            
            raise e

    @staticmethod
    def wait_for_elements_by_name(name, timeout=10, interval=1):
        '''
        :param name:
        :return:
        '''
        try:
            elements = Var.appinstance.find_elements_by_accessibility_id(name)
            return elements
        except Exception as e:
            raise e

    @staticmethod
    def black_for_elements(by,ele):
        '''
        :param name:ios
        :return:
        '''
        if by == 'name':
            elements = Var.appinstance.find_elements_by_accessibility_id(ele)
        elif by == 'id':
            elements = Var.appinstance.find_elements_by_id(ele)
        elif by == 'xpath':
            elements = Var.appinstance.find_elements_by_xpath(ele)
        elif by == 'classname':
            elements = Var.appinstance.find_elements_by_class_name(ele)
        else:
            elements = None
        return elements

    @staticmethod
    def wait_for_elements_by_xpath(xpath, timeout=10, interval=1):
        '''
        :param xpath:
        :return:
        '''
        try:
            elements = Var.appinstance.find_elements_by_xpath(xpath)
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
            elements = Var.appinstance.find_elements_by_class_name(classname)
            return elements
        except Exception as e:
            raise e

    @staticmethod
    def wait_for_element_by_id(id, timeout=10, interval=1):
        '''
        :param id:
        :return:
        '''
        try:
            element = Var.appinstance.find_element_by_id(id)
            return element

        except Exception as e:

            raise e

    @staticmethod
    def wait_for_element_by_name(name, timeout=10, interval=1):
        '''
        :param name:
        :return:
        '''
        try:
            element = Var.appinstance.find_element_by_accessibility_id(name)
            return element
        except Exception as e:
            raise e

    @staticmethod
    def wait_for_element_by_xpath(xpath, timeout=10, interval=1):
        '''
        :param xpath:
        :return:
        '''
        log_info("wait_for_element_by_xpath")
        element = Var.appinstance.find_element_by_xpath(xpath)
        log_info("element:{}".format(element))
        log_info(Var.appinstance.current_context)
        return element


    @staticmethod
    def wait_for_element_by_classname(classname, timeout=10, interval=1):
        '''
        :param classname:
        :return:
        '''
        try:
            element = Var.appinstance.find_element_by_class_name(classname)
            return element
        except Exception as e:
            raise e

    @staticmethod
    def get_page_source():
        try:
            page_source = Var.appinstance.page_source
            return page_source
        except Exception as e:
            raise e

    @staticmethod
    def save_context(self):
        _current_context = Var.appinstance.context
        if "WEBVIEW" in _current_context:
            _current_window = Var.appinstance.current_window_handle

    @staticmethod
    def restore_context(self):
        if self._current_context != Var.appinstance.context:
            Var.appinstance.switch_to.context(self._current_context)


        if "WEBVIEW" in self._current_context:
            Var.appinstance.switch_to.window(self._current_window)
            logging.info(Var.appinstance.page_source)

    @staticmethod
    def iosSeekBar(fromX,fromY,toX,toY):
        try:
            log_info("iosSeekBar-driver_appium")
            iOSDriver.swipe1(int(fromX), int(fromY), int(toX),int(toY),200)
        except Exception as e:
            raise e

    @staticmethod
    def executeScript(direction, ele):
        try:
            Var.appinstance.execute_script("mobile:swipe", {"direction": direction, 'element': ele, "duration": 1})
        except Exception as e:
            raise e

    @staticmethod
    def executeTap(x, y):
        try:
            Var.appinstance.execute_script("mobile:tap", {'x': x, 'y': y, 'duration': 500})
        except Exception as e:
            raise e

    @staticmethod
    def XYclick(x, y):
        try:
            print("XYclick-driver_appium")
            print(type(x))
            print(type(y))
            end_x = int(x)
            end_y = int(y)
            TouchAction(Var.appinstance).tap(x=end_x,y=end_y).perform()
        except Exception as e:
            raise e

    @staticmethod
    def adb_shell(cmd):
        '''
        :param cmd:
        :return:
        '''
        try:
            log_info('adb对应命令为: {}'.format(cmd))
            if cmd.startswith('shell'):
                cmd = ["adb", "-s", Var.udid, "shell", "{}".format(cmd.lstrip('shell').strip())]
                pipe = subprocess.Popen(cmd, stdin=subprocess.PIPE,
                                        stdout=subprocess.PIPE)
                out = pipe.communicate()
            else:
                cmd = ["adb", "-s", Var.udid, "{}".format(cmd)]
                os.system(' '.join(cmd))
        except:
            raise Exception(traceback.format_exc())
