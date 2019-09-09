#-*- coding: utf-8 -*-
"""
Created on  张斌 2019-08-27 15:58:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com
    
    自定义数据类型操作-简易库表
"""
import sys, os, time, copy, datetime, mySystem
from collections import OrderedDict
from operator import itemgetter, attrgetter

#引用根目录类文件夹--必须，否则非本地目录起动时无法找到自定义类
mySystem.Append_Us("", False) 
import myData, myData_Trans, myEnum, myIO, myIO_xlsx, myDebug 
from myGlobal import gol 



# 简易库表-行数据
class myData_Row():
    def __init__(self, dictRow = {}): 
        self.dictRow = dictRow      #用户名 
        self.Init_ByInfo(tradeInfo) #按信息解析(简易)
    #初始类型信息检查修正
    def Init_CheckInfo(self, usrOrderType, tradeType = "", tradeType_sub = ""): 
        # 基础信息修正
        self.usrOrderType = myData.iif(usrOrderType == "" or usrOrderType.count("买") == 1, myOrderType.买入, usrOrderType) 
        self.usrOrderType = myData.iif(usrOrderType == "" or usrOrderType.count("卖") == 1, myOrderType.卖出, usrOrderType) 
        self.tradeType = myData.iif(tradeType == "" or tradeType in myTradeType_投资, "投资", tradeType) 
        self.tradeType_sub = myData.iif(tradeType_sub == "", "股票", tradeType_sub) 
        self.tradeTime = myData.iif(self.tradeTime == None, datetime.datetime.now(), self.tradeTime)

        # 股票信息补全
        targets = myData.iif(self.targetID.count('.') == 0, ("." + self.targetID).split('.'), self.targetID.split('.')) 
        pStocks = gol._Get_Value('setsStock', None)
        stocks = pStocks._Find(targets[1], exType = targets[0])
        if(len(stocks) != 1):
            stocks = pStocks._Find(self.targetName)
            if(len(stocks) != 1): return False

        pStock = stocks[0]
        self.tradeType_sub = myQuote.stockTypes.get(pStock.type.lower(), '股票')
        self.targetID = pStock.code_id
        self.targetName = pStock.code_name
        self.targetMarket = pStock.exName
        self.targetMarketBoard = pStock.getMarketBoard()
        self.targetIndustries = pStock.getIndustries()
        self.targetConcepts = pStock.getConcepts()
        return True
    #生成信息字典
    def OnCreat_TradeInfo(self): 
        tradeInfo = {}
        tradeInfo['usrID'] = self.usrID
        tradeInfo['usrOrderType'] = self.usrOrderType
        tradeInfo['recordTime'] = self.recordTime
        tradeInfo['recorder'] = self.recorder
        
        tradeInfo['targetID'] = self.targetID
        tradeInfo['targetName'] = self.targetName
        tradeInfo['targetMarket'] = self.targetMarket
        tradeInfo['targetMarketBoard'] = self.targetMarketBoard
        tradeInfo['targetIndustries'] = self.targetIndustries
        tradeInfo['targetConcepts'] = self.targetConcepts
        tradeInfo['targetPrice'] = self.targetPrice
        tradeInfo['targetPrice_Ex'] = self.targetPrice_Ex
        tradeInfo['targetPosition'] = self.targetPosition

        tradeInfo['infoID'] = self.infoID
        tradeInfo['tradeType'] = self.tradeType 
        tradeInfo['tradeType_sub'] = self.tradeType_sub 
        tradeInfo['tradeNum'] = self.tradeNum
        tradeInfo['tradeMoney'] = self.tradeMoney
        tradeInfo['tradePosition'] = self.tradePosition
        tradeInfo['tradeProfit'] = self.tradeProfit
        tradeInfo['tradeProfit_total'] = self.tradeProfit_total

        tradeInfo['tradeTime'] = self.tradeTime
        tradeInfo['isDel'] = self.isDel
        tradeInfo['remark'] = self.remark
        return tradeInfo
    #生成list
    def ToList(self): 
        lstValue = [self.infoID, self.usrID, self.usrOrderType, self.targetID, self.targetName, self.targetMarket, self.targetMarketBoard, self.targetPrice, self.targetPrice_Ex, self.targetPosition, myData_Trans.Tran_ToStr(self.targetIndustries, symbol = '、'), myData_Trans.Tran_ToStr(self.targetConcepts, symbol = '、'), self.tradeType, self.tradeType_sub, self.tradeNum, self.tradeMoney, self.tradePosition, self.tradeProfit, self.tradeProfit_total, self.tradeTime.strftime("%Y-%m-%d %H:%M:%S"), self.isDel, self.recorder, self.recordTime.strftime('%Y-%m-%d %H:%M:%S'), self.remark]
        return lstValue
    #生成提示信息
    def ToTitlestr(self, nSpace = 0, isSimple = False, usrOrderType = "", tradeTarget = "", tradeType = "", tradeTypeTarget = ""): 
        if(isSimple == False):
            strSpace = " " * nSpace
            strTrade = strSpace + "编号: " + str(self.infoID) + "\n"
            strTrade += strSpace + "用户名: " + self.usrID + "\n"
            strTrade += strSpace + "交易类型: " + self.usrOrderType + "\n"
            strTrade += strSpace + "标的信息: " + self.targetID + "  " + self.targetName + "\n"
            if(self.usrOrderType not in myTradeAppetite):
                strTrade += strSpace + "交易金额: " + str(round(self.tradeMoney, 2)) + "元 \n" 
                strTrade += strSpace + "交易价格: " + str(round(self.targetPrice, 2)) + "元 \n"
            else: 
                strTrade += strSpace + "预期价格: " + str(round(self.targetPrice, 2)) + "元 \n"
            strTrade += strSpace + "账单时间: " + myData_Trans.Tran_ToDatetime_str(self.tradeTime, "%Y-%m-%d") + "\n"
            strTrade += strSpace + "备注: " + self.remark 
        else:
            strTrade = self.tradeParty
            if(trade.usrOrderType not in myTradeAppetite):
                strTrade += "，" + str(round(self.tradeMoney, 2)) + "元" 
            if(usrTradeType == ""): strTrade += "，" + self.usrTradeType
            if(tradeTarget == ""): strTrade += "，" + self.tradeTarget
            if(tradeType == ""): strTrade += "，" + self.tradeType
            if(tradeTypeTarget == ""): strTrade += "，" + self.tradeTypeTarget
            strTrade += "，" + str(self.infoID) 
            strTrade += "，" + myData_Trans.Tran_ToDatetime_str(self.tradeTime, "%Y-%m-%d") 
        return strTrade
    #是否相同
    def IsSame(self, trade, days = 1): 
        if(trade.tradeType == self.tradeType and trade.tradeType_sub == self.tradeType_sub):
            if(trade.targetID == self.targetID and trade.usrID == self.usrID):
                if((datetime.datetime.now() - trade.recordTime).days < days):         #一天内算相同
                    if(trade.usrOrderType in myTradeAppetite):
                        return True
                    else:
                        return trade.usrOrderType == self.usrOrderType
        return False
