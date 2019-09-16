#-*- coding: utf-8 -*-
"""
Created on  张斌 2018-06-25 10:58:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com

    监听--设置对象
"""
import sys, os, datetime, uuid, mySystem 

#引用根目录类文件夹--必须，否则非本地目录起动时无法找到自定义类
mySystem.Append_Us("", False)    
import myIO, myIO_xlsx, myData, myData_Trans, myQuote
from myGlobal import gol 
gol._Init()     #先必须在主模块初始化（只在Main模块需要一次即可）


        
#监听--设置对象
class myQuote_Setting():
    def __init__(self, monitorTag): 
        self.monitorTag = monitorTag    #监测类型标识    
        self.isValid = False            #设置是否生效
        self.setStr = ''                #完整设置
        self.mark = ''                  #备注说明
        self.msgUsers = {}              #消息发送用户字典(用户名：平台)  
    #是否为空
    def IsNull(self): 
        return len(self.msgUsers) == 0
    #配置字符串
    def ToString(self): 
        return ""

#监听--设置对象集(统一管理)
class myQuote_Settings():
    def __init__(self, exType, code_id, code_name, code_name_En): 
        self.stockInfos = gol._Get_Value('setsStock', None)
        self.stockInfo = None           #股票信息
        self.setTag = ""                #名称标识 
        self.settings = {}              #各监测对象设置
        self.Init(exType, code_id, code_name, code_name_En)    
    #初始股票信息
    def Init(self, exType, code_id, code_name, code_name_En): 
        pTocks = self.stockInfos._Find(code_id, code_name, code_name_En, exType)
        if(len(pTocks) == 1):  
            self.stockInfo = pTocks[0]      #唯一时有效
        else:
            self.stockInfo = None
            return False

        #更新信息
        if(self.stockInfo != None):
            self.setTag = self.stockInfo.extype + self.stockInfo.code_id     
            self.isIndex = self.stockInfo.IsIndex()
        return True
    #是否可用
    def IsEnable(self):
        bNull = True
        for x in self.settings:
            bNull = bNull and self.settings[x].IsNull()
        return not bNull
    #查找改设置的所有用户
    def _Find_Usrs(self):
        lstUsr = []
        for x in self.settings:
            pSetting = self.settings[x]
            for xx in pSetting.msgUsers:
                if(not xx in lstUsr):
                    lstUsr.append(xx)
        return lstUsr

    #提取配置信息
    def GetSetting(self, monitorTag): 
        return self.settings.get(monitorTag, None)
    #添加股票设置信息
    def AddSetting(self, pSetting): 
        if(pSetting != None and pSetting.monitorTag != ""):
            self.settings[pSetting.monitorTag] = pSetting
    #移除股票设置信息
    def RemoveSetting(self, usrID): 
        for x in self.settings.keys():
            pSetting = self.settings[x]  
            if(usrID in pSetting.msgUsers): 
                pSetting.msgUsers.pop(usrID)
        return True

