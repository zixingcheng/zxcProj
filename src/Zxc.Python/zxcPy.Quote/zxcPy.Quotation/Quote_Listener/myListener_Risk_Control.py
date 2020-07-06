#-*- coding: utf-8 -*-
"""
Created on  张斌 2020-07-02 11:58:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com

    监听--类 风险控制-止盈止损
"""
import sys, os, math, copy, mySystem 

#引用根目录类文件夹--必须，否则非本地目录起动时无法找到自定义类
mySystem.m_strFloders.append('/zxcPy.Quotation')
mySystem.Append_Us("../Quote_Source", False, __file__)
mySystem.Append_Us("../Quote_Data/Data_Risk", False, __file__)
mySystem.Append_Us("", False)    
import myData, myQuote_Data, myQuote_Listener, myData_StockRisk
from myGlobal import gol  
    

#风险控制-止盈止损
class Quote_Listener_Risk_Control(myQuote_Listener.Quote_Listener):
    def __init__(self):
        myQuote_Listener.Quote_Listener.__init__(self, 'Risk_Control')
        self.nameAlias = "风控监测"
        self.pRisks = gol._Get_Value('zxcRisk_Control')

    #处理接收信息
    def OnRecvQuote(self, quoteDatas): 
        #设置有效检查
        #if(self.IsEnable(quoteDatas)== False): return
        
        #提取值
        dValue_N = quoteDatas.datasS_M.dataS_Min_Now.dataS.getRise_Fall(0)  #当前涨跌幅
        key = quoteDatas.name

        #通知处理
        strMsg = self.DoRecvQuote(dValue_N, key, quoteDatas.datasS_M.data, quoteDatas.setting)
        if(strMsg != ""):
            self.OnHandleMsg(quoteDatas, strMsg)
    def DoRecvQuote(self, dValue_N, key, data, pSet): 
        strTag_suffix = ""
        price = data.value
        if(pSet.stockInfo.type == 'opt'):
            price = price * 10000           # 期权行情值修正
        
        #调用风险监测
        self.pRisks.notifyRisk(price, pSet.setTag, pSet.stockInfo.code_name, False)
        return "" 
    


#主启动程序--测试
if __name__ == "__main__":    
    import time
    import mySource_Sina_Stock
    import myListener_Printer, myListener_Hourly

    #示例数据监控(暂只支持单源，多源需要调整完善)
    pQuote = mySource_Sina_Stock.Source_Sina_Stock('sh600060')
    pQuote.addListener(Quote_Listener_Risk_Control())
    pQuote.addListener(myListener_Printer.Quote_Listener_Printer())
    
    #查询数据
    while True:
        pQuote.query()
        time.sleep(3)
         
    print()