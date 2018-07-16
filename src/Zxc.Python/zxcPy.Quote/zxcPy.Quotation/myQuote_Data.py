#-*- coding: utf-8 -*-
"""
Created on  张斌 2018-05-03 14:58:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com

    监听-数据对象 
"""
import sys, os, time, copy, mySystem 

#引用根目录类文件夹--必须，否则非本地目录起动时无法找到自定义类
mySystem.m_strFloders.append('/Quote_Data')
mySystem.Append_Us("", False) 
import myData_Trans, myIO, myIO_xlsx


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
    #由值组转换
    def fromValueList(self, lstValue):
        pass

    #获取时间信息(完整时间还是分钟时间)
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
    def getTime_str(self, bMinute = False):
        datetime = self.getTime(bMinute)
        return myData_Trans.Tran_ToDatetime_str(datetime)

    #输出
    def Print(self):
        print(self.toString())

#数据对象--统计 
class Quote_Data_CKD():
    #依次：时间标签，初始值，统计间隔
    def __init__(self, tagTime, data = Quote_Data(), lastCKD = None, interval_M = -1): 
        self.start = data.value         #开始       
        self.last = data.value          #结束     
        self.high = data.value          #最高       
        self.low = data.value           #最低     
        self.average = data.value       #均值  

        self.lastCKD = lastCKD          #前一个统计对象
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
        self.CKD = None
        self.CKD = self.newDataCKD(self.startTime, data) 
        self.data = data
        
    #初始统计对象 
    def newDataCKD(self, tagTime, data):
        pCDK = Quote_Data_CKD(tagTime, data, self.CKD, self.interval_M)
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
        self.datas[pData.getTime()] = pData         #记录细分数据
        self.autoSave = True
        self.autoSave_interval_M = 2
        self.timeM = 0
        if(self.loadData()):                            #加载已存数据
            self.setData(pData)
            
        
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

        #自动保存数据
        if(self.autoSave):
            nMin = self.datas_CKDs_M.CKD.tag.minute
            if(self.timeM != nMin):
                if(nMin % self.autoSave_interval_M == 0): 
                    self.saveData("")
                    self.timeM = nMin
        
    #初始统计对象 
    def newData_CKDs(self, pData):
        return Quote_Data_CKDs(pData, self.interval_M)

    #装载excel数据
    def loadData(self, strDir = ""):
        #组装路径
        if(strDir == ""): strDir = "./Data/"
        strDir += self.name + "/"
        strPath = strDir + self.data.date + ".xls"

        #装载表数据
        pDt = myIO_xlsx.DtTable()
        pDt.dataFieldType = ['datetime', 'float', 'float', 'float']     #数据字段类型集
        pDt.Load(strPath)

        #创建数据
        bCanSave = self.autoSave                                #屏蔽自动保存（必须）
        self.autoSave = False
        bInite = False
        nRows = len(pDt.dataMat)

        for x in range(nRows - 1, -1, -1):
            pData = copy.deepcopy(self.data)
            pData.datetime = None                               #清空时间(必须)
            pData.fromValueList(pDt.dataMat[x])                 #由表数据还原
            if(bInite == False):
                self.datas_CKDs_M = self.newData_CKDs(pData)    #统计数据--分钟级
                bInite = True
            self.setData(pData)                                 #设置数据(不允许保存)
        self.autoSave = bCanSave                                #恢复自动保存
        return bInite

    #保存为excel数据
    def saveData(self, strDir = ""):
        pDt = myIO_xlsx.DtTable()

        #字典排序
        keys = list(self.datas.keys())
        keys.sort(key = None, reverse = True)

        #组装数据
        pDt.dataField = self.data.csvHead().split(',')
        pDt.dataMat = []
        for x in keys:
            pDt.dataMat.append(self.datas[x].toValueList())

        #保存基础数据
        if(strDir == ""): strDir = "./Data/"
        strDir += self.name + "/"
        myIO.mkdir(strDir)
        fileName = self.data.date
        pDt.Save(strDir, fileName, row_start = 0, col_start = 0, cell_overwrite = True, sheet_name = self.name, row_end = -1, col_end = -1, bSave_AsStr = False)  
    
        
#主启动程序
if __name__ == "__main__":
    import myData_Stock
    pData = Quote_Data()
    pData.Print()

    pData = myData_Stock.Data_Stock()
    pData.Print()