#监听--设置对象集管理
class myQuote_Sets():
    def __init__(self): 
        self.sets = []              #设置集(不排序)
        self.setList = {}           #设置集(按名称索引)
        self.setList_Tag = {}       #设置集--(按Tag索引)
        self.setUsers = {}          #设置用户信息集

        #初始根目录信息
        strDir, strName = myIO.getPath_ByFile(__file__)
        self.Dir_Base = os.path.abspath(os.path.join(strDir, ".."))  
        self.Dir_Setting = self.Dir_Base + "/Setting"
        self.Path_SetQuote = self.Dir_Setting + "/Setting_Quote.csv"
        self.lstFields = ["代码","名称","类型","国家","是否指数","监测类型","是否生效","完整设置","消息发送用户","备注"]   
        self._Init()
    #初始参数信息等   
    def _Init(self):            
        #提取字段信息  
        dtSetting = myIO_xlsx.DtTable() 
        dtSetting.dataFieldType = ["","","","","bool","","bool","","",""]
        dtSetting.Load_csv(self.Path_SetQuote, 1, 0, isUtf = True) 
        if(len(dtSetting.dataMat) < 1 or len(dtSetting.dataField) < 1): return

        #转换为功能权限对象集
        lstFields_ind = dtSetting.Get_Index_Fields(self.lstFields)
        for dtRow in dtSetting.dataMat:
            if(len(dtRow) < len(self.lstFields)): continue
            strSet = myData_Trans.Tran_ToStr(dtRow, ',')
            self._Init_BySet_str(strSet)
    #初始参数信息--设置 
    def _Init_BySet_str(self, strSet):
        strSets = strSet.split(',')
        if(len(strSets) < 10): return False

        #初始设置集
        ids = strSets[0].split('.')
        pSet = self._Find("", ids[0] + ids[1])
        if(pSet == None):
            pSet = myQuote_Settings(ids[0], ids[1], "", "")
            self._Index(pSet)

        #按类型初始
        if(pSet):
            monitorTag = strSets[5]
            pSetting = pSet.settings.get(monitorTag, None)
            if(pSetting == None):
                if(monitorTag == "整点播报" or monitorTag == "涨跌监测"):   #特殊类型处理
                    pSetting = myQuote_Setting(monitorTag)
                else:
                    pSetting = None
                    return False

            #底层属性提取
            pSetting.monitorTag = monitorTag
            pSetting.isValid = myData_Trans.To_Bool(strSets[6])
            pSetting.setStr = strSets[7]
            pSetting.mark = strSets[9]
            msgUsers = myData_Trans.Tran_ToDict(strSets[8].replace('，', ','))
            for x in msgUsers:
                pSetting.msgUsers[x] = msgUsers[x]
            pSet.AddSetting(pSetting)
            self._Index_User(pSet)
            return True
        return False
    
    #保存
    def _Save(self):            
        dtSetting = myIO_xlsx.DtTable()     #监听设置信息表
        dtSetting.dataName = "dataName"
        dtSetting.dataField = self.lstFields
        dtSetting.dataFieldType = ["","","","","bool","","bool","","",""]
        
        # 组装行数据
        for pSet in self.sets:
            if(not pSet.IsEnable()): continue
            for x in pSet.settings:
                pSetting = pSet.settings[x]
                if(pSetting.IsNull()): continue

                pValues = []
                pValues.append(pSet.stockInfo.extype  + "." + pSet.stockInfo.code_id)
                pValues.append(pSet.stockInfo.code_name)
                pValues.append(pSet.stockInfo.type)
                pValues.append(pSet.stockInfo.area) 
                pValues.append(pSet.stockInfo.IsIndex())

                pValues.append(pSetting.monitorTag)
                pValues.append(pSetting.isValid)
                pValues.append(pSetting.setStr)
                pValues.append(str(pSetting.msgUsers).replace(',', '，'))
                pValues.append(pSetting.mark)
                dtSetting.dataMat.append(pValues)

        # 保存
        # dtSetting.Save(self.Dir_Setting, "Setting_Quote", 0, 0, True, "监听设置表", -1, -1, False)
        dtSetting.Save_csv(self.Dir_Setting, "Setting_Quote", True, 0, 0)

    #查找 
    def _Find(self, setName, setTag = ''):
        pSet = None

        #按名称查找
        if(pSet == None and setName != ""):
            pSet = self.setList.get(setName, None)
        if(pSet == None and setTag != ''):
            pSet = self.setList_Tag.get(setTag.lower()) 
        return pSet  
    #查找用户设置股票集
    def _Find_Sets(self, usrID):  
        dictCode = {}
        listCode = []
        for pSet in self.sets:
            if(dictCode.get(pSet.setTag, None) != None):
                continue
            for x in pSet.settings:
                pSetting = pSet.settings[x]
                if(pSetting.msgUsers != None and pSetting.msgUsers.get(usrID, "") != ""):
                    dictCode[pSet.setTag] = "True"
                    listCode.append(pSet.stockInfo)
                    break
        return listCode
    #查找用户集
    def _Find_Usrs(self):
        return self.setUsers.keys()

    #设置索引
    def _Index(self, pSet): 
        if(self._Find("", pSet.setTag)!=None):return
        self.sets.append(pSet)
        self.setList[pSet.stockInfo.code_name] = pSet
        self._Index_User(pSet)
                
        #用户集--(按标识索引)
        if(pSet.setTag != ""):
            self.setList_Tag[pSet.setTag.lower()] = pSet
    #设置索引--用户
    def _Index_User(self, pSet, usrID = ""): 
        for x in pSet.settings:
            pSetting = pSet.settings[x] 
            #索引所有用户
            for xx in pSetting.msgUsers:
                pUserInfo = self.setUsers.get(xx, {})
                pLstCode = pUserInfo.get(pSetting.monitorTag, [])
                if(not pSet.setTag in pLstCode):
                    pLstCode.append(pSet.setTag)
                pUserInfo[pSetting.monitorTag] = pLstCode
                self.setUsers[xx] = pUserInfo
        return True
    #移除索引--用户
    def _Index_User_remove(self, pSet, usrID = ""): 
        for x in pSet.settings:
            pSetting = pSet.settings[x]
            if(usrID != ""):
                #索引所有用户
                pUserInfo = self.setUsers.get(usrID, {})
                pLstCode = pUserInfo.get(pSetting.monitorTag, [])
                if(pSet.setTag in pLstCode):
                    pLstCode.remove(pSet.setTag)
        return True

    # 设置修改
    def _Edit(self, exType, code_id, code_name, strSets = {}):
        bResult = True
        for x in strSets:
            pSet = strSets[x]
            strSet = x + "," + str(pSet.get("isValid",False)) + "," + pSet.get("setStr","") + "," + str(pSet.get("msgUsers","")).replace(',', '，') + "," + pSet.get("mark", "")
            bResult = bResult and self._Init_BySet_str(exType + "." + code_id + "," + code_name + ",,,," + strSet)
        if(bResult): self._Save()
        return bResult   
    # 设置移除
    def _Remove(self, exType, code_id, code_name, usrID):
        bResult = True
        pSet = self._Find(code_name, exType + code_id)
        if(pSet != None):
            bResult = pSet.RemoveSetting(usrID)
            if(bResult): 
                self._Index_User_remove(pSet, usrID)
                self._Refresh(pSet, usrID) 
        if(bResult): self._Save()
        return bResult    
    # 设置更新--移除多余
    def _Refresh(self, pSet, usrID):
        #for x in pSet.settings.keys():
        #    if(len(pSet.settings[x].msgUsers) == 0):
        #        pSet.settings.pop(x)  #报错
        pUser = self.setUsers.get(usrID, {})


