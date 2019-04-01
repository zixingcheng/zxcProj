#-*- coding: utf-8 -*-
"""
Created on  张斌 2018-05-03 14:58:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com

    监听--类 定点监控
"""
import sys, os, math, copy, datetime, mySystem 

#引用根目录类文件夹--必须，否则非本地目录起动时无法找到自定义类
mySystem.m_strFloders.append('/zxcPy.Quotation')
mySystem.Append_Us("../Quote_Source", False, __file__)
mySystem.Append_Us("", False)    
import myData, myData_Trans, myQuote_Data, myQuote_Listener  


#定点监测类 
class myListener_Fixed():
    def __init__(self, monitorValue_Base, monitorValue, nNum, time):
        self.monitorValue_Base = monitorValue_Base  #基础值，一般为买入值，便于计算百分比
        self.monitorValue = monitorValue
        self.monitorType = 1                #正数为超过，负数为低于
        self.monitorValueMax = -9999        #监测到的最大值
        self.monitorValueMin = 9999         #监测到的最小值
        self.poundage = 0.0018              #手续费修正值(万三，实际双向为0.16%，考虑最小交易手续费，默认为0.18%)
        self.tradeNum = nNum                #交易数量
        self.tradeTime = time               #交易时间
        self.lastValue = -9999              #上次监控价格
        self.vecTrend = []                  #趋势

        self.isPercentage = False           #是否为百分比
        self.warnTimes = 2                  #报警次数
        self.monitorStep = 0.01             #监测间隔
        if(monitorValue_Base > 0.5 and monitorValue < 0.5):
            self.isPercentage = True
        monitorType = 1
        if(self.isPercentage):
            if(monitorValue < 0): monitorValue = -1
        else:
            if(monitorValue < monitorValue_Base): monitorValue = -1
        self.monitorType = monitorValue
    def _getKey(self):
        strKey = myData.iif(self.monitorType > 0, "+", "")
        strKey += str(round(self.monitorValue, 4)) + "-" +  str(round(self.monitorValue_Base, 4))
        return strKey

    #监测值     
    def checkValue(self, value):
        strReturn = ""
        strSufixPre = "    "
        strSuggest = ""
        strSuggest2 = ""

        #差价比例控制
        valuePer = (value - self.monitorValue_Base) / self.monitorValue_Base - self.poundage
        if(self.lastValue == -9999): self.lastValue = self.monitorValue_Base
        valuePer_L = (self.lastValue - self.monitorValue_Base) / self.monitorValue_Base - self.poundage


        #高低限处理
        if (self.monitorType > 0):   #超过判断
            #上涨区间控制
            if(abs(valuePer - valuePer_L) < 0.0025):    #上涨，区间必须大于0.25%,最大幅度0.5%
                return strReturn

            #超限判断
            if(self.isPercentage == True): value = valuePer     #百分比处理
            if(value >= self.monitorValue):  
                #超高限
                if(self.isPercentage == False):                 #固定价格 
                    valuePer_M = (self.monitorValue - self.monitorValue_Base) / self.monitorValue_Base - self.poundage
                    strReturn = str(self.monitorValue) + "元, 设定已达成.\n" + strSufixPre + "实际涨幅: " +  str(round(valuePer * 100, 2))  + "%." 
                else:   #固定比例
                    valuePer_M = self.monitorValue
                    strReturn = str(round(self.monitorValue * 100, 2)) + "%, 设定已达成.\n" + strSufixPre + "实际涨幅: " + str(round(valuePer * 100, 2))  + "%."

                #成交建议
                if(True):
                    #self.monitorValueMax = (11.8 - self.monitorValue_Base) / self.monitorValue_Base - self.poundage
                    if(self.monitorValueMax == -9999): self.monitorValueMax = valuePer_M 
                    deltaValue = valuePer - self.monitorValueMax
                    if(abs(deltaValue) > self.monitorStep):
                        if(deltaValue < 0):
                            strSuggest = "回调逾" + str(round(deltaValue * 100, 2)) + "%，建议止盈."
                        else:
                            strSuggest = "预期盈利逾" + str(round((valuePer - valuePer_M) * 100, 1)) + "%，建议止盈."
                    else:
                        strSuggest = "预期盈利，建议止盈."

                    #趋势提醒
                    nTrend = myData.iif(valuePer > valuePer_L, 1, -1)
                    self.vecTrend.append(nTrend)
                    if(nTrend > 0):
                        strSuggest2 = "短期上涨."
                    else:
                        strSuggest2 = "短期下跌."
                    if(self.monitorValueMax < valuePer): self.monitorValueMax = valuePer    #更新最大值处理
        else: 
            #下跌区间控制
            if(abs(valuePer - valuePer_L) < 0.0025):    #下跌，区间必须大于0.25%,最大幅度0.5%
                return strReturn 

            #超限判断
            if(self.isPercentage == True): value = valuePer     #百分比处理
            if(value <= self.monitorValue):  
                #超低限
                if(self.isPercentage == False):                 #固定价格 
                    valuePer_M = (self.monitorValue - self.monitorValue_Base) / self.monitorValue_Base - self.poundage
                    strReturn = str(self.monitorValue) + "元, 设定已达成.\n" + strSufixPre + "实际跌幅: " +  str(round(valuePer * 100, 2))  + "%."
                else:   #固定比例
                    valuePer_M = self.monitorValue
                    strReturn = str(round(self.monitorValue * 100, 2)) + "%, 设定已达成.\n" + strSufixPre + "实际跌幅: " + str(round(valuePer * 100, 2))  + "%."
                    
                #成交建议
                if(True):
                    #self.monitorValueMin = (11.2 - self.monitorValue_Base) / self.monitorValue_Base - self.poundage
                    if(self.monitorValueMin == 9999): self.monitorValueMin = valuePer_M 
                    deltaValue = valuePer - self.monitorValueMin
                    if(abs(deltaValue) > self.monitorStep):
                        if(deltaValue > 0):
                            strSuggest = "回调逾" + str(round(deltaValue * 100, 2)) + "%，建议止损."
                        else:
                            strSuggest = "预期亏损逾" + str(round((valuePer - valuePer_M) * 100, 1)) + "%，建议止损."
                    else:
                        strSuggest = "预期亏损，建议止损."

                    #趋势提醒
                    nTrend = myData.iif(valuePer > valuePer_L, 1, -1)
                    self.vecTrend.append(nTrend)
                    if(nTrend > 0):
                        strSuggest2 = "短期上涨."
                    else:
                        strSuggest2 = "短期下跌."
                    if(self.monitorValueMin < valuePer): self.monitorValueMin = valuePer    #更新最小值处理
        if(strReturn == ""): return  strReturn

        #详情信息
        self.lastValue = round((value + self.poundage + 1) * self.monitorValue_Base, 2)     #实际价格   
        if(self.tradeNum > 0):
            strReturn += "\n" + strSufixPre + "交易量价: " +  str(round(self.tradeNum, 0)) + "股, " + str(self.monitorValue_Base) + "元.\n" + strSufixPre + "交易时间: " + self.tradeTime + "."
        strReturn += "\n交易建议：" 
        strReturn += "\n" + strSufixPre + strSuggest2
        strReturn += "\n" + strSufixPre + strSuggest
        return strReturn
                
