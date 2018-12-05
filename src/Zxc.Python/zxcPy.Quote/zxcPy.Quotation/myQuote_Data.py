#-*- coding: utf-8 -*-
"""
Created on  张斌 2018-05-03 14:58:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com

    监听-数据对象 
"""
import sys, os, time, datetime, copy, mySystem 

#引用根目录类文件夹--必须，否则非本地目录起动时无法找到自定义类
mySystem.m_strFloders.append('/Quote_Data')
mySystem.m_strFloders.append('/Quote_Listener')
mySystem.Append_Us("", False) 
import myData_Trans, myDebug, myIO, myIO_xlsx, myQuote_Setting
from myGlobal import gol 


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
    def getMsg_str(self, bIndex = False):
        pass 

    #输出
    def Print(self):
        myDebug.Debug(self.toString())
        
#数据对象--统计 
class Quote_Data_Static():
    def __init__(self, dtTime = None, pData_L = None): 
        if(dtTime == None or type(dtTime) != datetime.datetime):
            self.dtTime = datetime.datetime.now()
        else:
            self.dtTime = dtTime
        self.seconds = 0                #时间间隔         
        self.base = 0                   #基价(前收盘价)            
        self.start = 0                  #开盘              
        self.last = 0                   #收盘     
        self.high = 0                   #最高       
        self.low = 0                    #最低    
        self.average = 0                #均值

        self.tradeVolume = 0            #成交量 
        self.tradeTurnover = 0          #成交额 
        self.tradeVolume_Start = 0      #成交量_开始 
        self.tradeVolume_End = 0        #成交量_结束 
        self.tradeTurnover_Start = 0    #成交额_开始  
        self.tradeTurnover_End = 0      #成交额_结束   

        #按上个统计对象初始部分继承信息
        if(pData_L != None):  
            self.Init(pData_L.base)
            self.base = pData_L.base
            self.start = pData_L.last
            self.tradeVolume_Start = pData_L.tradeVolume_End
            self.tradeTurnover_Start = pData_L.tradeTurnover_End
    def Init(self, dValue = 0):            
        self.base = dValue           
        self.start = dValue   
        self.last = dValue 
        self.high = dValue
        self.low = dValue
        self.average = dValue
        
    #序列化--csv列头
    @staticmethod
    def csvHead():
        head = "时间,间隔,基价,开盘,收盘,最高,最低,平均,成交量,成交额,成交量_开始,成交量_结束,成交额_开始,成交额_结束"
        return head
    #序列化--csv列头字段类型
    @staticmethod
    def csvFiled_Type():
        fieldType = ['datetime', 'int', 'float', 'float', 'float', 'float', 'float', 'float', 'float', 'float', 'float', 'float', 'float', 'float'] 
        return fieldType
    #序列化--csv行信息
    def toCSVString(self):
        return '\n' + myData_Trans.Tran_ToDatetime_str(self.dtTime) \
            + ',' + str(self.seconds)  \
            + ',' + str(self.base)  \
            + ',' + str(self.start)  \
            + ',' + str(self.last)  \
            + ',' + str(self.high)  \
            + ',' + str(self.low)  \
            + ',' + str(self.average)  \
            + ',' + str(self.tradeVolume)  \
            + ',' + str(self.tradeTurnover) \
            + ',' + str(self.tradeVolume_Start)  \
            + ',' + str(self.tradeVolume_End)  \
            + ',' + str(self.tradeTurnover_Start)  \
            + ',' + str(self.tradeTurnover_End)   

    #由值组转换
    def fromValueList(self, lstValue): 
        self.dtTime = lstValue[0]
        if(type(self.dtTime) != datetime.datetime):
            self.dtTime =  myData_Trans.Tran_ToDatetime(str(self.dtTime))

        self.seconds = lstValue[1]
        self.base = lstValue[2]
        self.start = lstValue[3]
        self.last = lstValue[4]
        self.high = lstValue[5]
        self.low = lstValue[6]
        self.average = lstValue[7]
        self.tradeVolume = lstValue[8]
        self.tradeTurnover = lstValue[9] 
        self.tradeVolume_Start = lstValue[10] 
        self.tradeVolume_End = lstValue[11] 
        self.tradeTurnover_Start = lstValue[12] 
        self.tradeTurnover_End = lstValue[13] 
          
    #其他统计接口
    def setData_Static(self, dValue, pData_S = None): 
        if(dValue > self.high):
            self.high = dValue
        if(dValue < self.low):
            self.low = dValue
        self.last = dValue
             
        if(pData_S == None): return True
        if(pData_S.high > self.high):
            self.high = pData_S.high
        if(pData_S.low < self.low):
            self.low = pData_S.low

        #self.tradeTurnover_End = pData_S.tradeTurnover_End 
        #self.tradeVolume_End = pData_S.tradeVolume_End 
        self.tradeTurnover = self.tradeTurnover_End - self.tradeTurnover_Start
        self.tradeVolume = self.tradeVolume_End - self.tradeVolume_Start
        self.average = self.tradeTurnover / self.tradeVolume
        return True

