#-*- coding: utf-8 -*-
"""
Created on  张斌 2018-05-03 14:58:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com

    监听--源基类 
"""
import sys, os, time, mySystem 
import threading

#引用根目录类文件夹--必须，否则非本地目录起动时无法找到自定义类
mySystem.m_strFloders.append('/Quote_Source')
mySystem.Append_Us("", False)    
import myQuote_Data, myQuote_Listener
 

#行情来源
class Quote_Source:
    def __init__(self, params):
        self.params = params
        self.datas = None
        self.listeners = []
     
    #添加监听
    def addListener(self, listener):
        self.listeners.append(listener)
    
    #通知所有监听处理接收（注入新数据对象）
    def notifyListeners(self, quoteDatas):
        for listener in self.listeners : 
            listener.OnRecvQuote(quoteDatas)
    
    #查询行情
    def query(self):pass
     

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
            print("")
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

    stockids = 'sh600006,sh510050'
    s = mySource_Sina_Stock.Source_Sina_Stock(stockids)
    s.addListener(myListener_Printer.Quote_Listener_Printer())
    
    #线程验证    
    thread = Quote_Thread(s)
    thread.setDaemon(True)
    thread.start()
    mainloop(thread)



 
