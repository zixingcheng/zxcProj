#-*- coding: utf-8 -*-
"""
Created on  张斌 2018-05-03 14:58:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com

    监听--类 涨跌监测-涨跌幅整数倍
"""
import sys, os, math, copy, mySystem 

#引用根目录类文件夹--必须，否则非本地目录起动时无法找到自定义类
mySystem.m_strFloders.append('/zxcPy.Quotation')
mySystem.Append_Us("../Quote_Source", False, __file__)
mySystem.Append_Us("", False)    
import myData, myQuote_Data, myQuote_Listener 
from myGlobal import gol  
    

#行情监听--涨跌幅整数位
class Quote_Listener_Rise_Fall_asInt(myQuote_Listener.Quote_Listener):
    def __init__(self):
        myQuote_Listener.Quote_Listener.__init__(self, 'Rise_Fall_asInt')
        self.nameAlias = "涨跌监测"
        self.values = {}
        self.data = {'max':-0.1, 'min':0.1, 'now':0}        #值结构
        self.deltaV = 0.5 / 100;

    #处理接收信息
    def OnRecvQuote(self, quoteDatas): 
        #设置有效检查
        if(self.IsEnable(quoteDatas)== False): return
        
        #提取值
        dValue_N = quoteDatas.datasS_M.dataS_Min_Now.dataS.getRise_Fall(0)  #当前涨跌幅
        key = quoteDatas.name

        #通知处理
        strMsg = self.DoRecvQuote(dValue_N, key, quoteDatas.datasS_M.data, quoteDatas.setting)
        if(strMsg != ""):
            self.OnHandleMsg(quoteDatas, strMsg)
    def DoRecvQuote(self, dValue_N, key, data, pSet): 
        strTag_suffix = ""
        value = self.values.get(key, None)
        nTim_M = -1
        if(value == None):
            #提取当前统计对象
            pDatas_S = gol._Get_Value('datas_Stics_D_' + data.id, None)     #全局统计信息
            pData_S = pDatas_S[0]
            
            #实例值对象
            value = copy.deepcopy(self.data)
            value['max'] = pData_S.high / pData_S.base - 1
            value['min'] = pData_S.low / pData_S.base - 1
            value['time'] = data.getTime()
            self.values[key] = value
            strTag_suffix = ""
        else:
            dtTime = data.getTime() - value['time']
            nTim_M = math.ceil(dtTime.seconds / 60)
        
        #判断涨跌幅
        dValue = value['now']                               #前一个记录值
        dDelta = dValue_N - dValue                          #当前-历史的差值
         
        #涨跌超限值
        deltaV = self.deltaV
        if(pSet.isIndex): deltaV = self.deltaV / 2                  #提高一倍精度
        if(pSet.stockInfo.type == 'opt'): deltaV = self.deltaV * 5  #降低五倍精度
        if(abs(dDelta) >= deltaV):
            #涨跌幅达到间隔值整数倍, 计算记录新值
            nTimes = int(dDelta / deltaV)
            value['now'] = dValue + nTimes * deltaV         #更新记录值
            value['time'] = data.getTime()
            
            #涨跌幅突破标识
            if(value['max'] < dValue_N):
                value['max'] = dValue_N
                if(dValue_N > 0): 
                    strTag_suffix = ", 涨幅新高" + self.CheckDays_MaxMin(dValue_N, data.id) + "."
            if(value['min'] > dValue_N):
                value['min'] = dValue_N
                if(dValue_N < 0):
                    strTag_suffix = ", 跌幅新低" + self.CheckDays_MaxMin(dValue_N, data.id, False) + "."
                
            #时间标识
            strTag_M = ""  
            if(nTim_M >= 0 and nTim_M < 99): strTag_M = str(nTim_M) + "分钟"
            if(strTag_M == ""): strTag_M = "区间"

            #计算涨跌返回对应说明标识
            strTag = ""  
            strDelta = str(round(nTimes * deltaV * 100, 2)) + "%"
            if(dDelta > 0):
                #涨
                strTag = strTag_M + "涨超：" + strDelta 
            else:
                strTag = strTag_M + "跌逾：" + strDelta 

            #涨跌反转标识 
            if(dValue_N >= 0 and dValue >= 0):
                nTimes2 = int(value['max'] / deltaV)
                if(strTag_suffix == "" and abs(nTimes2) > 1): 
                    dDelta2 = value['max'] - dValue_N
                    strDelta2 = str(round(dDelta2 * 100, 2)) + "%"
                    strTag_suffix = ", 涨幅回落 " + strDelta2 + "."
            else:
                nTimes2 = int(value['min'] / deltaV)
                if(strTag_suffix == "" and abs(nTimes2) > 1): 
                    dDelta2 = dValue_N - value['min']
                    strDelta2 = str(round(dDelta2 * 100, 2)) + "%"
                    strTag_suffix = ", 跌幅收窄 " + strDelta2 + "."
                
            #涨跌反转标识    
            strTag0 = myData.iif(dValue_N >=0, "涨", "跌")
            strTag0 = myData.iif(dValue_N ==0, "平", strTag0) 
            
            #组装返回结果
            #strMsg = "创业板指: 10000.34, 涨+10.01%;\n99分钟涨幅: 10.5%, 涨幅新高."
            strMsg = data.getMsg_str(pSet) 
            if(len(strMsg) < 24):       #定长度格式修正
                strMsg += " " * (24 - len(strMsg)) 

            if(strTag != "" and strTag_suffix != ""):
                strMsg += "\n" + strTag + strTag_suffix
            return strMsg
        return ""
    #检查最大最小N天--需完善
    def CheckDays_MaxMin(self, dValue, key, bMax = True):
        pDatas_S = gol._Get_Value('datas_Stics_D_' + key, None)    #全局统计信息
        if(pDatas_S == None): return ""
        nDay = 0
        if(bMax):
            for x in range(1, len(pDatas_S)):
                if(dValue < pDatas_S[x].high):
                    nDay = x
                    break
        else:
            for x in range(1, len(pDatas_S)):
                if(dValue > pDatas_S[x].low):
                    nDay = x
                    break
        if(nDay == 0): return ""
        return "(" + str(nDay) + "天)" 
    


#主启动程序--测试
if __name__ == "__main__":
    #pListener = Quote_Listener_Rise_Fall_asInt()
    #pListener.deltaV = 0.01

    #测试
    #key = '建设银行'
    #pListener.DoRecvQuote(0.032, key)
    #pListener.DoRecvQuote(0.041, key)
    #pListener.DoRecvQuote(0.0453, key)
    #pListener.DoRecvQuote(0.0152, key)
    #pListener.DoRecvQuote(0.01, key)
    #pListener.DoRecvQuote(0.0, key)
    #pListener.DoRecvQuote(-0.0051, key)
    #pListener.DoRecvQuote(-0.0152, key)
    #pListener.DoRecvQuote(-0.0453, key)
    #pListener.DoRecvQuote(-0.012, key)
    #pListener.DoRecvQuote(0.0, key)
    #pListener.DoRecvQuote(0.051, key)
    
    import time
    import mySource_Sina_Stock
    import myListener_Printer, myListener_Hourly

    #示例数据监控(暂只支持单源，多源需要调整完善)
    pQuote = mySource_Sina_Stock.Source_Sina_Stock('sh600060')
    pQuote.addListener(Quote_Listener_Rise_Fall_asInt())
    pQuote.addListener(myListener_Printer.Quote_Listener_Printer())
    
    #查询数据
    while True:
        pQuote.query()
        time.sleep(3)
         
    print()