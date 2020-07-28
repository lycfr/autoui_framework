#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import cv2
import sys
import time
import traceback
import threading

from commons.logging import log_error
from commons.variable_global import Var


def therading(func):
    def start(*args, **kwds):
        print("therading----start")
        def run():
            try:
                th.ret = func(*args, **kwds)
            except:
                th.exc = sys.exc_info()
        def get(timeout=None):
            th.join(timeout)
            if th.exc:
                raise th.exc[1]
            return th.ret
        th = threading.Thread(None,run)
        th.exc = None
        th.ret = None
        th.get = get
        th.start()
        return th
        print("th-----",th)
    return start

def keywords(func, *args, **kwds):
    print("keywords----decorator:")
    def wrapper(*args, **kwds):
        result = None
        exception_flag = False
        exception = None
        Var.ocrimg = None
        start_time = time.time()
        Var.case_snapshot_index += 1
        Var.exception_flag = False
        snapshot_index = Var.case_snapshot_index
        imagename = "Step_{}.png".format(snapshot_index)
        file = os.path.join(Var.snapshot_dir, imagename)
        action_step = args[-2].step
        action_tag = args[-2].tag
        style = args[-1]
        print("action_step---",action_step)
        print("action_tag---",action_tag)
        try:
            if args or kwds:
                print(args,kwds,"-=-=-=keywords-=54")
                result = func(*args, **kwds)
            else:
                result = func()
        except Exception as e:
            exception = e
            exception_flag = True
        finally:
            try:
                if Var.ocrimg is not None:
                    cv2.imwrite(file, Var.ocrimg)
                    Var.ocrimg = None
                else:
                    print("decorator---file::::",file)
                    # Var.appinstance.save_screenshot(file)
                stop_time = time.time()
                duration = str('%.1f' % (stop_time - start_time))

                # 获取变量值后需要替换掉原数据
                if action_tag == 'getVar':
                    step_ = action_step.split('=', 1)
                    if step_[-1].startswith(' '):
                        action_step = f'{step_[0]}= {result}'
                    else:
                        action_step = f'{step_[0]}={result}'
                    result = None

                # call action中某一语句抛出异常，会导致call action状态也是false,需要处理
                result_exception_flag = not exception_flag
                if Var.exception_flag:
                    result_exception_flag = True

                if result is not None:
                    # if while 等需要把结果放在语句后面
                    result_step = '{}|:|{}|:|{}s|:|{}|:|{}: {}\n'.format(snapshot_index, result_exception_flag, duration,
                                                                     imagename, f'{style}- {action_step}', result)
                else:
                    result_step = '{}|:|{}|:|{}s|:|{}|:|{}\n'.format(snapshot_index, result_exception_flag, duration,
                                                                     imagename, f'{style}- {action_step}')
                with open(os.path.join(Var.snapshot_dir, 'result.log'), 'a') as f:
                    f.write(result_step)
            except:
                log_error(traceback.format_exc(), False)
            if exception_flag:
                raise exception
        return result
    print("wrapper::::22222",wrapper)
    return wrapper