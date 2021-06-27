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


# M H D m d command
# M: 分（0-59） H：时（0-23） D：天（1-31） m: 月（1-12） d: 周（0-6） 0为星期日(或用Sun或Mon简写来表示) 
# 每周一，三，五的下午3：00系统进入维护状态，重新启动系统。
# 00 15 * * 1,3,5
class myTimeSets():
    class myTimeSet():
        def __init__(self, strSet, typeTime): 
            self.setTimes = []
            self.maxTime = 0
            self.minTime = 0
            self.allVlid = False
            self.InitBystr(strSet.replace(';', ','), typeTime)
        def InitBystr(self, strSet, typeTime): 
            self.values = []
            self.typeTime = typeTime
            if(strSet == "*"): 
                self.allVlid = True
                return 

            #多个配置
            if(strSet.count(",") > 0): 
                values = strSet.split(',')
                for x in values:
                    pSet = myTimeSets.myTimeSet(x, typeTime)
                    self.setTimes.append(pSet)
                    #self.values.append(myData_Trans.To_Int(x))
                return

            #区间配置
            if(strSet.count("-") > 0): 
                temps = strSet.split('-')
                self.minTime = myData_Trans.To_Float(temps[0])
                self.maxTime = myData_Trans.To_Float(temps[1])
                #self.values = range(myData_Trans.To_Int(temps[0]), myData_Trans.To_Int(temps[1]))
                return
            else:
                if(strSet.count(".") > 0): 
                    self.values.append(myData_Trans.To_Float(strSet))
                else:
                    self.values.append(myData_Trans.To_Int(strSet))
        #是否有效
        def IsValid(self, value):  
            if(self.allVlid): return True
            if(self.maxTime > 0 and self.minTime > 0):
                return self.minTime <= value and self.maxTime > value
            if(len(self.setTimes) > 0): 
                for x in self.setTimes:
                    if(x.IsValid(value)):
                        return True
            return value in self.values
    def __init__(self, tagSet, timeSets): 
        self.tagName = tagSet
        self.InitBystr(timeSets)
    def InitBystr(self, strSets): 
        temps = strSets.split(' ')
        if(len(temps) > 4): 
            self.M = myTimeSets.myTimeSet(temps[0], "M")
            self.H = myTimeSets.myTimeSet(temps[1], "H")
            self.D = myTimeSets.myTimeSet(temps[2], "D")
            self.m = myTimeSets.myTimeSet(temps[3], "m")
            self.d = myTimeSets.myTimeSet(temps[4], "d")
    #是否有效
    def IsValid(self, dtTime = None):  
        if(dtTime == None):
            dtTime = datetime.datetime.now()
        weekday = myData_Trans.To_Int(dtTime.strftime("%w"))
        return self.M.IsValid(dtTime.minute) and (self.H.IsValid(dtTime.hour) or self.H.IsValid(dtTime.hour + dtTime.minute/60)) and self.D.IsValid(dtTime.day) and self.m.IsValid(dtTime.month) and self.d.IsValid(weekday)

