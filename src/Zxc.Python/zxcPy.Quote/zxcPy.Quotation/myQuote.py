#-*- coding: utf-8 -*-
"""
Created on  张斌 2019-03-30 19:58:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com

    监听--股票基类 
"""
import sys, os, time, datetime, threading, mySystem 
import baostock as bs
import pandas as pd

#引用根目录类文件夹--必须，否则非本地目录起动时无法找到自定义类
mySystem.Append_Us("", False)    
import myData_Trans, myDebug, myIO, myIO_xlsx


#股票信息
class myStock_Info():
    def __init__(self, extype, code, code_name, code_name_En, type = "Stock", area = "CN"): 
        self.extype = extype                #股票交易所代码    
        self.code_id = code                 #股票代码    
        self.code_name = code_name          #数据名称  
        if(code_name_En == ""): code_name_En = myData_Trans.Tran_ToStr_FirstLetters(code_name, True)
        self.code_name_En = code_name_En    #数据名称首字母
        
        self.tradeStatus = 1                #状态（1：正常，0：停牌）
        self.type = type                    #数据类型
        self.area = area                    #国家分类
        self.isIndex = self.IsIndex()      
    #是否是指数
    def IsIndex(self): 
        if(self.type == "Stock" and self.area == "CN"):
            if(self.extype == "sh"): return self.code_id[0:3] == "000"
            if(self.extype == "sz"): return self.code_id[0:3] == "399"
        return False

#股票查询
class myStock:
    def __init__(self): 
        #初始根目录信息
        strDir, strName = myIO.getPath_ByFile(__file__)
        self.Dir_Base = os.path.abspath(os.path.join(strDir, ".."))  
        self.Path_Stock = self.Dir_Base + "/Setting/Setting_Stock.csv"
        self.setFields = ['extype', 'code', 'code_name_En', 'code_name', 'tradeStatus']

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
        if(bExist ==False or tNow.tm_year != t.tm_year or tNow.tm_mon != t.tm_mon or tNow.tm_mday != t.tm_mday):
            #获取最新
            lg = bs.login()  #登陆系统 
            rs = bs.query_all_stock(day="2017-06-30") # 获取全部股票代码

            #添加中文首字母
            data_list = []
            while (rs.error_code == '0') & rs.next():
                # 获取一条记录，将记录合并在一起
                datas = rs.get_row_data()
                pDatas = datas[0].split('.')
                pDatas.append(myData_Trans.Tran_ToStr_FirstLetters(datas[2], True))
                pDatas.append(datas[2])
                pDatas.append(datas[1])
                data_list.append(pDatas)
            bs.logout()  #登陆系统 

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
            pSet = myStock_Info(dtRow[0], dtRow[1], dtRow[3], dtRow[2],"Stock", "CN")
            pSet.tradeStatus = dtRow[4]
            self._Index(pSet)               #索引设置信息 
            
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
        print(x)
        
    print("名称查询：")
    for x in pStocks._Find("", "银行"):
        print(x)
    print("名称查询_EN：")
    for x in pStocks._Find("", "JS"):
        print(x)

    exit(0)

