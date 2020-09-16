#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import re
import platform
import subprocess
import zipfile, plistlib, sys, re

from atf.commons.logging import log_info


class DevicesUtils(object):

    def __init__(self,platformName,udid):
        self.__platformName = platformName
        self.__udid = udid



    def get_app_version(self,ROOT,packageName):
        """
        获取app版本号
        :return:
        """
        app_version = "0.0.0"
        if self.__platformName.lower() == 'android':
            if platform.system() == "Windows":
                #对应命令错误
                pipe = os.popen("adb -s {} shell getprop | findstr versionName".format(self.__udid))
            else:#linux\macos;
                pipe = os.popen("adb -s {} shell dumpsys package {} | grep versionName".format(self.__udid,packageName))
            result = pipe.read()
            app_version = "None" if not result else \
                str(re.split('=', result)[-1]).strip()

        elif self.__platformName.lower() == 'ios':
            if os.path.exists(os.path.join(ROOT, "IGCProject.ipa")):
                ipa_path = os.path.join(ROOT, "IGCProject.ipa")
                app_version = self.analyze_ipa_with_plistlib(ipa_path)
            else:
                app_version = self.get_ios_verson()
        else:
            raise Exception("Test Platform must be Android or iOS!")

        return app_version

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
                pipe = os.popen("adb -s {} shell getprop".format(self.__udid))

            result = pipe.read()
            manufacturer = "None" if not result else \
                re.search(r"\[ro.product.manufacturer\]:\s*\[(.[^\]]*)\]", result).groups()[0]
            model = "None" if not result else \
                re.search(r"\[ro.product.model\]:\s*\[(.[^\]]*)\]", result).groups()[0].split()[-1]
            # sdk = "None" if not result else \
            #     re.search(r"\[ro.build.version.sdk\]:\s*\[(.[^\]]*)\]", result).groups()[0].split()[-1]
            device_version = "None" if not result else \
                re.search(r"\[ro.build.version.release\]:\s*\[(.[^\]]*)\]", result).groups()[0].split()[-1]
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
                device_version = os.popen('ideviceinfo -u {} -k ProductVersion'.format(self.__udid)).read()
                if not DeviceName:
                    DeviceName = 'iOS'
                device_type = DeviceName.replace(' ', '_')
            else:
                device_type = self.__platformName
                device_version = None
        else:
            raise Exception("Test Platform must be Android or iOS!")

        return self.__udid,device_type,device_version



    def get_devices(self,cmd=''):
        if self.__platformName.lower() == 'android':
            pipe = os.popen("adb devices")
            deviceinfo = pipe.read()
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


    def get_ios_verson(self):
        """
        查询设备中的app版本号,不太准
        """
        version = '0.0.0'
        try:
            pipe = os.popen("ideviceinstaller -u {udid} -l".find(udid=self.__udid))
            deviceinfo = pipe.readlines()
            pattern = re.compile(r'com.igetcool.app')
            for line in deviceinfo:
                if 'com.igetcool.app' in line:
                    version = str(line).split('-')[1]
        except Exception as e:
            log_info(e)
        return version



    def analyze_ipa_with_plistlib(self,ipa_path):
        ipa_file = zipfile.ZipFile(ipa_path)
        plist_path = self.find_plist_path(ipa_file)
        plist_data = ipa_file.read(plist_path)
        plist_root = plistlib.loads(plist_data)

        self.print_ipa_info(plist_root)
        return plist_root['CFBundleShortVersionString']

    def find_plist_path(self,zip_file):
        name_list = zip_file.namelist()
        pattern = re.compile(r'Payload/[^/]*.app/Info.plist')
        for path in name_list:
            m = pattern.match(path)
            if m is not None:
                return m.group()

    def print_ipa_info(self,plist_root):
        log_info('Display Name: {}'.format(plist_root['CFBundleDisplayName']))
        log_info('Bundle Identifier: {}'.format(plist_root['CFBundleIdentifier']))
        log_info('Version: {}'.format( plist_root['CFBundleShortVersionString']))


