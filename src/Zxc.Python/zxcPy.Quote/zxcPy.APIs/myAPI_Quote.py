# -*- coding: utf-8 -*-
"""
Created on  张斌 2018-11-26 15:58:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com

    Rest API --行情操作
"""
import os, copy, ast 
import mySystem 
    
#引用根目录类文件夹--必须，否则非本地目录起动时无法找到自定义类
mySystem.Append_Us("../zxcPy.APIs", False, __file__)
mySystem.Append_Us("../zxcPy.Quotation", False, __file__)
mySystem.Append_Us("../zxcPy.Quotation/Quote_Data", False, __file__)
mySystem.Append_Us("../zxcPy.Quotation/Quote_Source", False, __file__)
mySystem.Append_Us("../zxcPy.Quotation/Quote_Listener", False, __file__)
mySystem.Append_Us("", False)    
import myWeb, myDebug, myData_Trans, myQuote_Source, myQuote_Setting
from myGlobal import gol   



#API-行情设置
class myAPI_Quote_Set(myWeb.myAPI): 
    #strSet @股票 ** +/-
    def get(self, strName, bAdd = True, usrName_Nick = ''):
        strTag = "股票设置："+ strName +"\n      "
        pMsg = copy.deepcopy(gol._Get_Setting('Return_strFormat', {}))
        pMsg['text'] =  strTag + "操作失败！" 
        if(strName == ""): return pMsg

        #解析参数
        bResult = False 
        if(bResult == False):
            #提取行情对象
            pSource = gol._Get_Value('quoteSource', None) 
            pSets = gol._Get_Value('setsQuote', None) 
            if(pSource != None and pSets != None):
                pSet = myQuote_Setting._Find(strName, strName)
                bAdd = myData_Trans.To_Bool(bAdd)
                if(pSet != None):
                    usrName = usrName_Nick.replace("@*", "")
                    if(bAdd):
                        if(usrName_Nick != "" and (usrName_Nick in pSet.msgUsers_wx) == False):
                            pSet.msgUsers_wx.append(usrName_Nick)
                            pSet.isEnable = len(pSet.msgUsers_wx) > 0
                            pSets._Save()
                            pSource.params = pSource._getDefault_Param()
                            pMsg['text'] = strTag + " 已添加推送用户(" + usrName + ")" 
                            print(pSource.params)
                            bResult = True 
                        else:
                            pMsg['text'] =  strTag + " 已存在推送用户(" + usrName + ")" 
                    else:
                        if(usrName_Nick != "" and usrName_Nick in pSet.msgUsers_wx):
                            pSet.msgUsers_wx.remove(usrName_Nick)
                            pSet.isEnable = len(pSet.msgUsers_wx) > 0
                            pSets._Save()
                            pSource.params = pSource._getDefault_Param()
                            pMsg['text'] =  strTag + " 已移除推送用户(" + usrName + ")" 
                            print(pSource.params)
                            bResult = True 
                        else:
                            pMsg['text'] =  strTag + " 不存在用户(" + usrName + ")" 
        pMsg['result'] = bResult 
        return pMsg

    
#初始行情对象
def init_Quote():     
    #全局对象提取
    myQuote_Source.mainStart()
    ms_Source = gol._Get_Value('quoteSource', None) 
    return ms_Source
#集中添加所有API
def add_APIs(pWeb):  
    #初始行情对象
    init_Quote()
    
    # 创建Web API
    pWeb.add_API(myAPI_Quote_Set, '/zxcAPI/robot/quote/set/<strName>/<bAdd>/<usrName_Nick>')


#主程序启动
if __name__ == '__main__':  
    #初始行情对象
    init_Quote()

    #注册平台, 取token
    pQuote_Set = myAPI_Quote_Set()
    msg = pQuote_Set.get("建设银行", True, "wxTT")
    print("msg::", msg)
    print()
    