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
mySystem.m_strFloders.append('/zxcPy.Quotation/Quote_Listener')
mySystem.m_strFloders.append('/zxcPy.Quotation/Quote_Data')
mySystem.Append_Us("", False)    
import myData_Trans, myData, myDebug
import myData_Stock, myQuote_Source, myQuote
from myGlobal import gol   
from jqdatasdk import *



#行情源--聚宽API
class Source_JQData_Stock(myQuote_Source.Quote_Source):
    def __init__(self, params = ""):
        myQuote_Source.Quote_Source.__init__(self, params, 'JqDataAPI')         #设置类型
        self.pSource = gol._Get_Value('quoteSource_API_JqData', None)
        self.setsStock = gol._Get_Value('setsStock', myQuote.myStocks())        #标的信息
        pass

    #查询行情
    def query(self, checkTime = True, nReturn = 0, parms = None):  
        #组装参数
        lstReturn = []
        if(parms == None): return lstReturn
        
        #示例参数: {'dataFrequency': "1d", 'stockBars': 1, 'stockTag': "10003418.XSHG"}
        timeEnd = parms.get('datetimeEnd', myData_Trans.Tran_ToDatetime_str(None, "%Y-%m-%d %H:%M:%S"))
        timeStart = parms.get('datetimeStart', myData_Trans.Tran_ToDatetime_str(None, "%Y-%m-%d %H:%M:%S"))
        dataFrequency = parms.get('dataFrequency', "1d")        # 查询周期价格信息，'1m', '5m', '15m', '30m', '60m', '120m', '1d', '1w', '1M'
        stockBars = parms.get('stockBars', 0)
        stockTag = parms.get('stockTag', None)
        if(stockTag == None): return lstReturn

        #校检标的信息
        stockTemps = stockTag.split('.')
        stockInfo = self.setsStock._Find(code_id = stockTemps[0])
        if(len(stockInfo) != 1): return lstReturn
        pStock = stockInfo[0]


        #调用接口
        _values = []
        _isBar = False
        if(stockBars <= 0):
            _values = self.pSource.getPrice(security = stockTag, frequency = dataFrequency, start_date = timeStart, end_date = timeEnd)
        else:
            _isBar = True
            _values = self.pSource.getPrice_bars(security = stockTag, count = stockBars, unit = dataFrequency, end_date = timeEnd, include_now = True)
        if(len(_values) < 1): return lstReturn 


        #组装返回信息
        nNum = nReturn; nResult = 0; 
        for x in range(0, len(_values)):
            #数据处理
            try: 
                dataInfo = {'setInfo': pStock, "values": _values, "ind": x, "_isBar": _isBar}
                dataQuote = self.newData_ByInfo(dataInfo, checkTime) 
                if(dataQuote == None):  continue
                
                if(nNum >= 0):
                    lstReturn.append(dataQuote)
                    nNum= nNum - 1
                self.notifyListeners(dataQuote)
            except Exception as e:
                myDebug.Error(str(e))
                pass  
        return lstReturn

    #生成数据对象--未完成
    def newData(self):
        return myData_Stock.Data_Stock()
    #生成数据对象--未完成
    def newData_ByInfo(self, dataInfo, checkTime = True):    
        #解析所有返回数据 
        #dataInfo = {'setInfo': pStock, "values": _values, "ind": x}
        if len(dataInfo['values']) == 1 : 
            _values = dataInfo['values']
            _stockInfo = dataInfo['setInfo']
            _ind = dataInfo['ind']
            _isBar = dataInfo['_isBar']
            times = myData.iif(_stockInfo.type == "opt", 10000, 1)

            qd = self.newData()     
            qd.id = _stockInfo.code_id
            qd.idTag = _stockInfo.extype + "." + _stockInfo.code_id
            qd.rawline = ""
            qd.name = _stockInfo.code_name
            qd.openPrice = float(_values['open'][_ind] * times)
            qd.preClose = 0
            qd.lastPrice = float(_values['close'][_ind] * times)
            qd.highPrice = float(_values['high'][_ind] * times)
            qd.lowPrice = float(_values['low'][_ind] * times)
            qd.tradeValume = float(_values['volume'][_ind])
            qd.tradeTurnover = float(_values['money'][_ind])
            qd.buyPrice = -1
            qd.sellPrice = -1

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
            if(_isBar):
                 qd.date = myData_Trans.Tran_ToDatetime_str(_values['date'][_ind], "%Y-%m-%d %H:%M:%S")
            else:
                 qd.date = str(_values.axes[0].array[_ind])
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
    pParams = {'dataFrequency': "1d", 'stockBars': 1, 'stockTag': "10003418.XSHG"}
    qd = pSource.query(False, 1, pParams) 
    
    # 通用查询，并记录
    while True:
        pSource.query() 
        time.sleep(3)