#爬虫--设置对象
class mySpider_Setting():
    def __init__(self, spiderName, spiderTag, spiderUrl, spiderRule, timeSet = "* * * * *"): 
        self.spiderName = spiderName    #爬虫名称    
        self.spiderTag = spiderTag      #爬虫类型标识    
        self.spiderUrl = spiderUrl      #爬虫网址   
        self.spiderRule = spiderRule    #爬虫规则设置 
        self.isValid = False            #设置是否生效
        self.isDeled = False            #设置是否已删除
        self.timeSet = timeSet          #时间规则
        self.timeRule = None
        self.mark = ''                  #备注说明
        self.dateEnd = 0                #结束日期
        
        self.validTime = False          #设置是否生效
        self.InitRule()
    #是否有效
    def IsValid(self):  
        return self.isValid and not self.isDeled and self.timeRule.IsValid()
    #由字符串初始
    def InitBystr(self, strSets): 
        if(len(strSets) > 5): 
            self.spiderName = strSets[0]
            self.spiderTag = strSets[1]
            self.spiderUrl = strSets[2]
            self.spiderRule = strSets[3].replace(';', ',')
            self.isValid = myData_Trans.To_Bool(strSets[4]) 
            self.timeSet = strSets[5].replace(';', ',')          #时间规则
            self.mark = strSets[6]
            self.InitRule()
        return True
    #初始规则信息
    def InitRule(self): 
        if(self.timeSet == ""): 
            self.timeSet = "* * * * *"
        self.timeRule = myTimeSets(self.spiderName, self.timeSet)    
        return True
    #转换信息组
    def ToList(self): 
        pValues = []
        pValues.append(self.spiderName)
        pValues.append(self.spiderTag)
        pValues.append(self.spiderUrl)
        pValues.append(self.spiderRule.replace(',', ';'))
        pValues.append(self.isValid)
        pValues.append(self.timeSet.replace(',', ';'))
        pValues.append(self.mark)
        return pValues
    #转换信息字典
    def ToDict(self): 
        pValues = {}
        pValues['spiderName'] = self.spiderName
        pValues['spiderTag'] = self.spiderTag
        pValues['spiderUrl'] = self.spiderUrl
        pValues['spiderRule'] = self.spiderRule
        pValues['isValid'] = self.isValid
        pValues['timeSet'] = self.timeSet
        pValues['mark'] = self.mark
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
        self.lstFields = ["名称","类型标识","网址","规则信息","是否生效","时间设置","备注"]   
        self._Init()
    #初始参数信息等   
    def _Init(self):            
        #提取字段信息  
        dtSetting = myIO_xlsx.DtTable() 
        dtSetting.dataFieldType = ["","","","","bool","",""]
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
            pSet.InitBystr(strSets) 
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
    #查找 
    def _Find_ByTypes(self, type):
        lstSet = []
        for x in self.setList:
            pSet = self.setList[x]
            if(pSet.spiderTag == ""): pSet.spiderTag = "webPage"
            if(type != ""):
                if(type != pSet.spiderTag):
                    continue
            lstSet.append(pSet)
        return lstSet  
    #设置索引
    def _Index(self, pSet): 
        if(pSet.spiderName == ""): return
        if(self._Find(pSet.spiderName) != None): return

        self.setList[pSet.spiderName.lower()] = pSet
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
        name = dictSet.get("spiderName", "")
        if(name == ""): return False

        #初始设置集
        pSet = self._Find(name)
        if(pSet == None):
            pSet = mySpider_Setting(name, dictSet.get("spiderTag", ""), dictSet.get("spiderUrl", ""), dictSet.get("spiderRule", ""), dictSet.get("timeSet", ""))
            bResult = self._Index(pSet)
        else:
            pSet.spiderTag = dictSet.get("spiderTag", pSet.spiderTag)
            pSet.spiderUrl = dictSet.get("spiderUrl", pSet.spiderUrl)
            pSet.spiderRule = dictSet.get("spiderRule", pSet.spiderRule)
            pSet.timeSet = dictSet.get("timeSet", pSet.timeSet)
            bResult = pSet.InitRule();
            bResult = True
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
    timeRule = myTimeSets("", "* 9.5-11.5;13-15 * * 1,3,5")
    print(timeRule.IsValid());

    pSets = gol._Get_Value('setsSpider')
    
    # 装饰函数，处理监测到的上升、下降、拐点
    @pSets.change_register("webPage")
    def Reply_Change(name): 
        #查找
        pSet = pSets._Find(name)
        if(pSet != None):
            print(pSet.ToList())


    #新增测试
    editInfo = {'spiderName': "ceshi", 'spiderTag': 'webPage', 'spiderUrl': "", "spiderRule": "", 'isValid':'True', 'mark':'测试设置' }
    pSets._Edit(editInfo)

    #修改测试
    editInfo = {'spiderName': "ceshi",  'isValid':'False', 'mark':'测试设置2' }
    pSets._Edit(editInfo)
    
    #移除测试
    pSets._Remove("ceshi")
     
