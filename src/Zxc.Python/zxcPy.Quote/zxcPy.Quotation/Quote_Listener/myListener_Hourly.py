#-*- coding: utf-8 -*-
"""
Created on  张斌 2018-07-31 11:58:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com

    监听--类 整点播报
"""
import sys, os, datetime, mySystem 

#引用根目录类文件夹--必须，否则非本地目录起动时无法找到自定义类
mySystem.m_strFloders.append('/zxcPy.Quotation')
mySystem.Append_Us("", False)    
import myData_Trans, myQuote_Data, myQuote_Listener  
    

#行情监听--整点播报
class myListener_Hourly(myQuote_Listener.Quote_Listener):
    def __init__(self):
        myQuote_Listener.Quote_Listener.__init__(self, 'Hourly')
        self.values = {}

    #处理接收信息
    def OnRecvQuote(self, quoteDatas): 
        #设置有效检查
        if(self.IsEnable()== False): return
        
        #提取值--时间
        dtNow = quoteDatas.data.getTime()
        if(dtNow.minute == 0 or dtNow.minute == 30):
            #提取值
            dValue_N = quoteDatas.datas_CKDs_M.CKD.Rise_Fall    #当前值
            key = quoteDatas.name

            #判断是否已经记录
            lstValue = self.values.get(key, None) 
            if(lstValue == None):
                lstValue = {}
                self.values[key] = lstValue

            strTime = myData_Trans.Tran_ToDatetime_str(dtNow, "%H:%M") + ":00"
            if(lstValue.get(strTime, None) == None):
                lstValue[strTime] = dValue_N                    #记录值

                #生成返回信息
                if(dValue_N > 0):
                    strTag = "涨"
                elif(dValue_N > 0):
                    strTag = "跌"
                else:
                    strTag = "平"
            
                #组装返回结果
                dRF = dValue_N * 100
                strMsg = key + ": " + strTag + str(round(dRF,2)) + "%,  at " + strTime + "."

                #通知处理
                self.OnHandleMsg(quoteDatas, strMsg) 

    #功能是否可用
    def IsEnable(self, quoteDatas):
        return quoteDatas.setting.isEnable_Hourly
    

