# -*- coding: utf-8 -*-
"""
Created on  张斌 2018-06-12 18:00:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com

    md文件操作 
"""
import sys, os, codecs, re

#加载自定义库
import myEnum, myData, myIO, myData_Trans
  
#定义数据结构枚举
myMD_node_Type = myEnum.enum('section', 'table')
pattern = '#+\s'


# 设置标题信息
def checkLine(strLine, strTag=""):
    if strTag != "": 
        if strLine.count("<" + strTag) > 0: 
            ind0 = strLine.index("<" + strTag)
            ind2 = strLine.index('>')
            strLine = strLine[0: ind0] + strLine[ind2+1:]
            
            ind0 = strLine.index("</" + strTag)
            ind2 = strLine.index('>')
            strLine = strLine[0: ind0] + strLine[ind2+1:]
    return strLine

# MD节点段信息
class myMD_node:
    def __init__(self, strTitle = ""):
        self.type = myMD_node_Type.section
        self.level = 0          # Node级别
        #self.headID = -1        # Node的标题 ID 
        #self.parentID = -1      # 父级ID
        self.titleName = ""     # 标题名称
        self.titleID = 0        # 标题ID
        self.titleID_str = ""   # 标题ID（父级级联或设定）
        self.contents = []      # 内容
        self.Parent = None      # 父级对象
        self.Childs = []        # 子集
        if(strTitle != ""): self.setTitle(strTitle)
        
    # 设置标题信息
    def setTitle(self, strTitle):
        if not re.match(pattern, strTitle.strip(' \t\n')): return False
        if(strTitle.count('<') > 0):
            strTitle = checkLine(strTitle, "span")
        
        # 提取级别 
        strTitle = strTitle.strip()
        self.level = strTitle.count("#")

        # 提取标题及标题编码
        strTitle = strTitle.replace("#"*self.level, "").strip()
        ind = strTitle.rfind(' ')
        if(ind == -1):
            # 查找非数字非.开始位置
            for x in range(0, len(strTitle)):
                strChar = strTitle[x:x+1]
                if (myData_Trans.Is_Numberic(strChar)) or strChar == "." or strChar == "-":
                    continue
                ind = x - 1
                break;
        
        if(ind == -1):
           self.titleName = strTitle
        else:
            ind += 1
            self.titleID_str = strTitle[0:ind]
            self.titleName = strTitle[ind:]
    def setTitle_info(self, strTitle, level = 0):
        self.titleName = strTitle
        self.level = myData.iif(level < 1, 1, level)

    # 新增子节点
    def addChild(self, child):
        if(child == None): return False
        self.Childs.append(child)
        child.Parent = self
        child.upData_Level()
        return True
    # 新增内容行
    def addContent(self, strContent, bNewLine = True):
        if(type(strContent) == str):
            self.contents.append(strContent + myData.iif(bNewLine, "\r\n", ""))
        else:
            self.contents.append(strContent)
    # 子集更新
    def upData_All(self, nId = 0):
        self.upData_Level()

        if(nId < 1): nId = self.level
        self.upData_ID(nId)

    def upData_Level(self):
        if(self.Parent == None):
            self.level = 1
        else:
            self.level = self.Parent.level + 1
        # 更新子集
        for x in self.Childs:
            x.upData_Level()
    def upData_ID(self, nID = 1):
        self.titleID = myData.iif(nID < 1, 1, nID)

        # 修改子集
        ind = 1
        for x in self.Childs:
            x.upData_ID(ind)
            ind += 1
    
    # 提取内容信息
    def getContent(self, bAll = False, bChild = False):
        strContent = ""
        if(bAll):    # 组装头标题信息
            strContent += self.getTitle() + "\r\n"
        
        # 组装内容
        for x in self.contents:
            if(type(x) != str):
               if(bAll == False): break
               else:
                   if(type(x) == myMD_table):
                       strContent += x.getContent() + "\r\n"
                   continue
            strContent += x

        # 组装子节点信息
        if(bChild):
            for x in self.Childs:
                strContent += x.getContent(bAll, bChild)
        return strContent
    def getTitle(self, bSpanInd = True):
        strTitle = "#" * self.level + " "
        if(self.titleID > 0):
            strTitle += self.gettitleID_str() + " "

        # 标题可能带索引
        if(bSpanInd):
            strTitle += "<span id=" + self.gettitleID_str() + ">"
            strTitle += self.titleName
            strTitle += "</span>"
        else:
            strTitle += self.titleName
        return strTitle
    def gettitleID_str(self):
        self.titleID_str = myData.iif(self.titleID < 1, "", str(self.titleID))

        # 组装父项ID
        strID_pre = ""
        parent = self.Parent 
        while(parent != None):
            strID_pre = str(parent.titleID) + "." + strID_pre
            parent = parent.Parent
        self.titleID_str = strID_pre + self.titleID_str
        return self.titleID_str
    
    # 提取表
    def getTable(self, ind = 0):
        num = -1
        pTable = None
        for x in self.contents:
            if(type(x) == myMD_table):
                num += 1
                if(ind == num): 
                    pTable = x
                    break  
        return pTable

    # 查找键值位置
    def _Find(self, key):
        if(type(key) == int):
            if(key < len(self.Childs)):
                return key
            else:
                return -1
        else:
            ind = -1
            for x in self.Childs:
                ind += 1
                if(x.titleName == key):
                    return ind
            return -1
    # 提取子对象
    def __getitem__(self, key):
        ind = self._Find(key)
        if(ind < 0): return None
        return self.Childs[ind] 
    
