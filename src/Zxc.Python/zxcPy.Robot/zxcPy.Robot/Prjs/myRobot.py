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

import myData, myEnum, myDebug, myManager_Msg
from myGlobal import gol 
myDoType = myEnum.enum_index('Cmd')  # 命令类型枚举


#机器人基类
class myRobot():
    def __init__(self, usrName = "", usrID = ""):
        # 功能信息
        self.doType = myDoType.Cmd  #类型   
        self.doTitle = "Robot"      #说明 
        self.doCmd = "@@myRobot"    #启动命令 
        self.usrName = usrName      #功能所属用户名称(启动者)
        self.usrID = usrID          #功能所属用户ID(启动者)
        self.strText_L = ""         #命令信息（缓存上次） 
        self._Init()                 #初始基础信息
    def _Init(self): 
        self.isEnable = True            #是否可用
        self.isRootUse = False          #是否为系统级使用(系统内置功能) 
        self.isSingleUse = True         #是否为单例使用(非单例时每个用户专属) 
        self.isBackUse = False          #是否为后台使用(后台可运行多个，一般为系统级功能，如日志) 
        self.isNoOwner = False          #是否为所有者除外不回复
        self.Init()                     #初始时间信息
        
        # 基础信息--必须设置，自动提取作为配置信息
        self.prjName = "消息处理功能"   #功能名
        self.fileName = "myRobot"       #文件名
        self.className = "myRobot"      #类名
        self.isNoReply = True           #是否无回复操作--功能自带    
        
        # 初始返回消息
        self.usrMMsg = gol._Get_Setting('manageMsgs')     #消息管理器
        self.msg = {}
        self.maxTime = 60 * 6       #有效时常 
    def Init(self): 
        self.isRunning = False          #是否启用中
        self.isValid = True             #合法性 
        self.tStart = datetime.now()
        self.tNow = datetime.now()
        self.tLast = datetime.now()

    #消息处理接口
    def Done(self, Text, msgID = "", isGroup = False, idGroup = "", usrID = "", usrName = "zxcRobot"):
        #消息处理  
        strReturn = None
        if(Text == self.doCmd):
            strReturn = self._Title(usrName, usrID)
        else:
            #检查
            if(self._Check()):  
                if(self.isNoOwner and self.usrName == usrName): return None     #开启者除外 
                strReturn = self._Done(Text, msgID, isGroup, idGroup, usrID, usrName)
            else:
                return None
        #创建返回消息
        return self._Return(usrID, usrName, strReturn, idGroup)
    #消息处理注册--需要主动注册
    def Done_Regist(self, Text, isGroup = False, idGroup = "", usrID = "", usrName = "", bRegistOut = False):   #消息处理  
        strReturn = None
        if(Text == self.doCmd):
            if(isGroup):
                strReturn = self._Title(usrName, usrID, True, bRegistOut)
            else:
                strReturn = self._Title("", "", True, bRegistOut)
        else: 
            return None
        #创建返回消息
        return self._Return(usrID, usrName, strReturn, "")
        
    #合法性(时效)
    def _Check(self):
        if(self.isRunning == False or self.isEnable == False or self.isValid == False):
            return False
        
        #时效
        self.tNow = datetime.now()
        if((self.tNow - self.tLast).total_seconds() > self.maxTime):
            self.isValid = False
            return self.isValid
        
        self.tLast = self.tNow    
        return True
    #消息处理--继承类重写，实现处理逻辑功能(可指定来源用户ID及名称)
    def _Done(self, Text, msgID = "", isGroup = False, idGroup = "", usrID = "", usrName = ""):
        self.strText_L = Text 
        return Text
    #创建返回消息
    def _Return(self, usrID, usrName, Text, idGroup):
        self.msg = self.usrMMsg.OnCreatMsg()
        self.msg['usrID'] = usrID
        self.msg['usrName'] = usrName
        self.msg['msg'] = Text  
        if(idGroup != ""):
            self.msg['groupID'] = idGroup  
        return self.msg
    #关闭功能
    def _Close(self):
        if(self._Check()):
            self.Done(self.doCmd)       #启动关闭命令

    #开关提示信息
    def _Title(self, usrName = "", usrID = "", bRegist = False, bRegistOut = False):
        if(self.isRunning):
            if(bRegist or bRegistOut):
                strReturn = myData.iif(usrName == "", "", "@" + usrName + "：")
                if(bRegistOut == False):
                    strReturn += self.doTitle + "功能" + "--已注册\n\t" + self._Title_User_Opened() + "(" + str(self.tStart) + ")"
                else:
                    strReturn += self.doTitle + "功能" + "--已注销\n\t" + self._Title_User_Opened() + "(" + str(self.tStart) + ")"
            else:
                self.isRunning = False      #标识非运行
                self.isValid = True         #有效性恢复
                strReturn = self.doTitle + "功能" + "--已关闭\n\t" + self._Title_User_Closed() + "(" + str(self.tStart) + ")"
        else:
            self.Init()                 #初始基础信息
            self.isRunning = True       #标识运行
            self.usrID = usrID          #功能所属用户ID(启动者)
            self.usrName = usrName      #功能所属用户名称(启动者)
            strReturn = self.doTitle + "功能" + "--已开启\n\t" + self._Title_User_Opened() + "(" + str(self.tStart) + ")"
        myDebug.Print(strReturn)
        return strReturn
    def _Title_User_Opened(self): 
            return ""
    def _Title_User_Closed(self): 
            return ""
        

#主启动程序
if __name__ == "__main__":
    pR = myRobot();

    time.sleep (0)
    print(pR.Done("Hello"))
    pR.Done("@@myRobot")["msg"]
    pR.Done_Regist("@@myRobot")["msg"]
    pR.Done_Regist("@@myRobot",False,'','','',True)["msg"]
    print(pR.Done("Test....")["msg"])
    print(pR.Done("Test2...."))
    pR.Done("@@myRobot")["msg"]
    print()

    pR.Done("@@myRobot")["msg"]
    pR.Done("@@myRobot")["msg"]
    print()

    
