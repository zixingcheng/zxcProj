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
import myQuote_Data

        
#行情监听
class Quote_Listener:
    def __init__(self, name):
        self.name = name
    def getName(self):
        return self.name  
    def OnRecvQuote(self, quoteData):pass 

    

#主启动程序
if __name__ == "__main__":
    import myListener_Printer
    pListener = myListener_Printer.Quote_Listener_Printer()

    pListener.OnRecvQuote(myQuote_Data.Quote_Data())
