# -*- coding: utf-8 -*-

import os
import subprocess
import time
import traceback
import grpc
import socket
import platform
import perfdog_pb2_grpc
import perfdog_pb2
import threading
from perfdog_config import *
from logzero import logger

base_path = os.path.dirname(__file__)  # 当前文件所在路径

def get_current_time():
    time_now = int(time.time())
    time_local = time.localtime(time_now)
    dt = time.strftime("%Y%m%d%H%M%S", time_local)
    return dt

report_out_path = base_path + '/perfdog_service_output_{}'.format(get_current_time())
logger.info('导出报告地址: {report_out_path}'.format(report_out_path=report_out_path))


def check_port_in_use(port, host='127.0.0.1'):
    s = None
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        s.connect((host, int(port)))
        return True
    except socket.error:
        return False
    finally:
        if s:
            s.close()


def __check_port_is_used(port):
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
        logger.error('The platform is {} ,this platform is not support.'.format(p))


def start_service(port):
    """
    启动服务
    """
    sys_command = jre_path + "/java -Dfile.encoding=UTF-8 -Xms128m -Xmx500m -jar {} --server.port={}".format(jar_path,port)
    logger.info('运行服务命令: {sys_command}'.format(sys_command=sys_command))
    subprocess.Popen(sys_command, stdout=subprocess.PIPE, shell=True)


def kill_service(port):
    """
    关闭服务
    """
    result, pid = __check_port_is_used(port)
    if result != False:
        sys_command = 'kill -9 {}'.format(pid)
        subprocess.Popen(sys_command, stdout=subprocess.PIPE, shell=True)
        logger.info('Kill PerfDog进程:{pid}'.format(pid=pid))



def run(collect_time=30,device_name=None,server_port='23456'):
    """
    第一次运行demo前需要通过pip安装grpcio(1.23.0)和protobuf(3.10.0)
    """
    kill_service(server_port)
    start_service(server_port)
    try:
        # 在代码里启动PerfDogService或手动启动PerfDogService
        print("0.启动PerfDogService")
        # 填入PerfDogService的路径
        perfDogService = subprocess.Popen(server_path)
        # 等待PerfDogService启动完毕
        time.sleep(5)
        logger.info("1.通过ip和端口连接到PerfDog Service")
        options = [('grpc.max_receive_message_length', 100 * 1024 * 1024)]
        channel = grpc.insecure_channel('127.0.0.1:23456', options=options)
        logger.info("2.新建一个stub,通过这个stub对象可以调用所有服务器提供的接口")
        stub = perfdog_pb2_grpc.PerfDogServiceStub(channel)
        logger.info("3.通过令牌登录，令牌可以在官网申请")
        userInfo = stub.loginWithToken(perfdog_pb2.Token(token=token))
        #logger.info("UserInfo:\n", userInfo)
        logger.info("4.启动设备监听器监听设备,每当设备插入和移除时会收到一个DeviceEvent")
        deviceEventIterator = stub.startDeviceMonitor(perfdog_pb2.Empty())
        for deviceEvent in deviceEventIterator:
            # 从DeviceEvent中获取到device对象，device对象会在后面的接口中用到
            device = deviceEvent.device
            if device.uid == device_name:
                logger.info('匹配到输入的手机uid:{}'.format(device.uid))
                if deviceEvent.eventType == perfdog_pb2.ADD:
                    logger.info("设备[%s:%s]插入\n" % (device.uid, perfdog_pb2.DEVICE_CONTYPE.Name(device.conType)))
                    # 每台手机会返回两个conType不同的设备对象(USB的和WIFI的),如果是测有线，取其中的USB对象
                    if device.conType == perfdog_pb2.USB:
                        #logger.info("5.初始化设备[%s:%s]\n" % (device.uid, perfdog_pb2.DEVICE_CONTYPE.Name(device.uid)))
                        stub.initDevice(device)
                        logger.info("6.获取app列表")
                        appList = stub.getAppList(device)
                        apps = appList.app
                        app_index = 0
                        app_input_index = 0
                        for app in apps:
                            app_index += 1
                            if app.packageName == 'com.dedao.juvenile':
                                app_input_index = app_index - 1
                                break
                        logger.info('查询到的序号: {}'.format(app_input_index))
                        # app_select = int(input("请选择要测试App: "))
                        app_select = app_input_index
                        app = apps[app_select]

                        logger.info("7.获取设备的详细信息")
                        deviceInfo = stub.getDeviceInfo(device)
                        logger.info("8.开启性能数据项")
                        stub.enablePerfDataType(
                            perfdog_pb2.EnablePerfDataTypeReq(device=device, type=perfdog_pb2.NETWORK_USAGE))
                        logger.info("9.开始收集[%s:%s]的性能数据\n" % (app.label, app.packageName))
                        logger.info(stub.startTestApp(perfdog_pb2.StartTestAppReq(device=device, app=app)))

                        req = perfdog_pb2.OpenPerfDataStreamReq(device=device)
                        perfDataIterator = stub.openPerfDataStream(req)

                        def perf_data_process():
                            for perfData in perfDataIterator:
                                logger.info(perfData)

                        threading.Thread(target=perf_data_process).start()
                        # 采集一些数据
                        logger.info('采集性能数据时间:{collect_time}'.format(collect_time=collect_time))
                        time.sleep(collect_time)
                        logger.info("10.设置label")
                        stub.setLabel(perfdog_pb2.SetLabelReq(device=device, label="I am a label"))
                        time.sleep(3)
                        logger.info("11.添加批注")
                        stub.addNote(perfdog_pb2.AddNoteReq(device=device, time=5000, note="I am a note"))
                        logger.info("12.上传和导出所有数据")
                        saveResult = stub.saveData(perfdog_pb2.SaveDataReq(
                            device=device,
                            caseName="case1",  # web上case和excel的名字
                            uploadToServer=True,  # 上传到perfdog服务器
                            exportToFile=True,  # 保存到本地
                            outputDirectory=  report_out_path,
                            dataExportFormat=perfdog_pb2.EXPORT_TO_JSON
                        ))

                        #logger.info("保存结果:\n", saveResult)
                        logger.info("12.上传和导出第5秒到20秒的数据")
                        stub.saveData(perfdog_pb2.SaveDataReq(
                            device=device,
                            beginTime=5000,  # 指定开始时间
                            endTime=20000,  # 指定结束时间
                            caseName="case2",  # web上case和excel的名字
                            uploadToServer=True,  # 上传到perfdog服务器
                            exportToFile=True,  # 保存到本地
                            outputDirectory=  report_out_path,
                            dataExportFormat=perfdog_pb2.EXPORT_TO_EXCEL
                        ))
                        logger.info("13.停止测试")
                        stub.stopTest(perfdog_pb2.StopTestReq(device=device))
                        logger.info("over")
                        break
                elif deviceEvent.eventType == perfdog_pb2.REMOVE:
                    logger.info("设备[%s:%s]移除\n" % (device.uid, perfdog_pb2.DEVICE_CONTYPE.Name(device.conType)))
            break

    except Exception as e:
        logger.info(e)
        traceback.print_exc()


if __name__ == '__main__':

    run(collect_time=60,device_name='SRK6R20B20007158',server_port='23456')
