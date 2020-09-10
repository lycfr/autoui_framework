#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import re
import sys
import time
import shutil

from atf.commons.variable_global import Var


class Template_mixin(object):
    """
     Define a HTML template for report customerization and generation.

     Overall structure of an HTML report

     HTML
     +------------------------+
     |<html>                  |
     |  <head>                |
     |                        |
     |   STYLESHEET           |
     |   +----------------+   |
     |   |                |   |
     |   +----------------+   |
     |                        |
     |  </head>               |
     |                        |
     |  <body>                |
     |                        |
     |   HEADING              |
     |   +----------------+   |
     |   |                |   |
     |   +----------------+   |
     |                        |
     |   REPORT               |
     |   +----------------+   |
     |   |                |   |
     |   +----------------+   |
     |                        |
     |   ENDING               |
     |   +----------------+   |
     |   |                |   |
     |   +----------------+   |
     |                        |
     |  </body>               |
     |</html>                 |
     +------------------------+
     """

    STATUS = {
        0: 'pass',
        1: 'fail',
        2: 'error',
        3: 'skip'
    }
    HTML_TMPL = r'''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>测试报告</title>
    <link rel="stylesheet" type="text/css" href="resource/css.css">
    <script type="text/javascript" src="http://libs.baidu.com/jquery/2.1.1/jquery.min.js"></script>
    <script src="https://cdn.bootcss.com/echarts/3.8.5/echarts.common.min.js"></script>
    <script src="resource/js.js"></script>
</head>
<body>
<div class="root">
    {heading}
    {pie}    
    {device}
    {apk}
    {trReportList}
    {tabdiv}
</div>
</body>
<script language="javascript" type="text/javascript">
{chart_script}
</script>
</html>
    '''


    ECHARTS_SCRIPT = """
    // 基于准备好的dom，初始化echarts实例
    var myChart = echarts.init(document.getElementById('chart'));

    // 指定图表的配置项和数据
    var option = {
    title : {
    text: '测试执行情况',
    x:'center'
    },
    tooltip : {
    trigger: 'item',
    formatter: "{a} <br/>{b} : {c} ({d}%%)"
    },
    color: ['#95b75d', 'grey', '#b64645'],
    legend: {
    orient: 'vertical',
    left: 'left',
    data: ['通过','失败','错误']
    },
    series : [
    {
    name: '测试执行情况',
    type: 'pie',
    radius : '60%%',
    center: ['50%%', '60%%'],
    data:[
    {value:%(Pass)s, name:'通过'},
    {value:%(fail)s, name:'失败'},
    {value:%(error)s, name:'错误'}
    ],
    itemStyle: {
    emphasis: {
    shadowBlur: 10,
    shadowOffsetX: 0,
    shadowColor: 'rgba(0, 0, 0, 0.5)'
    }
    }
    }
    ]
    };

    // 使用刚指定的配置项和数据显示图表。
    myChart.setOption(option);
    """


    # 结果饼图
    PIE_TMPL = r'''
        <div class="head" style="height: 240px">
            <div class="head_title">PIE</div>
            <div style="height: 210px;border: 1px solid rgb(220,220,220); background-color: white">
                <div id="chart" style="width:500px;height:200px;float:left;"></div>
            </div>
        </div>
        '''


    # 设备信息
    DEVICE_TMPL = r'''
        <div class="head" style="height: 240px">
            <div class="head_title">Device Info</div>
            <div style="height: 210px;border: 1px solid rgb(220,220,220); background-color: white">
                <p class="text">Device Name：{device_name}</p>
                <p class="text">Device Udid：{device_udid}</p>
                <p class="text">Device Version：{device_version}</p>
            </div>
        </div>
        '''


    # APK信息
    APK_TMPL = r'''
        <div class="head" style="height: 240px">
            <div class="head_title">Apk Info</div>
            <div style="height: 210px;border: 1px solid rgb(220,220,220); background-color: white">
                <p class="text">Apk Version：{apk_version}</p>
            </div>
        </div>
        '''

    # caseReport
    REPORT_TMPL = r'''
                    <div class="head" style="height: auto">
                        <div class="head_title">Report</div>
                        <div style="height: auto;border: 1px solid rgb(220,220,220); background-color: white">
                                {trReportList}
                        </div>
                    </div>
                    
        '''

    REPORT_TMPL_DIV = r'''<pre class="reportPardesc">{reportPardesc}    {reportDes}    {reportStatus}</pre>'''


    # 测试汇总
    HEADING_TMPL = r'''
        <div class="title">
            <h2 style="color: white;text-align: center;line-height: 65px">{title}</h2>
        </div>
        <div class="head" style="height: 240px">
            <div class="head_title">Summarization</div>
            <div style="height: 210px;border: 1px solid rgb(220,220,220); background-color: white">
                <p class="text">Total：{total}</p>
                <p class="text">Pass：{Pass}</p>
                <p class="text">Failure：{failure}</p>
                <p class="text">Error：{error}</p>
                <p class="text">Skipped：{skipped}</p>
                <p class="text">StartTime：{startTime}</p>
                <p class="text">Duration：{duration}</p>
            </div>
        </div>
        '''

    # 详细数据
    TABDIV_TMPL = r'''
        <div class="tabdiv" style="height: auto">
        <div class="head_title">Details</div>
        <div style="height:auto;border: 1px solid rgb(220,220,220); background-color: white">
            <table class="table" cellspacing="0">
                <tr>
                    <th width="20%%">CaseName</th>
                    <th width="30%%">Description</th>
                    <th width="20%%">StartTime</th>
                    <th width="10%%">Duration</th>
                    <th width="10%%">Status</th>
                    <th width="10%%">Open/Close</th>
                </tr>
                {trlist}
            </table>
        </div>
        </div>
    '''

    # module_name
    MODULE_NAME = r'''
                <tr>
                    <td class="module_td" colspan="1" style=" text-align:left; text-indent: 20px;">{module_name}</td>
                    <td class="module_td" colspan="1" style=" text-align:left; text-indent: 20px;">{pardescription}</td>
                    <td class="module_td" colspan="3"><span class="Pass status">&nbsp;Pass:{Pass}&nbsp;</span> | <span class="failure status">&nbsp;failure:{failure}&nbsp;</span> | <span class="error status">&nbsp;error:{error}&nbsp;</span> | <span class="skipped status">&nbsp;skipped:{skipped}&nbsp;</span></td>
                    <td class="module_name" data-tag='module_{tag_module_name}'>Open</td>
                </tr>
    '''

    # case
    CASE_TMPL = r'''
                <tr class='module_{module_name}' style="display: none">
                    <td class="module_td {b_color}" style=" text-align:left; text-indent: 40px;">{casename}</td>
                    <td class="module_td {b_color}">{description}</td>
                    <td class="module_td {b_color}">{startTime}</td>
                    <td class="module_td {b_color}">{duration}</td>
                    <td class="module_td {b_color}">{status}</td>
                    <td class="module_td_view {b_color}" data-tag='{dataId}'>Open</td>
                </tr>
    '''

    # case details
    CASE_DETA_NOT_SNAPSHOT = r'''
                <tr class="{dataId}" style="display: none">
                    <td class="module_deta" colspan="2" style="border-right: 0">
                        <div class="errordiv">
                            <h3 style="margin-bottom: 10px">Steps</h3>
                            <pre class="errorp" style="white-space: pre-wrap;overflow-wrap: break-word;margin-top: 0">{steplist}</pre>
                        </div>
                    </td>
                    <td class="module_deta" colspan="4">
                        <div class="errordiv">
                            <h3 style="margin-bottom: 10px">Logs</h3>
                            <pre class="errorp" style="white-space: pre-wrap;overflow-wrap: break-word;margin-top: 0">{errlist}</pre>
                        </div>
                    </td>
                </tr>
    '''

    CASE_DETA_SNAPSHOT = r'''
                <tr class="{dataId}" style="display: none">
                    <td class="module_deta" colspan="6" style="border-right: 0">
                        <div class="errordiv">
                            <h3 style="margin-bottom: 10px">Steps</h3>
                            {steplist}
                        </div>
                    </td>
                </tr>
    '''


    CASE_SNAPSHOT_DIV = r'''
                            <div class="Stepsdetails">
                                <div class="steps" style="display: inline-block">
                                        <pre class="StepsdetailsPre_duration">{runtime} | </pre>
                                        <pre class="StepsdetailsPre {status}">{steps}</pre>
                                </div>
                                <div class="img_errorp" style="display: none;">
                                    <img class="img" src="{image}">
                                </div>
                            </div>
    '''
    CASE_ERROR_DIV = r'''
                            <div class="Stepsdetails">
                                <div class="steps" style="display: inline-block">
                                        <pre class="StepsdetailsPre_duration">{runtime} | </pre>
                                        <pre class="StepsdetailsPre {status}">{steps}</pre>
                                </div>
                                <div class="img_errorp" style="display: none;">
                                    <img class="img" src="{image}">
                                    <pre class="errorp" style="white-space: pre-wrap;overflow-wrap: break-word;">{errlist}</pre>
                                </div>
                            </div>
    '''

    DEFAULT_TITLE = 'Unit Test Report'
    DEFAULT_DESCRIPTION = ''
    DEFAULT_PARDESCRIPTION = ''
