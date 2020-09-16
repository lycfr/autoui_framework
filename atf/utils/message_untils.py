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



    def get_wechat_markdown(self, params):
        return \
"""
客户端UI自动化报告通知，请相关同事注意。
> 通知时间:<font color="black"> {} </font>
> 报告地址: [点击查看]({})
""".format(time.strftime("%Y%m%d%H%M%S"), params['oss_url'])



    def text_format(self,text):
        """
        格式化文本
        :return:
        """
        msg = ""
        if "," in text:
            msg = '\n'.join(str(text).split(','))
        else:
            msg  = text
        return  msg



    def send_message_markdown(self ,params):
        '''
        发送企业微信机器人消息
        :param platform:
        :param app_version:
        :param tag:
        :param env:
        :param app_path:
        :return:
        '''
        logger.info('准备发送企业微信消息')
        try:
            webhook_api = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=6477f4cc-8405-4e6b-bc8e-7c970b9d3c28" #【机器人-客户端自动化测试群】
            data = {
                "msgtype": "markdown",
                "markdown": {
                    "content": params['content']
                  }
               }
            r = requests.post(webhook_api, json=data, verify=False)
            logger.info(r.json())
        except Exception as e:
            logger.error(e)


