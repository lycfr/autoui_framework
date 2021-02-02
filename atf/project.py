#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import glob
import os
import sys
import time
import json
import inspect
import unittest

from atf.utils.message_untils import MessageUtils
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
from atf.commons.logging import log_info
from atf.utils.scp_untils import scpFileToRemoteNode
from atf.__about__ import atf_version
from atf.utils.upload_untils import UploadUtils

class Project(object):

    def __init__(self,config_name='config.yaml',data_json='data.json',device_name=None):

        self.config_name = config_name
        self.device_name = device_name
        self.data_json = data_json
        self.__init_project()
        self.__init_config()
        self.__init_logging()
        self.__analytical_testcase_file()
        self.__analytical_pages_file()
        self.__init_data()
        self.__init_keywords()
        self.__init_images()
        self.__init_testcase_suite()

    def __init_project(self):

        for path in [path for path in inspect.stack() if str(path[1]).endswith("runtest.py")]:
            self.__ROOT = os.path.dirname(path[1])
            self.__config = analytical_file(os.path.join(self.__ROOT, self.config_name))
            sys.path.append(self.__ROOT)
            sys.path.append(os.path.join(self.__ROOT, 'Scripts'))
            Var.ROOT = self.__ROOT
            Var.global_var = {} # 全局变量
            Var.extensions_var = {} # 扩展数据变量
            Var.common_var = {} # common临时变量，call执行完后重置
            Var.cases_var = {}
            Var.black_list = list()

    def __init_config(self):

        # self.__config = analytical_file(os.path.join(self.__ROOT, 'config.yaml'))
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
            elif configK == 'black_list':
                Var.black_list = configV
            else:
                Var[configK] = configV

            if configK == 'testenv':
                Var.testenv = configV

            if configK == 'retry_count':
                Var.retry_count = configV

            # else:
            #     Var.retry_count = 0

        if "appdriver" in self.__config.keys():
            log_info("******************* appdriver 初始化 *******************")
            AppDriverBase.init()
        if "web_driver" in self.__config.keys():
            log_info("******************* web_driver 初始化 *******************")
            WebDriverBase.init()

        # 覆盖配置文件的udid
        if self.device_name != None:
           Var.desired_caps['udid'] = self.device_name
           Var.desired_caps['deviceName'] = self.device_name
           Var.udid = self.device_name


        log_info("******************* 设备号 {} *******************".format(Var.udid))


    def __init_data(self):
        # if os.path.exists(os.path.join(Var.ROOT, 'data.json')):
        if os.path.exists(os.path.join(Var.ROOT, self.data_json)):
            with open(os.path.join(Var.ROOT, self.data_json), 'r', encoding='utf-8') as f:

            # with open(os.path.join(Var.ROOT, 'data.json'), 'r', encoding='utf-8') as f:
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
        log_info('******************* __init_logging *******************')
        if Var.platformName != None:
            devices = DevicesUtils(Var.platformName, Var.udid)
            Var.__udid, deviceinfo, Var.device_version = devices.device_info()
            Var.device_type = deviceinfo
            if Var.platformName.lower() == 'ios':
                Var.apk_version = devices.get_app_version(self.__ROOT,Var.desired_caps['app'])
            else:
                Var.apk_version = devices.get_app_version(self.__ROOT,Var.desired_caps['package'])

            report_time = time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))
            report_child = "{}_{}".format(deviceinfo.strip(), report_time)
        else:
            report_time = time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))
            report_child = "{}_{}".format(Var.web_driver.lower(), report_time)


        # deleReportPath = os.path.join(os.getcwd(), deleReport)
        # if os.path.exists(deleReportPath):
        #     os.remove(deleReport)
        # 生成报告地址
        Var.report = os.path.join(Var.ROOT, "Report", report_child)
        print(Var.report)
        print(os.getcwd())
        ReportPath = os.path.join(os.getcwd(), Var.report)
        log_info('Report Path is {}'.format(ReportPath))
        if not os.path.exists(Var.report):
            os.makedirs(Var.report)
            os.makedirs(os.path.join(Var.report, 'resource'))
        log_init(Var.report)


    def __analytical_testcase_file(self):
        log_info('******************* analytical config *******************')
        for configK, configV in self.__config.items():
            log_info('{}: {}'.format(configK, configV))

            if configK == 'testcase' and 'TestShopWechatPay' in str(configV):
                   Var.isShopWechatPay = True
                   log_info('******************* TestShopWechatPay testcase *******************')

        log_info('******************* analytical testcase *******************')
        testcase = TestCaseUtils()
        self.__testcase = testcase.testcase_path(Var.ROOT, Var.testcase)
        Var.cases_var = self.__testcase



    def __analytical_pages_file(self):
        log_info('******************* analytical pages *******************')
        Var.pages_func = Dict()
        pages_dir = os.path.join(Var.ROOT, "pages")
        for rt, dirs, files in os.walk(pages_dir):
            if (rt == 'pages/app') | (rt == 'pages/web'):
                self.__load_common_func(rt, files)
        log_info('pages: {}'.format(Var.pages_func.keys()))


    def __load_common_func(self,rt ,files):
        for f in files:
            if not f.endswith('yaml'):
                continue
            for commonK, commonV in analytical_file(os.path.join(rt, f)).items():
                Var.pages_func[commonK] = commonV



    def __init_testcase_suite(self):
        self.__suite = []
        for case_path in self.__testcase:
            if type(case_path) == str:
                testcase = analytical_file(case_path)
                testcase['testcase_path'] = case_path
                Var.testcase = testcase
            else:
                testcase = analytical_file(case_path[0])
                testcase['testcase_path'] = case_path[0] +'/' +case_path[1]
                Var.testcase = testcase
            subsuite = unittest.TestLoader().loadTestsFromTestCase(RunCase)
            self.__suite.append(subsuite)
            Var.testcase = None


    def start(self):
        log_info('******************* analytical desired capabilities *******************')
        if Var.web_driver != None:
            web_driver = WebServerUtils(Var.web_driver,Var.path)
            Var.webinstance = web_driver.web_start_server(Var.prefs)
            Var.webinstance.get(Var.url)
            Var.webinstance.maximize_window()
            log_info('******************* web open {}*******************'.format(Var.url))
        if Var.appdriver != None:
            appserver = AppServerUtils(Var.appdriver, Var.appmodule,Var.caps, Var.desired_caps)
            appserver.start_server()
            Var.appinstance = appserver.start_connect()
            log_info('******************* app open *******************')

        suite = unittest.TestSuite(tuple(self.__suite))
        runner = TestRunner()
        runner.run(suite)
        if "appdriver" in self.__config.keys():
            appserver.stop_server()
        if "web_driver" in self.__config.keys():
            web_driver.init()

        log_info('Report Path is {}'.format(os.path.join(os.getcwd(),Var.report)))

        time.sleep(5)
        # 暂时写死生成报告时间
        ReportPath = scpFileToRemoteNode("root", "10.30.130.116", "5yKUHcxTynfDORnN1",
                            os.path.join(os.getcwd(),Var.report),
                            "/opt/data/reports", 22)

        log_info('******************* ui task over *******************')



        if Var.isShopWechatPay == True:
            message_params = {}
            message_params['content'] = self.create_shoppay_message_body(ReportPath)
            MessageUtils().send_shoppay_message_markdown(message_params)
        else:

            message_params = {}
            message_params['content'] = self.create_message_body(ReportPath)
            MessageUtils().send_message_result(message_params)
            MessageUtils().send_message_markdown(message_params)

        UploadUtils.post_result_info(ReportPath)


    def create_message_body(self,ReportPath):
        """
        创建提测消息体
        :return:
        """
        return '客户端UI自动化测试通知,请相关同事关注\n> ' \
                       '时间: ' + str(time.strftime("%Y-%m-%d %H:%M:%S")) + "\n" + \
                       '版本: ' + str(Var.apk_version) + "\n" + \
                       '平台: ' + str(Var.platformName.lower()) + "\n" + \
                       '环境: ' + str(Var.testenv) + "\n" + \
                       '持续时间: ' + str(Var.duration)  + "\n" + \
                       '累计用例: ' + str(Var.Total)  + "\n" + \
                       '成功用例: ' + str(Var.Pass)  + "\n" + \
                       '失败用例: ' + str(Var.Failure)  + "\n" + \
                       '错误用例: ' + str(Var.Error)  + "\n" + \
                       '跳过用例: ' + str(Var.skipped)  + "\n" + \
                       '报告地址: ' + str(ReportPath)   + "\n"



    def create_shoppay_message_body(self, ReportPath):
        """
        创建提测消息体
        :return:
        """
        status = 'SUCCESS' if Var.Pass == 1 else 'FAIL'
        return 'QA环境商城支付UI自动化测试通知,请相关同事关注 \n> ' \
               '时间: ' + str(time.strftime("%Y-%m-%d %H:%M:%S")) + "\n" + \
               '平台: ' + str(Var.platformName.lower()) + "\n" + \
               '环境: ' + str(Var.testenv) + "\n" + \
               '持续时间: ' + str(Var.duration) + "\n" + \
               '测试结果: ' + status + "\n" + \
               '报告地址: ' + str(ReportPath) + "\n"




    @staticmethod
    def get_version():
        return atf_version