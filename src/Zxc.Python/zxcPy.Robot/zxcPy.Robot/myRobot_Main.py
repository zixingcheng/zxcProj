# -*- coding: utf-8 -*-
"""
Created on  张斌 2018-08-12 23:58:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com

    Rest API --myRobot 操作  主程序，消息队列方式传递消息进行处理
"""
import os, copy  
import mySystem 
    
#引用根目录类文件夹--必须，否则非本地目录起动时无法找到自定义类
mySystem.Append_Us("../zxcPy.APIs", False, __file__)
mySystem.Append_Us("../zxcPy.Robot", False, __file__)
mySystem.Append_Us("../zxcPy.Robot/Prjs", False, __file__)
mySystem.Append_Us("../zxcPy.Robot/Reply", False, __file__)
mySystem.Append_Us("../zxcPy.Robot/Roots", False, __file__)
mySystem.Append_Us("", False)    
import myDebug, myMQ_Rabbit
from myGlobal import gol 


#
class myRobot_Main:
    #初始构造 
    def __init__(self, isSender = False, Host = "http://127.0.0.1", usrName = 'guest', usrPwd = 'guest'):
        self.isSender = isSender    #是否为生产者
        self.Host = Host            #指定远程RabbitMQ的地址
        self.usrName = usrName      #远程RabbitMQ的用户名
        self.usrPwd = usrPwd        #远程RabbitMQ的用户密码
        self.callback_RecvMsg = None#消息接收回调函数
        self.Init()                 #初始MQ

    #初始运行
    def Run(self):
        #认证信息


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
    