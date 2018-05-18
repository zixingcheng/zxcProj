#-*- coding: utf-8 -*-
"""
Created on  张斌 2018-05-03 14:58:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com

    监听-数据对象 
"""
import sys, os, time, mySystem 

#引用根目录类文件夹--必须，否则非本地目录起动时无法找到自定义类
mySystem.m_strFloders.append('/Quote_Data')
mySystem.Append_Us("", False) 
import myData_Trans


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

    #获取时间信息
    def getTime(self, bMinute = False):
        if(not bMinute):
            if(self.datetime == None):
                self.datetime = myData_Trans.Tran_ToDatetime(self.date + " " + self.time)
                print(self.datetime)
            return self.datetime
        else:
            datetime = myData_Trans.Tran_ToDatetime(self.date + " " + self.time[0: 5], "%Y-%m-%d %H:%M")
            print(datetime , "-- New Minutes")
            return datetime

    #输出
    def Print(self):
        print (self.toString())

#数据对象--统计 
class Quote_Data_CKD():
    #依次：时间标签，初始值，统计间隔
    def __init__(self, tagTime, data = Quote_Data(), interval_M = -1): 
        self.start = data.value         #开始       
        self.last = data.value          #结束     
        self.high = data.value          #最高       
        self.low = data.value           #最低     
        self.average = data.value       #均值   

        self.interval_M = interval_M    #分钟级间隔
        self.values = {}                #值集（按时间key记录）
        self.setValues(data.getTime(), data.toValueList())
        self.tag = tagTime
        
    #设置值（校检时间范围） 
    def setValues(self, key, values = []):
        self.values[key] = values
        return True
        
    #检查统计时段(起始+间隔) 
    def checkTimeRange(self, tagTime, pData):
        if(self.interval_M < 0): return True
        interval = tagTime - self.tag   #现在时间减时段起始
        return interval.seconds < self.interval_M * 60 

    #设置统计信息 
    def setData(self, pData):
        #分钟级数据处理
        time = pData.getTime()
        if(not self.checkTimeRange(time, pData)): 
            return False 
        self.setValues(time, pData.toValueList()) 

        #更新统计信息
        dValue = pData.value
        if(dValue > self.high):
            self.high = dValue
        if(dValue < self.low):
            self.low = dValue
        self.last = (self.high + self.low) * 0.5
        self.average = self.average
        self.setValues(time, pData.toValueList())

        #其他统计接口
        self.setData_Statics(pData)
        return True
        
    #其他统计接口
    def setData_Statics(self, pData):
        pass

#数据对象--统计集 
class Quote_Data_CKDs():
    #依次：时间标签，初始值，统计间隔
    def __init__(self, data = Quote_Data(), interval_M = -1): 
        self.name = data.name 
        self.startTime = data.getTime(True)   
        self.interval_M = interval_M    #分钟级间隔
        self.CKDs = {}                  #统计集
        self.CKD = self.newDataCKD(self.startTime, data) 
        self.data = data
        
    #初始统计对象 
    def newDataCKD(self, tagTime, data):
        pCDK = Quote_Data_CKD(tagTime, data, self.interval_M)
        self.CKDs[tagTime] = pCDK
        return pCDK

    #设置统计信息 
    def setData(self, pData):
        #分钟级数据处理
        time = pData.getTime()
        if(not self.CKD.checkTimeRange(time, pData)): 
            #过时间段，重新生成统计对象
            self.CKD = self.newDataCKD(pData.getTime(True), pData)

        #更新统计信息
        self.CKD.setData(pData)
        self.data = pData

#数据对象集
class Quote_Datas:
    def __init__(self, pData, interval = 1):
        self.name = pData.name
        self.interval_M = interval                      #分钟级间隔
        self.datas = {}                                 #原始数据
        self.datas_CKDs_M = self.newData_CKDs(pData)    #统计数据--分钟级
        self.data = pData                               #当前数据
        self.datas[pData.getTime()] = pData
        
    #设置值 
    def setData(self, pData):
        if(self.data.date == pData.date and self.data.time == pData.time):
            return 

        #记录原始数据,更新最新
        self.datas[pData.getTime()] = pData
        self.data = pData
        
        #统计
        self.setData_CKDs(pData)

    #设置统计信息 
    def setData_CKDs(self, pData):
        self.datas_CKDs_M.setData(pData)
        
    #初始统计对象 
    def newData_CKDs(self, pData):
        return Quote_Data_CKDs(pData, self.interval_M)

        
#主启动程序
if __name__ == "__main__":
    import myData_Stock
    pData = Quote_Data()
    pData.Print()

    pData = myData_Stock.Data_Stock()
    pData.Print()