#-*- coding: utf-8 -*-
"""
Created on  张斌 2020-06-23 22:58:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com

    行情爬取--源基类-聚宽 
"""
import sys, os, datetime, mySystem 


#引用根目录类文件夹--必须，否则非本地目录起动时无法找到自定义类 
mySystem.m_strFloders.append('/zxcPy.Quotation')
mySystem.m_strFloders.append('/zxcPy.Quotation/Quote_Data')
mySystem.Append_Us("", False)    
import myData_Trans, myData, myDebug
import myData_Stock, myQuote_Source  
from myGlobal import gol   
from jqdatasdk import *



#行情源--聚宽API
class Source_JQData_Stock(myQuote_Source.Quote_Source):
    def __init__(self, params = ""):
        myQuote_Source.Quote_Source.__init__(self, params, 'JqDataAPI')     #设置类型
        self.pSource = gol._Get_Value('quoteSource_API_JqData', None)
        pass

    #查询行情
    def query(self, checkTime = True, nReturn = 0, parms = None):  
        #组装参数
        lstSets = self.paramsSet[self.type]
        time_s = int(myData_Trans.Tran_ToDatetime_str(None, "%S"))
        dtNow = myData_Trans.Tran_ToDatetime_str(None, "%Y-%m-%d %H:%M")
        #dtNow = "2020-06-29 14:00"
        
        #返回组
        nNum = nReturn; nResult = 0; lstReturn = []

        #聚宽Stock接口查询
        dtStart = dtNow + myData.iif(time_s < 10, F":0{time_s}", F":{time_s}")
        for x in lstSets:
            _values = self.pSource.getPrice(security=x.stockInfo.source_code,frequency='1m',start_date=dtStart,end_date=dtNow + ":59")
            if(len(_values) < 1): continue 

            #转换数据
            dataInfo = {'setInfo': x, "values": _values, "time": dtStart}
            qd = self.newData_ByInfo(dataInfo, checkTime)  
            if(qd == None): 
                continue 

            #数据处理
            try:
                if(nReturn <= 0):
                    pDatas = self.setData(qd)
                    if(pDatas != None): nResult += 1
                else:
                    if(nNum > 0):
                        lstReturn.append(qd)
                        nNum= nNum - 1
            except Exception as e:
                myDebug.Error(str(e))
                pass
        if(nReturn>0): return lstReturn
        if(nResult > 0): 
            print("")
            return True 

    #生成数据对象--未完成
    def newData(self):
        return myData_Stock.Data_Stock()
    #生成数据对象--未完成
    def newData_ByInfo(self, dataInfo, checkTime = True):    
        #解析所有返回数据 
        if len(dataInfo['values']) == 1 : 
            _values = dataInfo['values']
            _setInfo = dataInfo['setInfo']
            times = myData.iif(_setInfo.stockInfo.type == "opt", 10000, 1)

            qd = self.newData()     
            qd.id = _setInfo.stockInfo.code_id
            qd.idTag = _setInfo.setTag
            qd.rawline = ""
            qd.name = _setInfo.stockInfo.code_name
            qd.openPrice = float(_values['open'][0] * times)
            qd.preClose = qd.openPrice
            qd.lastPrice = float(_values['close'][0] * times)
            qd.highPrice = float(_values['high'][0] * times)
            qd.lowPrice = float(_values['low'][0] * times)
            qd.tradeValume = float(_values['volume'][0])
            qd.tradeTurnover = float(_values['money'][0])
            qd.buyPrice = myData.iif(qd.tradeTurnover == 0, qd.preClose, qd.tradeTurnover / qd.tradeValume)
            qd.sellPrice = qd.buyPrice

            qd.buy1Volume = -1
            qd.buy1Price = -1
            qd.buy2Volume = -1
            qd.buy2Price = -1
            qd.buy3Volume = -1
            qd.buy3Price = -1
            qd.buy4Volume = -1
            qd.buy4Price = -1
            qd.buy5Volume = -1
            qd.buy5Price = -1
            qd.sell1Volume = -1
            qd.sell1Price = -1
            qd.sell2Volume = -1
            qd.sell2Price = -1
            qd.sell3Volume = -1
            qd.sell3Price = -1
            qd.sell4Volume = -1
            qd.sell4Price = -1
            qd.sell5Volume = -1
            qd.sell5Price = -1
            qd.date = dataInfo['time']
            qd.time = qd.date.split(' ')[1]
            qd.date = qd.date.split(' ')[0]

            #时间检查(是否当天)
            if(checkTime):
                if(qd.checkTime() == False): 
                    return None 

            #设置数据
            qd.value = qd.lastPrice
            return qd
        return None
    #生成数据集对象--未完成
    def newDatas(self, data, interval):
        return myData_Stock.Datas_Stock(data, interval)
    
#缓存全局对象
gol._Set_Value('quoteSource_JqData', Source_JQData_Stock())     #实例 行情对象



#主启动程序
if __name__ == "__main__": 
    # 提取标的信息
    pSource = gol._Get_Value('quoteSource_JqData', None)
 
    import myListener_Printer, time
    pSource.addListener(myListener_Printer.Quote_Listener_Printer())
    
    # 单独查询，不纪录
    qd = pSource.query(False, 1) 
    
    # 通用查询，并记录
    while True:
        pSource.query() 
        time.sleep(3)