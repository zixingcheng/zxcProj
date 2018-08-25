# -*- coding: utf-8 -*-
"""
Created on  张斌 2018-01-03 18:00:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com

    Excel操作 
    @依赖库： xlrd、xlwt
"""
import sys, os, datetime, codecs
import xlrd, xlwt 

#加载自定义库
import myEnum, myData, myIO, myData_Trans
  
#定义数据结构枚举
myFiledype = myEnum.enum('string', 'float', 'int', 'datetime')

#自定义表结构
class DtTable:
    def __init__(self):     
        self.dataName = ""      #数据集名称 
        self.dataMat = []       #数据集
        self.dataField = []     #数据字段集
        self.dataFieldType = [] #数据字段类型集
        self.sheet = None       #Sheet
        self.sheet_index = 0    #Sheet索引号
    def _Rows(self, row_end = -1):
        return myData.iif(row_end < 0 , len(self.dataMat), row_end)
    def _Cloumns(self, col_end = -1):
        return myData.iif(col_end < 0 , len(self.dataField), col_end)
        
    #载入文件数据
    def Load(self, strPath, sheet_index = 0, row_start = 1, col_start = 0, all_row = True, field_index = 0):
        #打开文件 
        if (os.path.exists(strPath) == False):
            return False         
        workbook = xlrd.open_workbook(strPath)
        
        # 获取所有sheet
        #print (workbook.sheet_names()) # [u'sheet1', u'sheet2'])
        #sheet2_name = workbook.sheet_names()[0]
        #
        # 获取单元格内容、数据类型
        # print (sheet2.cell(1,0).value.encode('utf-8'))
        # print (sheet2.cell_value(1,0).encode('utf-8'))
        # print (sheet2.row(1)[0].value.encode('utf-8')) 
        # print (sheet2.cell(1,0).ctype)

        # 根据sheet索引或者名称获取sheet内容  sheet2 = workbook.sheet_by_name('sheet2') 
        pSheet = workbook.sheet_by_index(sheet_index)   # sheet索引从0开始
        self.sheet_index = sheet_index
        self.sheet = pSheet

        #提取内容
        pTypes = self.dataFieldType
        nFields = len(pTypes)
        self.dataMat = []
        if(all_row == False): return False
        

        #提取字段信息
        self.dataField = self.loadDt_Row(field_index, col_start, True)

        #循环提取所有行
        for i in range(row_start, pSheet.nrows):
            pValues = self.loadDt_Row(i, col_start)
            self.dataMat.append(pValues)
        return True
    #载入文件数据
    def Load_csv(self, strPath, row_start = 1, col_start = 0, all_row = True, row_field = 0, strsplit = ',', isUtf = False):
        #打开文件 
        lstLines = myIO.getContents(strPath, True, isUtf)
        if(len(lstLines) < 2): return False 

        #提取字段信息   
        if(True):
            self.dataField  = lstLines[row_field].split(strsplit)
            nFields = len(self.dataField )

        #提取内容
        self.dataMat = []
        if(all_row == False): return False
        
        #循环提取所有行
        for i in range(row_start, len(lstLines)):
            pValues = lstLines[i].split(strsplit)
            self.dataMat.append(pValues)
        return True
    #载入文件数据行
    def loadDt_Row(self, ind_row, col_start = 0, isField = False):         
        pTypes = self.dataFieldType
        nFields = len(pTypes)
        pValues = []        
        rows = self.sheet.row_values(ind_row)      # 获取整行内容,列内容: pSheet.col_values(i)
        for j in range(col_start, self.sheet.ncols): 
            if(nFields > j and isField == False):
                if(pTypes[j] == myFiledype.float): 
                    pValues.append(float(rows[j]))
                    continue
                elif(pTypes[j] == myFiledype.datetime): 
                    pValues.append(myData_Trans.Tran_ToDatetime(rows[j]))
                    continue
            
            #其他全部为默认类型
            pValues.append(rows[j]) 
        return pValues

    #保存数据
    def Save(self, strDir, fileName, row_start = 0, col_start = 0, cell_overwrite = True, sheet_name = "", row_end = -1, col_end = -1, bSave_AsStr = True):  
        #创建workbook和sheet对象
        pWorkbook = xlwt.Workbook()  #注意Workbook的开头W要大写
        pName = myData.iif(sheet_name == "","sheet1", sheet_name)
        pSheet = pWorkbook.add_sheet(pName, cell_overwrite_ok = cell_overwrite) 
        
        #循环向sheet页中写入数据
        nCols = self._Cloumns(col_end)
        nRows = self._Rows(row_end)
        if(nRows > 0):
            nCols = myData.iif(col_end < 0 , len(self.dataMat[0]), col_end)
        
        # 写入字段
        for j in range(col_start, nCols):
            pSheet.write(row_start, j - col_start, self.dataField[j])  

        # 写入值
        for i in range(row_start, nRows):
            pValues = self.dataMat[i] 
            for j in range(col_start, nCols): 
                strVaulue = self.Trans_Value_str(pValues[j], bSave_AsStr)
                pSheet.write(i - row_start + 1, j - col_start, strVaulue)                
        
        #保存该excel文件,有同名文件时直接覆盖
        strPath = strDir + "/" + fileName + ".xls"
        strPath.replace("\/", "/")
        strPath.replace("//", "/")
        pWorkbook.save(strPath)
        return True 
    #保存数据
    def Save_csv(self, strDir, fileName, isUtf = False, row_start = 0, col_start = 0, symbol = ",", row_end = -1, col_end = -1, bSave_AsStr = True):  
        nCols = self._Cloumns(col_end)
        nRows = self._Rows(row_end)
        if(nRows > 0):
            nCols = myData.iif(col_end < 0 , len(self.dataMat[0]), col_end)
        
        # 写入字段
        strLines = ""
        for j in range(col_start, nCols):
            if(strLines == ""):
                strLines += self.dataField[j]
            else:
                strLines += symbol + self.dataField[j]
        strLines += "\n"

        #循环所有格子组装数据 
        for i in range(row_start, nRows):
            pValues = self.dataMat[i] 
            strLine = str(pValues[col_start])
            for j in range(col_start, nCols):
                strVaulue = self.Trans_Value_str(pValues[j], bSave_AsStr)
                if(strLine == ""):
                    strLine += strVaulue
                else:
                    strLine += symbol + strVaulue
            strLines += strLine + "\r\n" 

        #保存该csv文件,有同名文件时直接覆盖
        strPath = strDir + "/" + fileName + ".csv"
        myIO.Save_File(strPath, strLines, isUtf)
        return True     #保存数据 
    def Save_csv_append(self, file, pValues = [], isUtf = False, col_start = 0, symbol = ",", col_end = -1, bSave_AsStr = True):   
        # 写入字段
        strLines = ""
        nRows = self._Rows(-1)
        nCols = self._Cloumns(col_end) 
        if(nRows == 0):
            for j in range(col_start, nCols):
                if(strLines == ""):
                    strLines += self.dataField[j]
                else:
                    strLines += symbol + self.dataField[j]
            myIO.Save_File(file, strLines, isUtf, True) 
        
        #组装行数据
        strLine = ""
        for j in range(col_start, nCols):
            strVaulue = self.Trans_Value_str(pValues[j], bSave_AsStr)
            if(strLine == ""):
                strLine += strVaulue
            else:
                strLine += symbol + strVaulue
        
        #文件追加数据内容
        with open(file, 'a+') as f:
            f.write("\n" + strLine)    
        return True 
    #保存数据测试
    def Save_Test(self, strPath, row_start = 0, col_start = 0, cell_overwrite = True, sheet_name = "", row_end = -1, col_end = -1):  
        """
        #-----------使用样式-----------------------------------
        #初始化样式
        style = xlwt.XFStyle()
        #为样式创建字体
        font = xlwt.Font()
        font.name = 'Times New Roman'
        font.bold = True
        #设置样式的字体
        style.font = font
        #使用样式
        sheet.write(0,1,'some bold Times text',style)
        """  
        return True 
    
    #转换行格子数据为字符串
    def Trans_Value_str(self, value, bSave_AsStr = True):        
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

    #字段索引
    def Get_Index_Field(self, fieldName):
        return self.dataField.index(fieldName);
    def Get_Index_Fields(self, fieldNames):
        inds = {} 
        for x in fieldNames:
            inds[x] = self.Get_Index_Field(x)
        return inds;

    #数据长度
    def __len__(self):
        return len(self.dataMat) 
    #数据行
    def __getitem__(self, ind):
        return self.dataMat[ind]
    
    
