#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import os
import re
import platform
import subprocess
from atf.commons.logging import log_info
from atf.commons.variable_global import Var
import requests


class UploadUtils(object):

    @staticmethod
    def post_result_info(reports_path):
        """
        上传本次测试数据
        :return:
        """
        log_info('******************* post result to qacenter *******************')
        try:
            params = {}
            params['project'] = 'igetcool'
            params['context'] = Var.platformName
            params['type'] = 'ui'
            params['env'] = Var.testenv
            params['version'] = Var.apk_version
            params['duration'] = Var.duration
            params['all'] = Var.Total
            params['successes'] = Var.Pass
            params['failures'] = Var.Failure
            params['errors'] = Var.Error
            params['details'] = []
            params['status'] = "FAILURES" if int(Var.Failure) > 0 or int(Var.Error) > 0 else "SUCCESS"
            params['task_id'] = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
            params['build_number'] = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
            params['report_path'] = reports_path
            url = 'http://backend.igetcool.com/report/upload'
            r = requests.post(url, json=params, verify=False)
            log_info(r.status_code)
            log_info(r.json())
        except Exception as e:
            log_info(e)
