#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import re
import platform
import subprocess

from atf.commons.logging import log_info


class DevicesUtils(object):

    def __init__(self,platformName,udid):
        self.__platformName = platformName
        self.__udid = udid



    def get_app_version(self):
        """
        获取app版本号
        :return:
        """
        app_version = "0.0.0"
        try:
            cmd = 'adb -s {} shell dumpsys package com.dedao.juvenile'.format(self.__udid)
            log_info(cmd)
            result = subprocess.Popen(cmd, shell=True,
                                      stdout=subprocess.PIPE).stdout.readlines()
            for line in result:
                line = (str(line, encoding="utf-8"))
                if 'versionName=' in line:
                    app_version = line.split('versionName=')[-1].replace("'", ''). \
                        replace("\n", '').replace("platformBuildVersionName=", '').strip()
        except Exception as e:
            log_info("获取App版本号异常: {}".format(e))
        finally:
            return app_version



    def get_device_version(self):
        """
        获取系统版本号
        """
        pipe = os.popen("adb -s {} shell getprop ro.build.version.release".format(self.__udid))
        result = pipe.read()
        return result

    def get_device_sdk_version(self):
        """
        获取系统sdk版本号
        """
        pipe = os.popen("adb -s {} shell getprop ro.build.version.sdk".format(self.__udid))
        result = pipe.read()
        return result


    def device_info(self):
        if self.__platformName.lower() == 'android':
            devices = self.get_devices()
            if self.__udid and (self.__udid not in devices):
                raise Exception("device '{}' not found!".format(self.__udid))
            elif not self.__udid and devices:
                self.__udid = devices[0]
                log_info('使用的设备为：{}'.format(self.__udid))
            elif not self.__udid:
                raise Exception("Can‘t find device!")

            if platform.system() == "Windows":
                pipe = os.popen("adb -s {} shell getprop | findstr product".format(self.__udid))
            else:#linux\macos;查看设备配置
                pipe = os.popen("adb -s {} shell getprop | grep product".format(self.__udid))
            result = pipe.read()
            manufacturer = "None" if not result else \
                re.search(r"\[ro.product.manufacturer\]:\s*\[(.[^\]]*)\]", result).groups()[0]
            model = "None" if not result else \
                re.search(r"\[ro.product.model\]:\s*\[(.[^\]]*)\]", result).groups()[0].split()[-1]
            device_type = "{}_{}".format(manufacturer, model).replace(" ", "_")#Netease_MuMu;HUAWEI_DUK-AL20
        elif self.__platformName.lower() == 'ios':
            devices = self.get_devices('idevice_id -l')
            simulator_devices = self.get_devices('instruments -s Devices')
            if self.__udid and (self.__udid not in (devices or simulator_devices)):
                raise Exception("device '{}' not found!".format(self.__udid))
            elif not self.__udid and devices:
                self.__udid = devices[0]
            elif not self.__udid:
                raise Exception("Can‘t find device!")

            if self.__udid in devices:
                DeviceName = os.popen('ideviceinfo -u {} -k DeviceName'.format(self.__udid)).read()
                if not DeviceName:
                    DeviceName = 'iOS'
                device_type = DeviceName.replace(' ', '_')
            else:
                device_type = self.__platformName
        else:
            raise  Exception("Test Platform must be Android or iOS!")

        return self.__udid,device_type



    def get_devices(self,cmd=''):
        if self.__platformName.lower() == 'android':
            pipe = os.popen("adb devices")
            deviceinfo = pipe.read()
            #print(deviceinfo)
            devices = deviceinfo.replace('\tdevice', "").split('\n')
            devices.pop(0)
            while "" in devices:
                devices.remove("")
        else:
            pipe = os.popen(cmd)
            deviceinfo = pipe.read()
            r = re.compile(r'\[(.*?)\]', re.S)
            devices = re.findall(r, deviceinfo)
            devices = devices if devices else deviceinfo.split('\n')
            while "" in devices:
                devices.remove("")
        log_info('可用的设备列表：{}'.format(devices))
        return devices


"""
[ro.build.product]: [x86]
[ro.product.board]: []
[ro.product.brand]: [Android]
[ro.product.cpu.abi]: [x86]
[ro.product.cpu.abilist]: [x86,armeabi-v7a,armeabi]
[ro.product.cpu.abilist32]: [x86,armeabi-v7a,armeabi]
[ro.product.cpu.abilist64]: []
[ro.product.device]: [x86]
[ro.product.locale]: [zh-CN]
[ro.product.manufacturer]: [Netease]
[ro.product.model]: [MuMu]
[ro.product.name]: [cancro]
"""