#数据对象--统计 
class Quote_Data_Statics_M():
    #依次：时间标签，初始值，统计间隔
    def __init__(self, tagTime, data = Quote_Data(), lastData_S = None, interval_M = -1): 
        self.tag = tagTime                  #标识时间
        self.interval_M = interval_M        #分钟级间隔
        self.dataS_Last = lastData_S        #前一个统计对象
        self.values = {}                    #值集（按时间key记录）

        #更新统计信息 
        if(lastData_S != None):
            self.dataS = Quote_Data_Static(tagTime, lastData_S.dataS)    #当前统计值信息
        else:
            self.dataS = Quote_Data_Static(tagTime)                      #当前统计值信息

        #其他初始 
        self.dataS.Init(data.value)
        if(self.dataS_Last == None):
            datas = data.toValueList()
            self.dataS.base = data.priceBase        #基价，前一收盘
            self.dataS.start = data.priceOpen       #开盘价
        self.setData(data) 
    #清空
    def Clear(self, pData):
        self.values = {}
    

    #检查统计时段(起始+间隔) 
    def checkTimeRange(self, tagTime, pData):
        if(self.interval_M < 0): return True
        interval = tagTime - self.tag   #现在时间减时段起始
        return interval.seconds < self.interval_M * 60 
    
    #设置值（lst） 
    def setValues(self, key, values = []):
        self.values[key] = values
        return True
    #设置统计信息 
    def setData(self, pData):
        #分钟级数据处理
        time = pData.getTime()
        if(not self.checkTimeRange(time, pData)): 
            return False 

        #更新统计信息
        self.setData_Statics(pData)
        self.dataS.setData_Static(pData.value, self.dataS_Last.dataS)  

        #记录值
        self.setValues(time, pData.toValueList()) 
        return True        
    #其他统计接口
    def setData_Statics(self, pData):
        pass

