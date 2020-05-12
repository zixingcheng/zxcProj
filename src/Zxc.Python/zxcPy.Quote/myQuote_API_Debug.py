 # -*- coding: utf-8 -*-
"""
Created on  张斌 2018-05-03 14:58:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com

    Debug Linux调试用，监测运行该文件时为Debug
"""
import os, time
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
       
    #死循环阻塞
    while(True):
        time.sleep(10)
    exit(0)