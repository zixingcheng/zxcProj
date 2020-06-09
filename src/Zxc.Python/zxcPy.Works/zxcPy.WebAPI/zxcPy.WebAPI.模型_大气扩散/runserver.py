# -*- coding: utf-8 -*-
"""
Created on  张斌 2020-06-08 10:58:00 
    @author: zhang bin
    @email:  zhangbin@qq.com

    Rest Server --服务启动，单例
"""
from zxcPy_WebAPI import appWeb
from myGlobal import gol 
    

if __name__ == '__main__':
    # 单例运行检测
    # gol._Init()             #先必须在主模块初始化（只在Main模块需要一次即可）
    if(gol._Run_Lock(__file__) == False):
       exit(0)

    # 启动Web程序
    appWeb.run()

    # 退出
    gol._Run_UnLock(__file__)
    exit(0)
