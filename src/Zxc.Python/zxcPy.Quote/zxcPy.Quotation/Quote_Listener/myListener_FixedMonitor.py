#-*- coding: utf-8 -*-
"""
Created on  张斌 2018-05-03 14:58:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com

    监听--类 定点监控
"""
import sys, os, math, copy, mySystem 

#引用根目录类文件夹--必须，否则非本地目录起动时无法找到自定义类
mySystem.m_strFloders.append('/zxcPy.Quotation')
mySystem.Append_Us("../Quote_Source", False, __file__)
mySystem.Append_Us("", False)    
import myData, myQuote_Data, myQuote_Listener  


#定点监测类 
class myListener_Fixed():
    def __init__(self, monitorValue_Base, monitorValue, nNum, time):
        self.monitorValue_Base = monitorValue_Base  #基础值，一般为买入值，便于计算百分比
        self.monitorValue = monitorValue
        self.monitorType = 1                #正数为超过，负数为低于
        self.monitorValueMaxs = []          #监测到的最大值集 
        self.monitorValueMins = []          #监测到的最小值集
        self.poundage = 0.005               #手续费修正值 
        self.tradeNum = nNum                #交易数量
        self.tradeTime = time               #交易时间

        self.isPercentage = False           #是否为百分比
        self.warnTimes = 2                  #报警次数
        self.monitorStep = 1                #监测间隔
        if(monitorValue_Base > 0.5 and monitorValue < 0.5):
            self.isPercentage = True
        monitorType = 1
        if(self.isPercentage):
            if(monitorValue < 0): monitorValue = -1
        else:
            if(monitorValue < monitorValue_Base): monitorValue = -1
        self.monitorType = monitorValue
    def _getKey(self):
        strKey = myData.iif(self.monitorType > 0, "+", "-")
        strKey += str(round(self.monitorValue, 4)) + "-" +  str(round(self.monitorValue_Base, 4))
        return strKey

    #监测值     
    def checkValue(self, value):
        strReturn = ""
        strSufixPre = "    "
        if (self.monitorType > 0):   #超过判断
            if(self.isPercentage == True):  #百分比处理
                value = (value - self.monitorValue_Base) / self.monitorValue_Base - self.poundage

            #超限判断
            if(value >= self.monitorValue):  
                #超高限
                if(self.isPercentage == False):      #固定价格
                    valuePer = (value - self.monitorValue_Base) / self.monitorValue_Base - self.poundage
                    strReturn = str(self.monitorValue) + "元, 设定已达成.\n" + strSufixPre + "实际涨幅: " +  str(round(valuePer * 100, 2))  + "%."
                else:   #固定比例
                    valuePer = value
                    strReturn = str(round(self.monitorValue * 100, 2)) + "%, 设定已达成.\n" + strSufixPre + "实际涨幅: " + str(round(valuePer * 100, 2))  + "%."
        else:
            if(self.isPercentage == True):  #百分比处理
                value = (value - self.monitorValue_Base) / self.monitorValue_Base - self.poundage

            #超限判断
            if(value <= self.monitorValue):  
                #超低限
                if(self.isPercentage == False):      #固定价格
                    valuePer = (value - self.monitorValue_Base) / self.monitorValue_Base - self.poundage
                    strReturn = str(self.monitorValue) + "元, 设定已达成.\n" + strSufixPre + "实际跌幅: " +  str(round(valuePer * 100, 2))  + "%."
                else:   #固定比例
                    valuePer = value
                    strReturn = str(round(self.monitorValue * 100, 2)) + "%, 设定已达成.\n" + strSufixPre + "实际跌幅: " + str(round(valuePer * 100, 2))  + "%."

                     
        #if(valuePer > 0.003): strReturn += ".\n" + strSufixPre + "盈利逾3%，建议止盈"

        #详情信息
        if(strReturn == ""): return  strReturn
        strReturn += "\n" + strSufixPre + "交易量价: " +  str(round(self.tradeNum, 0)) + "股, " + str(self.monitorValue_Base) + "元.\n" + strSufixPre + "交易时间: " + self.tradeTime

        return strReturn
                
#行情监听--涨跌幅整数位
class Quote_Listener_FixedMonitor(myQuote_Listener.Quote_Listener):
    def __init__(self):
        myQuote_Listener.Quote_Listener.__init__(self, 'FixedMonitor')
        self.monitors = {}
    def _addMonitor(self, key, pMonitor):
        if(type(pMonitor) != myListener_Fixed): return False
        monitor = self.monitors.get(key, None)
        if(monitor == None):
            monitor = {}
            self.monitors[key] = monitor
        monitor[pMonitor._getKey()] = pMonitor 

    #处理接收信息
    def OnRecvQuote(self, quoteDatas): 
        #设置有效检查
        if(self.IsEnable(quoteDatas)== False): return
        
        #提取值
        dValue_N = quoteDatas.datas_CKDs_M.data.value       #当前价格
        key = quoteDatas.name

        #处理
        bIsIndex = False
        self.monitor = self.monitors.get(key, {})
        for x in self.monitor.keys():
            pMonitor = self.monitor.get(x, None)
            if(pMonitor == None): continue

            strTemp = pMonitor.checkValue(dValue_N)
            if(strTemp != ""):
                #通知处理,组装返回结果
                strMsg = quoteDatas.data.getMsg_str(bIsIndex)
                for x in range(0, pMonitor.warnTimes):
                    strMsg += "\n定点监测: " + strTemp + "."
                    self.OnHandleMsg(quoteDatas, strMsg)  

    #功能是否可用
    def IsEnable(self, quoteDatas):
        return True
        return quoteDatas.setting.isEnable_RFasInt
    


#主启动程序--测试
if __name__ == "__main__":
    import time
    import mySource_Sina_Stock
    import myListener_Printer, myListener_Rise_Fall_asInt, myListener_Hourly

    #示例数据监控(暂只支持单源，多源需要调整完善)
    pQuote = mySource_Sina_Stock.Source_Sina_Stock('sh600822')
    pListener = Quote_Listener_FixedMonitor() 
    pQuote.addListener(pListener)

    #添加固定监测项
    key = '上海物贸'
    #pListener._addMonitor(key, myListener_Fixed(10.8, 11.32, 1000, "2018-08-19"))
    #pListener._addMonitor(key, myListener_Fixed(11.8, 11.32, 1000, "2018-08-19"))
    #pListener._addMonitor(key, myListener_Fixed(10.8, 0.04, 1000, "2018-08-19"))
    pListener._addMonitor(key, myListener_Fixed(11.8, -0.02, 1000, "2018-08-19"))

    #查询数据
    while True:
        pQuote.query()
        time.sleep(3)
         
    print()