class HTMLTestRunner(Template_mixin):

    def __init__(self, stream=sys.stdout, verbosity=1, title=None, description=None):
        Var.case_reports = []
        self.stream = stream
        self.verbosity = verbosity
        self.title = title if title else self.DEFAULT_TITLE
        self.description = description if description else self.DEFAULT_DESCRIPTION


    def generateReport(self,result,starttime,stoptime):
        report_attrs = self._getReportAttributes(result, starttime, stoptime)
        report = self._generate_report(result)
        device = self._generate_device()
        apk = self._generate_apk()
        reportCase = self._generate_reportCase()
        heading = self._generate_heading(report_attrs)
        tabdiv = self.TABDIV_TMPL.format(
            trlist = report
        )
        chart = self._generate_chart()
        pie = self._generate_pie()
        output = self.HTML_TMPL.format(
            heading = heading,
            device=device,
            apk=apk,
            tabdiv = tabdiv,
            pie = pie,
            chart_script = chart,
            trReportList = reportCase
        )
        resource = os.path.join(os.path.split(os.path.abspath(__file__))[0], "resource")
        shutil.copy(os.path.join(resource,"css.css"), os.path.join(result.report,'resource'))
        shutil.copy(os.path.join(resource,"js.js"), os.path.join(result.report,'resource'))
        self.stream.write(output.encode('utf-8'))

    def _getReportAttributes(self,result,starttime,stoptime):

        startTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(starttime))
        duration = str(int(stoptime - starttime)) + 's'
        Total = result.testsRun
        Pass = len(result.successes)
        Failure = len(result.failures)
        Error = len(result.errors)
        skipped = len(result.skipped)


        Var.duration = duration
        Var.Total = Total
        Var.Pass = Pass
        Var.Failure = Failure
        Var.Error = Error
        Var.skipped = skipped

        return (Total,Pass,Failure,Error,skipped,startTime,duration)


    def _generate_pie(self):
        return self.PIE_TMPL




    def _generate_chart(self):
        chart = self.ECHARTS_SCRIPT % dict(
                Pass=str(Var.Pass),
                fail=str(Var.Failure),
                error=str(Var.Error),
                )
        return chart


    def _generate_report(self, result):
        sortedResult = self.sortResult(result.result)
        table_lsit = []
        Var.reportsList = []
        for cid, (cls, cls_results) in enumerate(sortedResult):
            module_name = cls
            status_list = ['Pass','failure','error','skipped']
            Pass = 0
            failure = 0
            error = 0
            skipped = 0
            cls_list = []
            pardescription = ""
            for tup_result in cls_results:
                _status = tup_result[0]
                testinfo = tup_result[1]
                descriptions = testinfo.description.split("/")
                pardescription = descriptions[0]
                description = descriptions[1]
                description = description if description else self.DEFAULT_DESCRIPTION
                Var.reportPardesc = "模块:" + pardescription
                Var.reportDes = "功能:" + description
                Var.reportStatus = "结果为:" + status_list[_status]
                report_tmpl_div = self.REPORT_TMPL_DIV.format(
                    reportPardesc = Var.reportPardesc,
                    reportDes = Var.reportDes,
                    reportStatus = Var.reportStatus
                )
                Var.reportsList.append(report_tmpl_div)
                caseinfo = self._generate_case(testinfo, status_list[_status])
                cls_list.append(caseinfo)
                if _status != 3: # 跳过
                    casedeta = self._generate_case_deta(testinfo)
                    cls_list.append(casedeta)

                if _status == 0:
                    Pass += 1
                elif _status == 1:
                    failure += 1
                elif _status == 2:
                    error += 1
                elif _status == 3:
                    skipped += 1
            pardescription = pardescription if pardescription else self.DEFAULT_PARDESCRIPTION

            module_name = self.MODULE_NAME.format(
                module_name = module_name,
                pardescription = pardescription,
                Pass = Pass,
                failure = failure,
                error = error,
                skipped = skipped,
                tag_module_name = module_name
            )
            table_lsit.append(module_name)
            for tr in cls_list:
                table_lsit.append(tr)
        tr_ = ''
        for tr in table_lsit:
            tr_ = tr_ + tr
        return tr_


    def sortResult(self,result_list):

        rmap = {}
        classes = []
        for n, t, o in result_list:
            cls = t.module_name
            if str(cls).count(".") == 0:
                cls = cls
            else:
                cls = ".".join(cls.split(".")[:-1])
            if not cls in rmap:
                rmap[cls] = []
                classes.append(cls)
            rmap[cls].append((n, t, o))
        r = [(cls, rmap[cls]) for cls in classes]
        return r


    def _generate_device(self):
        device = self.DEVICE_TMPL.format(
            device_name = Var.device_type,
            device_udid = Var.udid,
            device_version = Var.device_version,

        )
        return device


    def _generate_apk(self):
        apk = self.APK_TMPL.format(
            apk_version=Var.apk_version
        )
        return apk

    def _generate_reportCase(self):
        reportCase = self.REPORT_TMPL.format(
            trReportList="".join(Var.reportsList)
        )
        return reportCase

    def _generate_heading(self,report_attrs):

        if report_attrs:
            heading = self.HEADING_TMPL.format(
                title = self.title,
                total = report_attrs[0],
                Pass = report_attrs[1],
                failure = report_attrs[2],
                error = report_attrs[3],
                skipped = report_attrs[4],
                startTime = report_attrs[5],
                duration = report_attrs[6]
            )
            return heading

    def _generate_case(self,testinfo,status):
        casename = testinfo.casename
        descriptions = testinfo.description.split("/")
        description = descriptions[1]
        startTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(testinfo.start_time))
        duration = str(int(testinfo.stop_time - testinfo.start_time)) + 's'
        Var.reportDuration = duration
        dataId = testinfo.dataId
        module_name = testinfo.module_name

        caseinfo = self.CASE_TMPL.format(
            module_name=module_name,
            casename=casename,
            description=description,
            startTime=startTime,
            duration=duration,
            status=status,
            dataId=dataId,
            b_color=status
        )
        return caseinfo

    def _generate_case_deta(self,testinfo):
        dataId = testinfo.dataId
        steps = testinfo.stdout
        err = '\n' + testinfo.test_exception_info if testinfo.test_exception_info else 'Nothing'
        if testinfo.snapshot_dir and os.path.exists(testinfo.snapshot_dir):
            path = testinfo.snapshot_dir.split(testinfo.module_name, 1)[-1]
            steps = ""
            result = os.path.join(testinfo.snapshot_dir,'result.log')
            if os.path.isfile(result):
                file_list = []
                with open(result, 'r') as f:
                    for line in f:
                        file_list.append(line.strip())

                file_list = sort_string(file_list)
                for out in file_list:
                    out_list = out.split('|:|')
                    f_path = testinfo.module_name + os.path.join(path, out_list[-2].replace('/', '&2F').replace('\\',
                                                                                                            '&5C').replace(
                        '*', '&2a').replace('\n', ''))
                    if len(out_list[2]) < 6:
                        runtime = '{}{}'.format(out_list[2],' ' * (6-len(out_list[2])))
                    else:
                        runtime = out_list[2]
                    if out_list[1] in 'True':
                        case_snapshot = self.CASE_SNAPSHOT_DIV.format(
                            status = 'Passfont',
                            runtime = runtime,
                            steps = out_list[-1],
                            image = f_path
                        )
                    else:
                        case_snapshot = self.CASE_ERROR_DIV.format(
                            status = 'errorfont',
                            runtime = runtime,
                            steps = out_list[-1],
                            image = f_path,
                            errlist = err
                        )


                    steps = steps + case_snapshot
            else:
                case_snapshot = self.CASE_SNAPSHOT_DIV.format(
                    status='skipped',
                    runtime='0',
                    steps='Nothing',
                    image=''
                )

            casedeta = self.CASE_DETA_SNAPSHOT.format(
                dataId=dataId,
                steplist=steps,
            )

        else:
            casedeta = self.CASE_DETA_NOT_SNAPSHOT.format(
                dataId=dataId,
                steplist=steps,
                errlist=err
            )



        return casedeta


def embedded_numbers(s):
    '''
    :param s:
    :return:
    '''
    re_digits = re.compile(r'(\d+)')
    pieces = re_digits.split(s)
    pieces[1::2] = map(int,pieces[1::2])
    return pieces

def sort_string(lst):

    return sorted(lst,key=embedded_numbers)
