#-*- coding: utf-8 -*-
"""
Created on  张斌 2018-05-03 14:58:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com

    行情爬取-数据对象 
"""
import sys, os, json, datetime, mySystem 

#引用根目录类文件夹--必须，否则非本地目录起动时无法找到自定义类
mySystem.m_strFloders.append('/zxcPy.Quotation')
mySystem.Append_Us("", False)    
import myQuote_Data, myData, myData_Trans, myData_Json, myDebug



#行情数据对象
class Data_Stock(myQuote_Data.Quote_Data):
    def __init__(self):
        super().__init__()
        self.id = ''
        self.idTag = ''
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
        self.dataList = []
        self.priceOpen = 0      #开盘价格
        self.priceBase = 0      #前一收盘价格
        self.priceRiseFall = 0  #涨跌幅

    #序列化
    def toString(self):
        return self.name + '(' + myData.iif(self.idTag == "", self.id, self.idTag) + ')' \
            + ', openPrice=' + str(self.openPrice) \
            + ', preClose=' + str(self.preClose) \
            + ', lastPrice=' + str(self.lastPrice)  \
            + ', highPrice=' + str(self.highPrice)  \
            + ', lowPrice=' + str(self.lowPrice)  \
            + ', buyPrice=' + str(self.buyPrice)  \
            + ', sellPrice=' + str(self.sellPrice)  \
            + ', tradeValume=' + str(self.tradeValume)  \
            + ', buy1Volume=' + str(self.buy1Volume)  \
            + ', buy1Price=' + str(self.buy1Price) \
            + ', buy2Volume=' + str(self.buy2Volume) \
            + ', buy2Price=' + str(self.buy2Price) \
            + ', buy3Volume=' + str(self.buy3Volume) \
            + ', buy3Price=' + str(self.buy3Price) \
            + ', buy4Volume=' + str(self.buy4Volume) \
            + ', buy4Price=' + str(self.buy4Price) \
            + ', buy5Volume=' + str(self.buy5Volume) \
            + ', buy5Price=' + str(self.buy5Price) \
            + ', sell1Volume=' + str(self.sell1Volume)  \
            + ', sell1Price=' + str(self.sell1Price)  \
            + ', sell2Volume=' + str(self.sell2Volume)  \
            + ', sell2Price=' + str(self.sell2Price)  \
            + ', sell3Volume=' + str(self.sell3Volume)  \
            + ', sell3Price=' + str(self.sell3Price)  \
            + ', sell4Volume=' + str(self.sell4Volume)  \
            + ', sell4Price=' + str(self.sell4Price)  \
            + ', sell5Volume=' + str(self.sell5Volume)  \
            + ', sell5Price=' + str(self.sell5Price)  \
            + ', date=' + self.date  \
            + ', time=' + self.time
    
    #序列化--csv列头
    @staticmethod
    def csvHead():
        head = '时间,当前价,最高价,最低价,买价,卖价,成交量,成交额,买一量,买二量,买三量,买四量,买五量,买一价,买二价,买三价,买四价,买五价,卖一量,卖二量,卖三量,卖四量,卖五量,卖一价,卖二价,卖三价,卖四价,卖五价'
        return head
    #序列化--csv行信息
    def toCSVString(self):
        return '\n' + self.date + " " + self.time  \
            + ',' + str(self.lastPrice)  \
            + ',' + str(self.highPrice)  \
            + ',' + str(self.lowPrice)  \
            + ',' + str(self.buyPrice)  \
            + ',' + str(self.sellPrice)  \
            + ',' + str(self.tradeValume)  \
            + ',' + str(self.tradeTurnover) \
            + ',' + str(self.buy1Volume)  \
            + ',' + str(self.buy2Volume)  \
            + ',' + str(self.buy3Volume) \
            + ',' + str(self.buy4Volume) \
            + ',' + str(self.buy5Volume) \
            + ',' + str(self.buy1Price) \
            + ',' + str(self.buy2Price) \
            + ',' + str(self.buy3Price) \
            + ',' + str(self.buy4Price) \
            + ',' + str(self.buy5Price) \
            + ',' + str(self.sell1Volume)  \
            + ',' + str(self.sell2Volume)  \
            + ',' + str(self.sell3Volume)  \
            + ',' + str(self.sell4Volume)  \
            + ',' + str(self.sell5Volume)  \
            + ',' + str(self.sell1Price)  \
            + ',' + str(self.sell2Price)  \
            + ',' + str(self.sell3Price)  \
            + ',' + str(self.sell4Price)  \
            + ',' + str(self.sell5Price)
    
    #转为Dict
    def toDict(self):
        dictValue = {}
        dictValue["idTag"] = myData.iif(self.idTag == "", self.id, self.idTag)
        dictValue["id"] = self.id
        dictValue["name"] = self.name
        dictValue["openPrice"] = myData_Trans.To_Float(str(self.openPrice))
        dictValue["preClose"] = myData_Trans.To_Float(str(self.preClose))
        dictValue["lastPrice"] = myData_Trans.To_Float(str(self.lastPrice))
        dictValue["highPrice"] = myData_Trans.To_Float(str(self.highPrice))
        dictValue["lowPrice"] = myData_Trans.To_Float(str(self.lowPrice))
        dictValue["buyPrice"] = myData_Trans.To_Float(str(self.buyPrice))
        dictValue["sellPrice"] = myData_Trans.To_Float(str(self.sellPrice))
        dictValue["tradeValume"] = myData_Trans.To_Int(str(self.tradeValume))
        dictValue["tradeTurnover"] = myData_Trans.To_Float(str(self.tradeTurnover))
        dictValue["buy1Volume"] = myData_Trans.To_Int(str(self.buy1Volume))
        dictValue["buy1Price"] = myData_Trans.To_Float(str(self.buy1Price))
        dictValue["buy2Volume"] = myData_Trans.To_Int(str(self.buy2Volume))
        dictValue["buy2Price"] = myData_Trans.To_Float(str(self.buy2Price))
        dictValue["buy3Volume"] = myData_Trans.To_Int(str(self.buy3Volume))
        dictValue["buy3Price"] = myData_Trans.To_Float(str(self.buy3Price))
        dictValue["buy4Volume"] = myData_Trans.To_Int(str(self.buy4Volume))
        dictValue["buy4Price"] = myData_Trans.To_Float(str(self.buy4Price))
        dictValue["buy5Volume"] = myData_Trans.To_Int(str(self.buy5Volume))
        dictValue["buy5Price"] = myData_Trans.To_Float(str(self.buy5Price))
        dictValue["sell1Volume"] = myData_Trans.To_Int(str(self.sell1Volume))
        dictValue["sell1Price"] = myData_Trans.To_Float(str(self.sell1Price))
        dictValue["sell2Volume"] = myData_Trans.To_Int(str(self.sell2Volume))
        dictValue["sell2Price"] = myData_Trans.To_Float(str(self.sell2Price))
        dictValue["sell3Volume"] = myData_Trans.To_Int(str(self.sell3Volume))
        dictValue["sell3Price"] = myData_Trans.To_Float(str(self.sell3Price))
        dictValue["sell4Volume"] = myData_Trans.To_Int(str(self.sell4Volume))
        dictValue["sell4Price"] = myData_Trans.To_Float(str(self.sell4Price))
        dictValue["sell5Volume"] = myData_Trans.To_Int(str(self.sell5Volume))
        dictValue["sell5Price"] = myData_Trans.To_Float(str(self.sell5Price))
        dictValue["datetime"] =  self.date + " " + self.time
        return dictValue
    #转为Dict
    def toDict_Simple(self):
        dictValue = {}
        dictValue["idTag"] = myData.iif(self.idTag == "", self.id, self.idTag)
        dictValue["id"] = self.id
        dictValue["name"] = self.name
        dictValue["openPrice"] = myData_Trans.To_Float(str(self.openPrice))
        dictValue["preClose"] = myData_Trans.To_Float(str(self.preClose))
        dictValue["lastPrice"] = myData_Trans.To_Float(str(self.lastPrice))
        dictValue["highPrice"] = myData_Trans.To_Float(str(self.highPrice))
        dictValue["lowPrice"] = myData_Trans.To_Float(str(self.lowPrice))
        dictValue["buyPrice"] = myData_Trans.To_Float(str(self.buyPrice))
        dictValue["sellPrice"] = myData_Trans.To_Float(str(self.sellPrice))
        dictValue["tradeValume"] = myData_Trans.To_Int(str(self.tradeValume))
        dictValue["tradeTurnover"] = myData_Trans.To_Float(str(self.tradeTurnover))
        dictValue["datetime"] =  self.date + " " + self.time
        return dictValue
    #转为JsonStr
    def toJsonstr(self):
        return myData_Json.Trans_ToJson_str(self.toDict())

    #转换为值组
    def toValueList(self):
        dtNow = self.getTime(False)
        if(len(self.dataList) > 1 and self.dataList[0] == dtNow and type(self.dataList[4]) != str):
           return self.dataList
        self.dataList = [] 
        self.dataList.append(dtNow)                                      #时间
        if(type(self.lastPrice) == str):
            self.dataList.append(myData_Trans.To_Float(self.lastPrice))      #最后价格
            self.dataList.append(myData_Trans.To_Float(self.highPrice))      #最高价格
            self.dataList.append(myData_Trans.To_Float(self.lowPrice))       #最低价格 
            self.dataList.append(myData_Trans.To_Float(self.buyPrice))       #买价
            self.dataList.append(myData_Trans.To_Float(self.sellPrice))      #卖价
            self.dataList.append(myData_Trans.To_Float(self.tradeValume))    #成交量
            self.dataList.append(myData_Trans.To_Float(self.tradeTurnover))  #成交额
        
            self.dataList.append(myData_Trans.To_Float(self.buy1Volume))     #买1-5量
            self.dataList.append(myData_Trans.To_Float(self.buy2Volume))   
            self.dataList.append(myData_Trans.To_Float(self.buy3Volume))   
            self.dataList.append(myData_Trans.To_Float(self.buy4Volume))   
            self.dataList.append(myData_Trans.To_Float(self.buy5Volume))  
            self.dataList.append(myData_Trans.To_Float(self.buy1Price))      #买1-5价格
            self.dataList.append(myData_Trans.To_Float(self.buy2Price))   
            self.dataList.append(myData_Trans.To_Float(self.buy3Price))   
            self.dataList.append(myData_Trans.To_Float(self.buy4Price))   
            self.dataList.append(myData_Trans.To_Float(self.buy5Price))   
        
            self.dataList.append(myData_Trans.To_Float(self.sell1Volume))    #卖1-5量
            self.dataList.append(myData_Trans.To_Float(self.sell2Volume))   
            self.dataList.append(myData_Trans.To_Float(self.sell3Volume))   
            self.dataList.append(myData_Trans.To_Float(self.sell4Volume))   
            self.dataList.append(myData_Trans.To_Float(self.sell5Volume))  
            self.dataList.append(myData_Trans.To_Float(self.sell1Price))     #卖1-5价格
            self.dataList.append(myData_Trans.To_Float(self.sell2Price))   
            self.dataList.append(myData_Trans.To_Float(self.sell3Price))   
            self.dataList.append(myData_Trans.To_Float(self.sell4Price))   
            self.dataList.append(myData_Trans.To_Float(self.sell5Price))   

            self.priceOpen = myData_Trans.To_Float(self.openPrice)           #开盘价格
            self.priceBase = myData_Trans.To_Float(self.preClose)            #前一收盘价格
        else:
            self.dataList.append((self.lastPrice))      #最后价格
            self.dataList.append((self.highPrice))      #最高价格
            self.dataList.append((self.lowPrice))       #最低价格 
            self.dataList.append((self.buyPrice))       #买价
            self.dataList.append((self.sellPrice))      #卖价
            self.dataList.append((self.tradeValume))    #成交量
            self.dataList.append((self.tradeTurnover))  #成交额
        
            self.dataList.append((self.buy1Volume))     #买1-5量
            self.dataList.append((self.buy2Volume))   
            self.dataList.append((self.buy3Volume))   
            self.dataList.append((self.buy4Volume))   
            self.dataList.append((self.buy5Volume))  
            self.dataList.append((self.buy1Price))      #买1-5价格
            self.dataList.append((self.buy2Price))   
            self.dataList.append((self.buy3Price))   
            self.dataList.append((self.buy4Price))   
            self.dataList.append((self.buy5Price))   
        
            self.dataList.append((self.sell1Volume))    #卖1-5量
            self.dataList.append((self.sell2Volume))   
            self.dataList.append((self.sell3Volume))   
            self.dataList.append((self.sell4Volume))   
            self.dataList.append((self.sell5Volume))  
            self.dataList.append((self.sell1Price))     #卖1-5价格
            self.dataList.append((self.sell2Price))   
            self.dataList.append((self.sell3Price))   
            self.dataList.append((self.sell4Price))   
            self.dataList.append((self.sell5Price))   

            self.priceOpen = self.openPrice           #开盘价格
            self.priceBase = self.preClose            #前一收盘价格
        self.priceRiseFall = self.dataList[1] / self.priceBase - 1       #涨跌幅 
        return self.dataList
    #由值组转换
    def fromValueList(self, lstValue):
        self.dataList = lstValue
        dtNow = lstValue[0]
        if(type(dtNow) == str): dtNow = myData_Trans.Tran_ToDatetime(dtNow)

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

        self.priceOpen = myData_Trans.To_Float(self.openPrice)  #开盘价格
        self.priceBase = myData_Trans.To_Float(self.preClose)   #前一收盘价格
        return True
         
    #获取播报消息 
    def getMsg_str(self, pSet = None):
        lstValue = self.toValueList()
        strValue = str(round(lstValue[1], 2))
        
        bIndex = False
        bOpt = False
        if(pSet != None):
            bIndex = pSet.isIndex 
            bOpt = pSet.stockInfo.type == 'opt'
        nDigit = myData.iif(bIndex, 3, 2)
        strUnit = myData.iif(bIndex, "", "元")
        price = myData.iif(bOpt == False, lstValue[1], lstValue[1] * 10000)
        strMsg = self.name + "：" + str(round(price, nDigit)) + strUnit
           
        #涨跌标识    
        dValue_N = self.priceRiseFall
        strTag0 = myData.iif(dValue_N >=0, "涨", "跌")
        strTag0 = myData.iif(dValue_N ==0, "平", strTag0) 
             
        dRF = dValue_N * 100
        strMsg += ", " + strTag0 + str(round(dRF,2)) + "%."  
        return strMsg

    #输出
    def Print(self):
        myDebug.Debug(self.toString())
        myDebug.Debug(self.toJsonstr())



#主启动程序
if __name__ == "__main__":
    pData = Data_Stock()
    
    pData.name = "建设银行"
    pData.date = myData_Trans.Tran_ToTime_str(None, "%Y-%m-%d")
    pData.time = myData_Trans.Tran_ToTime_str(None, "%H:%M:%S")
    pData.Print()

