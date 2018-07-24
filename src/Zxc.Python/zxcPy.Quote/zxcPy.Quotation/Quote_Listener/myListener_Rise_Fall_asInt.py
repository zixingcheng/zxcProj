#-*- coding: utf-8 -*-
"""
Created on  张斌 2018-05-03 14:58:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com

    监听--类 涨跌幅整数位
"""
import sys, os, math, mySystem 

#引用根目录类文件夹--必须，否则非本地目录起动时无法找到自定义类
mySystem.m_strFloders.append('/zxcPy.Quotation')
mySystem.Append_Us("", False)    
import myData, myQuote_Data, myQuote_Listener  
    

#行情监听--涨跌幅整数位
class Quote_Listener_Rise_Fall_asInt(myQuote_Listener.Quote_Listener):
    def __init__(self):
        myQuote_Listener.Quote_Listener.__init__(self, 'Rise_Fall_asInt')
        self.values = {}

    #处理接收信息
    def OnRecvQuote(self, quoteDatas): 
        #提取值
        key = quoteDatas.name
        dValue = self.values.get(key, 1)
        dValue_N = quoteDatas.datas_CKDs_M.CKD.Rise_Fall
        dDelta = dValue_N - dValue                  #当前-历史
        if(abs(dDelta) > 0.01):
            #涨跌幅达到整数位, 1%
            nRF = int(math.modf((dValue_N -1) * 100)[1])
            self.values[key] = nRF / 100            #更新记录值

            #计算涨跌返回对应说明标识
            strTag = ""
            if(dDelta > 0):                         #涨
                strTag = myData.iif(dValue_N >= 0, "涨逾", "跌幅收窄至")
            else:                                   #跌
                strTag = myData.iif(dValue_N <= 0, "跌逾", "涨幅收窄至")
            strMsg = key + "：" + strTag + str(nRF) + "%"
            
            #通知处理
            self.OnHandleMsg(quoteDatas, strMsg)
            
    #创建消息内容
    def OnCreatMsgstr(self, quoteDatas):
        strMsg = self.getName()

        return strMsg