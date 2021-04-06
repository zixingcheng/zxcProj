#-*- coding: utf-8 -*-
"""
Created on  张斌 2019-08-27 15:58:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com
    
    自定义数据类型操作-简易库表
"""
import sys, os, time, copy, json, datetime, mySystem
from collections import OrderedDict
from operator import itemgetter, attrgetter

#引用根目录类文件夹--必须，否则非本地目录起动时无法找到自定义类
mySystem.Append_Us("", False) 
import myData, myData_DB, myData_DB_Mysql, myDebug 
from myGlobal import gol 


# 自定义简易库表操作-股票风险设置记录 
class myDataDB_Company(myData_DB_Mysql.myData_Table):
    def __init__(self, nameDB , dir):  
        #初始根目录信息
        super().__init__(nameDB, dir, True, {"hasAliaName": True}) 
        
    #生成信息字典
    def OnCreat_RowInfo(self, tableName = ""): 
        rowInfo = super().OnCreat_RowInfo(tableName)
        rowInfo['companyNumProcess'] = 0
        rowInfo['companyRecycle'] = 0
        rowInfo['companyVolumeTotal'] = 0
        rowInfo['companyRedate'] = "-"
        rowInfo['companyRevolume'] = 0
        rowInfo['companyTransferredvolume'] = 0
        rowInfo['companyNoTransferredvolume'] = 0
        return rowInfo

    # 单条有效修正
    def _Check_oneValid(self, rowInfo, tableName = ""): 
        if(rowInfo.get('companyID', '') != ""):
            datas = self.Query("companyID== " + rowInfo['companyID'])
            for x in datas:
                datas[x]['isDel'] = True
        return True
    # 检查是否相同 --重写  
    def _IsSame(self, rowInfo, rowInfo_Base, tableName = ""): 
        bRes, sameID = super()._IsSame(rowInfo, rowInfo_Base, tableName)
        if(bRes): return bRes, sameID
        
        # 组装查询条件
        strFilter = F"isDel==False && companyID=='{rowInfo['companyID']}' && companyName=='{rowInfo['companyName']}'" 
        rs = self._Query(strFilter, tableName = tableName)
        if(len(rs) > 0):
            return True, rs[0]['ID']
        return False, sameID
    
    # 提取设置集
    def getCompanyIDs(self, dataDB = None): 
        # 查询数据
        if(dataDB == None):
            dataDB = gol._Get_Value('dbCompany_fb')
        dictSet = dataDB.Query("isDel==False" , "", True, "Task_OrderCompany")
        return dictSet
    # 提取设置，指定公司名、公司代码
    def getCompany(self, idCompany, nameCompany, isDel = False, dataDB = None): 
        # 组装查询条件
        strFilter = F"isDel=={str(isDel)}" 
        if(idCompany != ""): strFilter += F" && companyID=='{idCompany}'"
        if(nameCompany != ""): strFilter += F" && companyName=='{nameCompany}'"

        # 查询数据
        if(dataDB == None):
            dataDB = gol._Get_Value('dbCompany_fb')
        lstData = dataDB.Query(strFilter, "", True, "Task_OrderCompany")
        #dictData = dataDB.Query(strFilter, "", True, "Task_OrderCompany")

        # 提取及返回
        #lstData = list(dictData.values())
        if(len(lstData) == 1):
            return lstData[0]
        return None
    # 提取符合筛选条件的公司信息
    def getCompanys(self, param = "", isDel = False, page = 1, per_page = 10, dataDB = None): 
        # 组装查询条件
        strFilter = F"isDel=={str(isDel)}"
        if(param != ""):
            strFilter += F" && {param}" 
        
        # 查询数据
        if(dataDB == None):
            dataDB = gol._Get_Value('dbCompany_fb')
        if(True):
            values = dataDB.Query(strFilter, "", True, "Task_OrderCompany")
            return len(values), values
        else:
            dictData = dataDB.Query(strFilter, "", True, "Task_OrderCompany")
            lstData = list(dictData.values())

            # 提取及返回
            numData = len(lstData)
            start = page * per_page - per_page;
            end = page * per_page;
            end = myData.iif(end < numData, end, numData)
            values = []
            if(numData > start):
                for x in range(start, end):
                    values.append(lstData[x])
            return len(lstData), values

