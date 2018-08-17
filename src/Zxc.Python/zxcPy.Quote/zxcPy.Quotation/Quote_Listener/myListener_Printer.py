#-*- coding: utf-8 -*-
"""
Created on  张斌 2018-05-03 14:58:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com

    监听--类 -直接输出 
"""
import sys, os, mySystem 

#引用根目录类文件夹--必须，否则非本地目录起动时无法找到自定义类
mySystem.m_strFloders.append('/zxcPy.Quotation')
mySystem.Append_Us("", False)    
import myDebug, myQuote_Data, myQuote_Listener  
    

#行情监听--直接输出
class Quote_Listener_Printer(myQuote_Listener.Quote_Listener):
    def __init__(self):
        myQuote_Listener.Quote_Listener.__init__(self, 'Printer')

    #处理接收信息
    def OnRecvQuote(self, quoteDatas): 
        #输出统计信息
        pData = quoteDatas.datas_CKDs_M.data
        pCKD = quoteDatas.datas_CKDs_M.CKD
        myDebug.Debug(pData.name, "Price: ",pData.lastPrice, "Price_A: ", round(pCKD.Price,4),  "Valume: ", pCKD.Valume)

        #输出数据信息
        pData.Print()

