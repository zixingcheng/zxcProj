#-*- coding: utf-8 -*-
"""
Created on  张斌 2017-11-17 15:16:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com

    Weixin网页版消息处理接口（功能库）
"""

import sys, os, time #, mySystem
from datetime import datetime, timedelta


#引用根目录类文件夹--必须，否则非本地目录起动时无法找到自定义类
#mySystem.m_strFloders.append('/myAPIs')
#mySystem.Append_Us("", True) 
#import myError, myData_Json #myDataSet, myData, myData_Trans 


#消息处理基类
class myWxDo():
    def __init__(self):
        self.usrType = ""           #类型   
        self.usrTag = ""            #标识  
        self.usrTitle = ""          #说明 
        self.usrName = ""           #用户名称(对方)
        self.strText_L = ""         #标识 
        
        self.msg = {}               #初始返回消息
        self.msg['FromUserName'] = "" 
        self.msg['Type'] = "TEXT" 
        self.msg['Text'] = "" 
        
        self.maxTime = 60 * 6       #有效时常
        self.Init()
    def Init(self): 
        self.isValid = True         #合法性 
        self.isOpened = False         
        
        self.tStart = datetime.now()
        self.tNow = datetime.now()
        self.tLast = datetime.now()

    #消息处理接口
    def Done(self, Text, isGroup = False, idGroup = ""):
        #检查
        if(self._Check() == False): 
            return None

        #消息处理  
        if(Text == self.usrTag):
            strReturn = self.usrTitle + "功能" + self._Title()
        else:
            strReturn = self._Done(Text)
        
        #创建返回消息
        return self._Create(strReturn)
        
    #合法性(时效)
    def _Check(self):
        if(self.isValid == False):
            return self.isValid
        
        #时效
        self.tNow = datetime.now()
        if((self.tNow - self.tLast).total_seconds() > self.maxTime):
            self.isValid = False
            return self.isValid
        
        self.tLast = self.tNow    
        return True
    #消息处理
    def _Done(self, Text):
        self.strText_L = Text 
        return ""
    #创建返回消息
    def _Create(self, Text):
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
    pR = myWxDo();

    time.sleep (0)
    pp = pR.Done("Hello")
    print(pp)

    
