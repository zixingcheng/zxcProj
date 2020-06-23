#-*- coding: utf-8 -*-
"""
Created on  张斌 2020-06-23 18:58:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com

    监听--统一源类(多源) 
"""
import sys, os, time, mySystem 

#引用根目录类文件夹--必须，否则非本地目录起动时无法找到自定义类
mySystem.m_strFloders.append('/zxcPy.Quotation')
mySystem.m_strFloders.append('/zxcPy.Quotation/Quote_Data')
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
        self.pQuotes = {}
        self.pQuotes['SinaAPI'] = gol._Get_Value('quoteSource_Sina', None)          #新浪源
        self.pQuotes['JqDataAPI'] = gol._Get_Value('quoteSource_JqData', None)      #聚宽源
        
    #添加监听
    def addListener(self, listener):
        for x in self.pQuotes.keys():
            self.pQuotes[x].addListener(listener)

    #查询行情
    def query(self, checkTime = True, nReturn = 0, parms = None): 
        if(parms == None):
            self.pQuotes['SinaAPI'].query(checkTime, nReturn)
            self.pQuotes['JqDataAPI'].query(checkTime, nReturn)
        else:
            api = self.pQuotes.get(parms.get('typeAPI', ''), None)
            if(api != None):
                api.query(checkTime, nReturn)
        pass
    #生成数据对象
    def newData(self):
        pass
    def newData_ByInfo(self, dataInfo, checkTime = True):   
        pass
    #生成数据集对象
    def newDatas(self, data, interval):
        pass


#缓存全局对象
gol._Set_Value('quoteSource', Source_Control())   #实例 行情对象



#主启动程序
if __name__ == "__main__":
    pSource = Source_Control()
    
    # 单独查询，不纪录
    qd = pSource.query(False, 1) 
    
    # 通用查询，并记录
    while True:
        pSource.query() 
        time.sleep(3)




 
