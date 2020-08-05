#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import time

from atf.common.logging import *
from atf.common.variable_global import Var
from atf.drivers.app_driver_base import AppDriverBase
from atf.drivers.web_driver_base import WebDriverBase
from atf.utils.opcv_utils import OpencvUtils


class ActionExecutor(object):


    def __init__(self):
        self.elifresults = []


    def __from_scripts_file(self):

        file_list = []
        try:
            for rt, dirs, files in os.walk(os.path.join(Var.ROOT, "Scripts")):
                for f in files:
                    if f == "__init__.py" or f.endswith("pyc") or f.startswith("."):
                        continue
                    file_list.append(f'from Scripts.{f[:-3]} import *')

        except Exception as e:
            log_error(e, False)

        return file_list

    def __action_start_app(self, action):
        """
        行为执行：start_app
        :param action:
        :return:
        """
        parms = action.parms
        if len(parms) == 1:
            AppDriverBase.launch_app(parms[0])
        else:
            raise TypeError('launchApp missing 1 required positional argument: package_info')

    def __action_stop_app(self, action):
        """
        行为执行：stop_app
        :param action:
        :return:
        """
        parms = action.parms
        if parms is None:
            AppDriverBase.close_app(Var.package)
        elif len(parms) == 1:
            AppDriverBase.close_app(parms[0])
        else:
            raise TypeError('closeApp takes 1 positional argument but {} were giver'.format(len(parms)))

    def __action_install_app(self, action):
        """
        行为执行：install_app
        :param action:
        :return:
        """
        if len(action.parms) == 1:
            AppDriverBase.install_app(action.parms[0])
        else:
            raise TypeError('installApp missing 1 required positional argument: app_path')

    def __action_uninstall_app(self, action):
        """
        行为执行：uninstall_app
        :param action:
        :return:
        """
        if len(action.parms) == 1:
            AppDriverBase.uninstall_app(action.parms[0])
        else:
            raise TypeError('uninstallApp missing 1 required positional argument: package_info')

    def __action_adb(self, action):
        """
        行为执行：adb
        :param action:
        :return:
        """
        if len(action.parms) == 1:
            AppDriverBase.adb_shell(action.parms[0])
        else:
            raise TypeError('adb missing 1 required positional argument')

    def __action_goback(self, action):
        """
        行为执行：goback
        :param action:
        :return:
        """
        AppDriverBase.adb_shell('shell input keyevent 4')

    def __action_tap(self, action):
        """
        行为执行：tap
        :param action:
        :return:
        """
        if len(action.parms) == 2:
            AppDriverBase.tap(float(action.parms[0]), float(action.parms[-1]))
        else:
            raise TypeError('tap missing 2 required positional argument: x, y')

    def __action_doubleTap(self, action):
        """
        行为执行：doubleTap
        :param action:
        :return:
        """
        if len(action.parms) == 2:
            AppDriverBase.double_tap(float(action.parms[0]), float(action.parms[-1]))
        else:
            raise TypeError('doubleTap missing 2 required positional argument: x, y')

    def __action_press(self, action):
        """
        行为执行：press
        :param action:
        :return:
        """
        if len(action.parms) == 2:
            AppDriverBase.press(float(action.parms[0]), float(action.parms[-1]))
        elif len(action.parms) == 3:
            AppDriverBase.press(float(action.parms[0]), float(action.parms[1]), float(action.parms[-1]))
        else:
            raise TypeError('press missing 2 required positional argument: x, y')

    def __action_swipe(self, action):
        """
        行为执行：swipe
        :param action:
        :return:
        """
        parms = action.parms
        if parms is None:
            raise TypeError('swipe missing 4 required positional argument: from_x, from_y, to_x, to_y')
        if parms[0] == 'up':
            AppDriverBase.swipe_up()
        elif parms[0] == 'down':
            AppDriverBase.swipe_down()
        elif parms[0] == 'left':
            AppDriverBase.swipe_left()
        elif parms[0] == 'right':
            AppDriverBase.swipe_right()
        elif len(parms) == 4:
            AppDriverBase.swipe(float(action.parms[0]), float (action.parms[1]), float(action.parms[2]), float(action.parms[3]))
        elif len(action.parms) == 5:
            AppDriverBase.swipe(float(action.parms[0]), float(action.parms[1]), float(action.parms[2]), float(action.parms[3]), int(action.parms[4]))
        else:
            raise TypeError('swipe takes 1 positional argument but {} were giver'.format(len(action.action)))

    def __action_getText(self, action):
        """
        行为执行：getText
        :param action:
        :return:
        """
        parms = action.parms
        if len(parms) == 1:
            text = AppDriverBase.get_text(key=parms[0], timeout=Var.timeout, interval=Var.interval, index=0)
        elif len(parms) == 2:
            text = AppDriverBase.get_text(key=parms[0], timeout=Var.timeout, interval=Var.interval, index=parms[-1])
        else:
            raise TypeError('getText missing 1 required positional argument: element')
        return text


    def __action_click(self, action):
        """
        行为执行：click
        :param action:
        :return:
        """
        parms = action.parms
        print('parms::::',parms)
        print(len(parms))
        if len(parms):


            # img_info = self.__ocr_analysis(action.action, parms[0], True)
            if len(parms) == 1:
                AppDriverBase.click(key=parms[0], timeout=Var.timeout, interval=Var.interval, index=0)
            elif len(parms) == 2:
                AppDriverBase.click(key=parms[0], timeout=Var.timeout, interval=Var.interval, index=parms[1])
            # elif not isinstance(img_info, bool):
            #     Var.ocrimg = img_info['ocrimg']
            #     x = img_info['x']
            #     y = img_info['y']
            #     AppDriverBase.tap(x, y)
        else:
            raise TypeError('click missing 1 required positional argument: element')

    def __action_check(self, action):
        """
        行为执行：check
        :param action:
        :return:
        """
        parms = action.parms
        print("parms:::",parms)
        print(len(parms))
        if len(parms):


            img_info = self.__ocr_analysis(action.action, parms[0], True)
            if not isinstance(img_info, bool):
                if img_info is not None:
                    Var.ocrimg = img_info['ocrimg']
                    check = True
                else:
                    check = False
            elif len(parms) == 1:
                check = AppDriverBase.check(key=parms[0], timeout=Var.timeout, interval=Var.interval, index=0)
            elif len(parms) == 2:
                check = AppDriverBase.check(key=parms[0], timeout=Var.timeout, interval=Var.interval, index=parms[1])
            else:
                raise TypeError('check takes 2 positional arguments but {} was given'.format(len(parms)))

            if not check:
                raise Exception("Can't find element {}".format(parms[0]))
            return check
        else:
            raise TypeError('click missing 1 required positional argument: element')

    def __action_input(self, action):
        """
        行为执行：input
        :param action:
        :return:
        """
        parms = action.parms
        if len(parms) == 2:
            AppDriverBase.input(key=parms[0], text=parms[1], timeout=Var.timeout, interval=Var.interval,
                             index=0)
        elif len(parms) == 3:
            AppDriverBase.input(key=parms[0], text=parms[1], timeout=Var.timeout, interval=Var.interval,
                             index=parms[2])
        else:
            raise TypeError('input missing 2 required positional argument: element, text')

    def __action_isContain(self,action):
        pagesource = AppDriverBase.get_page_source()
        print("action.parms的类型：",type(action.parms[0]),action.parms[0])
        if action.parms[0] in pagesource:
            return True
        else:
            return False



    def __action_ifcheck(self, action):
        """
        行为执行：ifcheck
        :param action:
        :return:
        """
        parms = action.parms
        if len(parms):
            img_info = self.__ocr_analysis(action.action, parms[0], True)
            if not isinstance(img_info, bool):
                if img_info is not None:
                    Var.ocrimg = img_info['ocrimg']
                    check = True
                else:
                    check = False
            elif len(parms) == 1:
                check = AppDriverBase.check(key=parms[0], timeout=Var.timeout, interval=Var.interval, index=0)
            elif len(parms) == 2:
                check = AppDriverBase.check(key=parms[0], timeout=Var.timeout, interval=Var.interval, index=parms[1])
            else:
                raise TypeError('check takes 2 positional arguments but {} was given'.format(len(parms)))

            return check
        else:
            raise TypeError('click missing 1 required positional argument: element')

    def __action_ifiOS(self, action):
        """
        行为执行：ifiOS
        :param action:
        :return:
        """
        if Var.platformName.lower() == 'ios':
            return True
        return False

    def __action_ifAndroid(self, action):
        """
        行为执行：ifAndroid
        :param action:
        :return:
        """
        if Var.platformName.lower() == 'android':
            return True
        return False

    def __action_sleep(self, action):
        """
        行为执行
        :param action:
        :return:
        """
        parms = action.parms
        if parms is None:
            raise TypeError('sleep missing 1 required positional argument')
        elif len(parms) == 1:
            time.sleep(float(parms[0]))

    def __ocr_analysis(self, action, element, israise):
        """
        :param action:
        :param element:
        :return:
        """
        print('action:',action,";element:",element,";israise:",israise,"Var.extensions_var['images_file'].keys():")
        if element not in Var.extensions_var['images_file'].keys():
            return False
        time.sleep(5)
        img_file = Var.extensions_var['images_file'][element]
        print("__ocr_analysis---img_file:",img_file)
        orcimg = OpencvUtils(action, img_file)
        orcimg.save_screenshot()
        img_info = orcimg.extract_minutiae()
        if img_info:
            return img_info
        else:
            if israise:
                raise Exception("Can't find element {}".format(element))
            else:
                return None

    def __action_getVar(self, action):
        '''
        :return:
        '''
        if action.key == '$.getText':
            print("进入text")
            result = self.__action_getText(action)
        elif action.key == '$.id':
            print("进入id")
            result = eval(action.parms)
        elif action.key == 'isContain':
            result = self.__action_isContain(action)
            print("isContain:result:",result)
        elif action.key == '$.getVar':
            print("进入getvar")
            if Var.global_var:
                if action.parms[0] in Var.global_var:
                    result = Var.global_var[action.parms[0]]
                else:
                    result = None
            else:
                result = None
            print("getVar:result:",result)
        elif action.key:
            list = self.__from_scripts_file()
            print(list,"这事一个list")
            for l in list:
                exec(l)
            func = f'{action.key}({action.parms})'
            print("func：：：",func)
            result = eval(func)
            print("action.key:result:",result)

        else:
           result = action.parms[0]
        print("action_executor:__action_getVar")
        log_info(f'{action.name}: {result}')
        return result

    def __action_setVar(self, action):
        '''
        :return:
        '''
        key = action.parms[0]
        values = action.parms[1]
        Var.global_var[key] = values
        return

    def __action_call(self, action):
        '''
        :param action:
        :return:
        '''
        key = action.key
        parms = action.parms
        print('ActionExecutor：__action_call：action',action)
        if  not key in Var.common_func.keys():
            print("Var.common_func.keys()")
            raise NameError('name "{}" is not defined'.format(key))
        if len(Var.common_func[key].input) != len(parms):
            print("len(Var.common_func[key].input) != len(parms)")
            raise TypeError('{}() takes {} positional arguments but {} was given'.format(key, len(
                Var.common_func[key].input), len(parms)))
        common_var = dict(zip(Var.common_func[key].input, parms))
        print("ActionExecutor：__action_call：common_var:",common_var,"Var.common_func[key].input:",Var.common_func[key].input, "parms:",parms)

        try:
            from atf.runner import CaseAnalysis
            case = CaseAnalysis()
            print("ActionExecutor：__action_call： case = CaseAnalysis()")
            print(Var.common_func[key].steps,"00000:", f'{action.style}  ', "ppppp",common_var)
            case.iteration(Var.common_func[key].steps, f'{action.style}  ', common_var)
        except Exception as e:
            # call action中如果某一句step异常，此处会往上抛异常，导致call action也是失败状态，需要标记
            Var.exception_flag = True
            raise e
        return





    def __action_web_click(self, action):
        """
        行为执行：click
        :param action:
        :return:
        """
        parms = action.parms
        print('web,parms::::', parms)
        print(len(parms))
        if len(parms):

            if len(parms) == 2:
                WebDriverBase.click(key1=parms[0],key2=parms[1], timeout=Var.timeout, interval=Var.interval, index=0)
            elif len(parms) == 3:
                WebDriverBase.click(key1=parms[0],key2=parms[1], timeout=Var.timeout, interval=Var.interval, index=parms[2])
            # elif not isinstance(img_info, bool):
            #     Var.ocrimg = img_info['ocrimg']
            #     x = img_info['x']
            #     y = img_info['y']
            #     AppDriverBase.tap(x, y)
        else:
            raise TypeError('click missing 1 required positional argument: element')

    def __action_web_input(self, action):
        """
        行为执行：click
        :param action:
        :return:
        """
        parms = action.parms
        print("__action_web_input:",parms)
        if len(parms) == 3:
            WebDriverBase.input(key1=parms[0], key2=parms[1], text=parms[2], timeout=Var.timeout, interval=Var.interval,
                                index=0)
        elif len(parms) == 4:
            WebDriverBase.input(key1=parms[0], key2=parms[1], text=parms[2], timeout=Var.timeout, interval=Var.interval,
                                index=parms[3])
        else:
            raise TypeError('input missing 2 required positional argument: element, text')






    def __action_other(self, action):
        '''
        :return:
        '''
        key = action.key
        parms = action.parms
        try:
            result = eval(parms)
            print("__action_other:result",result,"action.key:",key)
            log_info('{}: {}'.format(action.parms, result))

            if key == 'if':
                self.elifresults = []
                # if |elif |while |assert .
            if key == 'if' or key == 'elif':
                ifresult = result
                print("ifresult---", ifresult)
                self.elifresults.append(ifresult)
            print("elifresults----", self.elifresults)



            if key == 'assert':
                assert result
            return result
        except Exception as e:
            raise e

    def new_action_executor(self, action):

        if action.key:
            list = self.__from_scripts_file()
            for l in list:
                exec(l)
            func = f'{action.key}({action.parms})'
            result = eval(func)
            print("result:::::new_action_executor::",result)
            return result
        else:
            raise KeyError('The {} keyword is undefined!'.format(action.step))

    def action_executor(self, action):
        """
        行为执行
        :param action:
        :return:
        """
        print("action-----",action.tag,'----------',action.key)
        # 声明一个全局变量的list，在elif\else调用的时候使用，如果list中False为奇数，那就执行else;如果list

        if action.tag and action.tag == 'getVar' :
            result = self.__action_getVar(action)

        elif action.tag and action.tag == 'setVar':
            result = self.__action_setVar(action)

        elif action.tag and action.tag == 'call':
            result = self.__action_call(action)

        elif action.tag and action.tag == 'other':
            result = self.__action_other(action)

        elif action.key == 'installApp':
            result = self.__action_install_app(action)

        elif action.key == 'uninstallApp':
            result = self.__action_uninstall_app(action)

        elif action.key == 'launchApp':
            result = self.__action_start_app(action)

        elif action.key == 'closeApp':
            result = self.__action_stop_app(action)

        elif action.key == 'tap':
            result = self.__action_tap(action)

        elif action.key == 'doubleTap':
            result = self.__action_doubleTap(action)

        elif action.key == 'press':
            result = self.__action_press(action)

        elif action.key == 'goBack':
            result = self.__action_goback(action)

        elif action.key == 'adb':
            result = self.__action_adb(action)

        elif action.key == 'swipe':
            result = self.__action_swipe(action)

        elif action.key == 'click':
            result = self.__action_click(action)

        elif action.key == 'check':
            result = self.__action_check(action)

        elif action.key == 'input':
            result = self.__action_input(action)


        elif action.key == 'sleep':
            result = self.__action_sleep(action)

        elif action.key == 'ifiOS':
            result = self.__action_ifiOS(action)

        elif action.key == 'ifAndroid':
            result = self.__action_ifAndroid(action)

        elif action.key == 'ifcheck':
            result = self.__action_ifcheck(action)

        elif action.key == 'elifcheck':
            result = self.__action_ifcheck(action)

        elif action.key == 'break':
            result = None

        elif action.key == 'else':
            # elifresults = [True,False,False]
            #只要有一个True，就不会再继续执行else
            print("ction.key",self.elifresults)
            if True in self.elifresults:
                result = None
            else:
                result = "else"

        elif action.key == 'isContain':
            print(action,"这是一个action;",action.parms)
            result = self.__action_isContain(action)
            print("结果为：",result)
        elif action.key == 'webInput':
            result = self.__action_web_input(action)

        elif action.key == 'webClick':
            result = self.__action_web_click(action)
        else:
            raise KeyError('The {} keyword is undefined!'.format(action.key))

        return result