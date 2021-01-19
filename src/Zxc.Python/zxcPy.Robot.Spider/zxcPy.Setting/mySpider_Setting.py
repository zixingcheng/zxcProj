#-*- coding: utf-8 -*-
"""
Created on  张斌 2021-01-04 11:58:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com

    Spider Setting 操作  
"""
import sys, os, datetime, uuid, mySystem 

#引用根目录类文件夹--必须，否则非本地目录起动时无法找到自定义类
mySystem.Append_Us("", False)    
import myIO, myIO_xlsx, myData, myData_Trans

#爬虫类型
spideTypes = {'webPage': "静态页面", 'quote': "股票行情"}


 
#爬虫--设置对象
class mySpider_Setting():
    def __init__(self, spiderTitle, spiderTag, spiderUrl, spiderRule): 
        self.spiderTitle = spiderTitle  #爬虫名称    
        self.spiderTag = spiderTag      #爬虫类型标识    
        self.spiderUrl = spiderUrl      #爬虫网址   
        self.spiderRule = spiderRule    #爬虫规则设置 
        self.isValid = False            #设置是否生效
        self.isDeled = False            #设置是否已删除
        self.mark = ''                  #备注说明
        self.InitRule()
    #是否有效
    def IsValid(self):  
        return self.isValid
    #由字符串初始
    def InitBystr(self, strSets): 
        if(len(strSets) > 6): 
            self.spiderTitle = strSets[0]
            self.spiderTag = strSets[1]
            self.spiderUrl = strSets[2]
            self.spiderRule = strSets[3].replace('，', ',')
            self.isValid = myData_Trans.To_Bool(strSets[4])      
            self.mark = strSets[5]
            self.InitRule()
        return True
    #初始规则信息
    def InitRule(self): 
        return True
    #配置信息组
    def ToList(self): 
        pValues = []
        pValues.append(self.spiderTitle)
        pValues.append(self.spiderTag)
        pValues.append(self.spiderUrl)
        pValues.append(self.spiderRule)
        pValues.append(self.isValid)
        pValues.append(self.mark)
        return pValues

#爬虫--设置对象集管理
class mySpider_Settings():
    def __init__(self): 
        self.setList = {}           #设置集(按名称索引)
        self.funChanges = {}

        #初始根目录信息
        strDir, strName = myIO.getPath_ByFile(__file__)
        self.Dir_Base = os.path.abspath(os.path.join(strDir, ".."))  
        self.Dir_Setting = self.Dir_Base + "/Data/Setting"
        self.Path_SetSpider = self.Dir_Setting + "/Setting_Spider.csv"
        self.lstFields = ["名称","类型标识","网址","规则信息","是否生效","备注"]   
        self._Init()
    #初始参数信息等   
    def _Init(self):            
        #提取字段信息  
        dtSetting = myIO_xlsx.DtTable() 
        dtSetting.dataFieldType = ["","","","","","bool",""]
        dtSetting.Load_csv(self.Path_SetSpider, 1, 0, isUtf = True) 
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
        if(len(strSets) < 6): return False

        #初始设置集
        temps = strSets[0].split('.')
        pSet = self._Find(temps[0])
        if(pSet == None):
            pSet = mySpider_Setting(temps[0], "", "", "")
            self._Index(pSet)

        #按类型初始
        if(pSet):
            pSet.InitBystr(temps) 
            return True
        return False
    
    #保存
    def _Save(self):            
        dtSetting = myIO_xlsx.DtTable()     #监听设置信息表
        dtSetting.dataName = "dataName"
        dtSetting.dataField = self.lstFields
        
        # 组装行数据
        for key in self.setList:
            pSet = self.setList[key]
            if(pSet.isDeled): continue
            pValues = pSet.ToList()
            dtSetting.dataMat.append(pValues)

        # 保存
        dtSetting.Save_csv(self.Dir_Setting, "Setting_Spider", True, 0, 0)

    #查找 
    def _Find(self, setName):
        if(setName != ""):
            return self.setList.get(setName.lower()) 
        return None  
    #设置索引
    def _Index(self, pSet): 
        if(pSet.spiderTitle == ""): return
        if(self._Find(pSet.spiderTitle) != None): return

        self.setList[pSet.spiderTitle.lower()] = pSet
        return True
    
    # 设置移除
    def _Remove(self, setName):
        if(self._Find(setName.lower())):
            self.setList.pop(setName.lower())
            self._Save()
            print("已移除设置项(" + setName + ")")
            return True
        return False

    # 设置修改
    def _Edit(self, dictSet):
        bResult = False
        name = dictSet.get("spiderTitle", "")
        if(name == ""): return False

        #初始设置集
        pSet = self._Find(name)
        if(pSet == None):
            pSet = mySpider_Setting(name, dictSet.get("spiderTag", ""), dictSet.get("spiderUrl", ""), dictSet.get("spiderRule", ""))
            bResult = self._Index(pSet)
        else:
            pSet.spiderTag = dictSet.get("spiderTag", pSet.spiderTag)
            pSet.spiderUrl = dictSet.get("spiderUrl", pSet.spiderUrl)
            pSet.spiderRule = dictSet.get("spiderRule", pSet.spiderRule)
            bResult = pSet.InitRule();
        pSet.isValid = myData_Trans.To_Bool(dictSet.get("isValid", str(pSet.isValid)))      
        pSet.mark = dictSet.get("mark", pSet.mark)

        if(bResult): 
            self.change_reply(pSet.spiderTag, name)
            self._Save()
        return bResult        
    # 消息装饰函数，用于传递外部重写方法，便于后续调用      
    def change_register(self, type):
        def _fun_register(fn): 
            # 按消息类型记录
            self.funChanges[type] = fn
            return fn
        return _fun_register
    # 回调装饰函数，封装触发消息，并回调
    def change_reply(self, type, name):
        # 提取消息类型对应的装饰函数
        funChange = self.funChanges.get(type, None)
        if(funChange != None):
            r = funChange(name) 


#初始全局消息管理器
from myGlobal import gol 
gol._Init()     #先必须在主模块初始化（只在Main模块需要一次即可）
gol._Set_Value('setsSpider', mySpider_Settings())

#查找 
def _Find(setName, bCreatAuto = False):
    pSets = gol._Get_Value('setsSpider')
    if(pSets != None):
        pSet = pSets._Find(setName)
        if(pSet == None and bCreatAuto):
            pSet = mySpider_Setting(setName, "", "", "")
        return pSet
    return None



#主启动程序
if __name__ == "__main__":
    pSets = gol._Get_Value('setsSpider')
    
    # 装饰函数，处理监测到的上升、下降、拐点
    @pSets.change_register("webPage")
    def Reply_Change(name): 
        #查找
        pSet = pSets._Find(name)
        if(pSet != None):
            print(pSet.ToList())


    #新增测试
    editInfo = {'spiderTitle': "ceshi", 'spiderTag': 'webPage', 'spiderUrl': "", "spiderRule": "", 'isValid':'True', 'mark':'测试设置' }
    pSets._Edit(editInfo)

    #修改测试
    editInfo = {'spiderTitle': "ceshi",  'isValid':'False', 'mark':'测试设置2' }
    pSets._Edit(editInfo)
    
    #移除测试
    pSets._Remove("ceshi")
     
