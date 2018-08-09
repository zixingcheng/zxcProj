#-*- coding: utf-8 -*-
"""
Created on  张斌 2018-06-25 10:58:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com

    机器人-基础功能对象 
"""
import sys, os, time, mySystem
from datetime import datetime, timedelta

#引用根目录类文件夹--必须，否则非本地目录起动时无法找到自定义类
mySystem.Append_Us("../Prjs", False, __file__)
mySystem.Append_Us("", False) 
import myData, myEnum
myDoType = myEnum.enum_index('Cmd')  # 命令类型枚举


#机器人基类
class myRobot():
    def __init__(self, usrName = "", usrID = ""):
        # 功能信息
        self.doType = myDoType.Cmd  #类型   
        self.doTitle = "Robot"      #说明 
        self.doCmd = "@@myRobot"    #启动命令 
        self.usrName = usrName      #功能所属用户名称
        self.usrID = usrID          #功能所属用户ID
        self.strText_L = ""         #命令信息（缓存上次） 
        self.Init()                 #初始基础信息
    def Init(self): 
        self.isEnable = True            #是否可用
        self.isValid = True             #合法性 
        self.isOpened = False           #是否启用
        self.isSingleUse = True         #是否为单例使用(非单例时每个用户专属) 
        self.tStart = datetime.now()
        self.tNow = datetime.now()
        self.tLast = datetime.now()

        # 基础信息--必须设置，自动提取作为配置信息
        self.prjName = "消息处理功能"   #功能名
        self.fileName = "myRobot"       #文件名
        self.className = "myRobot"      #类名
        self.isNoReply = True           #是否无回复操作--功能自带    
        
        # 初始返回消息
        self.msg = {}              
        self.msg['FromUserName'] = "" 
        self.msg['Type'] = "TEXT" 
        self.msg['Text'] = ""         
        self.maxTime = 60 * 6       #有效时常

    #消息处理接口
    def Done(self, Text, msgID = "", isGroup = False, idGroup = ""):
        #检查
        if(self._Check() == False): 
            return None

        #消息处理  
        strReturn = None
        if(Text == self.doCmd):
            strReturn = self.doTitle + "功能" + self._Title()
        else:
            if(self.isOpened):
                strReturn = self._Done(Text, msgID, isGroup, idGroup)
        
        #创建返回消息
        return self._Return(strReturn)
        
    #合法性(时效)
    def _Check(self):
        if(self.isEnable == False or self.isValid == False):
            return False
        
        #时效
        self.tNow = datetime.now()
        if((self.tNow - self.tLast).total_seconds() > self.maxTime):
            self.isValid = False
            return self.isValid
        
        self.tLast = self.tNow    
        return True
    #消息处理--继承类重写，实现处理逻辑功能
    def _Done(self, Text, msgID = "", isGroup = False, idGroup = ""):
        self.strText_L = Text 
        return Text
    #创建返回消息
    def _Return(self, Text):
        self.msg['Text'] = Text  
        return self.msg

    #开关提示信息
    def _Title(self):
        if(self.isOpened):
            self.isOpened = False
            self.isValid = False
            return "--已关闭\n\t" + self._Title_User_Closed() + "(" + str(self.tStart) + ")"
        else:
            self.isOpened = True
            return "--已开启\n\t" + self._Title_User_Opened() + "(" + str(self.tStart) + ")"
    def _Title_User_Opened(self): 
            return ""
    def _Title_User_Closed(self): 
            return ""
        

#主启动程序
if __name__ == "__main__":
    pR = myRobot();

    time.sleep (0)
    print(pR.Done("Hello")["Text"])
    print(pR.Done("@@myRobot")["Text"])
    print(pR.Done("myRobot")["Text"])
    print(pR.Done("@@myRobot")["Text"])

    
