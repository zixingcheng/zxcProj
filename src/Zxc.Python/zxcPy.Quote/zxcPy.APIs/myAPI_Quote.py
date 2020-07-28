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
mySystem.Append_Us("../zxcPy.Quotation/Quote_Data/Data_Risk", False, __file__)
mySystem.Append_Us("../zxcPy.Quotation/Quote_Source", False, __file__)
mySystem.Append_Us("../zxcPy.Quotation/Quote_Listener", False, __file__)
mySystem.Append_Us("", False)    
import myWeb, myDebug, myData, myData_Trans, myData_Json, myQuote_Source, myQuote_Setting, myData_StockRisk
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
                    if(pSets._Edit(pStock.extype, pStock.code_id, pStock.code_name, editInfo)):
                        pSource.params = pSource._getDefault_Param()
                        pMsg['text'] = strTag + " --设置已成功修改。" 
                        bResult = True
                        print(pSource.params)
                else:
                    usrID = request.args.get('usrID', '') 
                    usrPlat = request.args.get('usrPlat', 'wx')
                    if(pSets._Remove(pStock.extype, pStock.code_id, pStock.code_name, usrID)):
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
    
#API-行情设置详情查询
class myAPI_Quote_SetInfoQuery(myWeb.myAPI):
    def get(self):
        exType=request.args.get('exType', "")
        stockID=request.args.get('stockID', "")
        stockName=request.args.get('stockName', "")
        usrID=request.args.get('usrID', "")
        pMsg = copy.deepcopy(gol._Get_Setting('Return_strFormat', {}))
        
        #初始返回组
        jsonInfo = {}
        pSets = gol._Get_Value('setsQuote', None)
        pSet = pSets._Find(stockName, exType + '.' + stockID)
        if(pSet != None):
            pMsg['result'] = True
            pParams = {}
            for xx in pSet.settings:
                pSetting = pSet.settings[xx]
                pParams[xx] = pSetting.IsValid(usrID)
            jsonInfo["设置状态"] = pParams
        else:
            pMsg['result'] = False
        pMsg['text'] = jsonInfo
        return pMsg
    
#API-行情设置-风控
class myAPI_Quote_Set_Risk(myWeb.myAPI):
    def get(self):
        #提取股票信息
        pMsg = copy.deepcopy(gol._Get_Setting('Return_strFormat', {}))
        pRisks = gol._Get_Value('zxcRisk_Control', None)
        bResult = True
        
        # 组装参数并添加
        #dicParam = {"边界限制": True,"定量监测": False, "监测间隔": 0.01,"止盈线": 0.20, "止损线": -0.05, "动态止盈": True, "动态止损": True, "止盈回撤": 0.01, "止盈比例": 0.20, "止损回撤": 0.01, "止损比例": 0.20 }
        usrID = request.args.get('usrID', '') 
        usrTag = request.args.get('usrTag', '') 
        code_id = request.args.get('code_id', "")
        code_name = request.args.get('code_name', "") 
        removeSet = myData_Trans.To_Bool(request.args.get('removeSet', False))
        paramInfo = myData_Trans.Tran_ToDict(request.args.get('setInfo', "{}"))
        paramInfo['removeSet'] = removeSet

        dtTrade = request.args.get('time', "")
        dateTag = request.args.get('dateTag', "")
        stockPrice = myData_Trans.To_Float(str(request.args.get('stockPrice', 0)))
        stockNum = myData_Trans.To_Int(str(request.args.get('stockNum', 0)))
        if(removeSet == False and (stockPrice == 0 or stockNum == 0)): 
            bResult = False; pMsg['text'] = "股价、数量不能为0."
        if(usrID == "" and usrTag == ""): 
            bResult = False; pMsg['text'] = "用户信息不能为空."
        if(bResult):
            strR = pRisks.addRiskSet(usrID, usrTag, code_id, code_name, stockPrice, stockNum, dtTrade, dateTag, paramInfo)
        
        #解析参数
        strTag = "风控设置："+ code_name +"\n"
        if(bResult):
            if(removeSet == False):
                if(stockPrice == 0 or stockNum == 0): 
                    pMsg['text'] = strTag + " --已成功修改参数信息." 
                else:
                    trade = myData.iif(stockNum >0, "买入", "卖出")
                    if(stockNum % 100 == 0):
                        pMsg['text'] = strTag + F"新增{trade}：{str(abs(stockNum))} 股.\n{trade}均价：{stockPrice} 元/股)." 
                    else:
                        pMsg['text'] = strTag + F"新增{trade}：{str(abs(stockNum))} 张.\n{trade}均价：{stockPrice} 元/张." 
                bResult = True
            else:
                pMsg['text'] = strTag + " --设置已成功移除." 
                bResult = True
        pMsg['result'] = bResult 
        if(bResult == ""):  pMsg['text'] =  strTag + "操作失败！"
        return pMsg
    
#API-行情设置-风控
class myAPI_Quote_SetQuery_Risk(myWeb.myAPI):
    def get(self):
        pMsg = copy.deepcopy(gol._Get_Setting('Return_strFormat', {}))
        usrID = request.args.get('usrID', '') 
        usrTag = request.args.get('usrTag', '') 
        code_id = request.args.get('code_id', "")
        code_name = request.args.get('code_name', "")
        
        #初始返回组
        lstDate_Tag = []
        lstInfos = {}

        #查询及组装
        pRisks = gol._Get_Value('zxcRisk_Control', None)
        dictRisks = pRisks.getRisks(usrID, usrTag, code_id, code_name, bCheck = True)
        if(dictRisks != None):
            for x in dictRisks:
                pRisk = dictRisks[x]
                if(pRisk.setRisk.valid):
                    lstDate_Tag.append(x)
                    dictSet = pRisk.setRisk.Trans_ToDict().copy()
                    dictSet['操作时间'] = myData_Trans.Tran_ToDatetime_str(dictSet['操作时间'], "%Y-%m-%d %H:%M:%S")
                    lstInfos[x] = dictSet
         
        jsonSetinfo = {}
        jsonSetinfo["dataTags"] = lstDate_Tag
        jsonSetinfo["setInfos"] = lstInfos

        pMsg['result'] = len(lstDate_Tag) > 0
        pMsg['text'] = jsonSetinfo
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
    pWeb.add_API(myAPI_Quote_SetInfoQuery, '/zxcAPI/robot/stock/QuoteSetInfo/Query')
    
    pWeb.add_API(myAPI_Quote_Set_Risk, '/zxcAPI/robot/stock/QuoteSetRisk')
    pWeb.add_API(myAPI_Quote_SetQuery_Risk, '/zxcAPI/robot/stock/QuoteSetRisk/Query')

    
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
    