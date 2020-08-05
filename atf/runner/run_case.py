from atf.commons.variable_global import Var
from atf.drivers.app_driver_base import AppDriverBase
from atf.drivers.web_driver_base import WebDriverBase
from atf.runner.case_analysis import CaseAnalysis
from atf.runner.test_case import TestCase


class RunCase(TestCase):

    def setUp(self):
        #web是否重启
        # if Var.restart and not self.skip:
        #     WebDriverBase.

        #app是否重启
        #
        if Var.restart and not self.skip:
            AppDriverBase.launch_app(None)

    def testCase(self):
        if self.skip:
            self.skipTest('skip')
        case = CaseAnalysis()
        print("testCase:steps",self.steps)
        case.iteration(self.steps)

    def tearDown(self):
        print("endsssssss")
        # if Var.restart and not self.skip:
        #     AppDriverBase.close_app(None)
