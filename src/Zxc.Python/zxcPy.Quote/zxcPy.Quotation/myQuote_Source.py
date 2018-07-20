#-*- coding: utf-8 -*-
"""
Created on  张斌 2018-05-03 14:58:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com

    监听--源基类 
"""
import sys, os, time,  mySystem 
import threading

#引用根目录类文件夹--必须，否则非本地目录起动时无法找到自定义类
mySystem.m_strFloders.append('/Quote_Source')
mySystem.Append_Us("", False)    
import myQuote_Data, myData_Trans, myQuote_Listener, myListener_StaticsM5
 

#行情来源
class Quote_Source:
    def __init__(self, params):
        self.params = params
        self.datas = {}
        self.datasNow = None
        self.listeners = []
        self.interval_M = 1       #分钟级间隔
        self.setTime()            #设置(时效)
     
    #添加监听
    def addListener(self, listener):
        self.listeners.append(listener)
    #通知所有监听处理接收（注入新数据对象）
    def notifyListeners(self, quoteDatas):
        for listener in self.listeners : 
            listener.OnRecvQuote(quoteDatas)
    
    #查询行情
    def query(self):pass

    #生成数据对象
    def newData(self):pass
    #生成数据集对象
    def newDatas(self, data, interval):pass

    #生成数据对象
    def setData(self, data, bNotify = True):
        #有效验证     
        if(data == None): return None
        if(self.checkTime(data.datetime_queryed) == False): 
            if(len(self.datas) > 0): return None  

        #提取数据对象
        pDatas = self.datas.get(data.name, None)
        if(pDatas == None):                     #不存在时初始 
            pDatas = self.newDatas(data, self.interval_M)
            self.datas[data.name] = pDatas
        else:     
            pDatas.setData(data)                #设置值
        
        #通知所有监听对象
        if(bNotify):
            self.notifyListeners(pDatas)
        self.datasNow = pDatas
        return pDatas
    #合法性(时效)
    def checkTime(self, tNow): 
        if(self.startTime < tNow and tNow < self.endTime):
            if(self.timeIntervals > 0):
                self.timeIntervals += 1
            return True
        elif(self.timeIntervals == 0 and self.endTime < tNow):
            self.startTime = myData_Trans.Tran_ToDatetime(self.dtDay + " 13:00:00")      #起始时间
            self.endTime = myData_Trans.Tran_ToDatetime(self.dtDay + " 15:02:00")        #结束时间
            self.timeIntervals += 1
            if(self.datasNow != None): 
                self.datasNow.saveData()        #保存数据（第一时段结束）  
            return self.checkTime(tNow)
        if(self.timeIntervals > 1):
            self.datasNow.saveData()            #保存数据（第二时段结束） 
        return False
    #设置(时效)
    def setTime(self):
        self.dtDay = myData_Trans.Tran_ToTime_str(None, "%Y-%m-%d")                 #当前天
        self.startTime = myData_Trans.Tran_ToDatetime(self.dtDay + " 9:28:00")      #起始时间
        self.endTime = myData_Trans.Tran_ToDatetime(self.dtDay + " 11:30:00")       #结束时间
        self.timeIntervals = 0
     

#行情监听线程
class Quote_Thread(threading.Thread):
    def __init__(self, source, intervalSecs = 3):
        self.source = source
        self.interval = intervalSecs
        self.threadRunning = False
        threading.Thread.__init__(self)

    def run(self):
        print ('StockQuote run')
        self.threadRunning = True;
        while self.threadRunning:
            self.source.query()
            time.sleep(self.interval)

    def stop(self):
        print ('StockQuote stop')
        self.threadRunning = False;

          
is_exit = False
def mainloop(s):
    global is_exit
    try:
        while True:
            time.sleep(1)
    except:
        s.stop()

#主启动程序
if __name__ == "__main__":
    import mySource_Sina_Stock, myListener_Printer
    
    # sh000001,sh601939,sh601288,sh600919,sh600718
    # sz399001,sz399006,sz300523,sz300512,sz300144,sz300036,sz002410,sz002024
    stockids = 'sh000001,sh601939,sh601288,sh600919,sh600718,sz399001,sz399006,sz300523,sz300512,sz300144,sz300036,sz002410,sz002024'
    stockids = 'sh601288'
    s = mySource_Sina_Stock.Source_Sina_Stock(stockids)
    s.addListener(myListener_Printer.Quote_Listener_Printer())
    s.addListener(myListener_StaticsM5.Quote_Listener_StaticsM5())

    myListener_StaticsM5
    #线程验证    
    thread = Quote_Thread(s)
    thread.setDaemon(True)
    thread.start()
    mainloop(thread)



 