#初始全局消息管理器
from myGlobal import gol 
gol._Init()     #先必须在主模块初始化（只在Main模块需要一次即可）
gol._Set_Value('setsQuote', myQuote_Sets())

#查找 
def _Find(setName, setTag = '', bCreatAuto = False):
    pSets = gol._Get_Value('setsQuote')
    if(pSets != None):
        pSet = pSets._Find(setName, setTag)
        if(pSet == None and bCreatAuto):
            pSet = myQuote_Setting(setTag, setName)
        return pSet
    return None


#主启动程序
if __name__ == "__main__":
    pSets = gol._Get_Value('setsQuote')

    #修改测试
    editInfo = {}
    editInfo["整点播报"] = {'isValid': True, 'setStr': '', 'msgUsers': {'@*测试群':'wx','茶叶一主号':'wx'}, 'mark':'测试设置' }
    editInfo["涨跌监测"] = {'isValid': True, 'setStr': '', 'msgUsers': {'@*测试群':'wx'}, 'mark':'测试设置' }
    pSets._Edit("sh", "000001", "", editInfo)
    editInfo["整点播报"] = {'isValid': True, 'setStr': '', 'msgUsers': {'茶叶一主号':'wx'}, 'mark':'测试设置' }
    editInfo["涨跌监测"] = {'isValid': True, 'setStr': '', 'msgUsers': {'茶叶一主号':'wx'}, 'mark':'测试设置' }
    pSets._Edit("sh", "000001", "", editInfo)

    #查找指定用户全部设置
    lstStock = pSets._Find_Sets("茶叶一主号")
    print("设置信息：")
    for x in lstStock:
        print(x.code_name)

    #移除用户设置()
    pSets._Remove("sh", "000001", "", '茶叶一主号')
    print("\n用户信息：")
    for x in pSets._Find_Usrs():
        print(x)

    #查找
    print("查找：")
    pSet = _Find("建设银行")
    print(pSet)
