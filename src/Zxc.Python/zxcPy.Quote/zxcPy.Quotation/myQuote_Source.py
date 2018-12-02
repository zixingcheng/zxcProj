#-*- coding: utf-8 -*-
"""
Created on  张斌 2018-05-03 14:58:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com

    监听--源基类 
"""
import sys, os, time, datetime, mySystem 
import threading

#引用根目录类文件夹--必须，否则非本地目录起动时无法找到自定义类
mySystem.m_strFloders.append('/Quote_Source')
mySystem.Append_Us("../../zxcPy.Robot/zxcPy.Robot/Prjs/Base", False, __file__)
mySystem.Append_Us("", False)    
import myData_Trans, myDebug, myIO
import myQuote_Data, myManager_Bill
from myGlobal import gol 

#行情来源
class Quote_Source:
    def __init__(self, params = "", type = ''):
        self.type = type
        if(params == ""): params = self._getDefault_Param()
        self.params = params
        self.datas = {}
        self.datasNow = None
        self.listeners = []
        self.interval_M = 1       #分钟级间隔
        self._initSetting()       #初始设置
        self.setTime()            #设置(时效) 
    def _initSetting(self):
        #初始根目录信息
        strDir, strName = myIO.getPath_ByFile(__file__)
        Dir_Base = os.path.abspath(os.path.join(strDir, ".."))  
        Dir_DataDB = Dir_Base + "/Data/DB_Trade/" 
        gol._Set_Setting('manageBills_Stock', myManager_Bill.myManager_Bill(Dir_DataDB ))     #实例 交易管理器   
    def _getDefault_Param(self):  #默认配置
        pSets = gol._Get_Value('setsQuote')
        if(pSets != None):
            keys = pSets.setList.keys()
            lstParam = []
            for x in keys:
                pSet = pSets._Find(x)
                if(pSet != None and pSet.isEnable and self.type == pSet.setType):
                    lstParam.append(pSet.setTag)
            strParams = myData_Trans.Tran_ToStr(lstParam)
            return strParams
    def _Stoped(self):
        keys = self.datas.keys()
        isStoped = False
        for x in keys:
            if(self.datas[x].stoped):
                isStoped = True
                break
        return isStoped
    
     
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
        if(self.checkTime(data) == False): return None 

        #提取数据对象
        pDatas = self.datas.get(data.name, None)
        if(pDatas == None):                     #不存在时初始 
            pDatas = self.newDatas(data, self.interval_M)
            self.datas[data.name] = pDatas
            
            #监听配置更新
            for listener in self.listeners : 
                listener.OnUpdataSet(pDatas)
        else:     
            if(pDatas.stoped): return None      #终止接收
            pDatas.setData(data)                #设置值
        
        #通知所有监听对象
        if(bNotify):
            self.notifyListeners(pDatas)
        self.datasNow = pDatas
        return pDatas
    #合法性(时效)
    def checkTime(self, data):
        tNow = data.datetime_queryed
        if(self.startTime < tNow and tNow < self.endTime):
            if(self.timeIntervals > 0):
                self.timeIntervals += 1
            return True
        elif(self.timeIntervals == 0 and self.endTime < tNow):
            self.startTime = myData_Trans.Tran_ToDatetime(self.dtDay + " 13:00:00")      #起始时间
            self.endTime = self.endTime2                                                #结束时间
            self.timeIntervals += 1
            if(self.datasNow != None): 
                self.datasNow.saveData()                    #保存数据（第一时段结束）  
            return self.checkTime(data)
        elif(self.endTime < tNow):
            if(self.datas.get(data.name,None) == None): #初始数据(当天结束时段后，只有一条数据)
                self.timeIntervals += 1
                return True
            elif(self.timeIntervals > 1):
                #设置数据监听停止
                if(self.datasNow.name != data.name):
                    self.datasNow = self.datas.get(data.name,None)
                if(self.datasNow.stoped == False):
                    self.datasNow.saveData()                #保存数据（第二时段结束） 
                    self.datasNow.stoped = True
                    myDebug.Print("... stoped data(" + data.name + ")...") 
        return False
    #设置(时效)
    def setTime(self):
        self.dtDay = myData_Trans.Tran_ToTime_str(None, "%Y-%m-%d")                 #当前天
        self.startTime = myData_Trans.Tran_ToDatetime(self.dtDay + " 9:26:30")      #起始时间
        self.endTime = myData_Trans.Tran_ToDatetime(self.dtDay + " 11:30:30")       #结束时间
        self.endTime2 = myData_Trans.Tran_ToDatetime(self.dtDay + " 15:16:00")      #结束时间--收盘
        self.timeIntervals = 0

        #时间段监测
        tNow = datetime.datetime.now()
        return (self.startTime < tNow and tNow < self.endTime2)

