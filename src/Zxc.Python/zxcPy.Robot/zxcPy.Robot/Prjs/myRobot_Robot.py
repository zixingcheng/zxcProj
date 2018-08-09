#-*- coding: utf-8 -*-
"""
Created on  张斌 2017-11-17 15:16:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com

    Weixin网页版消息处理接口（功能库）--机器人类--聊天机器人
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
        self.doTitle = "聊天机器人"     #说明 
        self.prjName = "聊天机器人"     #功能名
        self.doCmd = "@@ChatRobot"      #启动命令 
        
    #消息处理接口
    def _Done(self, Text, msgID = "", isGroup = False, idGroup = ""):  
        #聊天机器人(接入第三方接口进行处理)
        strText = Text + "--by zxcChatRobot"
        return strText 

    def _Title_User_Opened(self): 
        return "开启聊天Robot..." 
        

#主启动程序
if __name__ == "__main__":
    pR = myRobot_Robot("zxc", "zxcID");
    pp = pR.Done("@@ChatRobot")
    print(pp)
    print(pR.Done("Hello"))
    print(pR.Done("@@ChatRobot"))

    time.sleep (2)
    pp = pR.Done("Hello")
    print(pp)

    