#载入文件数据(按指定字符分隔)
def loadDataTable(strPath, sheet_index = 0, row_start = 1, col_start = 0, field_index = 0, filetype = []): 
    pDtTable = DtTable() 
    pDtTable.dataFieldType = filetype
    pDtTable.Load(strPath, sheet_index, row_start, col_start, True, field_index)

    #print(pDtTable[0])    
    #pDtTable2 = DtTable()
    #for i in range(0,len(pDtTable[0])):
    #    pValues = []
    #    pValues.append(pDtTable[0][i])
    #    pDtTable2.dataMat.append(pValues)

    #strDir = "F:/Working/张斌/工作文档/程序源码/模型工程化/GModel/src/GModel_Python/GModel_Py_All/GModel_Py_Prj_Department/表格/" 
    #pDtTable2.Save(strDir, "Test3")    
    return pDtTable


def main():
    pTable2 = DtTable()
    pTable2.Load_csv("D:\\myGit\\zxcProj\\src\\Zxc.Python\\zxcPy.Quote\\Data\\农业银行\\2018-07-20.csv")

    strPath = "D:\\我的工作\\学习\\MyProject\\zxcProj\\src\\Zxc.Python\\zxcPy.Robot\\Setting\\Setting.xlsx"    
    pTable = loadDataTable(strPath)
    strPath2 = "D:\\我的工作\\学习\\MyProject\\zxcProj\\src\\Zxc.Python\\zxcPy.Robot\\Setting"  
    pTable.Save(strPath2, "Test2")

if __name__ == '__main__':
     exit(main())