# MD表信息
class myMD_tableField:
    def __init__(self, nameFiled = "", col = 0, row = 0):
        self.row = row
        self.col = col
        self.nameFiled = nameFiled
        self.values = []
class myMD_table():
    def __init__(self):
        self.type = myMD_node_Type.table
        self.rows = 0
        self.cols = 0
        self.simpleField = True     # 简单行列结构,复杂需要记录行列数据位置
        self.fields = []            # 字段信息
        self.indFields = []
        
    # 设置表信息
    def setTable(self, lstLines, offset = 0):
        ind = offset
        lstTable = []
        for i in range(offset, len(lstLines)):
            # 两个以上| 则为疑似表格结构
            nNum = lstLines[i].count('|')
            if(nNum > 2):
                ind = i + 1
                while(lstLines[ind].count('|') == nNum):
                    ind += 1
                if(ind - i < 1): continue 

                # 确认为表格结构，提取表格数据
                for x in range(i, ind):
                    line = lstLines[x].strip().strip("|")
                    lstTable.append(line.split('|'))
                break

            # 限定在节点内 
            if(lstLines[i].count('#') > 0): break

        # 解析表格数据信息
        if(len(lstTable) < 1): return ind
        self.cols = len(lstTable[0])
        self.rows = len(lstTable) - 1
        if(lstTable[1][0].count("-") >= 5):
            self.simpleField = False    # 复杂类型

        # 解析表格值信息
        if(self.simpleField):
            for j in range(0, self.cols):
                pField = myMD_tableField()
                pField.col = j
                pField.nameFiled = lstTable[0][j]
                pField.values.append(pField.nameFiled)
                
                # 值表
                for i in range(2, self.rows + 1):
                    pField.values.append(lstTable[i][j].strip())
                addField(pField)
        else:
            # 提取字段信息 
            for j in range(0, self.cols):
                if(lstTable[1][j].count("-") < 5): continue     #忽略字段
                
                # 值表(字段值一对，多值占多行) 
                for i in range(0, self.rows + 1):
                    if(i == 1): continue

                    pField = myMD_tableField()
                    pField.row = myData.iif(i==0, 0, i-1)
                    pField.col = j
                    pField.nameFiled = lstTable[i][j]
                    pField.values.append(lstTable[i][j+1].strip())

                    # 继续向下,合并相同字段
                    for x in range(i + 1, self.rows + 1):
                        celValue = lstTable[x][j].strip()
                        if(celValue == pField.nameFiled or celValue == "^"):
                            pField.values.append(lstTable[x][j+1].strip())
                            continue
                        break
                    self.addField(pField)
        return ind
    def setTable_By_FieldValues(self, fields, values):
        self.__init__()
        self.cols = len(fields)
        self.rows = len(values)

        # 生成字段集信息
        for i in range(0, self.cols):
            self.indFields.append(1)
            pField = myMD_tableField(fields[i], i)
            self.fields.append(pField)

        # 添加值信息
        for x in values:
            self.addRow(x)

    # 添加字段信息
    def addField(self, field):
        if(len(self.indFields) != self.cols):
            self.indFields = [0] * self.cols
        self.indFields[field.col] = 1
        self.fields.append(field)
        field.nameFiled = field.nameFiled.replace("<B>", "").replace("<b>", "").strip()
        for x in field.values:
            x = x.strip()
    # 添加行数据信息
    def addRow(self, valueRow):
        if not self.simpleField: return
        if(type(valueRow) != list): return
        if(len(valueRow) != self.cols): return
        
        # 添加值信息
        for i in range(0, self.cols):
            self.fields[i].values.append(valueRow[i])

    # 提取内容信息
    def getContent(self, bAll = False):
        # 生成表结构
        lstTable = []
        lstField = []
        lstField2 = []
        lstTable.append(lstField)
        lstTable.append(lstField2)

        # 初始行列数据
        if(self.simpleField):
            for x in self.fields:
                lstField.append(x.nameFiled)
                lstField2.append(":---")        # 表字段结构
                
            # 循环填入所有数据
            for i in range(0, self.rows):
                lstValue = []
                lstTable.append(lstValue)
                for x in self.fields:
                    lstValue.append(x.values[i])
        else:
            for x in range(0, self.cols):
                lstField.append("")
                lstField2.append(myData.iif(self.indFields[x] == 1, ":-----", ":---"))
        
            # 初始行列数据
            for x in range(0, self.rows - 1):
                lstTable.append([""] * self.cols)

            # 循环填入所有数据
            for x in self.fields:
                indR = myData.iif(x.row > 0, x.row + 1, x.row)
                lstTable[indR][x.col] = x.nameFiled
                if(len(x.values) > 0):
                    lstTable[indR][x.col+1] = x.values[0]
                    for i in range(1, len(x.values)):
                        lstTable[indR + 1][x.col] = "^"
                        lstTable[indR + 1][x.col+1] = x.values[0]

        # 组装字符串
        strLines = ""
        indR = -1
        for row in lstTable: 
            indR += 1
            if(indR > 0): strLines += "\r\n"
            for i in range(0, self.cols):
                strLines += "| "
                if(not self.simpleField and self.indFields[i] == 1 and indR > 1 and row[i] != "^" and row[i] != ""):
                    strLines += "<b>"
                strLines += row[i] + " "
            strLines += "|"
        return strLines.strip() 

    # 查找键值位置
    def _Find(self, key):
        if(type(key) == int):
            if(key < len(self.fields)):
                return key
            else:
                return -1
        else:
            ind = -1
            for x in self.fields:
                ind += 1
                if(x.nameFiled == key):
                    return ind
            return -1
    # 提取子对象
    def __getitem__(self, key):
        ind = self._Find(key)
        if(ind < 0): return None
        return self.fields[ind] 

