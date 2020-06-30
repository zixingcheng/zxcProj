#-*- coding: utf-8 -*-
"""
Created on  张斌 2020-06-35 17:58:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com
    
    自定义简易库表操作-窗体设置记录
"""
import sys, os, time, copy, datetime, mySystem

#引用根目录类文件夹--必须，否则非本地目录起动时无法找到自定义类
mySystem.Append_Us("", False) 
import myIO, myData, myData_DB, myData_Trans, myDebug 



# 窗体设置记录 
class mySet_WinForm():
    def __init__(self, dictSets = None):  
        self.ID = -1
        self.usrID = ""
        self.usrTag = ""
        self.formName = ""          #窗体名称
        self.formType = ""          #窗体类型
        self.formRange = []         #窗体区域
        self.formPos = []           #窗体位置
        self.formRePos = False      #自动复位

        self.datetime = datetime.datetime.now()  
        self.remark = ""            #备注
        self.valid = True
        self.dictSets = {}          #字典型设置信息
        self.Trans_FromDict(dictSets, False)

    # 转换为字典结构
    def Trans_ToDict(self, dictSets = None):  
        if(dictSets == None): dictSets = self.dictSets
        dictSets['ID'] = self.ID
        dictSets['用户名'] = self.usrID
        dictSets['用户标签'] = self.usrTag
        dictSets['窗体名称'] = self.formName
        dictSets['窗体类型'] = self.formType
        dictSets['窗体区域'] = self.formRange
        dictSets['窗体位置'] = self.formPos
        dictSets['自动复位'] = self.formRePos

        dictSets['日期'] = self.datetime
        dictSets['isDel'] = not self.valid 
        dictSets['备注'] = self.remark
        return self.dictSets
    # 转换为对象，由字典结构
    def Trans_FromDict(self, dictSets, canLog = True):  
        #交易信息必须存在
        if(dictSets == None): return False
        bExsit = False; index = -1
        strTime = dictSets.get('日期', "")
        if(type(strTime) != str): strTime = myData_Trans.Tran_ToDatetime_str(dictSets['日期'], "%Y-%m-%d %H:%M:%S")

        #解析信息
        self.ID = dictSets.get('ID',-1)
        self.usrID = dictSets['用户名']
        self.usrTag = dictSets.get('用户标签',"")
        self.stockID = dictSets.get('标的编号',"")
        self.formName = dictSets.get('窗体名称',"")
        self.formType = dictSets.get('窗体类型',"")
        self.formRange = dictSets.get('窗体区域',[])
        self.formPos = dictSets.get('窗体位置',[])
        self.formRePos = dictSets.get('自动复位',False)

        self.datetime = dictSets.get("日期", self.datetime)
        self.remark = dictSets.get("备注", self.remark)
        self.isDel = dictSets.get('isDel', not self.valid)  
        return True

# 自定义简易库表操作-窗体设置记录 
class myDataDB_WinForm(myData_DB.myData_Table):
    def __init__(self, nameDB = "zxcDB_WinForm", dir = ""):  
        #初始根目录信息
        if(dir == ""):
            strDir, strName = myIO.getPath_ByFile(__file__)
            self.Dir_Base = os.path.abspath(os.path.join(strDir, ".."))  
            self.Dir_DataDB = self.Dir_Base + "/Data/Setting/"
            myIO.mkdir(self.Dir_DataDB, False) 
        super().__init__(nameDB, self.Dir_DataDB, False) 
         
    # 检查是否相同--继承需重写  
    def _IsSame(self, rowInfo, rowInfo_Base, tableName = ""): 
        res, sameID = super()._IsSame(rowInfo, rowInfo_Base, tableName)
        if(res): return res, sameID

        # 必须ID相同、是否删除相同
        if(rowInfo['窗体名称'] == rowInfo_Base['窗体名称']): 
            return True, rowInfo_Base['ID']
        return False, sameID
    # 更新
    def _Updata(self, x, rowInfo, bSave = False, bCheck = True): 
        #参数设置更新
        if(bCheck == True):
            psetWinForm = mySet_WinForm(self.rows[x])
            psetWinForm.Trans_FromDict(rowInfo)
            psetWinForm.Trans_ToDict(rowInfo)

        #调用基类更新
        super()._Updata(x, rowInfo, bSave)
    
    # 提取设置集
    def getSets(self, setDB = None): 
        # 查询数据
        if(setDB == None):
            setDB = gol._Get_Value('zxcDB_WinForm')
        dictSet = setDB.Query("isDel==False" , "", True)
        return dictSet
    # 提取设置，指定用户名、股票编号
    def getSet(self, usrNmae, usrTag, formName, isDel = False, setDB = None): 
        # 组装查询条件
        strFilter = F"isDel=={str(isDel)} && 用户名=={usrNmae} && 用户标签=={usrTag} && 窗体名称=={formName}" 

        # 查询数据
        if(setDB == None):
            setDB = gol._Get_Value('zxcDB_WinForm')
        dictSet = setDB.Query(strFilter, "", True)

        # 提取及返回
        lstSet = list(dictSet.values())
        if(len(lstSet) == 1):
            return lstSet[0]
        return None
    
# 窗体控制操作类 
class myWinForm_Control():
    def __init__(self):   
        self.setDB = gol._Get_Value('zxcDB_WinForm') 
        self.setWinForms = {}
        
    # 初始窗体设置类
    def initSet(self, usrID, usrTag, formName, formType, formRange = [], formPos = [], formRePos = False, remark = ''):  
        pSet = mySet_WinForm()
        pSet.ID = -1
        pSet.usrID = usrID
        pSet.usrTag = usrTag
        pSet.formName = formName
        pSet.formType = formType
        pSet.formRange = formRange
        pSet.formPos = formPos
        pSet.formRePos = formRePos
        pSet.remark = remark

        # 添加记录
        self.setDB.Add_Row(pSet.Trans_ToDict(), True, True)
        if(self.setWinForms.get(formName, None) != None):
            self.setWinForms.pop(formName)
        pSet = self.getSet(usrID, usrTag, formName)
        return pSet

    # 提取窗体设置类
    def getSet(self, usrID, usrTag, formName):  
        pSet = self.setWinForms.get(formName, None)
        if(pSet == None):       # 初始未存在项
            dictSet = self.setDB.getSet(usrID, usrTag, formName)
            if(dictSet != None):
                pSet = mySet_WinForm(dictSet)
                self.setWinForms[formName] = pSet
        return pSet
        

# 初始全局消息管理器
from myGlobal import gol 
gol._Init()                 # 先必须在主模块初始化（只在Main模块需要一次即可）
gol._Set_Value('zxcDB_WinForm', myDataDB_WinForm())         #实例 窗体设置库对象 
gol._Get_Value('zxcDB_WinForm').Add_Fields(['用户名', '用户标签', '窗体名称', '窗体类型', '窗体区域', '窗体位置', '自动复位', '日期', '备注'], ['string','string','string','string','list','list','bool','datetime','string'], [])
gol._Set_Value('zxcWinForm_Control', myWinForm_Control())   #实例 窗体控制操作类 



#主启动程序
if __name__ == "__main__":
    #测试库表操作
    pDB = gol._Get_Value('zxcDB_WinForm')
    pCtrl = gol._Get_Value('zxcWinForm_Control')
    
    #初始信息
    pSet = pCtrl.initSet("", "", "Tag_1", formType = "", formRange = [500, 0, 1000, 300], formPos = [600, 200], formRePos = True, remark = '')
    print(pSet.Trans_ToDict())
