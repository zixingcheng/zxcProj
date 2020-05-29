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
import myData, myData_Trans, myEnum, myIO, myIO_xlsx, myDebug 
from myGlobal import gol 



# 简易库表
class myData_Table():
    def __init__(self, nameDB = "zxcDB", dir = "", oneValid = False, params = {"hasAliaName": False}, initAuto = True): 
        self.dir = dir              #库表路径
        self.nameDB = nameDB        #库表名
        self.fields = OrderedDict() #库表字段信息
        self.fields_index = []      #库表字段-索引信息
        self.rows = OrderedDict()   #库表行数据集(带编号)
        self.indexs = {}            #索引集
        self.oneValid = oneValid    #是否只有一条记录有效
        self.params = params

        #初始根目录信息
        if(self.dir == ""):
            strDir, strName = myIO.getPath_ByFile(__file__)
            self.dirBase = os.path.abspath(os.path.join(strDir, ".."))  
            self.dir = self.dirBase + "/Data/DB_Data/"
            myIO.mkdir(self.dir, False)
        if(initAuto):
            self._Init_DB(self.dir + nameDB + ".csv"  )    #初始参数信息等 
    #初始信息库   
    def _Init_DB(self, path): 
        #提取行信息集
        if(path == ""): return False
        strLines = myIO.getContents(path)
        if(len(strLines) < 1): return False
        hasAlias = self.params.get("hasAliaName", False)
        if(hasAlias and len(strLines) < 2): return False

        #提取字段信息  
        lstTemps = strLines[0].replace("\r\n", "").split(',')
        lstFields_alias = []
        lstFields = []
        lstTypes = []
        lstIndexs = []
        for x in lstTemps:
            #是否索引
            if(x[0:2] == "**"):
                lstIndexs.append(True)
                x = x[2:]
            else:
                lstIndexs.append(False)
            
            #字段和类型
            if(x.count("(") == 1 and x.count(")") == 1):
                temps = x.split("(")
                lstFields.append(temps[0])
                lstFields_alias.append("")
                lstTypes.append(temps[1].replace(")", ""))
            else:
                lstFields.append(x)
                lstFields_alias.append("")
                lstTypes.append("string")
        #别名
        if(hasAlias):
            strLines.pop(0)
            lstFields_alias = strLines[0].replace("\r\n", "").split(',')
        self.Add_Fields(lstFields, lstTypes, lstIndexs, lstFields_alias)

        #提取行数据
        strLines.pop(0)
        for x in strLines:
            self.Add_Row_BySimply(x, False, False)
        return True
        
    # 添加字段信息集合
    def Add_Fields(self, fieldNames = [], fieldTypes = [], isIndexs = [] , fieldNames_alias = []): 
       if(len(fieldNames) < len(fieldTypes) or len(fieldNames) < len(isIndexs)): return False 
       fieldTypes.extend([""]*(len(fieldNames)-len(fieldTypes)))
       isIndexs.extend([""]*(len(fieldNames)-len(isIndexs)))

       #循环添加
       bResult = True
       for x in range(len(fieldNames)):
           if(fieldNames[x].lower() == 'id'): continue
           if(fieldNames[x].lower() == 'isdel'): continue
           bResult = bResult and self.Add_Field(fieldNames[x], fieldTypes[x], isIndexs[x], fieldNames_alias[x])
       return bResult
    # 添加字段信息
    def Add_Field(self, fieldName, fieldType = myIO_xlsx.myFiledype.string, isIndex = False, fieldName_alias = ''): 
        # 以字典方式组织字段头
        if(fieldType == ""):
            fieldType = myIO_xlsx.myFiledype.string
        isIndex = myData_Trans.To_Bool(str(isIndex))

        # 字段方式定义索引
        fieldName = fieldName.replace('\r\n', '').replace('\n', '')
        if(fieldName[:2] == '**'):
            isIndex = True
            fieldName = fieldName[2:]
        self.fields[fieldName] = {'name': fieldName,'nameAlias': fieldName_alias, 'type': fieldType, 'isIndex': isIndex}
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
    def Get_Field(self, fieldName, tableName = ""): 
        return self.fields.get(fieldName, None)
    # 提取字段信息集
    def Get_Fields(self, tableName = ""): 
        return self.fields
    # 总字段数
    def _FieldsCount(self, tableName = ""): 
        return len(self.fields)

    
    #生成信息字典
    def OnCreat_RowInfo(self, tableName = ""): 
        rowInfo = {}
        for x in self.fields:
            rowInfo[x] = ""
        return rowInfo
    # 添加行数据
    def Add_Row_BySimply(self, strInfo, updata = False, bSave = True):
        lines = strInfo.replace('\r\n', '').replace('\n', '').split(',')
        ind = 1
        rowInfo = {}
        for x in self.fields:
            rowInfo[x] = lines[ind]
            ind = ind + 1

        #系统字段初始
        rowInfo["ID"] = myData_Trans.To_Int(lines[0])
        if(len(lines) - 2 == len(self.fields)):
            rowInfo["isDel"] = myData_Trans.To_Bool(lines[len(self.fields) + 1])
        return self.Add_Row(rowInfo, updata, bSave)
    # 添加行数据
    def Add_Row(self, rowInfo = {}, updata = False, bSave = True, tableName = ""):
        # 检查可用性
        id = self._Check(rowInfo, updata)
        if(id != ""): 
            if(updata == False):
                return "信息已经存在：" + self._Trans_ToStr_Title(rowInfo) + "。"
            else:
                self.Save_DB()
                return "信息已经存在，已修改信息如下：\n" + self._Trans_ToStr_Title(rowInfo) 

        # 索引数据
        if(self._Index(rowInfo)):
            #单条有效修正
            if(self.oneValid):
                self._Check_oneValid(rowInfo)

            # 添加数据
            id = rowInfo['ID']
            self.rows[id] = rowInfo

            # 校正存量
            bAppend = (id + 1 < self._Get_ID())
            if(self.oneValid): bAppend = False         #全部重新保存

            #保存--排序
            if(bSave and self.Save_DB(bAppend, True)):
                return "添加成功，信息如下：\n" + self._Trans_ToStr_Title(rowInfo) 
    # 总行数
    def _RowsCount(self, tableName = ""): 
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
    

    # 查询筛选--多参数（&&、||）
    def Query(self, fliters, sortField="", reverse=False, tableName = ""): 
        # 解析参数
        nPos_And = myData.Find_Pos(u'&&', fliters)
        nPos_Or = myData.Find_Pos(u'||', fliters)
        nPos = nPos_And + nPos_Or + [len(fliters)]
        nPos.sort()
        
        #循环查询
        datas = {}
        pos = 0
        for x in nPos:
            fliter =  fliters[pos: x]
            data = self._Query(fliter)
            if(pos == 0):
                datas.update(data)
            else:
                # 按类型组装结果
                xxx = pos -2
                if(xxx in nPos_And):
                    indSames = []
                    for xx in datas:
                        if(xx not in data):
                            indSames.append(xx)

                    #移除不同
                    for xx in indSames:
                        datas.pop(xx)
                elif(xxx in nPos_Or):
                    datas.update(data)

            # 下一个
            pos = x + 2

        #排序
        if(sortField != ""):
            datas = sorted(datas.items(), key = lambda d:d[1].get(sortField,0), reverse = reverse)
        return datas
    # 查询筛选
    def _Query(self, fliter, tableName = ""): 
        lstSymbol = ['==', '!=', '>=', '>', '<=', '<']
        for x in lstSymbol:
            ind = fliter.find(x)
            if(ind < 1): continue

            #解析并执行查询
            field = fliter[0:ind].strip()
            fliter = x + " " + fliter[ind + 2:].strip()
            data = self._Find_ByFliter(field, fliter)
            return data
        return {}
    # 提取与指定筛选条件相同项--继承需重写
    def _Find_ByFliter(self, field, fliter, data = None, tableName = ""): 
        # 解析条件
        if(data == None): data = self.rows
        txts = fliter.strip().split(' ')
        if(len(txts) < 2): return data

        # 解析运算符及运算值
        strIF = txts[0]
        value = txts[1]
        if(field == "isDel"):
            type = "bool"
        else:
            type = self.fields[field]['type']
        value = self._Trans_Value(value, type)

        # 按条件组织
        if(strIF == "=="):
            return {k: v for k, v in data.items() if v[field] == value }
        if(strIF == "!="):
            return {k: v for k, v in data.items() if v[field] != value }
        elif(strIF == ">"):
            return {k: v for k, v in data.items() if v[field] > value }
        elif(strIF == ">="):
            return {k: v for k, v in data.items() if v[field] >= value }
        elif(strIF == "<"):
            return {k: v for k, v in data.items() if v[field] < value }
        elif(strIF == "<="):
            return {k: v for k, v in data.items() if v[field] <= value }
        return data 
    # 提取当前编号行数据
    def _Find(self, id, tableName = ""): 
        return self.rows.get(id, None)

    # 提取当前编号(最大编号+1)        
    def _Get_ID(self, tableName = ""):
        if(self._RowsCount() == 0): return 1
        return list(self.rows.keys())[-1] + 1
    # 检查是否已经存在   
    def _Check(self, rowInfo, updata = False, tableName = ""): 
        #修正数据类型 
        for x in self.fields:
            value = rowInfo.get(x, "")
            rowInfo[x] = self._Trans_Value(value, self.fields[x]['type'])
        if(rowInfo.get("isDel", "") == ""):
            rowInfo["isDel"] = False

        #检查是否已经存在
        keys = self.rows.keys()
        for x in keys:
            rowInfo_Base = self.rows[x]
            if(self._IsSame(rowInfo, rowInfo_Base)[0]): 
                # 修改
                if(updata):
                    self._Updata(x, rowInfo)
                return x
        return "" 
    #单条有效修正
    def _Check_oneValid(self, rowInfo, tableName = ""): 
        pass 
    # 检查是否相同--继承需重写  
    def _IsSame(self, rowInfo, rowInfo_Base, tableName = ""): 
        sameID = -1
        if(rowInfo.get('ID', "") != ""):
            if(rowInfo['ID'] > 0):  # 给定序号时，序号必须相同
                if(rowInfo['ID'] != rowInfo_Base['ID']): return False, sameID
        else:
            rowInfo["ID"] = -1
            return False, sameID
            
        #对比索引，是否完全一致
        for x in self.fields_index:
            if(rowInfo.get(x, "") == rowInfo_Base.get(x, "")):
                return True, sameID

        #对比属性，是否完全一致(可继承重写)
        for x in self.fields:
            if(rowInfo.get(x, "") != rowInfo_Base.get(x, "")):
                return False, sameID
        return True, rowInfo.get('ID', -1)
    # 更新
    def _Updata(self, x, rowInfo, bSave = False, tableName = "", idField = 'id'): 
        #保持原有编号
        rowInfo['ID'] = self.rows[x]['ID']
        self.rows[x] = rowInfo
        if(bSave == True):
            self.Save_DB()

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
    #转换行格子数据为对应数据类型
    def _Trans_Value(self, value, utype):  
        if(utype == "string"):
            return str(value)
        elif(utype == "float"):
            if(type(value) == float): return value
            if(type(value) == int): return value
            return myData_Trans.To_Float(value)
        elif(utype == "int"):
            if(type(value) == int): return value
            return myData_Trans.To_Int(value)
        elif(utype == "bool"):
            if(type(value) == bool): return value
            return myData_Trans.To_Bool(value)
        elif(utype == "datetime"):
            if(type(value) == datetime.datetime): return value
            return self._Trans_Value_Datetime(value)
        elif(utype == "list"):
            if(type(value) == list): return value
            if(value.count("~*^") > 0):
                data = list(json.loads(value.replace("~*^", ",")))
                return data
            else:
                return []
        return value
    #转换行格子数据为日期类型
    def _Trans_Value_Datetime(self, value):  
        return myData_Trans.Tran_ToDatetime(value, "%Y-%m-%d %H:%M:%S")
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
        elif(type(value) == list):
            strVaulue = strVaulue.replace(",", "~*^").replace("'", "\"")
        return strVaulue
    
    #生成list
    def _Trans_ToList(self, rowInfos): 
        #循环所有列
        lisValue = [rowInfos.get("ID", "")]
        for x in self.fields:
            lisValue.append(self._Trans_Value_str(rowInfos.get(x, ""), True))
        lisValue.append(rowInfos.get('isDel', False))
        return lisValue
    #生成字符串信息
    def _Trans_ToStr(self, rowInfos, nSpace = 0, isSimple = False, bTitle = False): 
        return myData_Trans.Tran_ToStr(self._Trans_ToList(rowInfos), ',')
    #生成字符串信息
    def _Trans_ToStr_Title(self, rowInfos, nSpace = 0, isSimple = False): 
        return str(rowInfos)


    #当前数据进行保存   
    def Save_DB(self, isAppend = False, isUtf = True):   
        #保存该csv文件,有同名文件时直接覆盖
        strPath = self.dir + "/" + self.nameDB + ".csv"
        strEnt = myData.iif(isUtf, "\r\n", "\n")

        # 写入字段
        nCols = self._FieldsCount() + 1
        nRows = self._RowsCount()
        strLines = "ID(int)" 
        for x in self.fields:
            strLines += "," + myData.iif(x in self.fields_index, "**", "") + x + "(" + self.fields[x]['type'] + ")"
        strLines += ",isDel(bool)" 

        # 写入字段别名
        if(self.params.get("hasAliaName", False)):
            strLines += strEnt
            for x in self.fields:
                strLines += "," + self.fields[x]['nameAlias']
            strLines += ",isDel(bool)" 


        #循环所有格子组装数据 
        if(isAppend == False or self._RowsCount() == 1):
            for x in self.rows:
                strLines += strEnt + self._Trans_ToStr(self.rows[x])
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
    pDB.Add_Fields(['字段1', '字段2', '字段3', '字段4'], ['str'], [True])
    
    # 添加行数据
    print(pDB.Add_Row({'字段1': 'value1', '字段2': 'value2'}))
    print(pDB.Add_Row({'字段1': 'value2', '字段2': 'value3'}))
    print(pDB.Add_Row({'字段1': 'value2', '字段2': 'value3'}))
    
    # 自定义筛选
    print("查询：", pDB._Find_ByFliter("字段1", '== value2'))


    print()

