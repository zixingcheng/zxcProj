#-*- coding: utf-8 -*-
"""
Created on  张斌 2020-06-30 14:58:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com

    监听--源基类-新浪 API
    参考：
        # 新浪财经50ETF期权和上交所300ETF期权行情接口
        # https://blog.csdn.net/u013781175/article/details/54374798
"""
import sys, os, mySystem 
import urllib, urllib.request


#引用根目录类文件夹--必须，否则非本地目录起动时无法找到自定义类 
mySystem.Append_Us("", False)    
import myData, myData_Trans, myData_Json, myDebug
from myGlobal import gol   



#行情源--聚宽API
class Source_Sina_API():
    def __init__(self, params = ""):
        pass
    
    # 获得当前有哪几个月份的合约
    def getOptInfos_Month(self, nameETF = "50ETF"):
        url = F"http://stock.finance.sina.com.cn/futures/api/openapi.php/StockOptionService.getStockName?exchange=null&cate={nameETF}"
        req = urllib.request.Request(url)
        res_data = urllib.request.urlopen(req)
        res = res_data.read().decode(encoding = "gbk")

        jsonRes = myData_Json.Trans_ToJson(res)
        return jsonRes['result']['data']["stockId"], jsonRes['result']['data']["contractMonth"]
    # 获得某月到期的看涨/跌期权代码列表
    def getOptInfos_Code(self, stockId = "510050", month = '2020-07', typeOpt = "UP"):
        monthInfo = month.replace('-', '')[2:]
        url = F"http://hq.sinajs.cn/list=OP_{typeOpt}_{stockId}{monthInfo}"
        req = urllib.request.Request(url)
        res_data = urllib.request.urlopen(req)
        res = res_data.read().decode(encoding = "gbk")
        
        values = res.split('=')
        info = values[1][1:len(values[1])-4]
        return info.split(',')
    # 查询期权信息-所有，当日的
    def getOptInfos(self, nameETF = "50ETF", month_Delta = 1, extype = "sh"):
        # 获得当前有哪几个月份的合约
        stockId, lstMonth = self.getOptInfos_Month(nameETF)
        lstMonth = {}.fromkeys(lstMonth).keys()

        # 获取所有期权名称
        lstOpt_names = []
        for x in lstMonth:
            lstOpt_names = lstOpt_names + self.getOptInfos_Code(stockId, x, "UP")
            lstOpt_names = lstOpt_names + self.getOptInfos_Code(stockId, x, "DOWN")

        # 提取期权信息
        queryList = myData_Trans.Tran_ToStr(lstOpt_names, ',')
        url = "http://hq.sinajs.cn/list=" + queryList
        req = urllib.request.Request(url)
        res_data = urllib.request.urlopen(req)
        res = res_data.read().decode(encoding = "gbk")
        
        lines = res.split('\n')
        infos = []
        for line in lines:
            if(line == ""): continue
            values = line.split('=')
            stkid = values[0][11:]
            info = values[1][1:len(values[1])-4]
            vargs = info.split(',')
            
            # 组装返回信息
            info = {}
            info['name'] = stkid[7:] + "." +  extype
            info['display_name'] = vargs[37]
            info['type'] = 'opt'
            info['extype2'] = "XSHG"
            info['source_code'] = stkid
            infos.append(info)
        return infos
    
    # 查询价格信息，指定日期范围、数据频率
    # fields:['open', ' close', 'low', 'high', 'volume', 'money', 'factor', 'high_limit',' low_limit', 'avg', ' pre_close', 'paused']
    def getPrice(self, security, start_date="", end_date="", frequency='daily', fields=None, skip_paused=True, count=None):
        # 同步参数
        dateTime = myData_Trans.Tran_ToDatetime_str(None, "%Y-%m-%d")
        start_date = myData.iif(start_date == "", dateTime + " 09:00:00", start_date)
        end_date = myData.iif(end_date == "", dateTime + " 13:00:00", end_date)
        
        # 查询数据
        host="http://hq.sinajs.cn/list="
        url = host + security

        req = urllib.request.Request(url)
        res_data = urllib.request.urlopen(req)
        res = res_data.read().decode(encoding = "gbk")

        values = res.split('=')
        stkid = values[0][11:]
        info = values[1][1:len(values[1])-4]
        vargs = info.split(',')
            
        # 区分股票与期权
        if(stkid.count('CON_OP') == 1):
            value = float(vargs[2])
        else:
            value = float(vargs[3])
        return value

#缓存全局对象
gol._Set_Value('quoteSource_API_Sina', Source_Sina_API())   #实例 行情对象



#主启动程序
if __name__ == "__main__": 
    # 提取标的信息
    pSource = gol._Get_Value('quoteSource_API_Sina', None)
    print(pSource.getOptInfos(nameETF = "50ETF", month_Delta = 1))
    
    print(pSource.getPrice('CON_OP_10002535', start_date="", end_date="", frequency='daily', fields=None, skip_paused=True, count=None))