#数据对象--统计集 
class Quote_Data_Statics_D():
    #依次：时间标签，初始值，统计间隔
    def __init__(self, data = Quote_Data(), interval_M = -1, bSetData = True): 
        self.dataS_Day = Quote_Data_Static()    #当天统计对象
        self.datasS_Min = []                    #当天分钟级统计对象
        self.dataS_Min_Now = None               #当前分钟统计集
        
        self.interval_M = interval_M            #分钟级间隔 
        self.name = data.name                   #标识名
        self.data = data
        
        #初始统计信息 
        if(self.dataS_Day != None):
            datas = data.toValueList()
            self.dataS_Day.base = data.priceBase     #基价，前一收盘
            self.dataS_Day.start = data.priceOpen    #开盘价

        #更新值 
        if(bSetData):
            self.setData(data) 

        #标识时间
        tt = self.dataS_Day.dtTime.timetuple()
        unix_ts = time.mktime(tt)
        self.dtNow =  datetime.datetime.fromtimestamp(unix_ts - tt.tm_hour * 60 * 60 - tt.tm_min * 60 - tt.tm_sec)
             

    #初始统计对象 
    def newData_S(self, tagTime, data):
        pData_S = Quote_Data_Statics_M(tagTime, data, self.dataS_Min_Now, self.interval_M)
        return pData_S
    #同步信息天统计
    def sameDataS_Day(self, data):
        pass

    #设置统计信息 
    def setData(self, pData):
        #分钟级数据处理
        time = pData.getTime()
        if(self.dataS_Min_Now == None or self.dataS_Min_Now.checkTimeRange(time, pData) == False):
            #过时间段，重新生成统计对象
            pData_S = self.newData_S(pData.getTime(True), pData)
            self.dataS_Min_Now = pData_S
            self.datasS_Min.append(self.dataS_Min_Now)  
        else:
            #更新统计信息
            self.dataS_Min_Now.setData(pData)
        self.sameDataS_Day(pData); 
    #其他统计接口
    def dataStatics(self, minute = 5):
        pass

    #载入数据
    def loadData(self, strPath = ""):
        #提取分钟数据 
        pDt_csv = myIO_xlsx.DtTable()
        pDt_csv.dataFieldType = Quote_Data_Static().csvFiled_Type()
        pDt_csv.Load_csv(strPath, isUtf = True)

        for x in range(0, len(pDt_csv.dataMat)):
            pData_S = Quote_Data_Static()
            pData_S.fromValueList(pDt_csv.dataMat[x]) 

            pDatas_S = Quote_Data_Statics_M(pData_S.dtTime, self.data, self.dataS_Min_Now, self.interval_M)
            pDatas_S.dataS = pData_S
            self.datasS_Min.append(pDatas_S)
            self.dataS_Min_Now = pDatas_S
        return True
    #保存数据
    def saveData(self, strPath = ""):
        #保存历史数据  
        myIO.Save_File(strPath, self.dataS_Min_Now.dataS.csvHead(), True, False)
        
        #文件追加数据内容
        with open(strPath, 'a+') as f:
            for x in self.datasS_Min: 
                f.write(x.dataS.toCSVString()) 
        return True 


