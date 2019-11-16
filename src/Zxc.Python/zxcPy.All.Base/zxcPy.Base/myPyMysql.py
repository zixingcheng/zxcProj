# -*- coding: utf-8 -*-
"""
Created on  张斌 2019-11-07 16:30:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com

    pySql操作 
"""
import os, sys, re
import pymysql
import myData, myDebug



# 自封装pymysql操作  
class myPyMysql():
    def __init__(self, usrName, usrPw, dbName = '', host = '127.0.0.1', port = 3306, charset = 'utf8'): 
        self._usrName = usrName
        self._usrPw = usrPw
        self._dbName = dbName
        self._dbHost = host
        self._dbPort = port
        self._dbCharset = charset
        self.dbCon = None
    # 析构   
    def __del__(self): 
        self.dbCon.close()
        
    # 检查sql连接  
    def checkConnect(self, dbName = ''): 
        if(self.dbCon == None):
            self.initConnect()
        if(dbName != self._dbName):
            self.clossCursor(None, True, True)
            self.initConnect(dbName)
    # 初始sql连接   
    def initConnect(self, dbName = ''): 
        self._dbName = myData.iif(dbName == '', self._dbName, dbName)  
        try:
            self.clossCursor(None, False, True)
            if(self._dbName != ""):
                self.dbCon = pymysql.connect(
                            user = self._usrName,
                            password = self._usrPw,
                            db = self._dbName,
                            host = self._dbHost,
                            port = self._dbPort,
                            charset = self._dbCharset
                            )
            else:
                self.dbCon = pymysql.connect(
                            user = self._usrName,
                            password = self._usrPw,
                            host = self._dbHost,
                            port = self._dbPort,
                            charset = self._dbCharset
                            )
        except Exception as e:
            myDebug.Debug(f'error:{e}')
            return None
        return self.dbCon
    # 初始游标
    def initCursor(self, dbName = ''): 
        try:
            self.checkConnect(dbName)
            cur = self.dbCon.cursor()
            return cur
        except Exception as e:
            myDebug.Debug(f'error:{e}')
            return None
        
    # 判断数据库是否存在
    def isExist_DB(self, dbName):
        # 查询数据库是否存在 
        try:
            rs = self.execute("", 'show databases;')
            db_list = re.findall('(\'.*?\')',str(rs).lower())
            db_list = [re.sub("'",'',each) for each in db_list]

            return dbName.lower() in db_list
        except Exception as e:
            myDebug.Debug(f'error:{e}')
            return False
    # 判断表是否存在
    def isExist_Table(self, tableName):
        try:
            rs = self.execute("", 'show tables;')
            table_list = re.findall('(\'.*?\')',str(rs).lower())
            table_list = [re.sub("'",'',each) for each in table_list]
            
            return tableName.lower() in table_list
        except Exception as e:
            myDebug.Debug(f'error:{e}')
            return False
    # 判断表字段是否存在
    def isExist_Field(self, tableName, fieldName):
        try:
            rs = self.execute("", f'SHOW COLUMNS FROM {tableName};')
            field_list = re.findall('(\'.*?\')',str(rs).lower())
            field_list = [re.sub("'",'',each) for each in field_list]
            
            return fieldName.lower() in field_list
        except Exception as e:
            myDebug.Debug(f'error:{e}')
            return False
         

    # 创建数据库（0：已存在，1：成功，-1：失败）
    def createDB(self, dbName):
        # 查询 数据库是否存在 
        nState = 0
        if(self.isExist_DB(dbName)): 
            myDebug.Debug(f'{dbName}已经存在.\n')
            return nState
        else:
            myDebug.Debug(f"开始创建库{dbName}......")
            try:
                rs = self.execute("", f'CREATE DATABASE {dbName} character set utf8mb4;')
                nState = myData.iif(rs == None, -1, 1)
            except Exception as e:
                myDebug.Debug(f'error:{e}')
                nState = -1
        myDebug.Debug(f'库{dbName}创建完毕!\n')
        return nState
    # 创建数据库表（0：已存在，1：成功，-1：失败）
    def createTable(self, tableName):
        # 查询 数据库是否存在 
        nState = 0
        if(self.isExist_Table(tableName)): 
            myDebug.Debug(f'表{tableName}已经存在.\n')
            return nState
        else:
            myDebug.Debug(f"开始创建表{tableName}......")
            try:
                my_table = f'CREATE TABLE {tableName}(' \
                            f'id INT NOT NULL AUTO_INCREMENT,' \
                            f'PRIMARY KEY (id)' \
                            f')CHARSET="utf8mb4"'
                rs = self.execute("", my_table)
                nState = myData.iif(rs == None, -1, 1)
            except Exception as e:
                myDebug.Debug(f'error:{e}')
                nState = -1
        myDebug.Debug(f'表{tableName}创建完毕!\n')
        return nState
    # 创建数据库表字段（0：已存在，1：成功，-1：失败）
    def createField(self, tableInfo):
        # 循环所有字段信息
        nState = 0
        tableName = tableInfo["tb_name"]
        for i in range(len(tableInfo['fields'])):
            fieldInfo = tableInfo['fields'][i]

            # 创建字段 
            if(self.isExist_Field(tableName, fieldInfo['columnName'])):
                try:
                    rs = self.editField(tableName, fieldInfo)
                    nState = myData.iif(rs == None, -1, 1)
                except Exception as e:
                    myDebug.Debug(f'error:{e}')
                    nState = -1
            else:
                myDebug.Debug(f"开始创建表字段{fieldInfo['columnName']}......")
                try:
                    field_length = fieldInfo.get("fieldLength", 0)
                    field_length = myData.iif(field_length > 0, f"({str(field_length)})", " ")
                    field_notnull = myData.iif(fieldInfo.get("nullable", False), "", "NOT NULL")
                    field_default = fieldInfo.get("columnDefault", '')
                    field_default = myData.iif(field_default == '', '', f'default {field_default}')

                    ad_col = f'alter table {tableInfo["tb_name"]} add ' \
                        f'{fieldInfo["columnName"]} ' \
                        f'{fieldInfo["dataType"]}{field_length} ' \
                        f'{field_notnull} {field_default}'
                    rs = self.execute("", ad_col)
                    nState = myData.iif(rs == None, -1, 1) 
                except Exception as e:
                    myDebug.Debug(f'error:{e}')
                    nState = -1
                myDebug.Debug(f'表字段{fieldInfo["columnName"]}创建完毕!')
        myDebug.Debug(f'表{tableName}字段创建完毕!\n')
        return nState
    # 编辑数据库表字段（0：不存在，1：成功，-1：失败）
    def editField(self, tableName, fieldInfo):
        #字段必须存在
        myDebug.Debug(f"开始校正表字段{fieldInfo['columnName']}......")
        nState = 0
        fieldName = fieldInfo['columnName']
        if(self.isExist_Field(tableName, fieldName)):
            try:
                #提取表字段信息
                rows = self.queryField(tableName, fieldName)
                if(len(rows) == 1):
                    pRow = rows[0]
                            
                    #值类型修改   
                    if(nState > 0): 
                        field_type = fieldInfo.get("dataType", pRow['dataType'])
                        setLength = myData.iif(pRow['strLength'] == 0, pRow['numLength'], pRow['strLength'])
                        field_length = fieldInfo.get("fieldLength", setLength)
                        if(pRow['dataType'] != field_type):    
                            rs = self.execute("", f"ALTER TABLE {tableName} MODIFY {fieldName} {field_type}({str(field_length)});")
                            nState = myData.iif(rs == None, -1, 1)

                    #非空修改    
                    if(nState > 0):
                        field_nullable = fieldInfo.get('nullable', pRow['nullable'])
                        if(pRow['nullable'] != field_nullable):          
                            nullable = myData.iif(fieldInfo['nullable'], "null", "not null")
                            rs = self.execute("", f"ALTER TABLE {tableName} MODIFY {fieldName} {pRow['columnType']} {nullable};")
                            nState = myData.iif(rs == None, -1, 1)
                        
                    #按类型分类比对修改 
                    if(nState > 0): 
                        field_default = fieldInfo.get('columnDefault', pRow['columnDefault'])
                        if(pRow['columnDefault'] != field_default):             #默认值修改
                            if(field_default != ""):
                                rs = self.execute("", f"ALTER TABLE {tableName} ALTER COLUMN {fieldName} SET DEFAULT {fieldInfo['columnDefault']};")
                                nState = myData.iif(rs == None, -1, 1)
                            else:
                                rs = self.execute("", f"ALTER TABLE {tableName} ALTER COLUMN {fieldName} DROP DEFAULT;")
                                nState = myData.iif(rs == None, -1, 1)
                else:
                    nState = -1
            except Exception as e:
                nState = -1
                myDebug.Debug(f'error:{e}')
        return nState

    # 删除数据库（0：不存在，1：成功，-1：失败）
    def dropDB(self, dbName):
        # 查询 数据库是否存在 
        nState = 0
        if(self.isExist_DB(dbName) == False): 
            myDebug.Debug(f'{dbName}不存在.\n')
            return nState
        else:
            myDebug.Debug(f"开始删除库{dbName}......")
            try:
                rs = self.execute(dbName, f'DROP DATABASE {dbName};')
                nState = myData.iif(rs == None, -1, 1)
            except Exception as e:
                myDebug.Debug(f'error:{e}')
                nState = -1
        myDebug.Debug(f'库{dbName}删除完毕!\n')
        return nState
    # 删除数据库表（0：不存在，1：成功，-1：失败）
    def dropTable(self, tableName):
        # 查询 数据库是否存在 
        nState = 0
        if(self.isExist_Table(tableName) == False): 
            myDebug.Debug(f'表{tableName}不存在.\n')
            return nState
        else:
            myDebug.Debug(f"开始删除表{tableName}......")
            try:
                rs = self.execute("", f'DROP TABLE {tableName};')
                nState = myData.iif(rs == None, -1, 1)
            except Exception as e:
                myDebug.Debug(f'error:{e}')
                nState = -1
        myDebug.Debug(f'表{tableName}删除完毕!\n')
        return nState
    # 删除数据库表字段（0：不存在，1：成功，-1：失败）
    def dropField(self, tableName, fieldName):
        # 查询 数据库是否存在 
        nState = 0
        if(self.isExist_Field(tableName, fieldName) == False): 
            myDebug.Debug(f'表{tableName}字段{fieldName}不存在.\n')
            return nState
        else:
            myDebug.Debug(f"开始删除表字段{fieldName}......")
            try:
                rs = self.execute(dbName, f'ALTER TABLE {tableName} DROP {fieldName};')
                nState = myData.iif(rs == None, -1, 1)
            except Exception as e:
                myDebug.Debug(f'error:{e}')
                nState = -1
        myDebug.Debug(f'表{tableName}字段{fieldName}删除完毕!\n')
        return nState


    # 执行命令
    def execute(self, dbName, sql):
        # 查询 数据库是否存在 
        rs = None
        try:
            cur = self.initCursor(dbName)
            cur.execute(sql)

            rs = cur.fetchall()
        except Exception as e:
            myDebug.Debug(f'error:{e}')
            self.dbCon.rollback()
            
        # 关闭连接及返回 
        self.clossCursor(cur, True)
        return rs
    # 通用查询(返回字段信息)
    def query(self, sql):
        result = []
        try:
            cur = self.initCursor()
            cur.execute(sql)
            
            # 按字段组装查询结果 
            rows = cur.fetchall()
            index = cur.description
            for res in rows:
                row = {}
                for i in range(len(index) - 1):
                    row[index[i][0]] = res[i]
                result.append(row)
                
            # 关闭连接及返回 
            self.clossCursor(cur, True)
        except Exception as e:
            myDebug.Debug(f'error:{e}')
            self.dbCon.rollback()
        return result
    # 判断表字段是否存在
    def queryField(self, tableName, fieldName):
        fieldInfo = f"SELECT TABLE_NAME AS 'tableName'," \
                                    "COLUMN_NAME AS 'columnName'," \
                                    "COLUMN_COMMENT AS 'columnComment'," \
                                    "COLUMN_KEY AS 'columnKey'," \
                                    "COLUMN_TYPE AS 'columnType'," \
                                    "COLUMN_DEFAULT AS 'columnDefault'," \
                                    "ORDINAL_POSITION AS 'columnIndex'," \
                                    "EXTRA AS 'columnExtra'," \
                                    "IS_NULLABLE AS 'nullable'," \
                                    "DATA_TYPE AS 'dataType'," \
                                    "CHARACTER_MAXIMUM_LENGTH AS 'strLength'," \
                                    "NUMERIC_PRECISION AS 'numLength'," \
                                    "NUMERIC_SCALE AS 'numBit' " \
                            f"FROM information_schema.`COLUMNS` " \
                            f"WHERE TABLE_SCHEMA = '{self._dbName}' " \
                            f"AND TABLE_NAME = '{tableName}' " \
                            f"ORDER BY  TABLE_NAME, ORDINAL_POSITION;" 
        rows = self.query(fieldInfo)

        #返回指定字段
        if(fieldName != ""):
            for x in rows:
                if(x['columnName'].lower() == fieldName.lower()):
                    return [x]
        return rows

    # 关闭游标、连接，默认提交数据 
    def clossCursor(self, cur, bCommit = True, bCloseCon = False):
        try:
            # 提交更新，关闭游标
            if(bCommit):
                self.dbCon.commit()
            if(cur != None):
                cur.close()
            if(bCloseCon and self.dbCon != None):
                if(self.dbCon.open):
                    self.dbCon.close()
            return True
        except Exception as e:
            myDebug.Debug(f'error:{e}')
            return False




