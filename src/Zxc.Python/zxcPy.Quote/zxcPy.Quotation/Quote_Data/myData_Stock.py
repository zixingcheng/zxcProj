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
        self.dateList = []

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
        head = '时间,当前价,最高价,最低价,买价,卖价,成交量,成交额,买一量,买二量,买三量,买四量,买五量,买一价,买二价,买三价,买四价,买五价,卖一量,卖二量,卖三量,卖四量,卖五量,卖一价,卖二价,卖三价,卖四价,卖五价'
        return head
        
    #序列化--csv行信息
    def toCSVString(self):
        return '\r\n' + self.date + " " + self.time  \
            + ',' + self.lastPrice  \
            + ',' + self.highPrice  \
            + ',' + self.lowPrice  \
            + ',' + self.buyPrice  \
            + ',' + self.sellPrice  \
            + ',' + self.tradeValume  \
            + ',' + self.tradeTurnover \
            + ',' + self.buy1Volume  \
            + ',' + self.buy2Volume  \
            + ',' + self.buy3Volume \
            + ',' + self.buy4Volume \
            + ',' + self.buy5Volume \
            + ',' + self.buy1Price \
            + ',' + self.buy2Price \
            + ',' + self.buy3Price \
            + ',' + self.buy4Price \
            + ',' + self.buy5Price \
            + ',' + self.sell1Volume  \
            + ',' + self.sell2Volume  \
            + ',' + self.sell3Volume  \
            + ',' + self.sell4Volume  \
            + ',' + self.sell5Volume  \
            + ',' + self.sell1Price  \
            + ',' + self.sell2Price  \
            + ',' + self.sell3Price  \
            + ',' + self.sell4Price  \
            + ',' + self.sell5Price
    
    #转换为值组
    def toValueList(self):
        dtNow = self.getTime(False)
        if(len(self.dateList) > 1 and self.dateList[0] == dtNow):
           return self.dateList
        self.dateList = [] 
        self.dateList.append(dtNow)                                      #时间
        self.dateList.append(myData_Trans.To_Float(self.lastPrice))      #最后价格
        self.dateList.append(myData_Trans.To_Float(self.highPrice))      #最高价格
        self.dateList.append(myData_Trans.To_Float(self.lowPrice))       #最低价格 
        self.dateList.append(myData_Trans.To_Float(self.buyPrice))       #买价
        self.dateList.append(myData_Trans.To_Float(self.sellPrice))      #卖价
        self.dateList.append(myData_Trans.To_Float(self.tradeValume))    #成交量
        self.dateList.append(myData_Trans.To_Float(self.tradeTurnover))  #成交额
        
        self.dateList.append(myData_Trans.To_Float(self.buy1Volume))     #买1-5量
        self.dateList.append(myData_Trans.To_Float(self.buy2Volume))   
        self.dateList.append(myData_Trans.To_Float(self.buy3Volume))   
        self.dateList.append(myData_Trans.To_Float(self.buy4Volume))   
        self.dateList.append(myData_Trans.To_Float(self.buy5Volume))  
        self.dateList.append(myData_Trans.To_Float(self.buy1Price))      #买1-5价格
        self.dateList.append(myData_Trans.To_Float(self.buy2Price))   
        self.dateList.append(myData_Trans.To_Float(self.buy3Price))   
        self.dateList.append(myData_Trans.To_Float(self.buy4Price))   
        self.dateList.append(myData_Trans.To_Float(self.buy5Price))   
        
        self.dateList.append(myData_Trans.To_Float(self.sell1Volume))    #卖1-5量
        self.dateList.append(myData_Trans.To_Float(self.sell2Volume))   
        self.dateList.append(myData_Trans.To_Float(self.sell3Volume))   
        self.dateList.append(myData_Trans.To_Float(self.sell4Volume))   
        self.dateList.append(myData_Trans.To_Float(self.sell5Volume))  
        self.dateList.append(myData_Trans.To_Float(self.sell1Price))     #卖1-5价格
        self.dateList.append(myData_Trans.To_Float(self.sell2Price))   
        self.dateList.append(myData_Trans.To_Float(self.sell3Price))   
        self.dateList.append(myData_Trans.To_Float(self.sell4Price))   
        self.dateList.append(myData_Trans.To_Float(self.sell5Price))   
        return self.dateList
    #由值组转换
    def fromValueList(self, lstValue):
        self.dateList = lstValue
        dtNow = lstValue[0]

        self.date = str(dtNow.year) + "-" + str(dtNow.month) + "-" + str(dtNow.day)
        self.time = str(dtNow.hour) + ":" + str(dtNow.minute) + ":" + str(dtNow.second)
        self.lastPrice = str(lstValue[1])
        self.highPrice = str(lstValue[2])
        self.lowPrice = str(lstValue[3])
        self.buyPrice = str(lstValue[4])
        self.sellPrice = str(lstValue[5])
        self.tradeValume = str(lstValue[6])
        self.tradeTurnover = str(lstValue[7])
         
        self.buy1Volume = str(lstValue[8])      #买1-5量
        self.buy2Volume = str(lstValue[9])
        self.buy3Volume = str(lstValue[10])
        self.buy4Volume = str(lstValue[11])
        self.buy5Volume = str(lstValue[12])
        self.buy1Price = str(lstValue[13])      #买1-5价格       
        self.buy2Price = str(lstValue[14])
        self.buy3Price = str(lstValue[15])
        self.buy4Price = str(lstValue[16])
        self.buy5Price = str(lstValue[17])
        
        self.sell1Volume = str(lstValue[18])    #卖1-5量
        self.sell2Volume = str(lstValue[19])
        self.sell3Volume = str(lstValue[20])
        self.sell4Volume = str(lstValue[21])
        self.sell5Volume = str(lstValue[22])
        self.sell1Price = str(lstValue[23])
        self.sell2Price = str(lstValue[24])
        self.sell3Price = str(lstValue[25])
        self.sell4Price = str(lstValue[26])
        self.sell5Price = str(lstValue[27])
        return True
         
    #输出
    def Print(self):
        print(self.toString())

