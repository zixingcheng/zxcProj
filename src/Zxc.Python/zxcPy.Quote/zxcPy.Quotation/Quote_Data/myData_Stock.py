#-*- coding: utf-8 -*-
"""
Created on  张斌 2018-05-03 14:58:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com

    监听-数据对象 
"""
import sys, os, mySystem 

#引用根目录类文件夹--必须，否则非本地目录起动时无法找到自定义类
mySystem.m_strFloders.append('/zxcPy.Quotation')
mySystem.Append_Us("", False)    
import myQuote_Data, myData_Trans


#行情数据对象
class Data_Stock(myQuote_Data.Quote_Data):
    def __init__(self):
        super().__init__()
        self.id = ''
        self.rawLine = ''
        #sorted with sina interface
        self.name = ''              
        self.openPrice = ''         #开盘价格
        self.preClose = ''          #前一收盘价
        self.lastPrice = ''         #最后价格
        self.highPrice = ''         #最高价格
        self.lowPrice = ''          #最低价格 
        self.buyPrice = ''          #买价
        self.sellPrice = ''         #卖价
        self.tradeValume = ''       #成交量
        self.tradeTurnover = ''     #成交额
        self.buy1Volume = ''        #买一量
        self.buy1Price = ''         #买一价格
        self.buy2Volume = ''
        self.buy2Price = ''
        self.buy3Volume = ''
        self.buy3Price = ''
        self.buy4Volume = ''
        self.buy4Price = ''
        self.buy5Volume = ''
        self.buy5Price = ''
        self.sell1Volume = ''
        self.sell1Price = ''
        self.sell2Volume = ''
        self.sell2Price = ''
        self.sell3Volume = ''
        self.sell3Price = ''
        self.sell4Volume = ''
        self.sell4Price = ''
        self.sell5Volume = ''
        self.sell5Price = ''
        self.date = ''
        self.time = ''

    #序列化
    def toString(self):
        return self.name + '(' + self.id + ')' \
            + ', openPrice=' + self.openPrice \
            + ', preClose=' + self.preClose \
            + ', lastPrice=' + self.lastPrice  \
            + ', highPrice=' + self.highPrice  \
            + ', lowPrice=' + self.lowPrice  \
            + ', buyPrice=' + self.buyPrice  \
            + ', sellPrice=' + self.sellPrice  \
            + ', tradeValume=' + self.tradeValume  \
            + ', buy1Volume=' + self.buy1Volume  \
            + ', buy1Price=' + self.buy1Price \
            + ', buy2Volume=' + self.buy2Volume \
            + ', buy2Price=' + self.buy2Price \
            + ', buy3Volume=' + self.buy3Volume \
            + ', buy3Price=' + self.buy3Price \
            + ', buy4Volume=' + self.buy4Volume \
            + ', buy4Price=' + self.buy4Price \
            + ', buy5Volume=' + self.buy5Volume \
            + ', buy5Price=' + self.buy5Price \
            + ', sell1Volume=' + self.sell1Volume  \
            + ', sell1Price=' + self.sell1Price  \
            + ', sell2Volume=' + self.sell2Volume  \
            + ', sell2Price=' + self.sell2Price  \
            + ', sell3Volume=' + self.sell3Volume  \
            + ', sell3Price=' + self.sell3Price  \
            + ', sell4Volume=' + self.sell4Volume  \
            + ', sell4Price=' + self.sell4Price  \
            + ', sell5Volume=' + self.sell5Volume  \
            + ', sell5Price=' + self.sell5Price  \
            + ', date=' + self.date  \
            + ', time=' + self.time
    
    #序列化--csv列头
    @staticmethod
    def csvHead():
        head = 'name,id,time,openPrice,preClose,lastPrice,highPrice,lowPrice,buyPrice,sellPrice,tradeValume,tradeTurnover,buy1Volume ,buy1Price,buy2Volume,buy2Price,buy3Volume,buy3Price,buy4Volume,buy4Price,buy5Volume,buy5Price,sell1Volume,sell1Price,sell2Volume,sell2Price,sell3Volume,sell3Price,sell4Volume,sell4Price,sell5Volume,sell5Price,date'
        return head
        
    #序列化--csv行信息
    def toCSVString(self):
        return '\n' + self.name \
            + ',' + self.id  \
            + ',' + self.time \
            + ',' + self.openPrice \
            + ',' + self.preClose \
            + ',' + self.lastPrice  \
            + ',' + self.highPrice  \
            + ',' + self.lowPrice  \
            + ',' + self.buyPrice  \
            + ',' + self.sellPrice  \
            + ',' + self.tradeValume  \
            + ',' + self.tradeTurnover \
            + ',' + self.buy1Volume  \
            + ',' + self.buy1Price \
            + ',' + self.buy2Volume \
            + ',' + self.buy2Price \
            + ',' + self.buy3Volume \
            + ',' + self.buy3Price \
            + ',' + self.buy4Volume \
            + ',' + self.buy4Price \
            + ',' + self.buy5Volume \
            + ',' + self.buy5Price \
            + ',' + self.sell1Volume  \
            + ',' + self.sell1Price  \
            + ',' + self.sell2Volume  \
            + ',' + self.sell2Price  \
            + ',' + self.sell3Volume  \
            + ',' + self.sell3Price  \
            + ',' + self.sell4Volume  \
            + ',' + self.sell4Price  \
            + ',' + self.sell5Volume  \
            + ',' + self.sell5Price  \
            + ',' + self.date

    #转换为值组
    def toValueList(self):
        lstV = []
        lstV.append(myData_Trans.To_Float(self.lastPrice))
        lstV.append(myData_Trans.To_Float(self.tradeValume))
        lstV.append(myData_Trans.To_Float(self.tradeTurnover))
        return lstV
         
    #输出
    def Print(self):
        print (self.toString())

#行情数据对象--统计 
class Data_CKD_Stock(myQuote_Data.Quote_Data_CKD):
    def __init__(self, tagTime, data = Data_Stock(), interval_M = -1): 
        super().__init__(tagTime, data, interval_M)
        datas = data.toValueList()
        self.Valume_S = datas[1]      #成交量_S
        self.Turnover_S = datas[2]    #成交额_S
        self.Valume = 0               #成交量
        self.Turnover = 0             #成交额   

    #其他统计接口
    def setData_Statics(self, pData):
        datas = pData.toValueList()
        self.Valume = datas[1] - self.Valume_S
        self.Turnover = datas[2] - self.Turnover_S
       
#数据对象--统计集 
class Data_CKDs_Stock(myQuote_Data.Quote_Data_CKDs):
    #依次：时间标签，初始值，统计间隔
    def __init__(self, data = Data_Stock(), interval_M = -1): 
        super().__init__(data, interval_M)
        
    #初始统计对象 
    def newDataCKD(self, tagTime, data):
        pCDK = Data_CKD_Stock(tagTime, data, self.interval_M)
        self.CKDs[tagTime] = pCDK
        return pCDK

#行情数据对象集
class Datas_Stock(myQuote_Data.Quote_Datas):
    def __init__(self, pData, interval = 1):
        super().__init__(pData, interval)
        
    #初始统计对象 
    def newData_CKDs(self, pData):
        return Data_CKDs_Stock(pData, self.interval_M)


#主启动程序
if __name__ == "__main__":
    pData = Data_Stock()
    pData.Print()
