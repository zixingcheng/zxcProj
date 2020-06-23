#-*- coding: utf-8 -*-
"""
Created on  张斌 2018-05-03 14:58:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com

    监听--源基类 
"""

import sys, os, time, threading, mySystem 
import urllib, threading
from time import ctime, sleep
from itchat.content import *


#引用根目录类文件夹--必须，否则非本地目录起动时无法找到自定义类
mySystem.m_strFloders.append('./')
import myDebug
mySystem.Append_Us("", True)    


#行情源--新浪--Stock
class QuoteSourceSina(Quote_Source):
    def queryStock(self, checkTime = True, nReturn = 0, parms = None):     
        host="http://hq.sinajs.cn/list="
        url = host + self.stocks
        req = urllib.request.Request(url)
        res_data = urllib.request.urlopen(req)
        res = res_data.read().decode(encoding = "gbk")
        
        #解析所有返回数据
        qd = Quote_Data()
        for line in res.split('\n'):
            #print line
            if len(line) < 50 :
                continue
            stkid = line[13: 19]
            info = line[21:len(line)-2]
            vargs = info.split(',')
            #print vargs
            qd.id = stkid
            qd.rawline = info
            qd.name = vargs[0]
            qd.openPrice = vargs[1]
            qd.preClose = vargs[2]
            qd.lastPrice = vargs[3]
            qd.highPrice = vargs[4]
            qd.lowPrice = vargs[5]
            qd.buyPrice = vargs[6]
            qd.sellPrice = vargs[7]
            qd.tradeValume = vargs[8]
            qd.tradeTurnover = vargs[9]
            qd.buy1Volume = vargs[10]
            qd.buy1Price = vargs[11]
            qd.buy2Volume = vargs[12]
            qd.buy2Price = vargs[13]
            qd.buy3Volume = vargs[14]
            qd.buy3Price = vargs[15]
            qd.buy4Volume = vargs[16]
            qd.buy4Price = vargs[17]
            qd.buy5Volume = vargs[18]
            qd.buy5Price = vargs[19]
            qd.sell1Volume = vargs[20]
            qd.sell1Price = vargs[21]
            qd.sell2Volume = vargs[22]
            qd.sell2Price = vargs[23]
            qd.sell3Volume = vargs[24]
            qd.sell3Price = vargs[25]
            qd.sell4Volume = vargs[26]
            qd.sell4Price = vargs[27]
            qd.sell5Volume = vargs[28]
            qd.sell5Price = vargs[29]
            qd.date = vargs[30]
            qd.time = vargs[31]
            
            self.notifyListeners(qd)

#行情监听线程
class QuoteThread(threading.Thread):
    def __init__(self, source, intervalSecs = 3):
        self.source = source
        self.interval = intervalSecs
        self.threadRunning = False
        threading.Thread.__init__(self)

    def run(self):
        myDebug.Print('StockQuote run')
        self.threadRunning = True;
        while self.threadRunning:
            self.source.queryStock()
            sleep(self.interval)

    def stop(self):
        myDebug.Print('StockQuote stop')
        self.threadRunning = False;

          

   
#主启动程序
if __name__ == "__main__":
    stockids = 'sh600006,sh510050'
    s = QuoteSourceSina(stockids)
    s.addListener(Quote_Printer())
    #s.addListener(QuoteDifferenceValueInformer('510050', '0.0', '-0.008', '0.005'))
    #s.addListener(QuoteSaveToCSV('510050'))
    #s.addListener(QuoteDiffValuesInformer('510050', [-0.009,-0.019,-0.029], [0.009, 0.019, 0.029], '0.0'))
    try:
        while True:
            s.queryStock()
            sleep(3)
    except :
        myDebug.Print('StockQuote stop')
      

    #exit()




 
