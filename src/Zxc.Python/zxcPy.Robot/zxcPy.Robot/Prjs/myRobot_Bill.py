#-*- coding: utf-8 -*-
"""
Created on  张斌 2018-07-04 15:58:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com
    
    机器人（功能库）  --账单(记录、查询)
"""
import sys, os, time , datetime, mySystem

#引用根目录类文件夹--必须，否则非本地目录起动时无法找到自定义类
mySystem.Append_Us("../Roots", False, __file__)
mySystem.Append_Us("../Prjs/Base", False, __file__)
mySystem.Append_Us("", False) 
import myIO, myIO_xlsx, myData, myData_Trans, myDebug, myManager_Bill, myRobot
from myGlobal import gol 


#机器人类----红包(记录、查询)
class myRobot_Bill(myRobot.myRobot):
    def __init__(self, usrID = "", usrName = ""):
        super().__init__(usrID, usrName)
        self.doTitle = "账单管家"       #说明 
        self.prjName = "账单管家"       #功能名
        self.doCmd = "@@BillManager"    #启动命令 
        self.isSingleUse = False        #是否为单例使用(非单例时每个用户专属) 
        self.msg['FromUserName'] = self.usrName 

        self.manageBills = gol._Get_Setting('manageBills', None)    #使用全局账单管理器
        self.billTypes = myManager_Bill.myBileType                  #账单类型集
        self.billTradeTypes = myManager_Bill.myTradeType            #交易品类型集
        self.bills = myManager_Bill.myObj_Bills("")                 #账单对象-当前
        self.billUsr = ""               #账单归属人-当前
        self.billType = ""              #账单类型-当前
        self.billTradeParty = ""        #账单交易人-当前
        self.billTradeTarget = ""       #账单交易物-当前
        self.billTradeType = ""         #账单交易物品类-当前
        self.billTradeTargetType = ""   #账单交易物品子类-当前

    #消息处理接口
    def _Done(self, Text, msgID = "", msgType = "TEXT", usrInfo = {}):
        #提取命令内容
        if(Text.count("@") != 1): return ""
        cmds = Text.strip()[1:].split(" ")
        cmd = cmds[0]
        myDebug.Print(Text.strip())
        
        #账单命令处理
        strReturn = ""
        if(cmd == "帮助"):
            return self._Title_Helper()
        elif(cmd == "当前设置"):
            strReturn += "账单归属：" + myData.iif(self.billUsr == "", "未设置", self.billUsr) + "，"
            strReturn += "账单类型：" + myData.iif(self.billType == "", "未设置", self.billType) + "，"
            strReturn += "交易人：" + myData.iif(self.billTradeParty == "", "未设置", self.billTradeParty) + "，"
            strReturn += "交易物：" + myData.iif(self.billTradeTarget == "", "未设置", self.billTradeTarget) + "，"
            strReturn += "交易品类：" + myData.iif(self.billTradeType == "", "未设置", self.billTradeType) + "，"
            strReturn += "交易品子类：" + myData.iif(self.billTradeTargetType == "", "未设置", self.billTradeTargetType) + "。"
            return "账单默认设置：" + strReturn
        elif(cmd == "账单人"):
            if(len(cmds) > 1): 
                self.bills = self.manageBills._Find(cmds[1])
                if(self.bills == None): return "账单人(" + cmds[1] + ")不存在！，但你仍可以指定该名称进行添加。"
                self.billUsr = cmds[1]
                return "已切换到账单人(" + cmds[1] + ")。"
        elif(cmd == "账单类型"):
            for x in range(0, len(self.billTypes)):
                strReturn += "，" + self.billTypes[x]
            return "账单类型：" + strReturn[1:]
        elif(cmd == "类型"): 
            if(len(cmds) > 1 and cmds[1] in self.billTypes):
                self.billType = cmds[1]
                return "已切换到账单类型(" + cmds[1] + ")。"
            return "账单类型(" + cmds[1] + ")不存在，请使用\"@账单类型\"查询可用类型。"
        elif(cmd == "交易品类"):
            for x in range(0, len(self.billTradeTypes)):
                strReturn += "，" + self.billTradeTypes[x]
            return "交易品类：" + strReturn[1:]
        elif(cmd == "品类"): 
            if(len(cmds) > 1 and cmds[1] in self.billTradeTypes):
                self.billTradeType = cmds[1]
                return "已切换到交易品类(" + cmds[1] + ")。"
            return "交易品类(" + cmds[1] + ")不存在，请使用\"@交易品类\"查询可用品类。"
        elif(cmd == "交易品"): 
            if(len(cmds) > 1):
                self.billTradeTarget = cmds[1]
                return "已切换到账单交易品(" + cmds[1] + ")。"
            return "参数有误，请使用\"@帮助\"查询命令。"
        elif(cmd == "交易人"): 
            if(len(cmds) > 1):
                self.billTradeParty = cmds[1]
                return "已切换到账单交易人(" + cmds[1] + ")。"
            return "参数有误，请使用\"@帮助\"查询命令。"
        elif(cmd == "新增"): 
            nLen = len(cmds)
            if(nLen > 2): 
                tradeParty = myData.iif(cmds[1] == "", self.billTradeParty, cmds[1])
                tradeTarget = self._Get_Param(cmds, nLen, 5, self.billTradeParty)
                typeBill = self._Get_Param(cmds, nLen, 8, self.billType)
                tradeType = self._Get_Param(cmds, nLen, 9, self.billTradeType)
                tradeTargetType = self._Get_Param(cmds, nLen, 10, self.billTradeTargetType)
                tradePrice = self._Get_Param(cmds, nLen, 3, 0)
                tradeNum = self._Get_Param(cmds, nLen, 4, 1)
                
                if(typeBill in self.billTypes == False):
                    return "账单类型(" + typeBill + ")不存在，请使用\"@账单类型\"查询可用类型。"
                dateTime = self._Get_Param(cmds, nLen, 6, "")
                remark = self._Get_Param(cmds, nLen, 7, "")
                return self.bills.Add(tradeParty, float(cmds[2]), tradeTarget, typeBill, tradeType, tradeTargetType, dateTime, remark, float(tradePrice), float(tradeNum))
        elif(cmd == "统计"):  
            cmds = Text[1:].split(" ")
            if(len(cmds) > 1  ): 
                tradeParty, typeBill, tradeTarget, tradeType, tradeTargetType, startTime, endTime, nMonth = self._Get_QueryParam(cmds) 
                return self.bills.Static(startTime, endTime, nMonth, tradeParty, typeBill, tradeTarget, tradeType, tradeTargetType)
        elif(cmd == "统计单次"):  
            cmds = Text[1:].split(" ")
            if(len(cmds) > 1  ): 
                tradeParty, typeBill, tradeTarget, tradeType, tradeTargetType, startTime, endTime, nMonth = self._Get_QueryParam(cmds)  
                return self.bills.Static_max(startTime, endTime, nMonth, tradeParty, typeBill, tradeTarget, tradeType, tradeTargetType, False, 10)
        elif(cmd == "统计累计"):  
            cmds = Text[1:].split(" ") 
            if(len(cmds) > 1  ): 
                tradeParty, typeBill, tradeTarget, tradeType, tradeTargetType, startTime, endTime, nMonth = self._Get_QueryParam(cmds) 
                return self.bills.Static_max(startTime, endTime, nMonth, tradeParty, typeBill, tradeTarget, tradeType, tradeTargetType, True, 10)
        elif(cmd == "查询"):  
            cmds = Text[1:].split(" ") 
            if(len(cmds) > 1  ): 
                tradeParty, typeBill, tradeTarget, tradeType, tradeTargetType, startTime, endTime, nMonth = self._Get_QueryParam(cmds) 
                return self.bills.Static_max(startTime, endTime, nMonth, tradeParty, typeBill, tradeTarget, tradeType, tradeTargetType, True, 30, False)
        return strReturn
        
    #解析通用查询、统计参数
    def _Get_QueryParam(self, cmds): 
        nLen = len(cmds)
        if(nLen > 1): 
            tradeParty = self._Get_Param(cmds, nLen, 2, self.billTradeParty)
            tradeTarget = self._Get_Param(cmds, nLen, 3, self.billTradeTarget)
            typeBill = self._Get_Param(cmds, nLen, 4, self.billType)
            tradeType = self._Get_Param(cmds, nLen, 5, self.billTradeType)
            tradeTargetType = self._Get_Param(cmds, nLen, 6, self.billTradeTargetType)

            startTime = self._Get_Param(cmds, nLen, 7, "")
            endTime = self._Get_Param(cmds, nLen, 8, "") 
            if(startTime != ""): startTime = myData_Trans.Tran_ToDatetime(startTime, "%Y-%m-%d") 
            if(endTime != ""): endTime = myData_Trans.Tran_ToDatetime(endTime, "%Y-%m-%d") 
            
            #时间修正, 区分年月
            nMonth = 0
            nYear = 0
            if(cmds[1].count("年") == 1):
                if(type(startTime) != datetime.datetime):
                    nYear = int(cmds[1].replace("年", "").strip())
                    startTime = self.bills._Trans_Time_year("", nYear)
            else:
                nMonth = int(cmds[1].replace("月", "").strip())
        return tradeParty, typeBill, tradeTarget, tradeType, tradeTargetType, startTime, endTime, nMonth
    def _Get_Param(self, cmds, nLen, ind,  value):
        if(nLen <= ind): return value
        strCmd = cmds[ind]
        if(strCmd == "*"): return value
        if(strCmd == "-"): return ""
        return strCmd

    def _Title_User_Opened(self): 
        return "输入命令进行账单管家操作... 帮助命令：\"@帮助\"."
    def _Title_Helper(self): 
        strReturn = "账单管家命令提示："
        strReturn += self.perfix + "@帮助：输出所有命令说明"
        strReturn += self.perfix + "@当前设置：输出当前设置信息"
        strReturn += self.perfix + "@账单人：参数(\"账单所属人\")"
        strReturn += self.perfix + "@账单类型：提取可用账单类型"
        strReturn += self.perfix + "@类型：切换到固定账单类型"
        strReturn += self.perfix + "@交易品类：提取可用交易品类"
        strReturn += self.perfix + "@品类：切换到固定交易品类"
        strReturn += self.perfix + "@交易人：切换到固定账单交易人"
        strReturn += self.perfix + "@新增：参数(\"交易人 金额 品名 单价 价格 时间 备注 类型 品类 品子类\")"
        strReturn += self.perfix + "@统计：参数(\"n年/月\")"
        strReturn += self.perfix + "@统计单次：参数(\"n年/月\")"
        strReturn += self.perfix + "@统计累计：参数(\"n年/月\")"
        strReturn += self.perfix + "@查询：参数(\"n年/月 交易人 品名 品类 品子类 起始时间 截止时间\")，查询统计通用完整格式，最少一个参数。"
        strReturn += "\n以上命令，参数间以空格区分，示例命令：\"@统计 3年\""
        return strReturn