#行情监听线程
class Quote_Thread(threading.Thread):
    def __init__(self, source, intervalSecs = 3):
        self.source = source
        self.interval = intervalSecs
        self.threadRunning = False
        self.stopped = False
        threading.Thread.__init__(self)

    def run(self):
        if(self.source.setTime() == False):
            myDebug.Print('StockQuote stoped.\n         --not stock time..')
            self.stop()
            return 

        myDebug.Print('StockQuote run')
        self.threadRunning = True;
        while self.threadRunning:
            try:
                #发生错误时继续
                self.source.query() 

                #判断结束
                if(self.source._Stoped()):
                    break
                time.sleep(self.interval)   
            except :
                pass
        self.stop()

    def stop(self):
        myDebug.Print('StockQuote stop')
        self.threadRunning = False
        self.stopped = True
        time.sleep(2)
        
        #退出 
        strDir, strName = myIO.getPath_ByFile(__file__)
        strDir_Base = os.path.abspath(os.path.join(strDir, ".."))  
        strPath = strDir_Base + "/myQuote_API.lock"
        gol._Run_UnLock(strPath)
        os._exit()
        exit(0)
  
        
def mainloop(thread):
    try:
        while thread.stopped == False:
            time.sleep(1)
    except:
        thread.stop()
    is_exit = True
def mainStart():
    #线程执行   
    pQuote = gol._Get_Value('quoteSource')
    if(pQuote == None):
        pQuote = mainSource()
        
    thrdQuote = gol._Get_Value('quoteSourceThread', None)
    if(pQuote != None and (thrdQuote == None or thrdQuote.threadRunning == False)):
        thrdQuote = Quote_Thread(pQuote)
        thrdQuote.setDaemon(True)
        thrdQuote.start()
        gol._Set_Value('quoteSourceThread', thrdQuote)
def mainSource():
    #初始全局行情对象
    from myGlobal import gol 
    gol._Init()     #先必须在主模块初始化（只在Main模块需要一次即可）
    if(gol._Get_Setting('quoteSource', None)== None):
        #示例数据监控(暂只支持单源，多源需要调整完善)
        import mySource_Sina_Stock
        pQuote = mySource_Sina_Stock.Source_Sina_Stock() 

        #添加监听对象
        import myListener_Printer, myListener_Rise_Fall_asInt, myListener_Hourly, myListener_FixedMonitor
        pQuote.addListener(myListener_Printer.Quote_Listener_Printer())
        pQuote.addListener(myListener_Hourly.Quote_Listener_Hourly())
        pQuote.addListener(myListener_Rise_Fall_asInt.Quote_Listener_Rise_Fall_asInt())
        #for x in pSets.setUsers:
        #    pQuote.addListener(myListener_FixedMonitor.Quote_Listener_FixedMonitor(x))

        gol._Set_Value('quoteSource', pQuote)    #实例 行情对象
        return pQuote


#主启动程序
if __name__ == "__main__":
    #单例运行检测
    if(gol._Run_Lock(__file__) == False):
       exit(0)


    #示例数据监控(暂只支持单源，多源需要调整完善)
    mainSource() 
    pQuote = gol._Get_Value('quoteSource')
    pSets = gol._Get_Value('setsQuote')


    #线程执行   
    thread = Quote_Thread(pQuote)
    thread.setDaemon(True)
    thread.start()
    mainloop(thread)
    time.sleep(1)
    myDebug.Print("Quote thread exited...")

    #退出
    #gol._Run_UnLock(__file__)
    exit(0)

 
