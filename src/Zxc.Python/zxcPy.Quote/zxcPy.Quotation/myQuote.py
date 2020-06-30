#-*- coding: utf-8 -*-
"""
Created on  张斌 2019-03-30 19:58:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com

    监听--股票基类 
"""
import sys, os, time, datetime, threading, mySystem 
import pandas as pd

#引用根目录类文件夹--必须，否则非本地目录起动时无法找到自定义类
mySystem.Append_Us("/Quote_Source", False, __file__)
mySystem.Append_Us("", False)    
import myData_Trans, myDebug, myIO, myIO_xlsx
import mySource_JQData_API, mySource_Sina_API

exInfos = {'XSHG': "上海证券交易所", 'XSHE': "深圳证券交易所", 'sh': "上海证券交易所", 'sz': "深圳证券交易所"}
stockTypes = {'stock': "股票", 'index': "指数", 'etf': "ETF基金", 'opt': "期权"}



#股票信息
class myStock_Info():
    def __init__(self, extype, code, code_name, code_name_En, type = "Stock", area = "CN", exName = "", extype2 = '', source_set = '', source_code = ''): 
        self.extype = extype                #股票交易所代码: 
        self.extype2 = extype2              #股票交易所代码
        self.exName = exName                #股票交易所名称       
        self.code_id = code                 #股票代码    
        self.code_name = code_name          #股票名称  
        if(code_name_En == ""): code_name_En = myData_Trans.Tran_ToStr_FirstLetters(code_name, True)
        self.code_name_En = code_name_En    #数据名称首字母
        self.source_set = source_set        #数据源名称
        self.source_code = source_code      #数据源对应的代码
        
        self.tradeStatus = 1                #状态（1：正常，0：停牌）
        self.type = type                    #数据类型
        self.area = area                    #国家分类
        self.isIndex = self.IsIndex()      
        self.CheckInfo()

    #是否是指数
    def IsIndex(self): 
        if(self.type.lower() == "index"): return True
        if(self.type.lower() == "etf"): return True
        return False
    #信息修正
    def CheckInfo(self): 
        if(self.exName == ''):
            self.exName = exInfos.get(self.extype, '未知')
        if(self.source_set == ''):
            if(self.extype == "XSHE"):
                self.extype = 'sz'
                self.area = 'CN'
            elif(self.extype == "XSHG"):
                self.extype = 'sh'
                self.area = 'CN'
        return True
    
    # 提取板块
    def getMarketBoard(self): 
        return ""
    # 提取标的行业分类
    def getIndustries(self, name='zjw'): 
        if(self.IsIndex()): return []

        quoteSource = gol._Get_Value('quoteSource_API_JqData', None)  #数据源操作对象
        security = self.getID()
        datas = quoteSource.getIndustrys(security)
        return [datas[security][name]['industry_name']]
    # 提取标的概念分类
    def getConcepts(self): 
        return [] 
    # 提取编码信息
    def getID(self, isJQ = True): 
        if(isJQ):
            return self.code_id + "." + self.extype2
        else:
            return self.extype + self.code_id

