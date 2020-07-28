#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from runner.action_analysis import ActionAnalysis


class CaseAnalysis(object):

    def __init__(self):
        self.action_nalysis = ActionAnalysis()
        self.testcase_steps = []

    def iteration(self, steps, style='', common={}):
        '''
        :param steps:
        :param style: 控制结果报告中每句case的缩进
        :param common: call 调用时需要的参数
        :return:
        '''
        print("CaseAnalysis---iteration:steps:",steps,"style:",style,"common:",common)
        if isinstance(steps, list):
            for step in steps:
                if isinstance(step, str):
                    self.case_executor(step, style, common)
                    if step == 'break':
                        return True
                elif isinstance(step, dict):
                    result = self.iteration(step, style, common)
                    if result:
                        return True
        elif isinstance(steps, dict):
            print("isinstance(steps, dict)")
            for key, values in steps.items():
                print("isinstance:key, values:",key, values)
                if key.startswith('while'):
                    while self.case_executor(key, style, common):
                        result = self.iteration(values, f'{style}  ', common)
                        if result:
                            break
                elif key.startswith('if') or key.startswith('elif') or key.startswith('else'):
                    print(key,"keystart else")
                    print("self.case_executor(key, style, common):", key, style, common)
                    if self.case_executor(key, style, common):
                        print("self.case_executor(key, style, common):sss",key, style, common)
                        result = self.iteration(values, f'{style}  ', common)
                        print("self.case_executor(key, style, common):result：",result)
                        if result:
                            return True
                        break
                else:
                    raise SyntaxError('- {}:'.format(key))

    def case_executor(self, step, style, common):
        result = self.action_nalysis.action_analysis(step, style, common)
        print("case_executor:",result)
        return result