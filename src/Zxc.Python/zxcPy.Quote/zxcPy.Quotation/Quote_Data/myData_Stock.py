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
import myQuote_Data


#行情数据对象
class Data_Stock(myQuote_Data.Quote_Data):
    def __init__(self):
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
        lstV.append(string.atof(self.lastPrice))
        return lstV
         
    #输出
    def Print(self):
        print (self.toString())

#行情数据对象--统计 
class Data_Stock__Statistics(myQuote_Data.Quote_Data_Statistics):
    def __init__(selff, tag, value = 0): 
        myQuote_Data.Quote_Data_Statistics.__init__(tag, value)
        self.Valume = 0        #成交量
        self.Turnover = 0      #成交额    
        
#行情数据对象集
class Datas_Stock:
    def __init__(self):
        self.name = ''
        self.dates = {}             #原始数据
        self.date = Quote_Data()    #当前数据
        self.keyMinutes = {}

        self.name = ''
        self.dates = {}             #原始数据
        self.dates_Statics_M = {}   #统计数据--分钟级
        self.date_Statics = Quote_Data_Statistics() #统计数据-当前
        self.date = Quote_Data()    #当前数据
        self.keyMinutes = {}
        
    #设置值 
    def setData(self, pDate):
        if(self.date.time == pDate.time):
            return 
        self.dates[pDate.time] = pDate
        self.date = pData
        
        #统计
        setData_Statistics(pDate)

    #设置统计信息 
    def setData_Statistics(self, pDate):
        dValue = pDate.lastPrice

        #分钟级数据处理
        time = pDate.getTime()
        if(self.date_Statics.tag + 1 >= time):
            self.dates_Statics_M[time] = self.date_Statics
            self.date_Statics = Data_Stock__Statistics(time, pDate) 

        #更新统计信息
        if(dValue > self.date_Statics.high):
            self.date_Statics.high = dValue
        if(dValue < self.date_Statics.low):
            self.date_Statics.low = dValue
        self.date_Statics.last = dValue
        self.date_Statics.average = average
        self.date_Statics.setValues(time, pDate.toValueList())
        

#主启动程序
if __name__ == "__main__":
    pData = Data_Stock()
    pData.Print()
