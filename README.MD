`fasttest` 在`macaca`、`appium`的基础上做了一层关键字的封装与解析，极大得简化了测试用例描述。我们有丰富的行为关键字，而且支持关键字模块级复用，自定义关键字等操作

![](https://img.shields.io/badge/python-3.7-green) 

## 运行示例
测试用例
```
    - click('标签页')
    - click('新建标签页')
    - input('URL', 'https://github.com/Jodeee')
    - sleep(3)
    - click('fasttest')
    - sleep(5)
```

结果报告

![image](https://cdn.nlark.com/yuque/0/2020/png/499819/1592730563272-b1519a95-e718-4166-8129-baa829408405.png?x-oss-process=image%2Fwatermark%2Ctype_d3F5LW1pY3JvaGVp%2Csize_20%2Ctext_am9kZWVl%2Ccolor_FFFFFF%2Cshadow_50%2Ct_80%2Cg_se%2Cx_10%2Cy_10)


## 框架介绍

[框架介绍](https://www.yuque.com/jodeee/kb/ywq037)

## 问题收集

[issues](https://github.com/Jodeee/fasttest/issues)


# 打包
```
建立setup.py

python3 setup.py bdist_egg

easy_install *.egg
```


# pip安装cd 

```
pip install git+http://gitlab.igetcool.com/qa/autoui_framework#egg=atf
```

# 参考

https://www.yuque.com/jodeee/kb/uie02g#77ZLs

https://testerhome.com/topics/24661

https://github.com/Jodeee/fasttestDemo 
 
https://www.yuque.com/jodeee/kb/ywq037

https://github.com/Jodeee/fasttest