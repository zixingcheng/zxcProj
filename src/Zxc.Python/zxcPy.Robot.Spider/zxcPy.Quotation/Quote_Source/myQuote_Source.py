#-*- coding: utf-8 -*-
"""
Created on  张斌 2018-05-03 14:58:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com

    行情爬取--源基类 
"""
import sys, os, time, datetime, mySystem 
import threading

#引用根目录类文件夹--必须，否则非本地目录起动时无法找到自定义类
mySystem.Append_Us("/Quote_Source", False, __file__)
mySystem.Append_Us("/Quote_Listener", False, __file__) 
mySystem.Append_Us("", False)    
import myData_Trans, myData, myDebug 



#行情来源
class Quote_Source:
    def __init__(self, params = "", type = ''):
        self.type = type
        self.params = params
        self.listeners = []
        self.setTime()            #设置(时效) 
     
    #添加监听
    def addListener(self, listener):
        self.listeners.append(listener)
    #通知所有监听处理接收（注入新数据对象）
    def notifyListeners(self, quoteDatas):
        for listener in self.listeners : 
            listener.OnRecvQuote(quoteDatas)
    
    #查询行情信息(返回n条)
    def query(self, checkTime = True, nReturn = 0, parms = None): 
        if(checkTime):
            if(self.checkTime() == False): return None
        pass 

    #生成数据对象
    def newData(self): pass
    def newData_ByInfo(self, dataInfo, checkTime = True): pass

    #合法性(时效)
    def checkTime(self, data=None):
        if(data==None):
            tNow = datetime.datetime.now()
            if(self.startTime < tNow and tNow < self.endTime): 
                return True
            else:
                if(tNow > self.endTime): 
                    self.startTime = myData_Trans.Tran_ToDatetime(self.dtDay + " 13:00:00")     #起始时间
                    self.endTime = self.endTime2                                                #结束时间
                    if(self.startTime < tNow and tNow < self.endTime):  return True
            return False

        #时间判断
        tNow = data.datetime_queryed
        if(self.startTime < tNow and tNow < self.endTime):
            if(self.timeIntervals > 0):
                self.timeIntervals += 1
            return True
        elif(self.timeIntervals == 0 and self.endTime < tNow):
            self.startTime = myData_Trans.Tran_ToDatetime(self.dtDay + " 13:00:00")     #起始时间
            self.endTime = self.endTime2                                                #结束时间
            self.timeIntervals += 1
            if(self.datasNow != None): 
                self.datasNow.saveData()                    #保存数据（第一时段结束）  
            return self.checkTime(data)
        elif(self.endTime < tNow):
            if(self.datas.get(data.name,None) == None):     #初始数据(当天结束时段后，只有一条数据)
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
        self.endTime2 = myData_Trans.Tran_ToDatetime(self.dtDay + " 19:16:00")      #结束时间--收盘
        self.timeIntervals = 0

        #时间段监测
        tNow = datetime.datetime.now()
        if(tNow.hour > 15): 
            self.timeIntervals = 1 
        return (self.startTime < tNow and tNow < self.endTime2)


