#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import platform
import subprocess
from atf.commons.logging import log_info
import requests
from logzero import logger


send_to_list = 'xinxi,gaijinfeng'

class MessageUtils(object):


    def send_message_result(self,params):
        """
        通过企业微信发送结果给某些人
        """

        url = "http://backend.igetcool.com/notice/igetcoolsendwechat"

        payload = {
                      "user": send_to_list,
                      "topic": "客户端UI自动化测试通知",
                      "body": params['content']
        }

        headers = {
            'Content-Type': 'application/json',
        }

        response = requests.request("POST", url, headers=headers, json=payload)

        logger.info(response.json())



