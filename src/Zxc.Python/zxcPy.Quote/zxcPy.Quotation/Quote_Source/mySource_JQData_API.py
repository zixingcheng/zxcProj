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
import myData_Trans, myData, myDebug
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

    #生成数据对象--未完成
    def newData(self):
        return myData_Stock.Data_Stock()
    #生成数据对象--未完成
    def newData_ByInfo(self, dataInfo, checkTime = True):     
        return None
    #生成数据集对象--未完成
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
    

    # 查询期权信息，指定日期，默认当天
    def getOptInfo(self, optPrice = 2500, dateTime = ""):
        # 同步参数
        if(dateTime == ""): dateTime = myData_Trans.Tran_ToDatetime_str(None, "%Y-%m-%d")
        dtFliter = myData_Trans.Tran_ToDatetime(dateTime, "%Y-%m-%d")
        strFliter = "50ETF" + myData.iif(optPrice > 0, "购", "沽") + str(dtFliter.month) + "月" + str(optPrice)

        # 查询
        optInfos = opt.run_query(query(opt.OPT_DAILY_PREOPEN).filter(opt.OPT_DAILY_PREOPEN.date==dateTime,opt.OPT_DAILY_PREOPEN.name==strFliter).limit(10))
        if(optInfos.shape[0] != 1): return None
        
        # 查询最新的期权基本资料数据
        code = optInfos['code'][0]
        optInfo = query(opt.OPT_CONTRACT_INFO).filter(opt.OPT_CONTRACT_INFO.code==code)
        value = opt.run_query(optInfo)
        if(len(value) != 1): return None
        return {'id': value['id'][0], 'code': value['code'][0], 'trading_code': value['trading_code'][0]}

    # 查询价格信息，指定日期范围、数据频率
    # fields:['open', ' close', 'low', 'high', 'volume', 'money', 'factor', 'high_limit',' low_limit', 'avg', ' pre_close', 'paused']
    def getPrice(self, security, start_date="", end_date="", frequency='daily', fields=None, skip_paused=True, count=None):
        # 同步参数
        dateTime = myData_Trans.Tran_ToDatetime_str(None, "%Y-%m-%d")
        start_date = myData.iif(start_date == "", dateTime + " 09:00:00", start_date)
        end_date = myData.iif(end_date == "", dateTime + " 13:00:00", end_date)
        
        # 查询数据
        values = jqdatasdk.get_price(security=security, frequency=frequency, start_date=start_date, end_date=end_date, skip_paused=skip_paused) 
        return values

    # 查询周期价格信息，'1m', '5m', '15m', '30m', '60m', '120m', '1d', '1w', '1M'
    # fields:['date', 'open', 'close', 'high', 'low', 'volume', 'money']
    def getPrice_bars(self, security, count, unit='1d', include_now=False, fields=None, end_date=None):
        # 查询数据
        try:
            if(fields == None): fields=['date', 'open', 'close', 'high', 'low', 'volume', 'money']
            values = jqdatasdk.get_bars(security=security, count=count, unit=unit, fields=fields, include_now=include_now, end_dt=end_date) 
            return values
        except :
            return []
        
    # 查询周期均价格信息，'1m', '5m', '15m', '30m', '60m', '120m', '1d', '1w', '1M' 
    def getPrice_avg(self, security, unit='1d', include_now=False, end_date=None):
        values = self.getPrice_bars(security, 1, unit, include_now, ['date', 'open', 'close', 'high', 'low', 'volume', 'money'], end_date)
        if(len(values) != 1):
            return {'date':"", 'open':-1, 'close':-1, 'high':-1, 'low':-1, 'volume':-1, 'money':-1, 'avg':-1}
        return {'date':values['date'][0], 'open':values['open'][0], 'close':values['close'][0], 'high':values['high'][0], 'low':values['low'][0], 'volume':values['volume'][0], 'money':values['money'][0], 'avg':values['money'][0]/values['volume'][0]}
    # 查询周期均价格信息，N天
    def getPrice_avg_day(self, security, N=1, include_now=False, end_date=None):
        values = self.getPrice_bars(security, N, '1d', include_now, ['date', 'open', 'close', 'high', 'low', 'volume', 'money'], end_date)
        if(len(values) <= 1):
            return {'date':"", 'open':-1, 'close':-1, 'high':-1, 'low':-1, 'volume':-1, 'money':-1, 'avg':-1}

        # 计算周期值
        num = len(values)
        dictValue = {'date':values['date'][num-1], 'open':values['open'][0], 'close':values['close'][num-1], 'high':0, 'low':0, 'volume':0, 'money':0, 'avg':0}
        for x in range(0, num):
            if(dictValue['high'] < values['high'][x]):
                dictValue['high'] = values['high'][x]
            if(dictValue['low'] > values['low'][x]):
                dictValue['low'] = values['low'][x]
            dictValue['volume'] += values['volume'][x]
            dictValue['money'] += values['money'][x]
        dictValue['avg'] = dictValue['money'] / dictValue['volume']
        return dictValue


    
#缓存全局对象
gol._Set_Value('quoteSource_API', Source_JQData_API())  #实例 行情对象
myDebug.Debug(jqdatasdk.get_query_count())              #打印当日可请求条数



#主启动程序
if __name__ == "__main__": 
    # 提取标的信息
    pSource = gol._Get_Value('quoteSource_API', None)
    print(pSource.getSecurities())
    print(pSource.getSecurities('index'))

    # 提取50期权信息
    print("当天3000的期权信息：")
    opt = pSource.getOptInfo(3000)
    print(opt)
    print(pSource.getPrice(security=opt['code'],frequency='1m',start_date='2019-10-14 09:00:00',end_date='2019-10-14 15:00:00'))

    print(pSource.getPrice_bars(security=opt['code'],count=1,unit='1d',end_date='2019-10-14 15:00:00',include_now=False))
    print(pSource.getPrice_bars(security=opt['code'],count=1,unit='1d',end_date='2019-10-14 15:00:00',include_now=True))

    print(pSource.getPrice_avg(security='ddd',unit='1d',end_date='2019-10-14 15:00:00',include_now=True))
    print(pSource.getPrice_avg(security=opt['code'],unit='1d',end_date='2019-10-14 15:00:00',include_now=True))
    print(pSource.getPrice_avg_day(security=opt['code'],N=5,end_date='2019-10-14 15:00:00',include_now=True))
     
    
    print()
