# -*- coding: utf-8 -*-
"""
Created on  张斌 2016-10-16 14:00:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com

    DataSet操作 
"""
import sys, os

#加载自定义库
import myEnum, myData_Trans
  
#定义数据结构枚举
myFiledype = myEnum.enum('string', 'float', 'datetime')

#自定义表结构
class Dt:
    def __init__(self):     
        self.dataName = ""  #数据集名称 
        self.dataMat = []   #数据集
        self.dataField = [] #数据字段集

    #载入文件数据(按指定字符分隔)
    def loadDataSet_Row(self, lineArr = []):
        pTypes = self.dataField  
        pValues = []
       
        nLen = len(lineArr) 
        for i in range(0, nLen):
            if(pTypes[i] == myFiledype.float):
                pValues.append(float(lineArr[i]))
                continue

            #其他全部为string
            pValues.append(str(lineArr[i])) 

        #print(pValues)
        return pValues

    def __len__(self):
        return len(self.dataMat) 
    def __getitem__(self, key):
        return self.dataMat[key]
    
    
#载入文件数据(按指定字符分隔)
def loadDataSet(path, offset = 0, strSplit = "\t", filetype = []):
    pDt = Dt()
    dataMat = []

    #路径修正
    if(path.count(":") == 0):
        path = sys.path[0] + "\\" + path
        #print(path)

 
    #打开文件
    if (os.path.exists(path) == False):
        return dataMat
    fr = open(path)
    pLines = fr.readlines() 
    if(len(pLines) < 1):
        return pDt

    #字段类型识别
    line = pLines[offset]
    lineArr = line.strip().split(strSplit)

    pTypes =[]
    nLen = len(filetype)
    nIndex = 0
    for strField in lineArr:
        if(nLen > nIndex):
            #存在设置，优先设置字段类型
            FieldType = myData_Trans.Tran_ToEnum(filetype[nIndex], myFiledype) #参数类型   
            pTypes.append(FieldType)            
        else:
            if(myData_Trans.Is_Numberic(strField)):
                pTypes.append(myFiledype.float)
            else:
                #应该还有个时间判断
                pTypes.append(myFiledype.string)                
        nIndex += 1

    if(len(pTypes) < len(filetype)):
        for i in range(len(pTypes), len(filetype)):
            FieldType = myData_Trans.Tran_ToEnum(filetype[nIndex], myFiledype) #参数类型   
            pTypes.append(FieldType) 
        
    pDt.dataField = pTypes 
    #print(pTypes)
    

    #循环所有
    nIndex = 0
    for line in pLines:
        if offset > nIndex or line.strip() == "":
            nIndex += 1
            continue
        
        #分割解析
        lineArr = line.strip().split(strSplit) 

        #类型转换        
        dataMat.append(pDt.loadDataSet_Row(lineArr))

    pDt.dataMat = dataMat
    return pDt



