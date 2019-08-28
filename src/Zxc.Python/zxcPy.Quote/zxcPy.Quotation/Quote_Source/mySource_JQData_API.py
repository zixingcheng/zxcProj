#-*- coding: utf-8 -*-
"""
Created on  张斌 2019-08-28 14:58:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com

    监听--源基类-聚宽 
"""
import sys, os, mySystem 
import jqdatasdk
jqdatasdk.auth('18002273029','zxcvbnm.123')     # 账户登陆


#引用根目录类文件夹--必须，否则非本地目录起动时无法找到自定义类 
mySystem.Append_Us("", False)    
import myData_Trans, myDebug
from myGlobal import gol   
from jqdatasdk import *


#行情源--聚宽API
class Source_JQData_API():
    def __init__(self, params = ""):
        # myQuote_Source.Quote_Source.__init__(self, params, 'Stock')     #设置类型
        pass

    #查询行情
    def query(self, checkTime = True, nReturn = 0):  
        # 未实现
        return True 

    #生成数据对象
    def newData(self):
        return myData_Stock.Data_Stock()
    def newData_ByInfo(self, dataInfo, checkTime = True):     
        return None

    #生成数据集对象
    def newDatas(self, data, interval):
        return myData_Stock.Datas_Stock(data, interval)

    
    # 提取所有标的信息
    def getSecurities(self, types=['stock'], data=None):
        return get_all_securities(types, data)
    # 查询股票所属行业
    def getIndustrys(self, security, data=None):
        return get_industry(security, '2019-08-19')
    # 获取行业板块成分股
    def getIndustry_Stocks(self, industry_code, data=None):
        return get_industry_stocks(industry_code, date=None)
    # 获取概念板块成分股
    def getConcepts_Stocks(self, concept_code, data=None):
        return get_concept_stocks(concept_code, date=None)


#缓存全局对象
gol._Set_Value('quoteSource_API', Source_JQData_API())  #实例 行情对象
myDebug.Debug(jqdatasdk.get_query_count())



#主启动程序
if __name__ == "__main__": 
    # 提取标的信息
    pSource = gol._Get_Value('quoteSource_API', None)
    print(pSource.getSecurities())
    print(pSource.getSecurities('index'))
 
    
    print()
