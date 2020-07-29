#-*- coding: utf-8 -*-
"""
Created on  张斌 2020-07-23 21:16:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com

    Weixin网页版消息处理接口（功能库）--机器人类--股票风控(风控设置)
"""
import sys, string, ast, os, time, datetime, random, mySystem
from urllib.parse import quote
from decimal import Decimal

#引用根目录类文件夹--必须，否则非本地目录起动时无法找到自定义类 
mySystem.Append_Us("../Prjs/Base", False, __file__)
mySystem.Append_Us("../../../zxcPy.Quote/zxcPy.Quotation", False, __file__)
mySystem.Append_Us("", False) 
import myDebug, myData, myData_Json, myData_Trans, myRobot, myWeb_urlLib
import myQuote
from myGlobal import gol   


#机器人类--股票偏好(群信息统计) 
class myRobot_StockRisk(myRobot.myRobot):
    def __init__(self, usrID = "", usrName = ""):
        super().__init__(usrID, usrName)
        self.doTitle = "Robot_StockRisk"         #说明 
        self.prjName = "股票风控"                #功能名
        self.doCmd = "@@zxcRobot_StockRisk"      #启动命令 
        self.isBackUse = True                    #后台运行
        self.maxTime = -1                        #永久有效 
                
    #消息处理接口
    def _Done(self, Text, msgID = "", msgType = "TEXT", usrInfo = {}):
        #按消息类型处理
        msgType = msgType.upper()
        strReturn = ""
        if(msgType == "TEXT") :
            strReturn = self._Done_Text(Text, msgID, usrInfo)
            pass
        return strReturn 
    
    #消息处理接口-Text
    def _Done_Text(self, Text, msgID = "", usrInfo = {}):
        #提取命令内容@￥*
        if(Text.count("@￥*") != 1): return ""
        cmds = Text.strip()[3:].split(" ")
        cmd = cmds[0].strip()
        nNum = len(cmds)
        myDebug.Print(Text.strip())
        
        #命令处理
        strReturn = ""
        if(cmd == "帮助"):
            return self._Title_Helper()  
        elif(cmd == "风控"):
            return self._Done_Text_set风控(cmd, cmds, usrInfo) 
        return strReturn
    #风控设置
    def _Done_Text_set风控(self, cmd, cmds = [], usrInfo = {}):
        if(cmd == "风控"):
            #解析参数   样例："@￥*风控 sh.10002626 50ETF沽8月3400 10股 1240元"   
            lstInd = ["风控"]
            stockPrice = 0
            stockNum = 0
            for x in cmds:
                strPrice = self.Matching_set(x, "元")
                if(strPrice != ""):
                    stockPrice = float(strPrice)
                    lstInd.append(x); continue;
                
                strNum = self.Matching_set(x, "股")
                if(strNum != ""):
                    stockNum = float(strNum)
                    lstInd.append(x); continue;
            for x in lstInd:
                cmds.remove(x)
                
            #提取股票信息
            pStocks = gol._Get_Value('setsStock', None)
            codeID = self.CheckName_set(cmds[0].strip())
            codeName = ""
            if(len(cmds) > 1): codeName = self.CheckName_set(cmds[1].strip())
            lstStock = pStocks._Find(codeID, codeName, "***")
            if(len(lstStock) != 1):
                lstStock = pStocks._Find(codeName, codeID, "***")
                if(len(lstStock) != 1):
                    return "股票代码、名称检索结果不唯一，无法操作！"

            pStock = lstStock[0]
            code_id = pStock.extype + '.' + pStock.code_id
            usrID = "@*" + usrInfo.get('groupName', '')
            if(usrID == "@*"): usrID = usrInfo.get('usrNameNick', '')
            
            #纠正风控账户名
            usrID_risk = usrID
            if(usrID_risk == '@*股票监测--自选行情'): 
                usrID_risk = '@*风控监测--股票'
            if(usrID_risk == '@*股票监测--期权行情'): 
                usrID_risk = '@*风控监测--期权'
            if(usrID_risk.count('股票监测') == 1): 
                usrID_risk = usrID_risk.replace('股票监测', '风控监测')
            stockDate = myData_Trans.Tran_ToDatetime_str(None, "%Y-%m-%d")

            #组装设置请求参数
            strUrl = "http://127.0.0.1:8669/zxcAPI/robot"                #实际网络地址在阿里云有问题，原因未明
            strPath = F'stock/QuoteSetRisk?usrID={usrID_risk}&code_id={code_id}&code_name={pStock.code_name}&dateTag={stockDate}&removeSet=False&stockPrice={stockPrice}&stockNum={stockNum}' #&setInfo=' + "{}"
            
            #修改接口执行
            pWeb = myWeb_urlLib.myWeb(strUrl, bPrint=False)
            strReturn = pWeb.Do_API_get(strPath, "zxcAPI-py")
            jsonRes = myData_Json.Trans_ToJson(strReturn)
            strReturn = myData.iif(jsonRes['result'], jsonRes['text'], jsonRes['err'])

            #设置账号风控有效
            if(jsonRes['result']):
                editInfo = {}
                editInfo["风控监测"] = {'msgUsers': {usrID : "wx，True"}, 'mark' :""}
                strPath = F'stock/QuoteSet?extype={pStock.extype}&code_id={pStock.code_id}&code_name={pStock.code_name}&editInfo={str(editInfo)}'  #+ form.code_name.data
            
                #修改接口执行
                strReturn2 = pWeb.Do_API_get(strPath, "zxcAPI-py")
                jsonRes = myData_Json.Trans_ToJson(strReturn2)
                strReturn = myData.iif(jsonRes['result'], strReturn, jsonRes['err'])
        myDebug.Debug(strReturn)
        return strReturn

    #匹配指定字符设置
    def Matching_set(self, Text, usrWord = "元"):
        length = len(Text)
        if(length < 2): return ""

        if(Text[length-1:] == usrWord):
            if(myData_Trans.Is_Numberic(Text[0:length-1])):
                return Text.replace(usrWord, "").strip()
        return "" 
    #修正期权名称
    def CheckName_set(self, stockName):
        #识别期权类型
        if(stockName.count('沽') == 1): 
            optType = '沽'
        elif(stockName.count('购') == 1): 
            optType = '购'

        #解析期权名称信息
        nameInfos = stockName.split(optType)
        if(nameInfos[0].count('50') == 1): 
            nameType = '50ETF'
        elif(nameInfos[0].count('300') == 1): 
            if(nameInfos[0].count('深') == 1): 
                nameType = '300ETF'
            else:
                nameType = '300ETF'
        else:
            nameType = '50ETF'

        #月份信息    
        if(nameInfos[1].count('月') == 1): 
            tmps = nameInfos[1].split('月')
            monthType = tmps[0].strip()
            priceType = tmps[1].strip()
        else:
            dtNow = datetime.datetime.now()
            dtLast = myData_Trans.Tran_ToDatetime_byWeekday(None, 4, 3)
            monthType = myData.iif(dtNow.day > dtLast.day, dtNow.month + 1, dtLast.month)
            if(monthType > 12): monthType = 1
            priceType = nameInfos[1].strip()
        
        #组装期权名称并返回
        optName = nameType + optType + str(monthType) + '月' + priceType
        return optName
    
    #创建返回消息
    def _Return(self, Text, usrInfo):
        self.msg = super()._Return(Text, usrInfo) 
        self.msg['msgTag'] = "Risk"
        return self.msg
    def _Title_User_Opened(self): 
        return "自动处理所有股票风控消息..."
    def _Title_Helper(self): 
        strReturn = "消息命令提示："
        strReturn += self.perfix + "@￥*帮助：输出所有命令说明"
        strReturn += "\n命令参数以空格区分，如：\"@￥*风控\""
        return strReturn
        

#主启动程序
if __name__ == "__main__": 
    #消息处理
    pRisk = myRobot_StockRisk()
    pRisk.Done("@@zxcRobot_StockRisk")
    
    #组装请求
    usrInfo = {}
    noteMsg = {}
    if(True):
        usrInfo["usrID"] = "zxcID"
        usrInfo["usrName"] = "zxcName"
        usrInfo["usrNameNick"] = "茶叶一主号"
        usrInfo['usrNameSelf'] = ""             #自己发自己标识 
        usrInfo["groupID"] = ""
        usrInfo["groupName"] = "" 

    #命令测试
    #myDebug.Debug(pRisk.Done("@￥*帮助")['msg'])
    #myDebug.Debug(pRisk.Done("@￥*风控 sh.10002626 50ETF沽8月3400 20股 1140元", usrNameNick = '茶叶一主号')['msg'])
    #pRisk.Done("@￥*风控  50沽8月3300 20股 1140元", usrNameNick = '茶叶一主号')
    pRisk.Done("@￥*风控 50沽3300 20股 1140元", usrNameNick = '茶叶一主号')
    print()

    #退出
    pRisk.Done("@@zxcRobot_StockRisk")
    print()
