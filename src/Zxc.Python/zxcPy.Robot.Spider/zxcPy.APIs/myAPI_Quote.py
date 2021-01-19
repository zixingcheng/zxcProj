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
mySystem.Append_Us("../zxcPy.Setting", False, __file__)
mySystem.Append_Us("../zxcPy.Quotation", False, __file__)
mySystem.Append_Us("../zxcPy.Quotation/Quote_Data", False, __file__)
mySystem.Append_Us("../zxcPy.Quotation/Quote_Source", False, __file__)
mySystem.Append_Us("../zxcPy.Quotation/Quote_Listener", False, __file__)
mySystem.Append_Us("", False)    
import myWeb, myDebug, myData, myData_Trans, myData_Json, mySource_Control, mySpider_Setting
from myGlobal import gol   
quoteSource = gol._Get_Value('quoteSource')     #实例 行情对象
setsSpider = gol._Get_Value('setsSpider')       #实例 爬虫设置



#API-行情设置
class myAPI_Quote_Set(myWeb.myAPI): 
    def get(self):
        #提取爬虫设置信息 
        #{'spiderTitle': "ceshi2", 'spiderTag': 'webPage', 'spiderUrl': "", "spiderRule": "", 'isValid':'False', 'isDel':'True', 'mark':'测试设置' }
        #{'spiderTitle': "sh000001", 'spiderTag': 'quote', 'spiderUrl': "", "spiderRule": "", 'isValid':'True', 'isDel':'False', 'mark':'测试设置' }
        params = request.args.get('setInfo', "{}")
        setInfo = myData_Trans.Tran_ToDict(params)
        bRemove = myData_Trans.To_Bool(setInfo.get('isDel', "False"))

        if(bRemove):
            bRes = setsSpider._Remove(setInfo['spiderTitle'])
        else:
            bRes = setsSpider._Edit(setInfo)
            
        pMsg = copy.deepcopy(gol._Get_Setting('Return_strFormat', {}))
        if(bRes):
            pMsg['result'] = True
        return myData_Json.Trans_ToJson_str(pMsg)
    
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
    

#API-行情查询
class myAPI_Quote_Query(myWeb.myAPI):
    def get(self):
        # queryIDs=sh000001,sh601939
        global quoteSource
        ids = request.args.get('queryIDs', "")
        lstReturn = quoteSource.query(parms = {'queryIDs' : ids})

        pMsg = copy.deepcopy(gol._Get_Setting('Return_strFormat', {}))
        if(lstReturn != None and len(lstReturn) > 1):
            datas = []
            for x in lstReturn:
                datas.append(x.toDict())
            pMsg['datas'] = datas
            pMsg['result'] = True
        return myData_Json.Trans_ToJson_str(pMsg)



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



#集中添加所有API
def add_APIs(pWeb):  
    #初始行情对象
    #init_Quote()
    
    # 创建Web API
    pWeb.add_API(myAPI_Quote_Set, '/zxcAPI/robot/stock/QuoteSet')
    pWeb.add_API(myAPI_Quote_SetQuery, '/zxcAPI/robot/stock/QuoteSet/Query')

    pWeb.add_API(myAPI_Quote_Query, '/zxcAPI/robot/stock/Query')


    #pWeb.add_API(myAPI_Quote_SetQuery, '/zxcAPI/robot/stock/QuoteSet/Query')
    #pWeb.add_API(myAPI_Quote_SetInfoQuery, '/zxcAPI/robot/stock/QuoteSetInfo/Query')
    
    #pWeb.add_API(myAPI_Quote_Set_Risk, '/zxcAPI/robot/stock/QuoteSetRisk')
    #pWeb.add_API(myAPI_Quote_SetQuery_Risk, '/zxcAPI/robot/stock/QuoteSetRisk/Query')

    

#行数监测线程 
#def thrd_Moniter_API_Quote():
#    time.sleep(10)                  #延时等待
#    pSource = init_Quote()
#    while(pSource.isClosed == False):
#        myDebug.Debug(myData_Trans.Tran_ToDatetime_str())
#        time.sleep(120)             #延时等待
#        myQuote_Source.mainStart()  #检查启动行情进程

#启动监测线程
#m_thrdAPI_Quote = threading.Thread(target = thrd_Moniter_API_Quote)
#m_thrdAPI_Quote.start()



#主程序启动
if __name__ == '__main__':  
    #初始行情对象
    #init_Quote()

    #注册平台, 取token
    #pQuote_Set = myAPI_Quote_Set()
    #msg = pQuote_Set.get()
    #print("msg::", msg)
    print()
    