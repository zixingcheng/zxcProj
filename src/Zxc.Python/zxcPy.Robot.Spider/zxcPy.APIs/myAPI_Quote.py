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
import myWeb, myDebug, myData, myData_Trans, myData_Json
import myQuote, mySource_Control, mySpider_Setting
from myGlobal import gol   
stocksInfo = gol._Get_Value('setsStock', None)
quoteSource = gol._Get_Value('quoteSource')     #实例 行情对象
setsSpider = gol._Get_Value('setsSpider')       #实例 爬虫设置 
pSource = gol._Get_Value('quoteSource_API_JqData', None)



#API--股票模糊查询 
class myAPI_Stock_Query(myWeb.myAPI): 
    def get(self):
        #载入配置
        code_id=request.args.get('code_id', "")
        code_name=request.args.get('code_name', "") 
        lstStock = stocksInfo._Find(code_id, code_name)
        
        lstExtypes = []
        lstCode_id = []
        lstCode_Name = []
        lstCode_NameEN = []
        for x in lstStock:
            lstExtypes.append(x.extype)
            lstCode_id.append(x.code_id)
            lstCode_Name.append(x.code_name)
            lstCode_NameEN.append(x.code_name_En)
            
        jsonStocks = myData_Json.Json_Object()
        jsonStocks["extypes"] = lstExtypes
        jsonStocks["code_ids"] = lstCode_id
        jsonStocks["code_names"] = lstCode_Name
        jsonStocks["code_namesEN"] = lstCode_NameEN
    
        pMsg = copy.deepcopy(gol._Get_Setting('Return_strFormat', {}))
        pMsg['result'] = True
        pMsg['datas'] = jsonStocks._dict_
        #return myData_Json.Trans_ToJson_str(pMsg)
        #使用jsonify来讲定义好的数据转换成json格式，并且返回给前端
        return jsonify(pMsg) 

#API-行情设置
class myAPI_Quote_Set(myWeb.myAPI): 
    def get(self):
        #提取爬虫设置信息 
        #?setInfo={'spiderName': "ceshi2", 'spiderTag': 'webPage', 'spiderUrl': "", "spiderRule": "", 'isValid':'False', 'isDel':'True', "timeSet" : "* * * * *", 'mark':'测试设置' }
        #?setInfo={'spiderName': "sh000001", 'spiderTag': 'quote', 'spiderUrl': "", "spiderRule": "", 'isValid':'True', 'isDel':'False', "timeSet" : "* 9-20 * * 1-6", 'mark':'测试设置' }
        params = request.args.get('setInfo', "{}")
        setInfo = myData_Json.Trans_ToJson(params)

        #setInfo = myData_Trans.Tran_ToDict(params)
        bRes = not (setInfo.get("spiderName", "") == "")
        bRemove = myData_Trans.To_Bool(setInfo.get('isDel', "False"))
        if(setInfo.get("timeSet", None) == None):
            setInfo['timeSet'] = "* 9-15 * * 1-5"
            
        if(bRes and bRemove):
            bRes = setsSpider._Remove(setInfo['spiderName'])
            bRes = setsSpider._Find(setInfo["spiderName"]) == None
        else:
            bRes = setsSpider._Edit(setInfo)
            
        pMsg = copy.deepcopy(gol._Get_Setting('Return_strFormat', {}))
        if(bRes):
            pMsg['result'] = True
            spiderInfo = setsSpider._Find(setInfo["spiderName"])
            if(bRemove != True and spiderInfo != None):
                if(spiderInfo.isValid and not spiderInfo.isDeled):
                    pMsg['datas'] = [spiderInfo.ToDict()] 
        #return myData_Json.Trans_ToJson_str(pMsg)
        #使用jsonify来讲定义好的数据转换成json格式，并且返回给前端
        return jsonify(pMsg) 
