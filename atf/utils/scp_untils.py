
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import paramiko
import subprocess
from paramiko import WarningPolicy
from scp import SCPClient
from contextlib import closing
from scpclient import WriteDir
from atf.commons.logging import *



def upload_img(remote_path=None,local_path=None):
    host = "10.30.130.116"  # 服务器ip地址
    port = 22  # 端口号
    username = "root"  # ssh 用户名
    password = "5yKUHcxTynfDORnN1"  # 密码

    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
    ssh_client.set_missing_host_key_policy(WarningPolicy())
    ssh_client.connect(host, port, username, password)
    scpclient = SCPClient(ssh_client.get_transport(), socket_timeout=15.0)
    try:
        #scpclient.put(local_path, remote_path)

        with closing(WriteDir(ssh_client.get_transport(), remote_path)) as scp:
            scp.send_dir(local_path, preserve_times=True)

    except FileNotFoundError as e:
        print(e)
        print("系统找不到指定文件" + local_path)
    else:
        print("文件上传成功")
    ssh_client.close()



def scpFileToRemoteNode(user,ip,password,localsource,remotedest,port=22):

    ServerHost = 'http://qa-jenkins-test.igetcool.com/apks/reports/'

    local_file = str(localsource).split('/')[-1]

    try:
        SCP_CMD_BASE = r"""
                expect -c "
                set timeout 300 ;
                spawn scp -o StrictHostKeyChecking=no -P {port} -r {localsource} {username}@{host}:{remotedest};
                expect *assword* {{{{ send {password}\r }}}}  ;
                expect *\r ;
                expect \r ;
                expect eof
                "
        """.format(username=user,password=password,host=ip,localsource=localsource,remotedest=remotedest,port=port)
        SCP_CMD = SCP_CMD_BASE.format(localsource = localsource)
        log_info("execute SCP_CMD:  {}".format(SCP_CMD))
        p  = subprocess.Popen( SCP_CMD , stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        p.communicate()
        os.system(SCP_CMD)

        ReportPath = ServerHost + local_file + '/report.html'
        log_info("ReportPath:  {}".format(ReportPath))
        return ReportPath
    except Exception as e:
        log_info('scpFileToRemoteNode is {e}'.format(e=e))




def sshpassFileToRemoteNode(user,ip,password,localsource,remotedest,port=22):
    """
    sshpass免密码登录
    """
    ServerHost = 'http://qa-jenkins-test.igetcool.com/apks/reports/'

    local_file = str(localsource).split('/')[-1]

    try:
        SCP_CMD_BASE = "sshpass -p {password} scp -o StrictHostKeyChecking=no -r {localsource} {username}@{host}:{remotedest}".\
            format(username=user,password=password,host=ip,localsource=localsource,remotedest=remotedest,port=port)
        log_info("execute SCP_CMD:  {}".format(SCP_CMD_BASE))
        p  = subprocess.Popen( SCP_CMD , stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        p.communicate()
        os.system(SCP_CMD)

        ReportPath = ServerHost + local_file + '/report.html'
        log_info("ReportPath:  {}".format(ReportPath))
        return ReportPath
    except Exception as e:
        log_info('sshpassFileToRemoteNode is {e}'.format(e=e))