#测试
if __name__ ==  "__main__":
    # 测试mysql操作
    #pMysql = myPyMysql(usrName='root', usrPw='Zxcvbnm123*', charset='utf8', host = '39.105.196.175')   #远程操作测试
    pMysql = myPyMysql(usrName='root', usrPw='Zxcvbnm123*', charset='utf8', host = '127.0.0.1')         #本地操作测试
    

    pMysql.createDB('myTestDB')
    pMysql.initConnect('myTestDB')
    pMysql.createTable('zxcTest')
    pMysql.createField({'tb_name': 'zxcTest', 'fields': [{"columnName": 'clo_test_1', "dataType": 'CHAR', "fieldLength": 13}]})
    pMysql.createField({'tb_name': 'zxcTest', 'fields': [{"columnName": 'clo_test_2', "dataType": 'int', "columnDefault": 0}]})
    pMysql.createField({'tb_name': 'zxcTest', 'fields': [{"columnName": 'clo_test_1', "dataType": 'CHAR', "fieldLength": 11, "columnDefault": "-1", "nullable": False}]})
    pRow2 = pMysql.queryField('zxcTest', 'clo_test_2')
    pRow1 = pMysql.queryField('zxcTest', 'clo_test_1')
    
    pMysql.initConnect('myTestDB')
    pMysql.dropField('zxcTest', 'clo_test_2')
    pMysql.dropField('zxcTest', 'clo_test_1')
    pMysql.dropTable('zxcTest')
    pMysql.dropDB('myTestDB')

     
    pass