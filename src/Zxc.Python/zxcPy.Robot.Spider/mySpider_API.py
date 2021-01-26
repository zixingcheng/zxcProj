 # -*- coding: utf-8 -*-
"""
Created on  张斌 2021-01-04 11:58:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com

    Rest API --Robot Spider API操作 
"""
import os  
import mySystem 

#引用根目录类文件夹--必须，否则非本地目录起动时无法找到自定义类
mySystem.Append_Us("/zxcPy.APIs", False, __file__)
mySystem.Append_Us("", False)    
import myWeb
from myGlobal import gol  



#主程序启动
if __name__ == '__main__': 
    gol._Init()             #先必须在主模块初始化（只在Main模块需要一次即可）
    #单例运行检测
    if(gol._Run_Lock(__file__) == False):
       exit(0)
       
    
    # 创建新线程
    import myAPI_Quote      #回重启导致多次输出信息，调整为不输出打印信息
    pWeb = myWeb.myWeb("0.0.0.0", 8667)
    pWeb.add_API(myWeb.myAPI, '/test')

    # 添加Robot接口并启动API
    myAPI_Quote.add_APIs(pWeb)
    pWeb.run()


    #退出
    gol._Run_UnLock(__file__)
    exit(0)