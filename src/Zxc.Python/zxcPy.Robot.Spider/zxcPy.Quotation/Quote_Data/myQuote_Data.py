#-*- coding: utf-8 -*-
"""
Created on  张斌 2018-05-03 14:58:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com

    行情爬取-数据对象 
"""
import sys, os, time, datetime, copy, mySystem 

#引用根目录类文件夹--必须，否则非本地目录起动时无法找到自定义类
mySystem.m_strFloders.append('/Quote_Data')
mySystem.m_strFloders.append('/Quote_Listener')
mySystem.Append_Us("", False) 
import myData_Trans, myDebug



#数据对象
class Quote_Data:
    def __init__(self):
        self.id = ''
        self.rawLine = '' 
        self.name = '' 
        self.date = ''
        self.time = ''
        self.value = 0
        self.datetime = None
        self.datetime_queryed = datetime.datetime.now()
    
    #序列化
    def toString(self):
        pass
    
    #序列化--csv列头
    @staticmethod
    def csvHead():
        head = 'name,id,time,date'
        return head
        
    #序列化--csv行信息
    def toCSVString(self):
        pass 
    
    #转换为值组
    def toValueList(self):
        pass
    #由值组转换
    def fromValueList(self, lstValue):
        pass
    
    #合法性(时效)
    def checkTime(self):
        if(self.datetime == None): self.getTime()
        return (self.datetime_queryed.year == self.datetime.year) \
                and (self.datetime_queryed.month == self.datetime.month) \
                 and (self.datetime_queryed.day == self.datetime.day) \
                    and (self.datetime_queryed.hour * 3600 + self.datetime_queryed.minute * 60 + self.datetime_queryed.second \
                        - self.datetime.hour * 3600 - self.datetime.minute * 60 - self.datetime.second < 60)
    #获取时间信息(完整时间还是分钟时间)
    def getTime(self, bMinute = False):
        if(not bMinute):
            if(self.datetime == None):
                self.datetime = myData_Trans.Tran_ToDatetime(self.date + " " + self.time)
                #print(self.datetime)
            return self.datetime
        else:
            times = self.time.split(":")
            datetime = myData_Trans.Tran_ToDatetime(self.date + " " + times[0] + ":" + times[1], "%Y-%m-%d %H:%M")
            myDebug.Debug(datetime , "-- New Minutes")
            return datetime
    def getTime_str(self, bMinute = False):
        datetime = self.getTime(bMinute)
        return myData_Trans.Tran_ToDatetime_str(datetime)
    #获取播报消息 
    def getMsg_str(self, pSet = None):
        pass 

    #输出
    def Print(self):
        myDebug.Debug(self.toString())


