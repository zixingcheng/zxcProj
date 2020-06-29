#-*- coding: utf-8 -*-
"""
Created on  张斌 2019-11-16 11:58:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com
    
    自定义数据类型操作-MySql库表
"""
import sys, os, time, copy, json, datetime, mySystem
from collections import OrderedDict
from operator import itemgetter, attrgetter

#引用根目录类文件夹--必须，否则非本地目录起动时无法找到自定义类
mySystem.Append_Us("", False) 
import myData, myData_DB, myData_Trans, myPyMysql, myIO_xlsx, myEnum, myDebug 
from myGlobal import gol 



# 简易库表
class myData_Table(myData_DB.myData_Table):
    def __init__(self, nameDB = "zxcDB", dir = "", oneValid = False, params = {}, initAuto = True):  
        super().__init__(nameDB, dir, oneValid, params, False)

        self.fields = {}            #调整为多字段集缓存
        self.pySql = None           #数据库操作对象
        if(initAuto):
            self._Init_DB(self.dir + self.nameDB + ".md"  )    #初始参数信息等 
    #初始信息库 --重写
    def _Init_DB(self, path): 
        #提取数据库信息 
        host = self.params.get('host', "127.0.0.1")   
        port = self.params.get('port', "3306")   
        charset = self.params.get('charset', "utf8")   
        usrName = self.params.get('usrName', "root")    
        usrPw = self.params.get('usrPw', "root")   
        
        # 测试mysql操作
        #self.pySql = myPyMysql.myPyMysql(usrName='root', usrPw='Zxcvbnm123*', charset='utf8', host = '39.105.196.175')   #远程操作测试
        self.pySql = myPyMysql.myPyMysql(usrName='root', usrPw='Zxcvbnm123*', charset='utf8', host = '127.0.0.1')         #本地操作测试

        #初始数据库-mysql
        #self.pySql = myPyMysql.myPyMysql(usrName=usrName, usrPw=usrPw, charset=charset, host=host, port=port, dbName=dbName)
        if(self.pySql.isExist_DB(self.nameDB) == False):
            self.pySql.createDB_ByFile(self.nameDB, path)

        #切换到当前数据库操作
        self.pySql.initConnect(self.nameDB)
        return True
        
    # 添加字段信息集合 --忽略
    def Add_Fields(self, fieldNames = [], fieldTypes = [], isIndexs = [] ): 
        pass        # sql操作以配置文件为准，简化操作
        return True 
    # 添加字段信息 --忽略
    def Add_Field(self, fieldName, fieldType = myIO_xlsx.myFiledype.string, isIndex = False): 
        pass        # sql操作以配置文件为准，简化操作
        return True 
    # 修改字段信息 --忽略
    def Edit_Field(self, fieldName, fieldName_new, fieldType = myIO_xlsx.myFiledype.string, isIndex = False, addAuto = False): 
        pass        # sql操作以配置文件为准，简化操作
        return True 
    # 移除字段信息 --忽略
    def Remove_Field(self, fieldName, fieldType = myIO_xlsx.myFiledype.string, isIndex = False): 
        pass        # sql操作以配置文件为准，简化操作
        return True 
    # 提取字段信息 --重写 --未实现
    def Get_Field(self, fieldName, tableName = ""): 
        return None
    # 提取字段信息集 --重写
    def Get_Fields(self, tableName = ""): 
        #缓存提取
        pFields = self.fields.get(tableName, None)
        if(pFields == None):
            pFields = self.pySql.queryFields(tableName)
            self.fields[tableName] = pFields
        return pFields
    # 总字段数 --重写 --未实现
    def _FieldsCount(self, tableName = ""): 
        return 0

    
    #生成信息字典 --继承 --未实现
    def OnCreat_RowInfo(self, tableName = ""): 
        return {}
    # 添加行数据 --忽略
    def Add_Row_BySimply(self, strInfo, updata = False, bSave = True):
        pass        # sql操作以配置文件为准，简化操作
        return True 
    # 添加行数据 --重写
    def Add_Row(self, rowInfo = {}, updata = False, bSave = True, tableName = ""):
        # 检查可用性
        id = self._Check(rowInfo, updata, tableName)
        if(id != ""): 
            if(updata == False):
                return "信息已经存在：" + self._Trans_ToStr_Title(rowInfo) + "。"
            else:
                self.pySql._Update(id, rowInfo = rowInfo, tableName = tableName)
                return "信息已经存在，已修改信息如下：\n" + self._Trans_ToStr_Title(rowInfo) 
            
        #单条有效修正
        if(self.oneValid):
            self._Check_oneValid(rowInfo, tableName)
          
        #新增 
        if(self.pySql._Add(tableName = tableName, rowInfo = rowInfo)):
            return "添加成功，信息如下：\n" + self._Trans_ToStr_Title(rowInfo) 
        return "" 
    # 总行数 --重写 --未实现
    def _RowsCount(self, tableName = ""): 
        return -1
    

    # 添加/移除索引字段信息 --忽略
    def _Add_IndexField(self, fieldName, isIndex): 
        pass        # sql操作以配置文件为准，简化操作
        return True    
    # 列索引信息初始 --忽略
    def _Init_Index_Field(self, fieldName, inds = None): 
        pass        # sql操作以配置文件为准，简化操作
        return True 
    # 索引行信息 --忽略
    def _Index(self, rowInfo): 
        pass        # sql操作以配置文件为准，简化操作
        return True 
    # 索引单行-单列数据 --忽略
    def _Index_Field(self, id, value, type, inds = None): 
        pass        # sql操作以配置文件为准，简化操作
        return True 
    

    # 查询筛选--多参数（&&、||）--重写
    def Query(self, fliters, sortField="", reverse=False, tableName = ""): 
        if(reverse and sortField != ""):
           sortField = reverse + "desc"
        return self.pySql._Query(fliter, tableName = tableName, orderField = sortField) 
    # 查询筛选 --重写
    def _Query(self, fliter, tableName = ""): 
        return self.pySql._Query(fliter, tableName = tableName) 
    # 提取与指定筛选条件相同项 --重写
    def _Find_ByFliter(self, field, fliter, data = None, tableName = ""): 
        # 解析条件
        txts = fliter.strip().split(' ')
        if(len(txts) < 2): return data

        # 解析运算符及运算值
        strIF = txts[0]
        value = txts[1]
        if(field == "isDel"):
            type = "bool"
        else:
            pFields = self.Get_Fields(tableName)
            type = pFields[field]['type']
        value = self._Trans_Value_str(value, type) 

        # 按条件组织
        symbol = ""
        if(type != "float" and type != "int"):
            symbol = "'"
        strFliter = F"{field} {strIF} {value}"
        return self.pySql._Query(strFliter, tableName = tableName)
    # 提取当前编号行数据 --重写
    def _Find(self, id, tableName = ""): 
        return self.pySql._Query(F"id={id}", tableName = tableName)

    # 提取当前编号(最大编号+1) 
    def _Get_ID(self, tableName = ""):
        fliter = F"select max(id) as maxid from {tableName};"
        rs = self.pySql.query(fliter)
        if(len(rs) == 0 or rs[0]['maxid'] == None): 
            return 1

        id = myData_Trans.To_Int(rs[0]['maxid'], 0)
        return id + 1
    # 检查是否已经存在 --重写
    def _Check(self, rowInfo, updata = False, tableName = ""): 
        #提取字段信息
        pFields = self.Get_Fields(tableName)

        #修正数据类型 
        for x in pFields:
            value = rowInfo.get(x, "")
            rowInfo[x] = self._Trans_Value(value, pFields[x]['type'])
        if(rowInfo.get("isDel", "") == ""):
            rowInfo["isDel"] = False

        #检查是否已经存在
        rs = self._IsSame(rowInfo, None, tableName)
        if(rs[0]):
            # 修改
            if(updata):
                self._Updata(rs[1], rowInfo)
            return 0
        return "" 
    #单条有效修正 --重写
    def _Check_oneValid(self, rowInfo, tableName = ""): 
        pass 
    # 检查是否相同 --重写  
    def _IsSame(self, rowInfo, rowInfo_Base, tableName = ""): 
        strFliter = ""
        id = rowInfo.get('id', "") 
        if(id != "" and id != 0):
            #ID查询
            strFliter = F"id={id}"
            rs = self.pySql._Query(strFliter, tableName = tableName)
            if(len(rs) > 0):
                sameID = rs[0]
                return True, id
        else:
            #所有条件查询
            pFields = self.Get_Fields(tableName)
            keys = rowInfo.keys()
            for x in keys:
                if(x.lower() == "id"): continue
                if(x.lower() == "edittime"): continue
                type = pFields[x]['type']
                value = rowInfo[x]

                value = self._Trans_Value_str(value, type)
                strFliter += F"and {x}={str(value)} "

            if(strFliter != ""):
                strFliter = strFliter[3:]
                rs = self._Query(strFliter, tableName = tableName)
                
                if(len(rs) > 0):
                    return True, rs[0]['id']
        return False,-1
    # 更新 --重写
    def _Updata(self, x, rowInfo, bSave = False, tableName = "", idField = 'id'): 
        #保持原有编号
        return self.pySql._Update(x, rowInfo, tableName, idField)

            
    #转换行格子数据为字符串 --重写
    def _Trans_Value_str(self, value, bSave_AsStr = True):   
        #特殊类型转换
        type = bSave_AsStr
        strVaulue = str(value)
        if(type == 'datetime'):
            strVaulue = myData_Trans.Tran_ToDatetime_str(value)
        elif(type in ["char","varchar"]):
            strVaulue = "'" + strVaulue + "'"  
        return strVaulue

    #当前数据进行保存 --忽略
    def Save_DB(self, isAppend = False, isUtf = True):   
        pass        # sql操作以配置文件为准，简化操作
        return True



#主启动程序
if __name__ == "__main__":
    #测试库表操作
    pDB = myData_Table()
    
    # 添加行数据
    print(pDB.Add_Row({'字段1': 'value1', '字段2': 'value2'}, tableName="zxcTable_0"))
    print(pDB.Add_Row({'字段1': 'value2', '字段2': 'value3'}, tableName="zxcTable_0"))
    print(pDB.Add_Row({'字段1': 'value2', '字段2': 'value4'}, tableName="zxcTable_0"))
    
    # 自定义筛选
    print("查询：", pDB._Find_ByFliter("字段1", '= value2', tableName="zxcTable_0"))
    print("查询：", pDB._Query("字段1 = 'value2'", tableName="zxcTable_0"))


    print()

