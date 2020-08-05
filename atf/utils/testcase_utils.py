#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os

class TestCaseUtils(object):

    def __init__(self):
        self.__testcase_list = []



    def __traversal_dir(self,path):
        print("TestCaseUtils__traversal_dir",path,"os.walk(path)",os.walk(path))
        # print("------", rt, dirs, files)

        for rt, dirs, files in os.walk(path):
            files.sort()
            for f in files:
                file_path = os.path.join(rt, f)
                print("--file_path==",file_path)
                if os.path.isfile(file_path):
                    self.__testcase_list.append(file_path)

    def testcase_path(self,dirname,paths):
        print("testcase_path(self,dirname,paths):",dirname,"---",paths)
        if not paths:
            raise Exception('test case is empty.')
        for path in paths:
            file_path = os.path.join(dirname,path)
            print('用例地址：',file_path)#testcase/zhibo.yaml
            if os.path.isfile(file_path):
                self.__testcase_list.append(file_path)
            else:
               self.__traversal_dir(os.path.join(dirname, path))
        if not self.__testcase_list:
            raise Exception('test case is empty.')
        print("查看当前测试用例列表，self.__testcase_list---testcase_path",self.__testcase_list)
        return self.__testcase_list