#-*- coding: utf-8 -*-
"""
Created on  张斌 2018-05-03 14:58:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com

    监听--源基类 
"""
import sys, os, time, mySystem 
import urllib, urllib.request

#引用根目录类文件夹--必须，否则非本地目录起动时无法找到自定义类
mySystem.m_strFloders.append('/zxcPy.Quotation')
mySystem.m_strFloders.append('/zxcPy.Quotation/Quote_Data')
mySystem.Append_Us("", False)    
import myData_Trans, myData_Json
import myQuote_Data, myData_Stock, myQuote_Listener, myQuote_Source  
from myGlobal import gol   



#行情源--新浪--Stock
class Source_Sina_Stock(myQuote_Source.Quote_Source):
    def __init__(self, params = ""):
        myQuote_Source.Quote_Source.__init__(self, params, '')     #设置类型
        
    #查询行情
    def query(self, checkTime = True, nReturn = 0, parms = None):    
        #新浪Stock接口查询
        host="http://hq.sinajs.cn/list="
        url = host + self.params
        if(parms != None):
            if(parms.get('queryIDs', None) != None):
                url = host + parms['queryIDs']

        req = urllib.request.Request(url)
        res_data = urllib.request.urlopen(req)
        res = res_data.read().decode(encoding = "gbk")
        
        #返回组
        nNum = nReturn
        lstReturn = []

        #解析所有返回数据
        lines = res.split('\n')
        nResult = 0
        for line in lines:
            qd = self.newData_ByInfo(line, checkTime)  
            if(qd == None): 
                continue 

            #测试步进时间
            #qd.time = myData_Trans.Tran_ToTime_str(None, "%H:%M:%S")
            #qd.date = myData_Trans.Tran_ToTime_str(None, "%Y-%m-%d")
             
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
                #Error(e)
                pass
        if(nReturn>0): return lstReturn
        if(nResult > 0): 
            print("")
            return True 

    #生成数据对象
    def newData(self):
        return myData_Stock.Data_Stock()
    def newData_ByInfo(self, dataInfo, checkTime = True):    
        #解析所有返回数据 
        if len(dataInfo) > 50 : 
            values = dataInfo.split('=')
            stkid = values[0][11:]
            info = values[1][1:len(values[1])-4]
            vargs = info.split(',')
            
            # 区分股票与期权
            qd = self.newData()     
            if(stkid.count('CON_OP') == 1):
                #var hq_str_CON_OP_代码=“买量(0)，买价，最新价，卖价，卖量，持仓量，涨幅，行权价，昨收价，开盘价，涨停价，跌停价(11), 
                #                    申卖 价五，申卖量五，申卖价四，申卖量四，申卖价三，申卖量三，申卖价二，申卖量二，申卖价一，申卖量一，申买价一，
                #                    申买量一 ，申买价二，申买量二，申买价三，申买量三，申买价四，申买量四，申买价五，申买量五，行情时间，主力合约标识，状态码， 
                #                    标的证券类型，标的股票，期权合约简称，振幅(38)，最高价，最低价，成交量，成交额，分红调整标志，昨结算价，认购认沽标志，
                #                    到期日，剩余天数，虚实值标志，内在价值，时间价值
                qd.id = stkid[7:] 
                qd.idTag = stkid
                qd.rawline = info
                qd.buyPrice = vargs[1]
                qd.lastPrice = vargs[2]
                qd.sellPrice = vargs[3]

                qd.preClose = vargs[8]
                qd.openPrice = vargs[9]
            
                qd.sell5Price = vargs[12]
                qd.sell5Volume = vargs[13]
                qd.sell4Price = vargs[14]
                qd.sell4Volume = vargs[15]
                qd.sell3Price = vargs[16]
                qd.sell3Volume = vargs[17]
                qd.sell2Price = vargs[18]
                qd.sell2Volume = vargs[19]
                qd.sell1Price = vargs[20]
                qd.sell1Volume = vargs[21]
                qd.buy1Price = vargs[22]
                qd.buy1Volume = vargs[23]
                qd.buy2Price = vargs[24]
                qd.buy2Volume = vargs[25]
                qd.buy3Price = vargs[26]
                qd.buy3Volume = vargs[27]
                qd.buy4Price = vargs[28]
                qd.buy4Volume = vargs[29]
                qd.buy5Price = vargs[30]
                qd.buy5Volume = vargs[31]
                qd.date = vargs[32].split(' ')[0]
                qd.time = vargs[32].split(' ')[1]

                qd.name = vargs[37]
                qd.highPrice = vargs[39]
                qd.lowPrice = vargs[40]
                qd.tradeValume = vargs[41]
                qd.tradeTurnover = vargs[42] 
            else:
                #var hq_str_sh510050=证券简称,今日开盘价,昨日收盘价,最近成交价,最高成交价,最低成交价,买入价,
                #                    卖出价,成交数量,成交金额,买数量一,买价位一,买数量二,买价位二,买数量三 ,买价位三,买数量四,
                #                    买价位四,买数量五,买价位五,卖数量一,卖价位一,卖数量二,卖价位二,卖数量三,卖价位三,卖数量四,
                #                    卖价位四,卖数量五,卖价位五,行情日期,行情时间,停牌状态
                qd.id = stkid[2:] 
                qd.idTag = stkid
                qd.rawline = info
                qd.name = vargs[0]
                qd.openPrice = vargs[1]
                qd.preClose = vargs[2]
                qd.lastPrice = vargs[3]
                qd.highPrice = vargs[4]
                qd.lowPrice = vargs[5]
                qd.buyPrice = vargs[6]
                qd.sellPrice = vargs[7]
                qd.tradeValume = vargs[8]
                qd.tradeTurnover = vargs[9]
                qd.buy1Volume = vargs[10]
                qd.buy1Price = vargs[11]
                qd.buy2Volume = vargs[12]
                qd.buy2Price = vargs[13]
                qd.buy3Volume = vargs[14]
                qd.buy3Price = vargs[15]
                qd.buy4Volume = vargs[16]
                qd.buy4Price = vargs[17]
                qd.buy5Volume = vargs[18]
                qd.buy5Price = vargs[19]
                qd.sell1Volume = vargs[20]
                qd.sell1Price = vargs[21]
                qd.sell2Volume = vargs[22]
                qd.sell2Price = vargs[23]
                qd.sell3Volume = vargs[24]
                qd.sell3Price = vargs[25]
                qd.sell4Volume = vargs[26]
                qd.sell4Price = vargs[27]
                qd.sell5Volume = vargs[28]
                qd.sell5Price = vargs[29]
                qd.date = vargs[30]
                qd.time = vargs[31]

            #时间检查(是否当天)
            if(checkTime):
                if(qd.checkTime() == False): 
                    return None 

            #设置数据
            qd.value = myData_Trans.To_Float(qd.lastPrice)
            return qd
        return None

    #生成数据集对象
    def newDatas(self, data, interval):
        return myData_Stock.Datas_Stock(data, interval)
  
    
#缓存全局对象
gol._Set_Value('quoteSource_Sina', Source_Sina_Stock())  #实例 行情对象



#主启动程序
if __name__ == "__main__":
    # sh000001,sh601939,sh601288,sh600919,sh600718
    # sz399001,sz399006,sz300523,sz300512,sz300144,sz300036,sz002410,sz002024
    stockids = 'hk002379'
    stockids = 'sh510050'
    stockids = 'CON_OP_10002544'
    s = Source_Sina_Stock(stockids)

    # 单独查询，不纪录
    qd = s.query(False, 1) 
    
    # 通用查询，并记录
    while True:
        s.query() 
        time.sleep(3)




 