#股票查询
class myStock:
    def __init__(self): 
        #初始根目录信息
        strDir, strName = myIO.getPath_ByFile(__file__)
        self.Dir_Base = os.path.abspath(os.path.join(strDir, ".."))  
        self.Path_Stock = self.Dir_Base + "/Setting/Setting_Stock.csv"
        self.setFields = ['extype', 'code', 'code_name', 'code_name_En', 'type', 'area', 'exName', 'extype2', 'source_set', 'source_code']

        self.quoteSource = gol._Get_Value('quoteSource_API_JqData', None)  #数据源操作对象
        self.quoteSource_2 = gol._Get_Value('quoteSource_API_Sina', None)  #数据源操作对象
        self.lstStock = []
        self._init_Updata()         #更新配置信息
        self._Init()                #初始配置信息等

    #更新配置信息
    def _init_Updata(self):
        #校检最新 
        bExist = os.path.exists(self.Path_Stock)
        if(bExist):
            t = os.path.getmtime(self.Path_Stock)
            t = time.localtime(t)
        tNow = time.localtime()
        if(bExist == False or tNow.tm_year != t.tm_year or tNow.tm_mon != t.tm_mon or tNow.tm_mday != t.tm_mday):
            #获取标的信息 
            dataSecurities = self.quoteSource.getSecurities(['index', 'stock', 'etf'])

            #循环所有
            data_list = []
            for indexs in dataSecurities.index:
                data = dataSecurities.loc[indexs]
                pDatas = data.name.split('.')
                pDatas.reverse() 

                pDatas.append(data['display_name'])
                pDatas.append(myData_Trans.Tran_ToStr_FirstLetters(data['display_name'], True))
                pDatas.append(data['type'])
                pDatas.append('')
                pDatas.append(exInfos.get(pDatas[0], '未知'))
                pDatas.append(pDatas[0])
                pDatas.append("")
                pDatas.append("")
                 
                if(pDatas[0] == "XSHE"):
                    pDatas[0] = 'sz'
                    pDatas[5] = 'CN'
                elif(pDatas[0] == "XSHG"):
                    pDatas[0] = 'sh'
                    pDatas[5] = 'CN'
                data_list.append(pDatas)
                # pDatas.append(data['name'])
                # pDatas.append(data['start_date'])
                # pDatas.append(data['end_date'])

            '''
            #期权信息
            opts = []
            opts_300ETF = self.quoteSource.getOptInfos("510050.XSHG", 12)
            opts = opts + opts_300ETF
            for x in opts:
                pDatas = []
                pDatas.append(x['name'].split('.')[1])
                pDatas.append(x['name'].split('.')[0])
                pDatas.append(x['display_name'])
                pDatas.append(myData_Trans.Tran_ToStr_FirstLetters(x['display_name'], True))
                pDatas.append(x['type'])
                pDatas.append('')
                pDatas.append(exInfos.get(pDatas[0], '未知'))
                pDatas.append(pDatas[0])
                pDatas.append("JqDataAPI")
                pDatas.append(x['name'])
                
                if(pDatas[0] == "XSHE"):
                    pDatas[0] = 'sz'
                    pDatas[5] = 'CN'
                elif(pDatas[0] == "XSHG"):
                    pDatas[0] = 'sh'
                    pDatas[5] = 'CN'
                data_list.append(pDatas)
                '''
                
            #期权信息
            opts = []
            opts_300ETF = self.quoteSource_2.getOptInfos("50ETF", extype = "sh")
            opts_300ETF = opts_300ETF + self.quoteSource_2.getOptInfos("300ETF", extype = "sh")
            opts = opts + opts_300ETF
            for x in opts:
                pDatas = []
                pDatas.append(x['name'].split('.')[1])
                pDatas.append(x['name'].split('.')[0])
                pDatas.append(x['display_name'])
                pDatas.append(myData_Trans.Tran_ToStr_FirstLetters(x['display_name'], True))
                pDatas.append(x['type'])
                pDatas.append('CN')
                pDatas.append(exInfos.get(pDatas[0], '未知'))
                pDatas.append(x['extype2'])
                pDatas.append("")
                pDatas.append(x['source_code'])
                data_list.append(pDatas)
            self._Init_Default(data_list)
            
            #组合输出结果
            result = pd.DataFrame(data_list, columns=self.setFields)
            result.to_csv(self.Path_Stock, encoding="utf-8", index=False)

    #初始配置信息等
    def _Init(self):            
        #提取字段信息 
        dtSetting = myIO_xlsx.DtTable()  
        dtSetting.dataFieldType = ["","","","",""]
        dtSetting.Load_csv(self.Path_Stock, 1, 0, isUtf = True)
        if(len(dtSetting.dataMat) < 1 or len(dtSetting.dataField) < 1): return

        #转换为功能权限对象集
        for dtRow in dtSetting.dataMat:
            if(len(dtRow) < len(self.setFields)): continue
            pSet = myStock_Info(dtRow[0], dtRow[1], dtRow[2], dtRow[3], dtRow[4], dtRow[5], dtRow[6], dtRow[7], dtRow[8], dtRow[9])
            self._Index(pSet)               #索引设置信息 
    #初始默认配置
    def _Init_Default(self,data_list):
        #data_list.append(['sh','510050','50ETF','50ETF','1']) 
        #data_list.append(['sh','512180','建信MSCI','JXMSCI','1']) 
        #data_list.append(['sz','002958','青农商行','QNSH','1']) 
        pass

    #查找 
    def _Find(self, code_id, code_name = '', code_nameEN = '', exType = "", nReturn = 10):
        if(code_nameEN == ""): code_nameEN = myData_Trans.Tran_ToStr_FirstLetters(code_name, True)
        length = len(code_id)
        length_name = len(code_name)
        length_nameEN = len(code_nameEN)

        lstR = []
        for x in self.lstStock:  
            if(length > 0):
                if(x.code_id[0: length] == code_id):   #等长匹配
                    if(len(lstR) < nReturn): 
                        if(exType == "" or exType == x.extype):
                            lstR.append(x)
                            continue
            
            if(length_name > 0):
                if(x.code_name[0: length_name] == code_name or x.code_name.find(code_name)>=0):   #等长、模糊匹配
                    if(len(lstR) < nReturn): 
                        lstR.append(x)
                        continue
            if(length_nameEN > 0):
                if(x.code_name_En[0: length_nameEN] == code_nameEN):   #等长匹配
                    if(len(lstR) < nReturn): 
                        lstR.append(x)
                    continue 
        return lstR  
    #设置索引
    def _Index(self, pStock): 
        self.lstStock.append(pStock) 
        
#初始全局消息管理器
from myGlobal import gol 
gol._Init()     #先必须在主模块初始化（只在Main模块需要一次即可）
gol._Set_Value('setsStock', myStock())



#主启动程序
if __name__ == "__main__":
    #示例股票查询
    pStocks = myStock() 

    print("代码查询：")
    for x in pStocks._Find("00002"):
        print(x.getIndustries())
        
    print("名称查询：")
    for x in pStocks._Find("", "银行"):
        print(x)
    print("名称查询_EN：")
    for x in pStocks._Find("", "JS"):
        print(x)

    exit(0)

