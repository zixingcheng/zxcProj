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
import myIO, myIO_xlsx, myData, myData_Trans


#监听--设置对象
class myQuote_Setting():
    def __init__(self, datasTag, datasName, datasType = "Stock", area = "CN"): 
        self.setTag = datasTag      #数据标识    
        self.setName = datasName    #数据名称  
        self.setType = datasType    #数据类型
        self.setArea = area         #国家分类
        self.mark = ''              #备注说明
        self.msgUsers_wx = []       #消息发送用户-微信
        
        self.isIndex = False            #是否是指数
        self.isEnable = False           #是否设置有效
        self.isEnable_RFasInt = False   #是否设置有效--涨跌幅监测
        self.isEnable_Hourly = False    #是否设置有效--整点播报

#监听--设置对象集
class myQuote_Settings():
    def __init__(self): 
        self.setList = {}           #设置集(按名称索引)
        self.setList_Tag = {}       #设置集--(按Tag索引)
        self.setUsers = []          #设置用户信息集

        #初始根目录信息
        strDir, strName = myIO.getPath_ByFile(__file__)
        self.Dir_Base = os.path.abspath(os.path.join(strDir, ".."))  
        self.Dir_Setting = self.Dir_Base + "/Setting"
        self.Path_SetQuote = self.Dir_Setting + "/Setting_Quote.csv"
        self.lstFields = ["代码","名称","类型","国家","是否指数","有效性","消息发送用户_wx","涨跌监测","整点播报","备注"]
        self._Init()
    #初始参数信息等   
    def _Init(self):            
        #提取字段信息 
        #dtSetting = myIO_xlsx.loadDataTable(self.Path_SetQuote, 0, 1)            #监听设置信息
        dtSetting = myIO_xlsx.DtTable() 
        dtSetting.Load_csv(self.Path_SetQuote, 1, 0, isUtf = True)

        if(len(dtSetting.dataMat) < 1 or len(dtSetting.dataField) < 1): return
        lstFields_ind = dtSetting.Get_Index_Fields(self.lstFields)

        #转换为功能权限对象集
        for dtRow in dtSetting.dataMat:
            if(len(dtRow) < len(self.lstFields)): continue
            pSet = myQuote_Setting("", "")
            pSet.setTag = dtRow[lstFields_ind["代码"]]
            pSet.setName = dtRow[lstFields_ind["名称"]]
            pSet.setType = dtRow[lstFields_ind["类型"]]
            pSet.setArea = dtRow[lstFields_ind["国家"]]
            pSet.isIndex = myData.iif(dtRow[lstFields_ind["是否指数"]] == True, True, False)
            pSet.isEnable = myData.iif(dtRow[lstFields_ind["有效性"]] == True, True, False)
            pSet.isEnable_RFasInt = myData.iif(dtRow[lstFields_ind["涨跌监测"]] == True, True, False)
            pSet.isEnable_Hourly = myData.iif(dtRow[lstFields_ind["整点播报"]] == True, True, False)
            
            pSet.mark = dtRow[lstFields_ind["备注"]] 
            pSet.msgUsers_wx = str(dtRow[lstFields_ind["消息发送用户_wx"]]).split('、')
            self._Index(pSet)               #索引设置信息

            #用户信息--未完善
            self.setUsers = ["Test"]     

    def _Save(self):            
        dtSetting = myIO_xlsx.DtTable()     #监听设置信息表
        dtSetting.dataName = "dataName"
        dtSetting.dataField = self.lstFields
        dtSetting.dataFieldType = ['string', 'string', 'string', 'string', 'bool', 'string', 'string']
       
        # 组装行数据
        keys = self.setList.keys()
        for x in keys:
            pSet = self.setList[x]
            pValues = []
            pValues.append(pSet.setTag)
            pValues.append(pSet.setName)
            pValues.append(pSet.setType)
            pValues.append(pSet.setArea)
            pValues.append(pSet.isEnable)
            pValues.append(myData_Trans.Tran_ToStr(pSet.msgUsers_wx))
            pValues.append(pSet.mark)
            dtSetting.dataMat.append(pValues)

        # 保存
        # dtSetting.Save(self.Dir_Setting, "Setting_Quote", 0, 0, True, "监听设置表", -1, -1, False)
        dtUser.Save_csv(self.Dir_Setting, "Setting_Quote", True, 0, 0)

    #查找 
    def _Find(self, setName, setTag = ''):
        pSet = None

        #按名称查找
        if(pSet == None):
            pSet = self.setList.get(setName, None)
        if(pSet == None and setTag != ''):
            pSet = self.usrList_Tag.get(setTag.lower()) 
        return pSet  
    #设置索引
    def _Index(self, pSet): 
        self.setList[pSet.setName] = pSet
                
        #用户集--(按标识索引)
        if(pSet.setTag != ""):
            self.setList_Tag[pSet.setTag.lower()] = pSet.setName 
    # 设置修改
    def Edit(self, setName, setTag = ''): 
        pSet = self._Find(setName, setTag)
        if(pSet != None):
            pass 
        return True
    
#初始全局消息管理器
from myGlobal import gol 
gol._Init()     #先必须在主模块初始化（只在Main模块需要一次即可）
gol._Set_Value('setsQuote', myQuote_Settings())

#查找 
def _Find(setName, setTag = ''):
    pSets = gol._Get_Value('setsQuote')
    if(pSets != None):
        pSet = pSets._Find(setName, setTag)
        if(pSet == None):
            pSet = myQuote_Setting(setTag, setName)
        return pSet
    return None


#主启动程序
if __name__ == "__main__":
    pSets = gol._Get_Value('setsQuote')

    pSet = _Find("建设银行")
    pSets._Save()
    print()