#主启动程序
if __name__ == "__main__":
    pR = myRobot_Bill("zxcID", "zxcName");
    pR.Done("@@BillManager")
    myDebug.Debug(pR.Done("@帮助")['msg'])
    myDebug.Debug(pR.Done("@账单类型")['msg'])
    myDebug.Debug(pR.Done("@交易品类")['msg'])
    myDebug.Debug(pR.Done("@当前设置")['msg'])
    myDebug.Debug(pR.Done("@账单人 Test")['msg'])
    myDebug.Debug(pR.Done("@类型 受赠")['msg'])
    myDebug.Debug(pR.Done("@品类 人际")['msg'])
    myDebug.Debug(pR.Done("@交易人 老豆")['msg'])
    myDebug.Debug(pR.Done("@交易品 红包")['msg'])
    myDebug.Debug(pR.Done("@当前设置")['msg'])
    
    #添加、查询
    myDebug.Debug(pR.Done("@新增 老豆 100 0 1 红包 2018-8-1 测试")['msg'])
    myDebug.Debug(pR.Done("@统计 1月")['msg'])
    myDebug.Debug(pR.Done("@统计 1年")['msg'])
    myDebug.Debug(pR.Done("@统计 1年   2018-8-1 2018-8-16")['msg'])
    print()
    
    myDebug.Debug(pR.Done("@统计单次 1年")['msg'])
    myDebug.Debug(pR.Done("@统计单次 1年  ")['msg'])
    myDebug.Debug(pR.Done("@统计累计 1年")['msg'])
    myDebug.Debug(pR.Done("@统计累计 1年  ")['msg'])

    
    #切换统计对象 
    myDebug.Debug(pR.Done("@账单人 多多")['msg'])
    myDebug.Debug(pR.Done("@交易人 爸爸")['msg'])
    myDebug.Debug(pR.Done("@统计单次 3年 *")['msg'])
    myDebug.Debug(pR.Done("@统计单次 3年 - -")['msg'])
    myDebug.Debug(pR.Done("@统计累计 3年 -")['msg'])
    myDebug.Debug(pR.Done("@统计累计 3年 - 红包 受赠 人际  -")['msg'])
    myDebug.Debug(pR.Done("@统计 3年 - - - -")['msg'])


    pR.Done("@@账单管家")

    exit()
     