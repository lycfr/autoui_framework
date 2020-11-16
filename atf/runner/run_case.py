from atf.commons.variable_global import Var
from atf.drivers.app_driver_base import AppDriverBase
from atf.runner.case_analysis import CaseAnalysis
from atf.runner.test_case import TestCase

import sys
import functools
import traceback

from atf.commons.logging import *


def retry_method():  # n为重试次数,不包括必要的第一次执行


    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):

            log_info("******************* 重试用例 *******************")

            n = Var.retry_count

            log_info("******************* 准备最大重试用例次数 {} *******************".format(n))

            num = 0
            while num <= n:
                try:
                    log_info('Go into Retry Method')
                    num += 1
                    func(*args, **kwargs)
                    return
                # except AssertionError:
                except Exception as e:
                    log_info('Retry_method Exception {}'.format(e))
                    log_info('Retry_method AssertionError')
                    if num <= n:
                        trace = sys.exc_info()
                        traceback_info = ""
                        for trace_line in traceback.format_exception(trace[0], trace[1], trace[2], 3):
                            traceback_info += trace_line
                        log_info(traceback_info)
                        args[0].tearDown()
                        args[0].setUp()
                    else:
                        raise
        return wrapper
    return decorator


class RunCase(TestCase):

    def setUp(self):
        #web是否重启
        # if Var.restart and not self.skip:
        #     WebDriverBase.

        #app是否重启
        #
        if Var.restart and not self.skip:
            AppDriverBase.launch_app(None)

    # @retry_method()
    def testCase(self):
        if self.skip:
            self.skipTest('skip')
        case = CaseAnalysis()
        case.iteration(Var.testcase_steps)


    def tearDown(self):
        if Var.restart and not Var.testcase_steps:
            AppDriverBase.close_app(None)