#API-行情设置查询
class myAPI_Quote_SetQuery(myWeb.myAPI):
    def get(self):
        # http://127.0.0.1:8666/zxcAPI/robot/stock/QuoteSet/Query?spiderName=sh000001
        spiderName = request.args.get('spiderName', "")
        lstSets = []
        if(spiderName == ""):
            for x in setsSpider.setList:
                spiderInfo = setsSpider._Find(x)
                if(spiderInfo.isValid and not spiderInfo.isDeled):
                    lstSets.append(spiderInfo.ToDict())
        else:
            spiderInfo = setsSpider._Find(spiderName)
            if(spiderInfo.isValid and not spiderInfo.isDeled):
                lstSets.append(spiderInfo.ToDict())
        
        pMsg = copy.deepcopy(gol._Get_Setting('Return_strFormat', {}))
        if(spiderInfo != None):
            pMsg['result'] = True
            pMsg['datas'] = lstSets 
        #return myData_Json.Trans_ToJson_str(pMsg)
        #使用jsonify来讲定义好的数据转换成json格式，并且返回给前端
        return jsonify(pMsg) 

#API-行情查询(实时、多个)
class myAPI_Quote_Query(myWeb.myAPI):
    def get(self):
        # queryIDs=sh000001,sh601939
        global quoteSource
        ids = request.args.get('queryIDs', "")
        lstReturn = quoteSource.query(params = {'queryIDs' : ids})

        pMsg = copy.deepcopy(gol._Get_Setting('Return_strFormat', {}))
        if(lstReturn != None):
            datas = []
            for x in lstReturn:
                datas.append(x.toDict())
            pMsg['datas'] = datas
            pMsg['result'] = True
        #使用jsonify来讲定义好的数据转换成json格式，并且返回给前端
        return jsonify(pMsg) 
#API-行情查询(历史)
class myAPI_Quote_QueryHistory(myWeb.myAPI):
    def get(self):
        # dataFrequency=1d&stockBars=1&stockTag="10003418.XSHG"
        # {'dataFrequency': "1d", 'datetimeStart': "2021-06-23 09:00:00", 'stockTag': "10003418.XSHG"}
        global quoteSource
        stockTag = request.args.get('queryID', "")
        dataFrequency = request.args.get('dataFrequency', "1d")
        params = {'dataFrequency': dataFrequency, 'stockTag': "10003418.XSHG"}
        
        stockBars = myData_Trans.To_Int(request.args.get('stockBars', "0"))
        if(stockBars > 0):
            params["stockBars"] = stockBars

        timeEnd = request.args.get('datetimeEnd', "")
        timeStart = request.args.get('datetimeStart', "")
        if(timeEnd != ""): params["datetimeEnd"] = timeEnd
        if(timeStart != ""): params["datetimeStart"] = timeStart
            
        #调用
        lstReturn = quoteSource.queryHistory(checkTime = False, params = params)

        pMsg = copy.deepcopy(gol._Get_Setting('Return_strFormat', {}))
        if(lstReturn != None):
            datas = []
            for x in lstReturn:
                datas.append(x.toDict_Simple())
            pMsg['datas'] = datas
            pMsg['result'] = True
        #使用jsonify来讲定义好的数据转换成json格式，并且返回给前端
        return jsonify(pMsg) 


#集中添加所有API
def add_APIs(pWeb):  
    # 创建Web API
    pWeb.add_API(myAPI_Quote_Set, '/zxcAPI/robot/stock/QuoteSet')
    pWeb.add_API(myAPI_Quote_SetQuery, '/zxcAPI/robot/stock/QuoteSet/Query')
    
    pWeb.add_API(myAPI_Stock_Query, '/zxcAPI/robot/stock/Query')
    pWeb.add_API(myAPI_Quote_Query, '/zxcAPI/robot/quote/Query')
    pWeb.add_API(myAPI_Quote_QueryHistory, '/zxcAPI/robot/quote/QueryHistory')

    # 启动行情监测线程
    mySource_Control.initSource()
    mySource_Control.quoteStart()



#主程序启动
if __name__ == '__main__':  
    #初始行情对象
    #init_Quote()

    #注册平台, 取token
    #pQuote_Set = myAPI_Quote_Set()
    #msg = pQuote_Set.get()
    #print("msg::", msg)
    print()
    