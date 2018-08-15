#-*- coding: utf-8 -*-
"""
Created on  张斌 2018-07-04 15:58:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com
    
    机器人（功能库）  --复读机(回复相同消息)
"""
import sys, os, time ,mySystem

#引用根目录类文件夹--必须，否则非本地目录起动时无法找到自定义类
mySystem.Append_Us("", False) 
import myRobot

    
#机器人类--复读机(回复相同消息)
class myRobot_Repeater(myRobot.myRobot):
    def __init__(self, usrName, usrID):
        super().__init__(usrName, usrID)
        self.doTitle = "复读机"     #说明 
        self.prjName = "复读机"     #功能名
        self.doCmd = "@@Repeater"   #启动命令 

    #消息处理接口
    def _Done(self, Text, msgID = "", isGroup = False, idGroup = "", usrID = "", usrName = ""):
        #复读机(回复相同消息)
        if(isGroup):
            return "@" + usrName + " " + Text 
        else:
            return Text 
    def _Title_User_Opened(self): 
        return "发送任何消息均同声回复..."
        

#主启动程序
if __name__ == "__main__":
    pR = myRobot_Repeater("zxc", "zxcID");
    pR.Done("@@Repeater")["msg"]
    print(pR.Done("Hello")["msg"])
    pR.Done("@@Repeater")["msg"]
    print()
    
    time.sleep (1)
    pR.Done("@@Repeater")["msg"]
    pR.Done("@@Repeater")["msg"]
    print()

    time.sleep (2)
    print(pR.Done("Hello"))

    pR = myRobot_Repeater("zxc", "zxcID");
    print(pR.Done("@@zxcWeixin"))
    print(pR.Done("Hello"))
    print(pR.Done("@@zxcWeixin"))

    