# 简易库表
class myData_Table():
    def __init__(self, nameDB = "zxcDB", dir = ""):  
        self.dir = dir              #库表路径
        self.nameDB = nameDB        #库表名
        self.fields = OrderedDict() #库表字段信息
        self.fields_index = []      #库表字段-索引信息
        self.rows = OrderedDict()   #库表行数据集(带编号)
        self.indexs = {}            #索引集

        #初始根目录信息
        if(self.dir == ""):
            strDir, strName = myIO.getPath_ByFile(__file__)
            self.dirBase = os.path.abspath(os.path.join(strDir, ".."))  
            self.dir = self.dirBase + "/Data/DB_Data/"
            myIO.mkdir(self.dir, False)
        self._Init_DB(self.dir + nameDB + ".csv"  )    #初始参数信息等 
    #初始信息库   
    def _Init_DB(self, path): 
        #提取行信息集
        if(path == ""): return False
        strLines = myIO.getContents(path)
        if(len(strLines) < 1): return False

        #提取字段信息  
        lstFields = strLines[0].split(',')
        self.Add_Fields(lstFields)

        #提取行数据
        strLines.pop(0)
        for x in strLines:
            self.Add_Row_BySimply(x)
        return True
        
    # 添加字段信息集合
    def Add_Fields(self, fieldNames = [], fieldTypes = [], isIndexs = [] ): 
       if(len(fieldNames) < len(fieldTypes) or len(fieldNames) < len(isIndexs)): return False 
       fieldTypes.extend([""]*(len(fieldNames)-len(fieldTypes)))
       isIndexs.extend([""]*(len(fieldNames)-len(isIndexs)))

       #循环添加
       bResult = True
       for x in range(len(fieldNames)):
           if(fieldNames[x].lower() == 'id'): continue
           bResult = bResult and self.Add_Field(fieldNames[x], fieldTypes[x], isIndexs[x])
       return bResult
    # 添加字段信息
    def Add_Field(self, fieldName, fieldType = myIO_xlsx.myFiledype.string, isIndex = False): 
        # 以字典方式组织字段头
        if(fieldType == ""):
            fieldType = myIO_xlsx.myFiledype.string
        isIndex = myData_Trans.To_Bool(str(isIndex))

        # 字段方式定义索引
        fieldName = fieldName.replace('\r\n', '').replace('\n', '')
        if(fieldName[:2] == '**'):
            isIndex = True
            fieldName = fieldName[2:]
        self.fields[fieldName] = {'name': fieldName, 'type': fieldType, 'isIndex': isIndex}
        self._Add_IndexField(fieldName, isIndex)
        return True
    # 修改字段信息
    def Edit_Field(self, fieldName, fieldName_new, fieldType = myIO_xlsx.myFiledype.string, isIndex = False, addAuto = False): 
        fieldInfo = self.fields.get(fieldName, {})
        if(addAuto and len(fieldInfo) == 0): return

        fieldInfo = {'name': fieldName_new, 'type': fieldType, 'isIndex':isIndex}
        self.fields[fieldName] = fieldInfo
        self._Add_IndexField(fieldName, isIndex)
        return True
    # 移除字段信息
    def Remove_Field(self, fieldName, fieldType = myIO_xlsx.myFiledype.string, isIndex = False): 
        fieldInfo = self.fields.get(fieldName, None)
        if(fieldInfo != None):
            self.fields.pop(fieldName)
            self._Add_IndexField(fieldName, False)
        return True
    # 提取字段信息
    def Get_Field(self, fieldName): 
        return self.fields.get(fieldName, None)
    # 总字段数
    def _FieldsCount(self): 
        return len(self.fields)
    
    
    # 添加行数据
    def Add_Row_BySimply(self, strInfo, updata = False):
        lines = strInfo.replace('\r\n', '').replace('\n', '').split(',')
        ind = 1
        rowInfo = {}
        for x in self.fields:
            rowInfo[x] = lines[ind]
            ind = ind + 1
        return self.Add_Row(rowInfo)
    # 添加行数据
    def Add_Row(self, rowInfo = {}, updata = False):
        # 检查可用性
        id = self._Check(rowInfo, updata)
        if(id != ""): 
            if(updata == False):
                return "信息已经存在：" + str(rowInfo) + "。"
            else:
                self.Save_DB()
                return "信息已经存在，已修改信息如下：\n" + trade.ToTitlestr(4) 

        # 索引数据
        if(self._Index(rowInfo)):
            # 添加数据
            id = rowInfo['ID']
            self.rows[id] = rowInfo

            # 校正存量
            bAppend = (id + 1 < self._Get_ID())
        
            #保存--排序
            if(self.Save_DB(bAppend, True)):
                return "添加成功，信息如下：\n" + str(rowInfo)

    # 总行数
    def _RowsCount(self): 
        return len(self.rows)
    

    # 添加/移除索引字段信息
    def _Add_IndexField(self, fieldName, isIndex): 
        if(isIndex):
            if(fieldName not in self.fields_index):
                self.fields_index.append(fieldName)
            self._Init_Index_Field(fieldName)
        else:
            if(fieldName in self.fields_index):
                self.fields_index.remove(fieldName)      
    # 列索引信息初始  
    def _Init_Index_Field(self, fieldName, inds = None): 
        if(inds == None):
            inds = self.indexs.get(fieldName, None)
            if(inds == None):
                self.indexs[fieldName] = {}

    # 索引行信息
    def _Index(self, rowInfo): 
        # 提取索引值, 未设置则修正
        id = rowInfo.get('ID', -1)
        if(id < 0):
            id = self._Get_ID()
            rowInfo['ID'] = id
            
        # 索引相关列
        for x in self.fields_index:
            inds = self.indexs[x]
            inds[rowInfo[x]] = id 
        return True
    # 索引单行-单列数据
    def _Index_Field(self, id, value, type, inds = None): 
        if(id <= 0 or inds == None): return False

        # 按索引唯一处理
        ind = inds.get(value, None)
        if(ind != None): return "唯一索引已存在！"
        inds[value] = ind 
        return ""
            
    # 提取与指定数据相同项--继承需重写
    def _Find_ByRowInfo(self, rowInfo): 
        return self._Find(0)
    # 提取当前编号行数据
    def _Find(self, id): 
        return self.rows.get(id, None)
    # 提取当前编号(最大编号+1)        
    def _Get_ID(self):
        if(self._RowsCount() == 0): return 1
        return list(self.rows.keys())[-1] + 1

    
    # 检查是否已经存在   
    def _Check(self, rowInfo, updata = False): 
        keys = self.rows.keys()
        for x in keys:
            rowInfo_Base = self.rows[x]
            if(self._IsSame(rowInfo, rowInfo_Base)): 
                # 修改
                if(updata):
                    self.rows[x] = row_base
                return x
        return "" 
    # 检查是否相同--继承需重写  
    def _IsSame(self, rowInfo, rowInfo_Base): 
        if(rowInfo.get('ID', "") != ""):
            if(rowInfo['ID'] == rowInfo_Base['ID']): return True
            
        #对比索引，是否完全一致
        for x in self.fields_index:
            if(rowInfo.get(x, "") == rowInfo_Base.get(x, "")):
                return True

        #对比属性，是否完全一致(可继承重写)
        for x in self.fields:
            if(rowInfo.get(x, "") != rowInfo_Base.get(x, "")):
                return False
        return True 


    # 总行数
    def __len__(self):
        return len(self.rows) 
    def __getitem__(self, key):
        return self.dataMat[key]

     
    #时间转换为月初
    def _Trans_Time_moth(self, dtTime = '', nMonth = 1): 
        if(type(dtTime) != datetime.datetime): dtTime = datetime.datetime.now() 
        dtTime = dtTime - datetime.timedelta(days=(dtTime.day - 1))
        while(nMonth > 1):
            dtTime = self._Trans_Time_moth(dtTime - datetime.timedelta(days=1))
            nMonth -= 1
        strTime = myData_Trans.Tran_ToDatetime_str(dtTime, "%Y-%m-%d")
        return myData_Trans.Tran_ToDatetime(strTime, "%Y-%m-%d")
    #时间转换为年初
    def _Trans_Time_year(self, dtTime = "", nYears = 1): 
        if(type(dtTime) != datetime.datetime): dtTime = datetime.datetime.now() 
        nMonths = dtTime.month 
        if(nYears > 1): nMonths += (nYears -1) * 12
        return self._Trans_Time_moth(dtTime, nMonths)
    #转换行格子数据为字符串
    def _Trans_Value_str(self, value, bSave_AsStr = True):        
        if(bSave_AsStr):
            strVaulue = str(value)
        else:
            strVaulue = value

        #特殊类型转换
        if(type(value) == bool):
            strVaulue = myData.iif(value, "TRUE", "FALSE")
        elif(type(value) == datetime.datetime):
            strVaulue = myData_Trans.Tran_ToDatetime_str(value)
        return strVaulue

    
    #生成行数据信息
    def To_str(self, rowInfos): 
        #循环所有列
        strLine = str(rowInfos.get("ID", ""))
        for x in self.fields:
            strLine += "," + self._Trans_Value_str(rowInfos.get(x, ""), True) 
        return strLine
    #当前数据进行保存   
    def Save_DB(self, isAppend = False, isUtf = True):   
        #保存该csv文件,有同名文件时直接覆盖
        strPath = self.dir + "/" + self.nameDB + ".csv"

        # 写入字段
        nCols = self._FieldsCount() + 1
        nRows = self._RowsCount()
        strLines = "ID" 
        for x in self.fields:
            strLines += "," + myData.iif(x in self.fields_index, "**", "") + x

        #循环所有格子组装数据 
        strEnt = myData.iif(isUtf, "\r\n", "\n")
        if(isAppend == False or self._RowsCount() == 1):
            for x in self.rows:
                strLines += strEnt + self.To_str(self.rows[x])
            myIO.Save_File(strPath, strLines, isUtf, False)
        else:
            #文件追加数据内容
            strLine = self.To_str(self.rows[list(self.rows.keys())[-1]])
            if(isUtf):
                with open(strPath, 'a+',encoding="utf-8") as f:
                    f.write("\n" + strLine)    
            else: 
                with open(strPath, 'a+') as f:
                    f.write("\n" + strLine)    
        return True     #保存数据 




#主启动程序
if __name__ == "__main__":
    #测试库表操作
    pDB = myData_Table()
    pDB.Add_Fields(['字段1', '字段2', '字段3', '字段4'], ['int'], [True])
    
    # 添加行数据
    print(pDB.Add_Row({'字段1': 'value1', '字段2': 'value2'}))
    print(pDB.Add_Row({'字段1': 'value2', '字段2': 'value3'}))
    print(pDB.Add_Row({'字段1': 'value2', '字段2': 'value3'}))
    

    print()

