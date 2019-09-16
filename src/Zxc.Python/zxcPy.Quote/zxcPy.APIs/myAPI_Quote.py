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
import myWeb, myDebug, myData_Trans, myData_Json, myQuote_Source, myQuote_Setting
from myGlobal import gol   



#API-行情设置
class myAPI_Quote_Set(myWeb.myAPI): 
    def get(self):
        #提取股票信息
        extype=request.args.get('extype', "")
        code_id=request.args.get('code_id', "")
        code_name=request.args.get('code_name', "") 
        removeSet=myData_Trans.To_Bool(request.args.get('removeSet', ''))
        
        pMsg = copy.deepcopy(gol._Get_Setting('Return_strFormat', {}))
        pStocks = gol._Get_Value('setsStock', None)
        lstStock = pStocks._Find(code_id, "", exType=extype)
        if(len(lstStock) != 1):
            pMsg['text'] =  "股票代码或名称错误！" 
            return pMsg
        pStock = lstStock[0]
        strTag = "股票设置："+ pStock.code_name +"\n      "

        #解析参数
        bResult = False 
        if(bResult == False):
            #提取行情对象
            pSource = gol._Get_Value('quoteSource', None) 
            pSets = gol._Get_Value('setsQuote', None) 
            if(pSource != None and pSets != None):
                if(removeSet == False):
                    editInfo = myData_Trans.Tran_ToDict(request.args.get('editInfo', "{}"))
                    
                    # 特殊同步
                    usrIDs = list(editInfo.get("msgUsers",{}).keys())
                    if("茶叶一主号" in usrIDs or "老婆" in usrIDs):
                        usrPlat = request.args.get('usrPlat', 'wx')
                        editInfo['msgUsers']['茶叶一主号'] = usrPlat
                        editInfo['msgUsers']['老婆'] = usrPlat

                    if(pSets._Edit(pStock.extype, pStock.code_id, "", editInfo)):
                        pSource.params = pSource._getDefault_Param()
                        pMsg['text'] = strTag + " --设置已成功修改。" 
                        bResult = True
                        print(pSource.params)
                else:
                    usrID = request.args.get('usrID', '') 
                    usrPlat = request.args.get('usrPlat', 'wx')
                    if(pSets._Remove(pStock.extype, pStock.code_id, "", usrID)):
                        # 特殊同步
                        if(usrID == '茶叶一主号'): pSets._Remove(pStock.extype, pStock.code_id, "", '老婆')
                        if(usrID == '老婆'): pSets._Remove(pStock.extype, pStock.code_id, "", '茶叶一主号')

                        pSource.params = pSource._getDefault_Param()
                        pMsg['text'] = strTag + " --设置已成功移除。" 
                        bResult = True
                        print(pSource.params) 
        pMsg['result'] = bResult 
        if(bResult == ""):  pMsg['text'] =  strTag + "操作失败！"
        return pMsg

#API-行情设置查询
class myAPI_Quote_SetQuery(myWeb.myAPI):
    def get(self):
        usrID=request.args.get('usrID', "")
        pMsg = copy.deepcopy(gol._Get_Setting('Return_strFormat', {}))
        
        #初始返回组
        lstExtypes = []
        lstCode_id = []
        lstCode_Name = []
        lstCode_NameEN = []

        #查询及组装
        pSets = gol._Get_Value('setsQuote', None)
        if(pSets != None and usrID != ""):
            lstStock = pSets._Find_Sets(usrID)
            for x in lstStock:
                lstExtypes.append(x.extype)
                lstCode_id.append(x.code_id)
                lstCode_Name.append(x.code_name)
                lstCode_NameEN.append(x.code_name_En)
    
        jsonStocks = {}
        jsonStocks["extypes"] = lstExtypes
        jsonStocks["code_ids"] = lstCode_id
        jsonStocks["code_names"] = lstCode_Name
        jsonStocks["code_namesEN"] = lstCode_NameEN

        pMsg['result'] = len(lstExtypes) > 0
        pMsg['text'] = jsonStocks
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
    pWeb.add_API(myAPI_Quote_SetQuery, '/zxcAPI/robot/stock/QuoteSet/Query')
    

    
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
    