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
        self.msg['FromUserName'] = self.usrName 

        self.manageBills = gol._Get_Setting('manageBills', None)    #使用全局账单管理器
        self.billTypes = myManager_Bill.myBillType                  #账单类型集
        self.bills = myManager_Bill.myObj_Bills("")                  #账单对象-当前
        self.billUsr = ""               #账单归属人-当前
        self.billSrcUsr = ""            #账单来源人-当前
        self.billType = ""              #账单归属人-当前

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
            strReturn += "账单人：" + myData.iif(self.billUsr == "", "未设置", self.billUsr) + "，"
            strReturn += "账单类型：" + myData.iif(self.billType == "", "未设置", self.billType) + "，"
            strReturn += "账单来源：" + myData.iif(self.billSrcUsr == "", "未设置", self.billSrcUsr) + "。"
            return "当前设置：" + strReturn
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
        elif(cmd == "来源"): 
            if(len(cmds) > 1):
                self.billSrcUsr = cmds[1]
                return "已切换到账单来源人(" + cmds[1] + ")。"
            return "参数有误，请使用\"@帮助\"查询命令。"
        elif(cmd == "新增"): 
            nLen = len(cmds)
            if(nLen > 2): 
                usrSrc = myData.iif(cmds[1] == "", self.billSrcUsr, cmds[1])
                typeBill = self._Get_Param(cmds, nLen, 3, self.billSrcUsr)
                if(typeBill in self.billTypes == False):
                    return "账单类型(" + typeBill + ")不存在，请使用\"@账单类型\"查询可用类型。"
                dateTime = self._Get_Param(cmds, nLen, 4, "")
                remark = self._Get_Param(cmds, nLen, 5, "")
                return self.bills.Add(usrSrc, float(cmds[2]), typeBill, dateTime, remark)
        elif(cmd == "统计"):  
            if(len(cmds) > 1  ): 
                usrSrc, typeBill, startTime, endTime, nMonth = self._Get_QueryParam(cmds) 
                return self.bills.Static(usrSrc, typeBill, startTime, endTime, nMonth)
        elif(cmd == "统计单次"):  
            cmds = Text[1:].split(" ")
            if(len(cmds) > 1  ): 
                usrSrc, typeBill, startTime, endTime, nMonth = self._Get_QueryParam(cmds) 
                return self.bills.Static_max(usrSrc, typeBill, False, 10, startTime, endTime, nMonth)
        elif(cmd == "统计累计"):  
            cmds = Text[1:].split(" ")
            if(len(cmds) > 1  ): 
                usrSrc, typeBill, startTime, endTime, nMonth = self._Get_QueryParam(cmds) 
                return self.bills.Static_max("", typeBill, True, 10, startTime, endTime, nMonth)
        return strReturn
        
    #解析通用查询、统计参数
    def _Get_QueryParam(self, cmds): 
        nLen = len(cmds)
        if(nLen > 1): 
            usrSrc = self._Get_Param(cmds, nLen, 2, self.billSrcUsr)
            typeBill = self._Get_Param(cmds, nLen, 3, self.billType)
            startTime = self._Get_Param(cmds, nLen, 4, "")
            endTime = self._Get_Param(cmds, nLen, 5, "") 
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
        return usrSrc, typeBill, startTime, endTime, nMonth
    def _Get_Param(self, cmds, nLen, ind ,value):
        if(nLen <= ind): return value
        return cmds[ind]

    def _Title_User_Opened(self): 
        return "输入命令进行账单管家操作... 帮助命令：\"@帮助\"."
    def _Title_Helper(self): 
        strReturn = "账单管家命令提示："
        strReturn += self.perfix + "@帮助：输出所有命令及参数示例"
        strReturn += self.perfix + "@当前设置：输出当前设置信息"
        strReturn += self.perfix + "@账单人：参数(\"账单所属人\")"
        strReturn += self.perfix + "@账单类型：提取可用账单细分类型"
        strReturn += self.perfix + "@类型：切换到固定账单分类"
        strReturn += self.perfix + "@来源：切换到固定账单来源"
        strReturn += self.perfix + "@新增：参数(\"来源 金额 类型 时间 备注\")"
        strReturn += self.perfix + "@统计：参数(\"n年/月  来源 类型\")"
        strReturn += self.perfix + "@统计单次：参数(\"n年/月 来源 类型\")"
        strReturn += self.perfix + "@统计累计：参数(\"n年/月 来源 类型\")"
        strReturn += "\n以上命令，参数间以空格区分，示例：\"@统计 3年\""
        return strReturn


#主启动程序
if __name__ == "__main__":
    pR = myRobot_Bill("zxcID", "zxcName");
    pR.Done("@@BillManager")
    myDebug.Debug(pR.Done("@帮助")['msg'])
    myDebug.Debug(pR.Done("@账单类型")['msg'])
    myDebug.Debug(pR.Done("@当前设置")['msg'])
    myDebug.Debug(pR.Done("@账单人 Test")['msg'])
    myDebug.Debug(pR.Done("@类型 红包")['msg'])
    myDebug.Debug(pR.Done("@来源 老豆")['msg'])
    myDebug.Debug(pR.Done("@当前设置")['msg'])
    
    #添加、查询
    myDebug.Debug(pR.Done("@新增 老豆 100 红包 2018-8-1 测试")['msg'])
    myDebug.Debug(pR.Done("@统计 1月")['msg'])
    myDebug.Debug(pR.Done("@统计 1年")['msg'])
    myDebug.Debug(pR.Done("@统计 1年   2018-8-1 2018-8-16")['msg'])
    print()
    
    myDebug.Debug(pR.Done("@统计单次 1年")['msg'])
    myDebug.Debug(pR.Done("@统计单次 1年  ")['msg'])
    myDebug.Debug(pR.Done("@统计累计 1年")['msg'])
    myDebug.Debug(pR.Done("@统计累计 1年  ")['msg'])


    pR.Done("@@BillManager")

    exit()
     