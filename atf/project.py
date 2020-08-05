#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import time
import json
import inspect
import unittest

from atf.commons.logging import *
from atf.drivers.app_driver_base import AppDriverBase
from atf.drivers.web_driver_base import WebDriverBase
from atf.result.test_runner import TestRunner
from atf.runner.run_case import RunCase
from atf.utils.app_server_utils import AppServerUtils
from atf.utils.devices_utils import DevicesUtils
from atf.utils.testcase_utils import TestCaseUtils
from atf.utils.web_server_utils import WebServerUtils
from atf.utils.yaml_utils import analytical_file, Dict
from atf.commons.variable_global import Var


class Project(object):

    def __init__(self):

        self.__init_project()
        self.__init_config()
        self.__init_logging()
        self.__analytical_testcase_file()
        # self.__analytical_common_file()
        self.__init_data()
        self.__init_keywords()
        self.__init_images()
        self.__init_testcase_suite()

    def __init_project(self):

        for path in [path  for path in inspect.stack() if str(path[1]).endswith("runtest.py")]:
            self.__ROOT = os.path.dirname(path[1])
            sys.path.append(self.__ROOT)
            sys.path.append(os.path.join(self.__ROOT, 'Scripts'))
            Var.ROOT = self.__ROOT
            print(" Var.ROOT:::", Var.ROOT)
            Var.global_var = {} # 全局变量
            Var.extensions_var = {} # 扩展数据变量
            Var.common_var = {} # common临时变量，call执行完后重置

    def __init_config(self):

        self.__config = analytical_file(os.path.join(self.__ROOT, 'config.yaml'))
        print("config::::",self.__config)

        for configK, configV in self.__config.items():
            if configK == 'desiredcaps':
                Var.desired_caps = configV[0]
                for desiredcapsK, desiredcapsV in Var.desired_caps.items():
                    Var[desiredcapsK] = desiredcapsV
            elif configK == 'caps':
                Var.caps = configV[0]
                for capsK, capsV in Var.caps.items():
                    Var[capsK] = capsV
            elif configK == 'prefs':
                Var.prefs = configV[0]
                for profileK, profileV in Var.prefs.items():
                    Var[profileK] = profileV
            else:
                Var[configK] = configV
        print('============Var.desired_caps', Var.desired_caps)
        print('Var.prefs',Var.prefs)

        AppDriverBase.init()
        WebDriverBase.init()


    def __init_data(self):

        if os.path.exists(os.path.join(Var.ROOT, 'data.json')):
            with open(os.path.join(Var.ROOT, 'data.json'), 'r', encoding='utf-8') as f:
                dict = Dict(json.load(fp=f))
                if dict:
                    log_info('******************* analytical data *******************')
                for extensionsK, extensionsV in dict.items():
                    log_info('{}: {}'.format(extensionsK, extensionsV))
                    Var.extensions_var[extensionsK] = extensionsV


    def __init_keywords(self):

        default_keywords_path = os.path.join(__file__.split('project.py')[0], 'runner', 'resource', 'keywords.json')
        if os.path.exists(default_keywords_path):
            with open(default_keywords_path, 'r', encoding='utf-8') as f:
                dict = Dict(json.load(fp=f))
                if dict:
                    Var.default_keywords_data = dict
                else:
                    raise KeyError('Default keyword is empty!')
        if 'keywords' in  Var.extensions_var.keys():
            Var.new_keywords_data = Var.extensions_var['keywords']

    def __init_images(self):

        if Var.extensions_var and Var.extensions_var['images']:
            log_info('******************* analytical images *******************')
            images_dict = {}
            for images in Var.extensions_var['images']:
                images_file = os.path.join(Var.ROOT, 'images/{}'.format(images))
                if os.path.isfile(images_file):
                    images_dict[images] = images_file
                else:
                    raise FileNotFoundError('No such file or directory: {}'.format(images_file))
            Var.extensions_var['images_file'] = images_dict
            log_info('image path: {}'.format(Var.extensions_var['images_file']))

    def __init_logging(self):
        devices = DevicesUtils(Var.platformName, Var.udid)
        Var.udid, deviceinfo = devices.device_info()
        report_time = time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))
        report_child = "{}_{}".format(deviceinfo, report_time)#Netease_MuMu_20200718155040
        #生成报告地址
        Var.report = os.path.join(Var.ROOT, "Report", report_child)#/Users/gaijinfeng/PycharmProjects/autoui_base/Report/Netease_MuMu_20200718155137
        if not os.path.exists(Var.report):
            os.makedirs(Var.report)
            os.makedirs(os.path.join(Var.report, 'resource'))
        log_init(Var.report)


    def __analytical_testcase_file(self):
        log_info('******************* analytical config *******************')
        for configK, configV in self.__config.items():
            log_info('{}: {}'.format(configK, configV))
        log_info('******************* analytical testcase *******************')
        testcase = TestCaseUtils()
        print('testcase------',Var.ROOT,'     ',testcase)
        self.__testcase = testcase.testcase_path(Var.ROOT, Var.testcase)
        log_info('testcase:{}'.format(self.__testcase))



    def __analytical_common_file(self):

        log_info('******************* analytical common *******************')
        Var.common_func = Dict()
        common_dir = os.path.join(Var.ROOT, "Common")
        print("common_dir:",common_dir)
        for rt, dirs, files in os.walk(common_dir):
            print(rt,"===", dirs,"----", files)
            '''
            Common === ['iOS', 'Android'] ---- ['main.yaml']
            Common/iOS === [] ---- ['common.yaml']
            Common/Android === [] ---- ['TestInClass.yaml', 'AppProfile.yaml', 'common.yaml', 'AppProfileB.yaml']

            '''
            if rt == common_dir:
                self.__load_common_func(rt, files)
            elif rt.split(os.sep)[-1].lower() == Var.platformName.lower():
                self.__load_common_func(rt, files)
        log_info('common: {}'.format(Var.common_func.keys()))




    def __load_common_func(self,rt ,files):

        for f in files:
            if not f.endswith('yaml'):
                continue
            for commonK, commonV in analytical_file(os.path.join(rt, f)).items():
                Var.common_func[commonK] = commonV
                print(commonK,"******",Var.common_func[commonK])
                '''
                module ****** APPmain
                skip ****** False
                methods ****** {'CheckProfile': {'description': 'CheckProfile,查看对应的用户资料信息', 'steps': ["click('头像')"]}}
                '''



    def __init_testcase_suite(self):

        self.__suite = []
        for case_path in self.__testcase:
            testcase = analytical_file(case_path)
            testcase['testcase_path'] = case_path
            Var.testcase = testcase
            print('testcase::::',testcase)
            #testcase:::: {'module': 'OpenUrl', 'skip': False, 'description': '打开淘宝', 'steps': ["openUrl('https://www.taobao.com/')"], 'testcase_path': '/Users/gaijinfeng/PycharmProjects/autoui_base/webTestcase/TeacherEntryRoom.yaml'}
            #testCaseClass必须是TestCase的子类（或孙类也行）
            subsuite = unittest.TestLoader().loadTestsFromTestCase(RunCase)
            print("subsuite;;;;",subsuite)
            self.__suite.append(subsuite)
            Var.testcase = None







    def start(self):
        log_info('******************* analytical desired capabilities *******************')
        web_driver = WebServerUtils(Var.web_driver,Var.path)
        Var.webinstance = web_driver.web_start_server(Var.prefs)
        Var.webinstance.get(Var.url)
        Var.webinstance.maximize_window()
        log_info('******************* web open {}*******************'.format(Var.url))

        appserver = AppServerUtils(Var.appdriver, Var.caps, Var.desired_caps)
        appserver.start_server()
        Var.appinstance = appserver.start_connect()
        log_info('******************* app open *******************')
        suite = unittest.TestSuite(tuple(self.__suite))
        print("suite;;;",suite)
        runner = TestRunner()
        runner.run(suite)
        # server.stop_server()