#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
import platform
import subprocess
from selenium import webdriver

from atf.common.logging import *
from atf.driver import web_driver


class WebServerUtils(object):

    def __getattr__(self, item):
        print("WebUtils--__getattr__")
        try:
            return self.__getattribute__(item)
        except:
            return None

    def __init__(self, web_driver,path):
        print("WebUtils--__init__")

        if web_driver.lower() in ['chrome', 'fix']:
            self.web_driver = web_driver.lower()
        else:
            self.web_driver = 'chrome'

        # prefs_dict = {}
        if self.web_driver == 'chrome':
            if 'chrome' in path:
                self.chromepath = path
            else:
                log_error("path地址错误")
        else:
            print("passweb")

        # log_info('web    {}: {}'.format(key, value))
        # object.__setattr__(self, key, value)
        self.webinstance = None

    def __check_port_is_used(self,port):
        print("ServerUtils--__check_port_is_used")
        p = platform.system()
        if p == 'Windows':
            sys_command = "netstat -ano|findstr %s" % port
            pipe = subprocess.Popen(sys_command, stdout=subprocess.PIPE, shell=True)
            out, error = pipe.communicate()
            if str(out, encoding='utf-8') != "" and "LISTENING" in str(out, encoding='utf-8'):
                pid = re.search(r"\s+LISTENING\s+(\d+)\r\n", str(out, encoding='utf-8')).groups()[0]
                return True, pid
            else:
                return False, None
        elif p == 'Darwin' or p == 'Linux':
            sys_command = "lsof -i:%s" % port
            pipe = subprocess.Popen(sys_command, stdout=subprocess.PIPE, shell=True)
            for line in pipe.stdout.readlines():
                if "LISTEN" in str(line, encoding='utf-8'):
                    pid = str(line, encoding='utf-8').split()[1]
                    return True, pid
            return False, None
        else:
            log_error('The platform is {} ,this platform is not support.'.format(p))



    def web_start_server(self,prefs):
        print("WebUtils--web_start_server")

        try:
            log_info('Start the web_driver')
            if self.web_driver == 'chrome':
                from selenium import webdriver
                option = webdriver.ChromeOptions()
                option.add_experimental_option('prefs', prefs)

                self.webinstance = webdriver.Chrome(executable_path=self.chromepath, chrome_options=option)
                self.webinstance.implicitly_wait(10)
            else:
                #todo:其他的浏览器
                pass

            return self.webinstance
        except Exception as e:
            raise e