#数据对象集
class Quote_Datas:
    def __init__(self, pData, interval = 1):
        self.name = pData.name
        self.interval_M = interval                      #分钟级间隔
        self.datas = {}                                 #原始数据 
        self.datasS = []                                #统计数据集--天
        self.datasS_M = None                            #统计数据对象--分钟级
        self.data = pData                               #当前数据对象

        self.setting = myQuote_Setting._Find(pData.name)#配置项
        self.autoSave = True 
        self.stoped = False 
        self.tagTime = datetime.datetime.now()
        self.manageTrades = gol._Get_Setting('manageBills_Stock', None)     #使用交易管理器
        gol._Set_Value('datas_Stics_D_' + pData.id, self.datasS)            #全局统计信息


        #保存基础数据
        strDir, strName = myIO.getPath_ByFile(__file__)
        Dir_Base = os.path.abspath(os.path.join(strDir, ".."))   

        self.dir = Dir_Base + "/Data/" + self.name + "/"
        self.fileName = myData_Trans.Tran_ToDatetime_str(pData.getTime(), "%Y-%m-%d")
        myIO.mkdir(self.dir) 
        if(self.loadData()):                            #加载已存数据
            self.setData(pData)
        
    #设置值 
    def setData(self, pData):
        if(len(self.datas) > 0 and self.data.date == pData.date and self.data.time == pData.time):
            return 

        #记录原始数据,更新最新
        self.datas[pData.getTime()] = pData
        self.data = pData
        
        #统计
        self.setData_Statics(pData)
        
        #自动保存数据
        if(self.autoSave):
            self.saveData_stream("", pData)
    #设置统计信息 
    def setData_Statics(self, pData):
        self.datasS_M.setData(pData) 
        self.datasS[0] = self.datasS_M.dataS_Day
        
    #初始统计对象 
    def newData_S(self, pData):
        return Quote_Data_Statics_D(pData, self.interval_M, False)

    #装载excel数据
    def loadData(self, strDir = ""):
        #提取历史数据 
        strPath = self.dir + strDir + "History.csv"
        pDt_csv = myIO_xlsx.DtTable()
        pDt_csv.dataFieldType = Quote_Data_Static().csvFiled_Type()
        pDt_csv.Load_csv(strPath, isUtf = True)

        pDtNow = datetime.datetime.now()
        for x in range(0, len(pDt_csv.dataMat)):
            pData_S = Quote_Data_Static()
            pData_S.fromValueList(pDt_csv.dataMat[x])
            self.datasS.append(pData_S)


        #初始当前(未初始，或六小时内数据，默认当天)
        if(len(self.datasS) < 1 or ((pDtNow - self.datasS[0].dtTime).total_seconds() / 3600 > 6)):
            pData_S = Quote_Data_Static()
            self.datasS.append(pData_S) 

        #载入当天分钟数据集
        self.datasS_M = self.newData_S(self.data)       #只初始
        self.datasS_M.loadData(self.dir + self.fileName + "_M.csv")
        return True
    #提取用户买入信息
    def queryTrade(self, usrName):
        #交易记录
        self.tradeBills = self.manageTrades._Find(usrName)
        if(self.tradeBills == None): 
            self.tradeBills = self.manageBills._Find(billName, True)

        #查询所有未卖出(12个月内)
        lstBill, startTime, endTime = self.tradeBills.Query('', '', 12, '', '买入', self.name, '投资',"股票")
        return lstBill

    #保存为excel数据
    #保存数据
    def saveData(self, strDir = ""):             
        #保存历史数据 
        strPath = self.dir + strDir + "History.csv"
        myIO.Save_File(strPath, self.datasS[0].csvHead(), True, False)
        
        #文件追加数据内容
        with open(strPath, 'a+') as f:
            for x in self.datasS: 
                f.write(x.toCSVString()) 
                
        #保存当天分钟数据集
        self.datasS_M.saveData(self.dir + self.fileName + "_M.csv")

    #保存数据(分段)--单个数据追加
    def saveData_stream(self, file = "", pData = None):
        pTime = pData.getTime()
        if((pTime - self.datasS_M.dtNow).total_seconds() < 1): 
            return False    #未时间步进 

        #文件头写入 
        if(file == ""): file = self.dir + self.fileName + ".csv"
        if(len(self.datas) <= 1): 
            myIO.Save_File(file, pData.csvHead(), True, False)

        #文件追加数据内容
        if(pData == None): pData = self.data
        with open(file, 'a+') as f:
            f.write(pData.toCSVString())    
        self.datasS_M.dtNow = pTime     #更新时间
    #保存数据(分段-合并)
    def saveData_stream_Trans(self, strDir = ""):
        #提取当前数据
        if(strDir == ""): strDir = self.dir
        dictDatas = {}
        if(True):
            myDebug.Print("... load data(" + self.name + ")...")
            path = strDir + self.fileName + ".csv"
            pDt_csv = myIO_xlsx.DtTable()
            pDt_csv.dataFieldType = ['datetime', 'float', 'float', 'float']             #数据字段类型集
            pDt_csv.Load_csv(path, isUtf = True)
        
            #组装数据
            nRows = len(pDt_csv.dataMat)
            for x in range(nRows - 1, -1, -1):
                pData = copy.deepcopy(self.data)
                pData.datetime = None                           #清空时间(必须)
                pData.fromValueList(pDt_csv.dataMat[x])         #由表数据还原
                dictDatas[pData.getTime()] = pData

        #字典排序
        keys = list(dictDatas.keys())
        keys.sort(key = None, reverse = True)
        
        #组装数据
        pDt = myIO_xlsx.DtTable()
        pDt.dataField = self.data.csvHead().split(',')
        pDt.dataMat = []
        for x in keys:
            pDt.dataMat.append(dictDatas[x].toValueList())

        #保存基础数据
        myIO.mkdir(strDir)
        pDt.Save(strDir, self.fileName, row_start = 0, col_start = 0, cell_overwrite = True, sheet_name = self.name, row_end = -1, col_end = -1, bSave_AsStr = False) 


        
#主启动程序
if __name__ == "__main__":
    import myData_Stock
    pData = Quote_Data()
    pData.Print()

    pData = myData_Stock.Data_Stock()
    pData.Print()