# MD节点段信息集
class myMD:
    def __init__(self, path=""):
        self.nodesMD = []
        self.Current = None 
        if(path != ""): self.loadMD(path)

    # 加载md文件 
    def loadMD(self, path):
        # 文件必须存在 
        if (os.path.exists(path) == False): return False

        # 提取所有行数据、解析所有
        lstLines = myIO.getContent(path, True, True)
        ind = 0
        for i in range(0, len(lstLines)):
            if i < ind: continue
            line = lstLines[i]

            # 解析标题、内容分别处理
            if re.match(pattern, line.strip(' \t\n')):
                self.addNode(myMD_node(line))
            else:
                # 内容，逐行记录
                if(line.count('|') > 2):
                    pTable = myMD_table()
                    ind = pTable.setTable(lstLines, i) 
                    if (ind > i):
                        self.Current.contents.append(pTable)
                        continue;
                self.Current.contents.append(line)
                continue
    # 保存md文件 
    def saveMD(self, path):
        self.upData_ALl()
        strContent = self.getContent()
        myIO.Save_File(path, strContent, True, True)

    # 提取内容信息
    def getContent(self): 
        # 组装字符串
        strLines = ""
        for md in self.nodesMD: 
            strLines += md.getContent(True, True)
        return strLines
    
    # 添加节点
    def addNode(self, node):
        if(self.upData_Current(node) == 0):
            self.nodesMD.append(node)
        node.upData_Level()
                            
    # 更新当前节点  
    def upData_Current(self, node):
        # 初始记录节点信息
        if(self.Current == None or node.level <= 1):
            self.Current = node
            return 0

        # 更新节点信息
        if(self.Current.level < node.level):
            # 当前标题级别比前一个小，则为子ID
            self.Current.addChild(node)
            self.Current = node
        else:
            # 同级或更高级(非顶级)
            parent = self.Current.Parent
            while(parent != None and parent.level >= node.level):
                parent = parent.Parent

            # 更新
            if(parent != None):
                parent.addChild(node)
                self.Current = node
        return 1
    def upData_ALl(self):
        ind = 1
        for x in self.nodesMD:  
            x.upData_All(ind);
            ind += 1
    
    # 查找键值位置
    def _Find(self, key):
        if(type(key) == int):
            if(key < len(self.nodesMD)):
                return key
            else:
                return -1
        else:
            ind = -1
            for x in self.nodesMD:
                ind += 1
                if(x.titleName == key):
                    return ind
            return -1
    # 提取子对象
    def __getitem__(self, key):
        ind = self._Find(key)
        if(ind < 0): return None
        return self.nodesMD[ind] 


if __name__ == '__main__': 
    filename= "D:\\Test\\test.md"
    #getMenu(filename)
    pMD = myMD(filename)

    # 提取测试
    pMD[0][0][1].headID = 1000
    aa = pMD[0][0][1]
    aa2 = pMD['sf']
    stra = pMD[0].getContent()

    pTable = pMD[0].getTable()
    aaaa = pTable["库类型"].values[0]

    pMD.saveMD("D:\\Test\\test.md")
    bb =1