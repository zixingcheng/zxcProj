#-*- coding: utf-8 -*-
"""
Created on  张斌 2020-06-23 22:58:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com

    监听--源基类-聚宽 
"""
import sys, os, mySystem 


#引用根目录类文件夹--必须，否则非本地目录起动时无法找到自定义类 
mySystem.m_strFloders.append('/zxcPy.Quotation')
mySystem.m_strFloders.append('/zxcPy.Quotation/Quote_Data')
mySystem.Append_Us("", False)    
import myData_Trans, myData, myDebug
import myData_Stock, myQuote_Listener, myQuote_Source  
from myGlobal import gol   
from jqdatasdk import *



#行情源--聚宽API
class Source_JQData_Stock(myQuote_Source.Quote_Source):
    def __init__(self, params = ""):
        myQuote_Source.Quote_Source.__init__(self, params, 'JqDataAPI')     #设置类型
        self.pSource = gol._Get_Value('quoteSource_API_JqData', None)
        pass

    #查询行情
    def query(self, checkTime = True, nReturn = 0, parms = None):  
        # 未实现
        return True 

    #生成数据对象--未完成
    def newData(self):
        return myData_Stock.Data_Stock()
    #生成数据对象--未完成
    def newData_ByInfo(self, dataInfo, checkTime = True):     
        return None
    #生成数据集对象--未完成
    def newDatas(self, data, interval):
        return myData_Stock.Datas_Stock(data, interval)

    
#缓存全局对象
gol._Set_Value('quoteSource_JqData', Source_JQData_Stock())     #实例 行情对象



#主启动程序
if __name__ == "__main__": 
    # 提取标的信息
    pSource = gol._Get_Value('quoteSource_JqData', None)
    print()
 