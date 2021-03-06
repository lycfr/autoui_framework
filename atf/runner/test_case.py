#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import re
import unittest
import traceback

from atf.commons.logging import log_info
from atf.commons.variable_global import Var
from atf.utils.commom_utils import *


class TestCase(unittest.TestCase):
    def __getattr__(self, item):
        try:
            return self.__getattribute__(item)
        except:
            attrvalue = None
            self.__setattr__(item, attrvalue)
            return attrvalue

    def __init__(self, methodName="runTest"):
        super(TestCase, self).__init__(methodName)
        if not Var.testcase:
            raise NameError("name 'testcase' is not defined")
        for key, value in Var.testcase.items():
            setattr(self, key, value)

        self.testcase_path_list = []
        self.testcase_path_list = split_yaml(self.testcase_path)
        methodname = self.testcase_path_list[1]
        self.method = self.methods[methodname]
        self.desc = self.method['desc']
        self.description = self.description + "/" + self.desc
        self.snapshot_dir = os.path.join(Var.report, self.module, self.testcase_path.split(os.sep)[-1].split(".")[0])


    def setUp(self):
        # 重新赋值failureException，注意：failureException的值是一个类，不是类实例
        self.failureException = self.failure_monitor()

    def failure_monitor(self):
        test_case = self  # 将self赋值给test_case，以便下方的AssertionErrorPlus内部类可调用外部类的方法

        class AssertionErrorPlus(AssertionError):
            def __init__(self, msg):
                try:
                    app_screenshot_steps(None, Var.tmp_file, Var.file, zoom=1.0)
                    log_info('失败截图已保存到: %s' % Var.tmp_file)
                except BaseException:
                    log_info('截图失败: %s' % traceback.format_exc())

                super(AssertionErrorPlus, self).__init__(msg)

        return AssertionErrorPlus  # 返回AssertionErrorPlus类

    def run(self, result=None):
        try:
            Var.case_step_index = 0
            Var.case_snapshot_index = 0
            Var.testcase_steps = []
            Var.methodnames = {}
            Var.snapshot_dir = self.snapshot_dir
            if not os.path.exists(Var.snapshot_dir):
                os.makedirs(Var.snapshot_dir)
            log_info("******************* TestMthod {} Start *******************".format(self.description))
            log_info("******************* TestSteps *******************")

            testSteps = self.method['steps']
            self.__testcases_list = yaml_testMethod(testSteps)
            for ii in self.__testcases_list:
                if type(ii) == str:
                    Var.testcase_steps.append(ii)
                elif (type(ii) == list) and (len(ii) == 2):
                    listyaml = yaml_steps(ii)
                    for l in listyaml:
                        log_info(l)
                        Var.testcase_steps.append(l)
            log_info("******************* Run TestSteps *******************")
            unittest.TestCase.run(self, result)
            Var.testcase_steps = []


            log_info(
                "******************* Total: {}, Pass: {}, Failed: {}, Error: {}, Skipped: {} ********************\n"
                    .format(len(Var.methodnames), len(result.successes), len(result.failures),
                            len(result.errors),
                            len(result.skipped)))
        except:
            traceback.print_exc()

