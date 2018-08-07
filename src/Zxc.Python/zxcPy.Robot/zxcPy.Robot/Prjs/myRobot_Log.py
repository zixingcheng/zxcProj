#-*- coding: utf-8 -*-
"""
Created on  张斌 2017-11-17 15:16:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com

    Weixin网页版消息处理接口（功能库）--机器人类--日志
"""
import sys, os, time ,mySystem

#引用根目录类文件夹--必须，否则非本地目录起动时无法找到自定义类 
mySystem.Append_Us("", False) 
import myRobot
from myGlobal import gol   

    
#机器人类--聊天机器人
class myRobot_Robot(myRobot.myRobot):
    def __init__(self, usrName, usrID):
        super().__init__(usrName, usrID)
        self.doTitle = "Robot_Log"     #说明 
        self.prjName = "Robot_Log"     #功能名
        self.doCmd = "@@zxcRobot_Log"  #启动命令 
        self
        
    #消息处理接口
    def _Done(self, Text, isGroup = False, idGroup = ""): 
        #聊天机器人(接入第三方接口进行处理)
        strText = Text + "--by zxcChatRobot"
        self.usrName

        return strText 

    def _Title_User_Opened(self): 
        return "开启Robot Log..." 
        

#主启动程序
if __name__ == "__main__":
    pR = myRobot_Robot("zxc", "zxcID");
    pp = pR.Done("@@zxcRobot_Log")
    print(pp)
    print(pR.Done("Hello"))
    print(pR.Done("@@zxcRobot_Log"))

    time.sleep (2)
    pp = pR.Done("Hello")
    print(pp)

    
