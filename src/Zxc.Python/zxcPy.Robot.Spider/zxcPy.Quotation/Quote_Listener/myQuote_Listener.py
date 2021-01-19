#-*- coding: utf-8 -*-
"""
Created on  张斌 2018-05-03 14:58:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com

    监听--基类 
"""
import sys, os, mySystem 

#引用根目录类文件夹--必须，否则非本地目录起动时无法找到自定义类
mySystem.m_strFloders.append('/Quote_Listener')
mySystem.Append_Us("", False) 
import myData, myQuote_Data, myManager_Msg


        
#行情监听
class Quote_Listener:
    def __init__(self, name = "", nameAlias = ""):
        self.name = name
        self.nameAlias = nameAlias
        self.isValid = True
    def getName(self):
        return self.name  

    def OnRecvQuote(self, quoteDatas):pass 
    #创建消息内容
    def OnCreatMsgstr(self, quoteDatas):
        pass

    #功能是否可用
    def IsEnable(self):
        return self.isValid

