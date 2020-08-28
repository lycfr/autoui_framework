#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''=================================================
@Project -> File   ：autoui_base -> commom_utils
@IDE    ：PyCharm
@Author ：GAI
@Date   ：2020/8/12 11:25 上午
@Desc   ：
=================================================='''
import os

import cv2

from atf.commons.variable_global import Var
from atf.utils.yaml_utils import analytical_file


def strip(listname):
    relist = []
    for i in listname:
        d = i.strip()
        relist.append(d)
    return relist

# #config解析
# def yaml_method(spaths):
#     '''
#     :param spaths: 传入一个list
#     :return: 返回一个list
#     '''
#     respath = {}
#     for sp in spaths:
#         if sp.endswith(".yaml"):
#             # print(sp)
#             respath[sp] = ""
#         else:
#             s = sp.split(".yaml/")
#             s[0] = s[0] + ".yaml"
#             print(s)
#             respath[s[0]] = s[1]
#     print(respath)
#     return respath

# #test里面yaml文件解析
def split_yaml(sp):
    '''
    :param spaths: 传入一个list
    :return: 返回一个步骤step的list
    '''
    dd = []
    s = sp.split(".yaml/")
    key = s[0] + '.yaml'
    value = s[1]
    dd.append(key)
    dd.append(value)
    return dd

#test里面yaml文件解析
def yaml_testMethod(spaths):
    '''
    :param spaths: 传入一个list
    :return: 返回一个步骤step的list
    '''
    ll = []
    dd = []
    for sp in spaths:
        if 'yaml/' in sp:
            s = sp.split(".yaml/")
            key = s[0] + '.yaml'
            value = s[1]
            dd.append(key)
            dd.append(value)
            ll.append(dd)
            dd = []
        else:
            ll.append(sp)
    return ll

def yaml_steps(respath):
    files = os.path.join(Var.ROOT, '{}'.format(respath[0]))
    dicts = analytical_file(files)
    listmethods = dicts['methods']
    methodname = respath[1]
    dictmethod = listmethods[methodname]
    liststeps = dictmethod['steps']
    steps_list = list(liststeps)
    return steps_list


def app_screenshot_steps(element,filepath,redFilepath,zoom=1.0):
    if element is None:
        return Var.appinstance.save_screenshot(redFilepath)
    else:
        # 标注元素位置
        print(Var.appinstance)
        Var.appinstance.get_screenshot_as_file(filepath)
        img = cv2.imread(filepath)
        location = element.location
        size = element.size
        x = int(location['x'] * zoom)
        y = int(location['y'] * zoom)
        cv2.rectangle(img, (x, y), (x + int(size['width'] * zoom), y + int(size['height'] * zoom)), (0, 0, 255), 5)
        cv2.imwrite(redFilepath, img)
        with open(redFilepath, 'rb') as f:
            file = f.read()
        if (os.path.exists(filepath)):
            os.remove(filepath)
        return file

def app_screenshot_eles_steps(elements,filepath,redFilepath,zoom=1.0):
    if elements is None:
        return Var.appinstance.save_screenshot(redFilepath)
    else:
        # 标注元素位置
        print(Var.appinstance)
        Var.appinstance.get_screenshot_as_file(filepath)
        img = cv2.imread(filepath)
        for ele in elements:
            location = ele.location
            size = ele.size
            x = int(location['x'] * zoom)
            y = int(location['y'] * zoom)
            cv2.rectangle(img, (x, y), (x + int(size['width'] * zoom), y + int(size['height'] * zoom)), (0, 0, 255), 5)
        cv2.imwrite(redFilepath, img)
        with open(redFilepath, 'rb') as f:
            file = f.read()
        if (os.path.exists(filepath)):
            os.remove(filepath)
        return file