#行情数据对象--统计 
class Data_CKD_Stock(myQuote_Data.Quote_Data_CKD):
    def __init__(self, tagTime, data = Data_Stock(), lastCKD = None, interval_M = -1): 
        super().__init__(tagTime, data, lastCKD, interval_M)
        self.Valume = 0         #当前成交量
        self.Turnover = 0       #当前成交额   
        self.Price = 0          #成交均价  

        if(lastCKD == None):
            datas = data.toValueList()
            self.Valume_pre = datas[6]         #前一统计成交量_S
            self.Turnover_pre = datas[7]       #前一统计成交额_S
        else:
            self.Valume_pre = lastCKD.Valume_pre + lastCKD.Valume        #前一统计成交量_S
            self.Turnover_pre = lastCKD.Turnover_pre + lastCKD.Turnover  #前一统计成交额_S
            self.Price = lastCKD.Price
        self.setData(data)                     #设置数据

    #其他统计接口
    def setData_Statics(self, pData):
        datas = pData.toValueList()
        self.Valume = datas[6] - self.Valume_pre
        self.Turnover = datas[7] - self.Turnover_pre
        if(self.Valume > 0):
            self.Price = self.Turnover / self.Valume
        elif(self.Valume < 0):
            a =0
       
#数据对象--统计集 
class Data_CKDs_Stock(myQuote_Data.Quote_Data_CKDs):
    #依次：时间标签，初始值，统计间隔
    def __init__(self, data = Data_Stock(), interval_M = -1): 
        super().__init__(data, interval_M)
        
    #初始统计对象 
    def newDataCKD(self, tagTime, data):
        pCDK = Data_CKD_Stock(tagTime, data, self.CKD, self.interval_M)
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
    
    pData.name = "建设银行"
    pData.date = myData_Trans.Tran_ToTime_str(None, "%Y-%m-%d")
    pData.time = myData_Trans.Tran_ToTime_str(None, "%H:%M:%S")
    pDatas = Datas_Stock(pData)

    pDatas.saveData("./Data/")
    pDatas.loadData("./Data/")

