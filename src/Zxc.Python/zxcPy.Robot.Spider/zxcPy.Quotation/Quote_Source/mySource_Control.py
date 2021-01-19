#-*- coding: utf-8 -*-
"""
Created on  张斌 2020-06-23 18:58:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com

    行情爬取--统一源类(多源) 
"""
import sys, os, time, mySystem 

#引用根目录类文件夹--必须，否则非本地目录起动时无法找到自定义类
mySystem.m_strFloders.append('/zxcPy.Quotation')
mySystem.m_strFloders.append('/zxcPy.Quotation/Quote_Data')
mySystem.m_strFloders.append('/zxcPy.Quotation/Quote_Listener')
mySystem.Append_Us("", False)    
import myData_Trans
import myQuote_Data, myData_Stock, myQuote_Listener, myQuote_Source  
import mySource_Sina_Stock, mySource_JQData_Stock
from myGlobal import gol 
gol._Init()                 #先必须在主模块初始化（只在Main模块需要一次即可）



#行情源--控制
class Source_Control(myQuote_Source.Quote_Source):
    def __init__(self, params = ""):
        myQuote_Source.Quote_Source.__init__(self, params, 'Control')                   #设置类型

        #初始行情源对象(多源)
        self.srcQuotes = {}
        self.srcQuotes['SinaAPI'] = gol._Get_Value('quoteSource_Sina', None)          #新浪源
        self.srcQuotes['JqDataAPI'] = gol._Get_Value('quoteSource_JqData', None)      #聚宽源
        
    #添加监听
    def addListener(self, listener):
        for x in self.srcQuotes.keys():
            self.srcQuotes[x].addListener(listener)

    #查询行情
    def query(self, checkTime = True, nReturn = 0, parms = None): 
        if(parms == None):
            return self.srcQuotes['SinaAPI'].query(checkTime, nReturn)
            #self.pQuotes['JqDataAPI'].query(checkTime, nReturn)
        else:
            typeAPI = parms.get('typeAPI', '')
            if(typeAPI == ""): typeAPI = "SinaAPI"
            api = self.srcQuotes.get(typeAPI, None)
            if(api != None):
                return api.query(checkTime, nReturn, parms)
        return []


#缓存全局对象
gol._Set_Value('quoteSource', Source_Control())   #实例 行情对象



#主启动程序
if __name__ == "__main__":
    import myListener_Printer
    pSource = gol._Get_Value('quoteSource')
    pSource.addListener(myListener_Printer.Quote_Listener_Printer())
    
    # 单独查询，不纪录
    qd = pSource.query(False, 1, {"typeAPI" : "", "queryIDs" : "sh510050"}) 
    
    # 通用查询，并记录
    while True:
        pSource.query() 
        time.sleep(3)




 
