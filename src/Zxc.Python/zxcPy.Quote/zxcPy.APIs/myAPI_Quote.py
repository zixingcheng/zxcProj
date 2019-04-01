# -*- coding: utf-8 -*-
"""
Created on  张斌 2018-11-26 15:58:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com

    Rest API --行情操作
"""
import os, copy, ast, time, threading 
import mySystem 
from flask import jsonify, request, flash, render_template, redirect    #导入模块
    
#引用根目录类文件夹--必须，否则非本地目录起动时无法找到自定义类
mySystem.Append_Us("../zxcPy.APIs", False, __file__)
mySystem.Append_Us("../zxcPy.Quotation", False, __file__)
mySystem.Append_Us("../zxcPy.Quotation/Quote_Data", False, __file__)
mySystem.Append_Us("../zxcPy.Quotation/Quote_Source", False, __file__)
mySystem.Append_Us("../zxcPy.Quotation/Quote_Listener", False, __file__)
mySystem.Append_Us("", False)    
import myWeb, myDebug, myData_Trans, myQuote_Source, myQuote_Setting
from myGlobal import gol   



#API-行情设置
class myAPI_Quote_Set(myWeb.myAPI): 
    #strSet @股票 ** +/-
    def get(self):
        #提取股票信息
        extype=request.args.get('extype', "")
        code_id=request.args.get('code_id', "")
        code_name=request.args.get('code_name', "") 
        
        pMsg = copy.deepcopy(gol._Get_Setting('Return_strFormat', {}))
        pStocks = gol._Get_Value('setsStock', None)
        lstStock = pStocks._Find(code_id, "", exType=extype)
        if(len(lstStock) != 1):
            pMsg['text'] =  "股票代码或名称错误！" 
            return pMsg
        pStock = lstStock[0]
        strTag = "股票设置："+ pStock.code_name +"\n      "

        #解析参数
        editInfo = myData_Trans.Tran_ToDict(request.args.get('editInfo', "{}"))
        bResult = False 
        if(bResult == False):
            #提取行情对象
            pSource = gol._Get_Value('quoteSource', None) 
            pSets = gol._Get_Value('setsQuote', None) 
            if(pSource != None and pSets != None):
                if(pSets._Edit(pStock.extype, pStock.code_id, "", editInfo)):
                    pSource.params = pSource._getDefault_Param()
                    pMsg['text'] = strTag + " 设置已成功修改。" 
                    bResult = True
                    print(pSource.params)
        pMsg['result'] = bResult 
        if(bResult == ""):  pMsg['text'] =  strTag + "操作失败！"
        return pMsg
     
    
#初始行情对象
def init_Quote():     
    #全局对象提取
    myQuote_Source.mainStart()
    ms_Source = gol._Get_Value('quoteSource', None) 
    return ms_Source
#集中添加所有API
def add_APIs(pWeb):  
    #初始行情对象
    #init_Quote()
    
    # 创建Web API
    pWeb.add_API(myAPI_Quote_Set, '/zxcAPI/robot/stock/QuoteSet')
    

    
#行数监测线程 
def thrd_Moniter_API_Quote():
    time.sleep(10)                  #延时等待
    pSource = init_Quote()
    while(pSource.isClosed == False):
        myDebug.Debug(myData_Trans.Tran_ToDatetime_str())
        time.sleep(120)             #延时等待
        myQuote_Source.mainStart()  #检查启动行情进程

#启动监测线程
m_thrdAPI_Quote = threading.Thread(target = thrd_Moniter_API_Quote)
m_thrdAPI_Quote.start()



#主程序启动
if __name__ == '__main__':  
    #初始行情对象
    #init_Quote()

    #注册平台, 取token
    #pQuote_Set = myAPI_Quote_Set()
    #msg = pQuote_Set.get()
    #print("msg::", msg)
    print()
    