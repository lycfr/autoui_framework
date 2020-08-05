#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import re
import json

from atf.common.decorator import keywords
from atf.common.variable_global import Var
from atf.runner.action_executor import ActionExecutor, log_info
from atf.common import Var, Dict, log_info


class ActionAnalysis(object):

    def __init__(self):
        self.variables = {}
        self.action_executor = ActionExecutor()


    def __get_variables(self, name):
        '''
        获取变量
        :param name:
        :return:
        '''
        print('ActionAnalysis,__get_variables',name)
        if not re.match(r'^\${(\w+)}$', name):
            raise SyntaxError(name)
        name = name[2:-1]
        if name in self.common_var.keys():
            object_var = self.common_var[name]
        elif name in self.variables:
            object_var = self.variables[name]
        elif name in vars(Var).keys():
            object_var = vars(Var)[name]
        elif Var.extensions_var and name in Var.extensions_var['variable'].keys():
            object_var = Var.extensions_var['variable'][name]
        else:
            object_var = None
        return object_var

    def __join_value(self, contents, join):
        '''
        拼接字符串
        :param contents:
        :param join:
        :return:
        '''
        print("__join_value---",contents,"----",join)

        content_str = None
        if contents:
            for content in contents:
                if content_str:
                    content_str = content_str + join +  self.__replace_string(content)
                else:
                    content_str = self.__replace_string(content)
        else:
            content_str = ''
        print("content_str:::",content_str)
        return content_str

    def __replace_string(self, content):
        """
        字符串替换
        :param content:
        :return:
        """
        print("__replace_string---",content)

        if isinstance(content, str):
            if re.match(r"^'(.*)'$", content):
                content = '"{}"'.format(content)
            elif  re.match(r'^"(.*)"$', content):
                content = "'{}'".format(content)
            else:
                content = '\'{}\''.format(content)
        else:
            content = str(content)
        print("__replace_string::content::",content)
        return content

    def __get_replace_string(self, content):
        '''

        :param content:
        :return:
        '''
        print("__get_replace_string---",content)

        pattern_content = re.compile(r'(\${\w+}+)')
        while True:
            if isinstance(content, str):
                search_contains = re.search(pattern_content, content)
                if search_contains:
                    search_name = self.__get_variables(search_contains.group())
                    if search_name is None:
                        search_name = 'None'
                    elif isinstance(search_name, str):
                        if re.search(r'(\'.*?\')', search_name):
                            search_name = '"{}"'.format(search_name)
                        elif re.search(r'(".*?")', search_name):
                            search_name = '\'{}\''.format(search_name)
                        else:
                            search_name = '\'{}\''.format(search_name)
                    else:
                        search_name = str(search_name)
                    content = content[0:search_contains.span()[0]] + search_name + content[search_contains.span()[1]:]
                else:
                    break
            else:
                content = str(content)
                break
        print("content:::----",content)
        return content

    def __get_params_type(self, param):
        '''
        获取参数类型
        :param param:
        :return:
        '''
        print("__get_params_type---",param)

        if re.match(r"^'$", param):
            param = param.strip("'")
        elif re.match(r'^"$', param):
            param = param.strip('"')
        elif re.search(r'(^\${\w+}?$)', param):
            param = self.__get_variables(param)
        else:
            try:
                param = eval(param)
            except:
                param = param
        print("param:::--=-=-=",param)
        return param

    def __get_parms(self, parms):
        '''
        获取参数,传参非（）形式
        :param parms:
        :return:
        '''
        print("__get_parms---",parms)

        parms = parms.strip()
        if re.match('^\(.*\)$', parms):
            params = []
            pattern_content = re.compile(r'(".*?")|(\'.*?\')|,| ')
            find_content = re.split(pattern_content, parms[1:-1])
            find_content = [x.strip() for x in find_content if x]
            for param in find_content:
                var_content = self.__get_params_type(param)
                params.append(var_content)
            print("params__get_parms:",params)
            return params
        else:
            raise SyntaxError(parms)

    def __get_parm(self, content):
        '''
        获取参数,传参非（）形式
        :param params_str:
        :return:
        '''
        print("__get_parm---",content)

        pattern_content = re.compile(r'(\'.*?\'|".*?"|\S+)')
        content_split = re.findall(pattern_content, content)
        contents = []
        for c in content_split:
            var_content = self.__get_params_type(c)
            contents.append(var_content)
        print("params-contents",contents)
        return contents

    def __analysis_exist_parms_keywords(self, step):
        print("__analysis_exist_parms_keywords:",step)# check('com.dedao.juvenile:id/itemTitle', 1)
        key = step.split('(', 1)[0].strip()
        print("key:::__analysis_exist_parms_keywords:",key)# check
        parms = self.__get_parms(step.lstrip(key))
        print("parms:::__analysis_exist_parms_keywords:",parms)# com.dedao.juvenile:id/itemTitle

        action_data = Dict({
            'key': key,
            'parms': parms,
            'step': step
        })
        print('action_data::-----',action_data)
        #{'key': 'check', 'parms': ['com.dedao.juvenile:id/itemTitle', 1], 'step': "check('com.dedao.juvenile:id/itemTitle', 1)"}

        #action_data::----- {'key': 'click', 'parms': ['xpath', "//*[@resource-id='com.dedao.juvenile:id/notificationBtn']"], 'step': 'click("xpath","//*[@resource-id=\'com.dedao.juvenile:id/notificationBtn\']")'}
        return action_data

    def __analysis_not_exist_parms_keywords(self, step):
        print("__analysis_not_exist_parms_keywords---",step)

        key = step
        parms = None
        action_data = Dict({
            'key': key,
            'parms': parms,
            'step': step
        })
        print("action_data====",action_data)
        return action_data

    def __analysis_setVar_keywords(self, step):
        print("__analysis_setVar_keywords---",step)

        key = '$.setVar'
        parms = self.__get_parms(step.lstrip('$.setVar'))
        if len(parms) != 2:
            raise SyntaxError(f'"{step}" Missing required parameter key or value!')
        if not isinstance(parms[0], str):
            raise TypeError(f'"{step}" Key must be str, not {type(parms[0])}')
        action_data = Dict({
            'key': key,
            'parms': parms,
            'tag': 'setVar',
            'step': step
        })
        print("====---action_data",action_data)
        return action_data

    def __analysis_variable_keywords(self, step):
        print("__analysis_variable_keywords---",step)
        step_split = step.split('=', 1)
        print("step_split====",step_split)
        if len(step_split) != 2:
            raise SyntaxError(f'"{step}"')
        elif not step_split[-1].strip():
            raise SyntaxError(f'"{step}"')
        name =  step_split[0].strip()[2:-1]
        var_value = step_split[-1].strip()

        if re.match(r'\$\.(\w)+\(.*\)', var_value):
            key = var_value.split('(', 1)[0]
            print("key----",key)
            if key == '$.id':
                parms = self.__get_replace_string(var_value.split(key, 1)[-1][1:-1])
            else:
                parms = self.__get_parms(var_value.split(key, 1)[-1])
            print("parms----",parms)
        elif re.match(r'(\w)+\(.*\)', var_value):
            key =  var_value.split('(', 1)[0]
            print("key----0000000",key)
            parms = self.__get_replace_string(var_value.split(key, 1)[-1][1:-1])
            print("parms---0000-",parms)

        else:
            key = None
            parms = self.__get_parm(var_value)
            print("parms-99---",parms)

        action_data = Dict({
            'key': key,
            'parms': parms,
            'name': name,
            'tag': 'getVar',
            'step': step
        })
        return action_data

    def __analysis_common_keywords(self, step, style):
        print("__analysis_common_keywords",step,"style:",style)

        key = step.split('call', 1)[-1].strip().split('(', 1)[0].strip()
        parms = step.split('call', 1)[-1].strip().split(key, 1)[-1]
        parms = self.__get_parms(parms)
        action_data = Dict({
            'key': key,
            'parms': parms,
            'tag': 'call',
            'style': style,
            'step': step
        })
        print("action_data0-0-0-0-",action_data)
        return action_data

    def __analysis_other_keywords(self, step):
        print("__analysis_other_keywords",step)
        key = step.split(' ', 1)[0].strip()
        parms = self.__get_replace_string(step.lstrip(key).strip())
        action_data = Dict({
            'key': key,
            'parms': parms,
            'tag': 'other',
            'step': f'{key} {parms}'
        })
        print("action_data0-0-0-09090-__analysis_other_keywords:",action_data)

        return action_data

    def __match_keywords(self, step, style):
        print("__match_keywords",step,'style:::',style)#step: check('com.dedao.juvenile:id/itemTitle', 1)
        if re.match(' ', step):
            raise SyntaxError(f'"{step}"')
        step = step.strip()

        if re.match(r'\w+\((.*)\)', step):
            return self.__analysis_exist_parms_keywords(step)
        elif re.match(r'^\w+$', step):
            return self.__analysis_not_exist_parms_keywords(step)
        elif re.match(r'\$\{\w+\}=|\$\{\w+\} =', step):
            return self.__analysis_variable_keywords(step)
        elif re.match(r'\$\.setVar\(.*\)', step):
            return self.__analysis_setVar_keywords(step)
        elif re.match(r'call \w+\(.*\)', step):
            return self.__analysis_common_keywords(step, style)
        elif re.match(r'if |elif |else |while |assert .+', step):

            return self.__analysis_other_keywords(step)
        else:
            raise SyntaxError(f'"{step}"')

    @keywords
    def executor_keywords(self, action, style):
        print("action_analysis----executor_keywords",action,'style:::',style)
        #action:{'key': 'click', 'parms': ['id', 'notificationBtn'], 'step': "click('id','notificationBtn')"}

        try:
            if action.tag in ['setVar', 'getVar', 'call', 'other']:
                result = self.action_executor.action_executor(action)
            elif action.key in Var.default_keywords_data.keywords:
                result = self.action_executor.action_executor(action)
            elif action.key in Var.new_keywords_data:
                action.parms = self.__join_value(action.parms, ', ')
                result = self.action_executor.new_action_executor(action)
            else:
                raise KeyError('The {} keyword is undefined!'.format(action.key))

            if action.tag == 'getVar':
                self.variables[action.name] = result
                return result
            else:
                return result
        except Exception as e:
            raise e

    def action_analysis(self, step, style, common):
        log_info('action_analysis::::{}'.format(step))
        self.common_var = common
        action_dict = self.__match_keywords(step, style)
        log_info('action_analysis::::==={}'.format(action_dict))
        log_info('action_analysis::::===9999{}'.format(self.common_var))


        result = self.executor_keywords(action_dict, style)
        print("result::::action_analysis",result)
        return result

if __name__ == '__main__':
    action = ActionAnalysis()


