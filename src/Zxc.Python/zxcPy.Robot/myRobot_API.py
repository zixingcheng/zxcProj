# -*- coding: utf-8 -*-
"""
Created on  张斌 2018-08-12 23:58:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com

    Rest API --myRobot 操作
"""
import os, copy  
import mySystem 
    
#引用根目录类文件夹--必须，否则非本地目录起动时无法找到自定义类
mySystem.Append_Us("/zxcPy.APIs", False, __file__)
mySystem.Append_Us("", False)    
import myWeb
from myGlobal import gol 



#主程序启动
if __name__ == '__main__': 
    gol._Init()             #先必须在主模块初始化（只在Main模块需要一次即可）
    #gol._Set_Setting("CanPrint", False)
    import myAPI_Robot      #回重启导致多次输出信息，调整为不输出打印信息
    
    # 创建新线程
    pWeb = myWeb.myWeb("127.0.0.1", 8668)
    pWeb.add_API(myWeb.myAPI, '/test')

    # 添加Robot接口并启动API
    myAPI_Robot.add_APIs(pWeb)
    pWeb.run()
    