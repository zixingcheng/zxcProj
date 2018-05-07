#-*- coding: utf-8 -*-
"""
Created on  张斌 2018-05-03 14:58:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com

    监听-数据对象 
"""
import sys, os, mySystem 

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
    def getTime(self):
        return myData_Trans.Tran_ToTime(self.date + " " + self.time)

    #输出
    def Print(self):
        print (self.toString())

#数据对象--统计 
class Quote_Data_Statistics():
    def __init__(self, tag, value = 0): 
        self.name = ''   
        self.start = value         #开始       
        self.last = value          #结束     
        self.high = value          #最高       
        self.low = value           #最低     
        self.average = value       #均值   
        self.values = {}           #值集（按时间key记录）
        self.tag = tag
        
    #设置值 
    def setValues(self, key, values = []):
        self.values[key] = values

#数据对象集
class Quote_Datas:
    def __init__(self):
        self.name = ''
        self.dates = {}             #原始数据
        self.dates_Statics_M = {}   #统计数据--分钟级
        self.date_Statics = Quote_Data_Statistics() #统计数据-当前
        self.date = Quote_Data()    #当前数据
        self.keyMinutes = {}
        
    #设置值 
    def setData(self, pDate):
        if(self.date.time == pDate.time):
            return 
        self.dates[pDate.time] = pDate
        self.date = pData
        
        #统计
        setData_Statistics(pDate)

    #设置统计信息 
    def setData_Statistics(self, pDate):
        pass

        
#主启动程序
if __name__ == "__main__":
    import myData_Stock
    pData = Quote_Data()
    pData.Print()

    pData = myData_Stock.Data_Stock()
    pData.Print()