#行情监听--涨跌幅整数位
class Quote_Listener_FixedMonitor(myQuote_Listener.Quote_Listener):
    def __init__(self, usrName = 'Test'):
        myQuote_Listener.Quote_Listener.__init__(self, 'FixedMonitor')
        self.usrName = usrName
        self.monitors = {}
    def _addMonitor(self, key, pMonitor):
        if(type(pMonitor) != myListener_Fixed): return False
        monitor = self.monitors.get(key, None)
        if(monitor == None):
            monitor = {}
            self.monitors[key] = monitor
        monitor[pMonitor._getKey()] = pMonitor 
    def _removeMonitor(self, key, bNew = False):
        if(self.monitors.get(key, None) != None and bNew == True):
            self.monitors[key] = {}

    #更新定点配置
    def OnUpdataSet(self, quoteDatas):
        #设置有效检查
        if(self.IsEnable(quoteDatas)== False): return

        #买入交易记录
        lstBill = quoteDatas.queryTrade(self.usrName)

        #生成所有定点监测配置 
        self._removeMonitor(quoteDatas.name)
        for x in lstBill:
            if(x.tradeNum_Stock < 100): continue    #忽略剩余量较少的

            tradePrice = x.tradePrice
            tradeNum = x.tradeNum_Stock          #交易数量
            tradeTime = x.tradeTime
            if(type(tradeTime) == datetime.datetime):
                tradeTime = myData_Trans.Tran_ToDatetime_str(tradeTime, "%Y-%m-%d")

            #生成配置
            self._addMonitor(quoteDatas.name, myListener_Fixed(tradePrice, 0.04, tradeNum, tradeTime))
            self._addMonitor(quoteDatas.name, myListener_Fixed(tradePrice, -0.02, tradeNum, tradeTime))  
        return True
    #处理接收信息
    def OnRecvQuote(self, quoteDatas): 
        #设置有效检查
        if(self.IsEnable(quoteDatas)== False): return
        
        #提取值
        dValue_N = quoteDatas.datasS_M.data.value       #当前价格
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
                strMsg_str = quoteDatas.data.getMsg_str(bIsIndex)
                for x in range(0, pMonitor.warnTimes):
                    strMsg = strMsg_str + "\n定点监测: " + strTemp 
                    self.OnHandleMsg(quoteDatas, strMsg, 5 * x )    # 多次延时提醒
                    print(strMsg)

    #功能是否可用
    def IsEnable(self, quoteDatas):
        return False 
    


#主启动程序--测试
if __name__ == "__main__":
    import time
    import mySource_Sina_Stock
    import myListener_Printer, myListener_Rise_Fall_asInt, myListener_Hourly

    #示例数据监控(暂只支持单源，多源需要调整完善)
    pQuote = mySource_Sina_Stock.Source_Sina_Stock('sz002124')
    pListener = Quote_Listener_FixedMonitor() 
    pQuote.addListener(pListener)
    pQuote.addListener(myListener_Printer.Quote_Listener_Printer())

    #添加固定监测项
    key = '天邦股份'
    #pListener._addMonitor(key, myListener_Fixed(10.8, 11.2, 1000, "2018-08-19"))
    #pListener._addMonitor(key, myListener_Fixed(11.8, 11.5, 1000, "2018-08-19"))
    #pListener._addMonitor(key, myListener_Fixed(10.8, 0.03, 1000, "2018-08-19"))
    #pListener._addMonitor(key, myListener_Fixed(11.8, -0.04, 1000, "2018-08-19"))
    pListener._addMonitor(key, myListener_Fixed(5.36, -0.04, 0, "2018-08-19"))
    pListener._addMonitor(key, myListener_Fixed(5.33, 0.06, 0, "2018-08-19"))

    #查询数据
    while True:
        pQuote.query()
        time.sleep(3)
         
    print()