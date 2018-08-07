#-*- coding: utf-8 -*-
"""
Created on  张斌 2018-05-03 14:58:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com

    监听--类 涨跌幅整数倍
"""
import sys, os, math, copy, mySystem 

#引用根目录类文件夹--必须，否则非本地目录起动时无法找到自定义类
mySystem.m_strFloders.append('/zxcPy.Quotation')
mySystem.Append_Us("", False)    
import myData, myQuote_Data, myQuote_Listener  
    

#行情监听--涨跌幅整数位
class Quote_Listener_Rise_Fall_asInt(myQuote_Listener.Quote_Listener):
    def __init__(self):
        myQuote_Listener.Quote_Listener.__init__(self, 'Rise_Fall_asInt')
        self.values = {}
        self.data = {'max':-0.1, 'min':0.1, 'now':0}        #值结构
        self.deltaV = 0.5 / 100;

    #处理接收信息
    def OnRecvQuote(self, quoteDatas): 
        #设置有效检查
        if(self.IsEnable(quoteDatas)== False): return
        
        #提取值
        dValue_N = quoteDatas.datas_CKDs_M.CKD.Rise_Fall    #当前涨跌幅
        key = quoteDatas.name

        #通知处理
        strMsg = self.DoRecvQuote(dValue_N, key, quoteDatas.datas_CKDs_M.data, quoteDatas.setting.isIndex)
        self.OnHandleMsg(quoteDatas, strMsg)
    def DoRecvQuote(self, dValue_N, key, data, bIndex): 
        strTag_suffix = ""
        value = self.values.get(key, None)
        nTim_M = -1
        if(value == None):
            #实例值对象
            value = copy.deepcopy(self.data)
            value['max'] = dValue_N
            value['min'] = dValue_N
            value['time'] = data.getTime()
            self.values[key] = value
            strTag_suffix = "."
        else:
            dtTime = data.getTime() - value['time']
            nTim_M = math.ceil(dtTime.seconds / 60)
        
        #判断涨跌幅
        dValue = value['now']                               #前一个记录值
        dDelta = dValue_N - dValue                          #当前-历史的差值
         
        #涨跌超限值
        if(abs(dDelta) >= self.deltaV):
            #涨跌幅达到间隔值整数倍, 计算记录新值
            nTimes = int(dDelta / self.deltaV)
            value['now'] = dValue + nTimes * self.deltaV    #更新记录值
            value['time'] = data.getTime()
            
            #涨跌幅突破标识
            if(value['max'] < dValue_N):
                value['max'] = dValue_N
                if(dValue_N > 0): strTag_suffix = ", 涨幅新高."
            if(value['min'] > dValue_N):
                value['min'] = dValue_N
                if(dValue_N < 0): strTag_suffix = ", 跌幅加深."
                
            #时间标识
            strTag_M = ""  
            if(nTim_M >= 0 and nTim_M <99): strTag_M = str(nTim_M) + "分钟"
            if(strTag_M == ""): strTag_M = "区间"

            #计算涨跌返回对应说明标识
            strTag = ""  
            strDelta = str(round(nTimes * self.deltaV * 100, 2)) + "%"
            if(dDelta > 0):
                #涨
                strTag = strTag_M + "涨超: " + strDelta 
            else:
                strTag = strTag_M + "跌逾: " + strDelta 

            #涨跌反转标识 
            if(dValue_N >= 0 and dValue >= 0):
                nTimes2 = int(value['max'] / self.deltaV)
                if(strTag_suffix == "" and abs(nTimes2) > 1): 
                    strTag_suffix = ", 涨幅回落."
            else:
                nTimes2 = int(value['min'] / self.deltaV)
                if(strTag_suffix == "" and abs(nTimes2) > 1): 
                    strTag_suffix = ", 跌幅收窄."
                
            #涨跌反转标识    
            strTag0 = myData.iif(dValue_N >=0, "涨", "跌")
            strTag0 = myData.iif(dValue_N ==0, "平", strTag0) 
            
            #组装返回结果
            #strMsg = "创业板指: 10000.34, 涨+10.01%;\n99分钟涨幅: 10.5%, 涨幅新高."
            strMsg = data.getMsg_str(bIndex) 
            if(len(strMsg) < 24):       #定长度格式修正
                strMsg += " " * (24 - len(strMsg))
            print(len(strMsg))

            if(strTag != "" and strTag_suffix != ""):
                strMsg += "\n" + strTag + strTag_suffix
            return strMsg
        return ""

    #功能是否可用
    def IsEnable(self, quoteDatas):
        return quoteDatas.setting.isEnable_RFasInt
    


#主启动程序--测试
if __name__ == "__main__":
    pListener = Quote_Listener_Rise_Fall_asInt()
    #pListener.deltaV = 0.01

    #测试
    key = '建设银行'
    pListener.OnRecvQuote(0.032, key)
    pListener.OnRecvQuote(0.041, key)
    pListener.OnRecvQuote(0.0453, key)
    pListener.OnRecvQuote(0.0152, key)
    pListener.OnRecvQuote(0.01, key)
    pListener.OnRecvQuote(0.0, key)
    pListener.OnRecvQuote(-0.0051, key)
    pListener.OnRecvQuote(-0.0152, key)
    pListener.OnRecvQuote(-0.0453, key)
    pListener.OnRecvQuote(-0.012, key)
    pListener.OnRecvQuote(0.0, key)
    pListener.OnRecvQuote(0.051, key)

    print()