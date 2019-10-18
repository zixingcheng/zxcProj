#-*- coding: utf-8 -*-
"""
Created on  张斌 2018-05-03 14:58:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com

    监听-数据对象 
"""
import sys, os, datetime, mySystem 

#引用根目录类文件夹--必须，否则非本地目录起动时无法找到自定义类
mySystem.m_strFloders.append('/zxcPy.Quotation')
mySystem.Append_Us("", False)    
import myQuote_Data, myData, myData_Trans, myDebug


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
        self.dataList = []
        self.priceOpen = 0      #开盘价格
        self.priceBase = 0      #前一收盘价格
        self.priceRiseFall = 0  #涨跌幅

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
        return '\n' + self.date + " " + self.time  \
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
        if(len(self.dataList) > 1 and self.dataList[0] == dtNow and type(self.dataList[4]) != str):
           return self.dataList
        self.dataList = [] 
        self.dataList.append(dtNow)                                      #时间
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
    def getMsg_str(self, bIndex = False):
        lstValue = self.toValueList()
        strValue = str(round(lstValue[1], 2))
        
        strMsg = self.name + ": "  
        if(bIndex == False):
            strMsg += + str(round(lstValue[1], 2)) + "元"
        else:
            strMsg += + str(round(lstValue[1], 3)) 
            
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

#行情数据对象--统计 
class Datas_M_Stock(myQuote_Data.Quote_Data_Statics_M):
    def __init__(self, tagTime, data = Data_Stock(), lastCKD = None, interval_M = -1): 
        super().__init__(tagTime, data, lastCKD, interval_M)

    #其他统计接口
    def setData_Statics(self, pData):
        datas = pData.toValueList()
        self.dataS.tradeTurnover_End = datas[7] 
        self.dataS.tradeVolume_End = datas[6]  
       
#数据对象--统计集 
class Datas_D_Stock(myQuote_Data.Quote_Data_Statics_D):
    #依次：时间标签，初始值，统计间隔
    def __init__(self, data = Data_Stock(), interval_M = -1, bSetData = True): 
        super().__init__(data, interval_M, bSetData)
        
    #初始统计对象 
    def newData_S(self, tagTime, data):
        pData_S = Datas_M_Stock(tagTime, data, self.dataS_Min_Now, self.interval_M)  
        return pData_S

    #同步信息统计--天
    def sameDataS_Day(self, pData):
        datas = pData.toValueList()  
        self.dataS_Day.dtTime = pData.getTime()
        self.dataS_Day.start = pData.priceOpen
        self.dataS_Day.base = pData.priceBase
         
        self.dataS_Day.last = datas[1] 
        self.dataS_Day.high = datas[2] 
        self.dataS_Day.low = datas[3] 
        self.dataS_Day.tradeVolume = datas[6] 
        self.dataS_Day.tradeTurnover = datas[7] 
        self.dataS_Day.tradeVolume_End = datas[6] 
        self.dataS_Day.tradeTurnover_End = datas[7] 
        self.dataS_Day.average = self.dataS_Day.tradeTurnover / self.dataS_Day.tradeVolume  
         

#行情数据对象集
class Datas_Stock(myQuote_Data.Quote_Datas):
    def __init__(self, pData, interval = 1):
        super().__init__(pData, interval)
        
    #初始统计对象 
    def newData_S(self, pData):
        return Datas_D_Stock(pData, self.interval_M, False)
    
    #其他统计接口
    def dataStatics(self, minute = 5):
        #统计指定时间内数据
        dNow = self.datas_CKDs_M.data.lastPrice
        dMin = dNow
        dMax = dNow
        dtEnd = self.datas_CKDs_M.CKD.tag
        dtStart = self.datas_CKDs_M.CKD.tag
        nSeconds = 0
        if(len(self.datas_CKDs_M.CKDs) > minute * 10000):
            for x in range(0, minute):
                dtTime = dtEnd - datetime.timedelta(minutes = x)
                pCKD = self.datas_CKDs_M.CKDs.get(dtTime, None)
                if(pCKD != None):
                    if(dMin > pCKD.low): dMin = pCKD.low
                    if(dMax < pCKD.high): dMax = pCKD.high

                    #起始时间
                    dtStart = pCKD.tag

        #计算方向
        pData = myQuote_Data.Quote_Data_Static()
        #pData.high = dMax
        #pData.low = dMin
        #pData.last = dNow
        #pData.seconds = (dtEnd - dtStart).seconds
        return pData


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

