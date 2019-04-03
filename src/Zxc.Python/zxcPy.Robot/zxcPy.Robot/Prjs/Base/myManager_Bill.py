#-*- coding: utf-8 -*-
"""
Created on  张斌 2018-08-24 15:58:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com
    
    管家功能--账单(记录、查询)
"""
import sys, os, time, copy, datetime, mySystem
from operator import itemgetter, attrgetter

#引用根目录类文件夹--必须，否则非本地目录起动时无法找到自定义类
mySystem.Append_Us("../Prjs", False, __file__)
mySystem.Append_Us("", False) 
import myEnum, myIO, myIO_xlsx, myData, myData_Trans, myDebug 


#定义账单类型枚举
myBileType = myEnum.enum('买入', '卖出', '受赠', '赠予', '分红', '转账')
#myTradeType = myEnum.enum('购物', '买菜', '买衣服', '投资', '红包', '投资回笼')
myTradeType = myEnum.enum('投资', '居家', '日用品', '衣服', '餐饮', '交通', '烟酒', '零食', '通讯', '娱乐', '旅游', '人际', '水费', '电费', '燃气', '取暖', '房租', '医疗', '教育', '健身', '美容', '装修')
myTradeType_居家_蔬菜 = ['蔬菜', '菜']
myTradeType_居家_肉类 = ['肉', '猪肉', '鸡肉', '牛肉', '羊肉', "鸡蛋"]
myTradeType_居家_海鲜 = ["螃蟹", "小龙虾", "虾", "花蛤", "竹蛏"]
myTradeType_居家_调料 = ['油', '盐', '调料']
myTradeType_居家_主食 = ['米', '面粉', '面条']
myTradeType_居家 = [] + myTradeType_居家_蔬菜 + myTradeType_居家_肉类 + myTradeType_居家_海鲜 + myTradeType_居家_调料 + myTradeType_居家_主食
myTradeType_投资 = ['活期', '定期', '股票', '基金', '可转债', '国债逆回购', '理财', '转入', '转出']
myTradeType_双向 = ['投资']


#账单对象
class myObj_Bill():
    def __init__(self): 
        self.usrID = ""             #用户名
        self.usrBillType = ""       #账单类型
        self.recordTime = None      #记录时间
        self.recorder = None        #记录人

        self.tradeID = 0            #编号
        self.tradeID_Relation = ""  #关联交易编号
        self.tradeParty = ""        #交易方（当事交易人或单位）
        self.tradeType = ""         #交易分类
        self.tradeTypeTarget = ""   #交易内容分类(细分小类)
        self.tradeTarget = ""       #交易内容
        self.tradePrice = 0         #交易单价
        self.tradeNum = 1           #交易数量
        self.tradeNum_Stock = 0     #交易数量(当前库存，买入有效)
        self.tradeMoney = 0         #交易金额
        self.tradePoundage = 0      #交易手续费
        self.tradeProfit = 0        #交易收益
        self.tradeTime = None       #交易时间
        
        self.isDel = False          #是否已删除
        self.remark = ""            #备注
        self.billInfo = None        #属性信息字典 
    def Init(self, recorder, usrID, tradeParty, tradeMoney, tradeTarget, usrBillType = "", tradeType = "", tradeTypeTarget = "", dateTime = "", remark = "", tradePrice = 0, tradeNum = 0, tradeID_Relation = "", tradeProfit = 0):
        self.usrID = usrID 
        self.usrBillType = usrBillType
        self.tradeID_Relation = str(tradeID_Relation)
        self.tradeParty = tradeParty 
        self.tradeNum = tradeNum 
        self.tradePrice = tradePrice 
        self.tradeMoney = tradeMoney 
        self.tradeProfit = tradeMoney 
        self.tradeTarget = tradeTarget 
        self.tradeType = tradeType 
        self.tradeTypeTarget = tradeTypeTarget 
        self.tradeTime = dateTime
        self.remark = remark
        self.recorder = myData.iif(recorder == "", "zxcRobot", recorder)
        
        self.billInfo = self.OnCreat_BillInfo()
        self.Init_ByDict(self.billInfo) 
    def Init_ByDict(self, tradeInfo = {}): 
        self.usrID = tradeInfo.get("usrID", "")
        usrBillType = tradeInfo.get("usrBillType", "")
        self.recordTime = tradeInfo.get("recordTime", datetime.datetime.now())
        if(self.recordTime == None): self.recordTime = datetime.datetime.now()
        self.recorder = tradeInfo.get("recorder", "zxcRobot")
        if(self.recorder == ''): self.recorder = 'zxcRobot'

        self.tradeID = tradeInfo.get("tradeID", 0)
        self.tradeID_Relation = tradeInfo.get("tradeID_Relation", "")
        self.tradeParty = tradeInfo.get("tradeParty", "")
        tradeType = tradeInfo.get("tradeType", "")
        tradeTypeTarget = tradeInfo.get("tradeTypeTarget", "")
        tradeTarget = tradeInfo.get("tradeTarget", "")
        self.tradePrice = tradeInfo.get("tradePrice", 0)
        self.tradeNum = tradeInfo.get("tradeNum", 0)
        self.tradeNum_Stock = tradeInfo.get("tradeNum_Stock", 0)
        if(usrBillType == '买入'):
            self.tradeNum_Stock = self.tradeNum 
        self.tradeMoney = tradeInfo.get("tradeMoney", 0)
        self.tradePoundage = tradeInfo.get("tradePoundage", 0)
        self.tradeProfit = tradeInfo.get("tradeProfit", 0)

        dateTime = tradeInfo.get("tradeTime", "")
        self.tradeTime = myData.iif(dateTime == "", datetime.datetime.now(), dateTime)
        if(type(self.tradeTime) == str): 
            if(self.tradeTime.count(":") == 2):
                self.tradeTime =  myData_Trans.Tran_ToDatetime(dateTime)
            else:
                self.tradeTime =  myData_Trans.Tran_ToDatetime(dateTime, "%Y-%m-%d")
        
        self.isDel = tradeInfo.get("isDel", False)
        self.remark = tradeInfo.get("remark", "")
        self.Init_TypeInfo(usrBillType, tradeTarget, tradeType, tradeTypeTarget)
    #初始类型信息
    def Init_TypeInfo(self, usrBillType, tradeTarget, tradeType = "", tradeTypeTarget = ""): 
        self.usrBillType = myData.iif(usrBillType == "" or usrBillType.count("买") == 1, myBileType.买入, myBileType.卖出)
        self.tradeTarget = tradeTarget

        if(tradeType == ""): tradeType= usrBillType.replace("买入", "").replace("买", "").replace("卖出", "").replace("卖", "")
        if(tradeTarget == "红包"):
            self.usrBillType = myBileType.受赠
            self.tradeType = myTradeType.人际 
            self.tradeTypeTarget = tradeTarget
        elif(tradeTarget == "发红包" or tradeTarget == "送礼"):
            self.usrBillType = myBileType.赠予
            self.tradeType = myTradeType.人际
            self.tradeTypeTarget = tradeTarget.replace("发", "")
        elif(tradeTarget in myTradeType_居家):
            self.tradeType = myTradeType.居家
            if(tradeTarget in myTradeType_居家_蔬菜):
                self.tradeTypeTarget = "蔬菜"
            elif(tradeTarget in myTradeType_居家_肉类):
                self.tradeTypeTarget = "肉类"
            elif(tradeTarget in myTradeType_居家_海鲜):
                self.tradeTypeTarget = "海鲜"
            elif(tradeTarget in myTradeType_居家_调料):
                self.tradeTypeTarget = "调料"
            elif(tradeTarget in myTradeType_居家_主食):
                self.tradeTypeTarget = "主食"

        elif(tradeType.count("分红") == 1 or tradeType.count("利息") == 1):
            self.usrBillType = myBileType.分红
            self.tradeType = myTradeType.投资 
            self.tradeTypeTarget = tradeTarget.replace("分红", "")
        elif(tradeType in myTradeType_投资):
            self.tradeType = myTradeType.投资 
            self.tradeTypeTarget = tradeType 
        elif(usrBillType != "" and tradeTarget != "" and tradeType != ""):     #有明确指定则不解析
            self.usrBillType = usrBillType
            self.tradeType = tradeType
            self.tradeTypeTarget = tradeTypeTarget
            self.tradeTarget = tradeTarget
        else:
            #买卖区分
            if(tradeType == "" or tradeTarget == ""): return False 
            self.tradeType = tradeType
        return True
    #生成信息字典
    def OnCreat_BillInfo(self): 
        billInfo = {}
        billInfo['usrID'] = self.usrID
        billInfo['usrBillType'] = self.usrBillType
        billInfo['recordTime'] = self.recordTime
        billInfo['recorder'] = self.recorder
        billInfo['tradeID'] = self.tradeID
        billInfo['tradeID_Relation'] = self.tradeID_Relation
        billInfo['tradeParty'] = self.tradeParty
        billInfo['tradeType'] = self.tradeType
        billInfo['tradeTypeTarget'] = self.tradeTypeTarget
        billInfo['tradeTarget'] = self.tradeTarget
        billInfo['tradePrice'] = self.tradePrice
        billInfo['tradeNum'] = self.tradeNum
        billInfo['tradeMoney'] = self.tradeMoney
        billInfo['tradePoundage'] = self.tradePoundage
        billInfo['tradeProfit'] = self.tradeProfit
        billInfo['tradeTime'] = self.tradeTime
        billInfo['isDel'] = self.isDel
        billInfo['remark'] = self.remark
        return billInfo
    def ToList(self): 
        lstValue = [self.tradeID, self.usrBillType, self.tradeParty, self.tradeType, self.tradeTypeTarget, self.tradeTarget, self.tradePrice, self.tradeNum, self.tradeNum_Stock, self.tradeMoney, self.tradePoundage, self.tradeProfit, self.tradeTime.strftime("%Y-%m-%d %H:%M:%S"), self.tradeID_Relation, self.isDel, self.recorder, self.recordTime.strftime('%Y-%m-%d %H:%M:%S'), self.remark]
        return lstValue
    def ToString(self, nSpace = 0, isSimple = False, usrBillType = "", tradeTarget = "", tradeType = "", tradeTypeTarget = ""): 
        if(isSimple == False):
            strSpace = " " * nSpace
            strBill = strSpace + "编号: " + str(self.tradeID) + "\n"
            strBill += strSpace + "账单人: " + self.usrID + "\n"
            strBill += strSpace + "账单类型: " + self.usrBillType + "\n"
            strBill += strSpace + "交易方: " + self.tradeParty + "\n"
            strBill += strSpace + "交易金额: " + str(round(self.tradeMoney, 2)) + "元 \n"
            strBill += strSpace + "交易物: " + self.tradeTarget + "\n"
            if(self.tradeType != ""): strBill += strSpace + "交易分类: " + self.tradeType + "\n"
            if(self.tradeTypeTarget != ""): strBill += strSpace + "交易子类: " + self.tradeTypeTarget + "\n"
            strBill += strSpace + "账单时间: " + myData_Trans.Tran_ToDatetime_str(self.tradeTime, "%Y-%m-%d") + "\n"
            strBill += strSpace + "备注: " + self.remark 
        else:
            strBill = self.tradeParty
            strBill += "，" + str(round(self.tradeMoney, 2)) + "元" 
            if(usrBillType == ""): strBill += "，" + self.usrBillType
            if(tradeTarget == ""): strBill += "，" + self.tradeTarget
            if(tradeType == ""): strBill += "，" + self.tradeType
            if(tradeTypeTarget == ""): strBill += "，" + self.tradeTypeTarget
            strBill += "，" + str(self.tradeID) 
            strBill += "，" + myData_Trans.Tran_ToDatetime_str(self.tradeTime, "%Y-%m-%d") 
        return strBill
    def ToString2(self, nSpace = 0): 
        strSpace = " " * nSpace
        strBill = strSpace + "编号: " + str(self.tradeID) + "\n"
        strBill += strSpace + "红包归属: " + self.usrID + "\n"
        strBill += strSpace + "红包金额: " + str(self.tradeMoney) + "元 \n"
        strBill += strSpace + "红包来源: " + self.tradeParty + "\n"
        strBill += strSpace + "红包事由: " + self.usrBillType + "\n"
        strBill += strSpace + "红包时间: " + myData_Trans.Tran_ToDatetime_str(self.tradeTime, "%Y-%m-%d") + "\n"
        strBill += strSpace + "备注: " + self.remark 
        return strBill
    #是否收入（是为正支出为负）
    def IsInCome(self): 
        if(self.usrBillType == myTradeType.红包 or self.usrBillType == myTradeType.投资回笼):
            return True
        return False
    def Check(self): 
        if(self.usrID == ""): return False
        if(not self.usrBillType in myBileType): return False
        if(not self.tradeType in myTradeType): return False 
        return True
    def IsSame(self, bill, mseconds = 1000): 
        if(bill.usrBillType == self.usrBillType and bill.tradeType == self.tradeType):
            if(bill.tradeTarget == self.tradeTarget and self.tradeParty == bill.tradeParty):
                timeDelta = myData.iif(bill.tradeTime > self.tradeTime, bill.tradeTime - self.tradeTime, self.tradeTime - bill.tradeTime)
                nMiniSeconds = (timeDelta.days * 3600 * 24 + timeDelta.seconds) * 1000 + timeDelta.microseconds
                if(nMiniSeconds < mseconds):         #n毫秒内算相同
                    if(self.isDel == bill.isDel):
                        if(self.remark != "" and self.remark == bill.remark):   #remark相同则默认相同(慎用)
                            return True
                        if(bill.usrBillType == "卖出"): return True
                        if(bill.tradeMoney == self.tradeMoney and self.tradeNum == bill.tradeNum and self.tradePrice == bill.tradePrice):
                            return True
        return False
#账单对象集
class myObj_Bills():
    def __init__(self, usrID, dir = ""):  
        self.usrID = usrID      #当前账单归属用户
        self.usrDB = {}         #当前账包信息集 
        self.dir = dir
        self._Init_DB(dir + usrID + ".csv"  )    #初始参数信息等 
    #初始账单库   
    def _Init_DB(self, path): 
        #提取字段信息  
        dtDB = myIO_xlsx.DtTable()
        dtDB.Load_csv(path, 1, 0, True, 0, ',', isUtf = True)
        
        lstFields = ["编号","账单类型","交易方","交易类型","交易子类","交易内容","交易单价","交易数量","剩余数量","交易金额","手续费","交易收益","交易时间","关联编号","是否删除","记录人","记录时间","备注"]
        if(dtDB.sheet == None): dtDB.dataField = lstFields
        lstFields_ind = dtDB.Get_Index_Fields(lstFields)
        self.lstFields = lstFields
        self.pathData = path

        #装载账单记录
        self.usrDB = {} 
        self.indLst = []
        for dtRow in dtDB.dataMat:
            bill = myObj_Bill()
            bill.usrID = self.usrID
            if(dtRow[lstFields_ind["记录时间"]] == ""): continue
            bill.recordTime = myData_Trans.Tran_ToDatetime(dtRow[lstFields_ind["记录时间"]])
            bill.recorder = dtRow[lstFields_ind["记录人"]]       
            bill.usrBillType = dtRow[lstFields_ind["账单类型"]]

            bill.tradeID = int(dtRow[lstFields_ind["编号"]])
            bill.tradeParty = dtRow[lstFields_ind["交易方"]] 
            bill.tradeType = dtRow[lstFields_ind["交易类型"]]
            bill.tradeTypeTarget = dtRow[lstFields_ind["交易子类"]]
            bill.tradeTarget = dtRow[lstFields_ind["交易内容"]]
            bill.tradePrice = float(dtRow[lstFields_ind["交易单价"]])
            bill.tradeNum = float(dtRow[lstFields_ind["交易数量"]])
            bill.tradeNum_Stock = float(dtRow[lstFields_ind["剩余数量"]])
            bill.tradeMoney = float(dtRow[lstFields_ind["交易金额"]])
            bill.tradePoundage = float(dtRow[lstFields_ind["手续费"]])
            bill.tradeProfit = float(dtRow[lstFields_ind["交易收益"]])
            bill.tradeTime = myData_Trans.Tran_ToDatetime(dtRow[lstFields_ind["交易时间"]])
            bill.tradeID_Relation = dtRow[lstFields_ind["关联编号"]]
            if(bill.tradeID_Relation == "0"): 
                bill.tradeID_Relation = ""
                                         
            bill.isDel = myData.iif(dtRow[lstFields_ind["是否删除"]] == "TRUE", True, False)
            bill.remark = dtRow[lstFields_ind["备注"]] 
            self.usrDB[bill.tradeID] = bill
            self.indLst.append(bill.tradeID)     # 顺序记录索引
        self.dtDB = dtDB
             
    #添加账单记录
    def Add(self, recorder, tradeParty, tradeMoney, tradeTarget, usrBillType = "", tradeType = "", tradeTypeTarget = "", dateTime = "", remark = "", tradePrice = 0, tradeNum = 0, tradeID_Relation = ""): 
       bill = myObj_Bill()
       bill.Init(recorder, self.usrID, tradeParty, tradeMoney, tradeTarget, usrBillType, tradeType, tradeTypeTarget, dateTime, remark, tradePrice, tradeNum, tradeID_Relation)
       return self._Add(bill)
    def Add_ByDict(self, billInfo = {}): 
       bill = myObj_Bill()
       bill.Init_ByDict(billInfo)
       return self._Add(bill)
    def _Add(self, bill, bCheck = True): 
        if(bill.usrID == "" or bill.tradeMoney == 0 or bill.tradeParty == "" or bill.tradeTarget == ""):
            return "用户名、交易金额、交易方、交易物，输入不全。"
        if(self._Check(bill) == False): return "账单信息已经存在。"
        
        #添加(记录索引)
        bill.tradeID = self._Get_ID()
        self.usrDB[bill.tradeID] = bill 
        if(bill.recordTime == "" or bill.recordTime == None):
            bill.recordTime = datetime.datetime.now()
          
        #校正存量
        bAppend = True
        if(bill.usrBillType == myBileType.买入):
            bill.tradeNum_Stock = bill.tradeNum
            
        #取ID号(usrTime排序)
        nID = self._Find_ind(bill.tradeTime)
        if(nID < len(self.indLst)):             #索引最后一个序号
            bAppend = False 
        self.indLst.insert(nID, bill.tradeID)   #记录索引


        #关联编号处理(投资卖出) 
        if(bCheck and bill.usrBillType == myBileType.卖出 and bill.tradeType in myTradeType_双向):
            bills_Last = []
            startTime = self._Trans_Time_moth(bill.tradeTime, 36) 
            if(bill.tradeID_Relation != ""):
                bill_Last = self._Find(int(bill.tradeID_Relation))
                if(bill_Last != None and bill_Last.tradeNum_Stock < bill.tradeNum):             #数量不足查询剩余
                    lstValues = self.Query(startTime, bill.tradeTime, 0, bill.tradeParty, myBileType.买入, bill.tradeTarget, bill.tradeType, bill.tradeTypeTarget)
                    bills_Last = sorted(lstValues[0], key=lambda myObj_Bill: myObj_Bill.tradePrice, reverse=True)   # sort by usrMoney
                
                #移除相同
                for x in bills_Last:
                    if(x.IsSame(bill_Last)): bills_Last.remove(x)
                if(bill_Last.tradeNum_Stock > 0):
                    bills_Last.insert(0, bill_Last)         #查询项置首
            else:
                lstValues = self.Query(startTime, bill.tradeTime, 36, bill.tradeParty, myBileType.买入, bill.tradeTarget, bill.tradeType, bill.tradeTypeTarget)
                bills_Last = sorted(lstValues[0], key=lambda myObj_Bill: myObj_Bill.tradePrice, reverse=False)   # sort by usrMoney
                
            #循环处置
            dSum = bill.tradeNum
            for x in bills_Last:
                if(dSum <= 0): break
                if(x.tradeNum_Stock <= 0): continue
                bAppend = False
                if(x.tradeNum_Stock >= bill.tradeNum):            #相等，一对一
                    x.tradeNum_Stock = x.tradeNum_Stock - bill.tradeNum   
                    x.tradeID_Relation = myData.iif(x.tradeID_Relation == "", str(bill.tradeID), str(x.tradeID_Relation) + "、" + str(bill.tradeID))
                    bill.tradeID_Relation = str(x.tradeID)
                    bill.tradeProfit = bill.tradeMoney - bill.tradePoundage - (x.tradeMoney + x.tradePoundage) * (bill.tradeNum / x.tradeNum)  
                    bill.tradeProfit = round(bill.tradeProfit, 2)
                    dSum -= bill.tradeNum
                elif(x.tradeNum_Stock < bill.tradeNum):           #小于，单一不够，拆分卖出
                    bill_New = copy.copy(bill)
                    bill_New.tradeNum = bill.tradeNum - x.tradeNum_Stock                #拆分不够部分为新记录
                    nRatio = bill_New.tradeNum / bill.tradeNum
                    bill_New.tradeMoney = bill.tradeMoney * nRatio                      #拆分总价
                    bill_New.tradePoundage = bill.tradePoundage * nRatio                #拆分手续费
                    bill_New.remark += "@@" + str(bill.tradeID)                         #调整remark，避免无法插入
                    bill_New.tradeTime = bill_New.tradeTime + datetime.timedelta(seconds=1)
                    bill.tradeNum = bill.tradeNum - bill_New.tradeNum                   #修改原始数量为当前卖出数量
                    bill.tradeMoney = bill.tradeMoney - bill_New.tradeMoney             #修改原始总价
                    bill.tradePoundage = bill.tradePoundage - bill_New.tradePoundage    #修改手续费

                    x.tradeID_Relation = myData.iif(x.tradeID_Relation == "", str(bill.tradeID), str(x.tradeID_Relation) + "、" + str(bill.tradeID))
                    bill.tradeID_Relation = str(x.tradeID)
                    bill.tradeProfit = bill.tradeMoney - bill.tradePoundage - (x.tradeMoney + x.tradePoundage) * (bill.tradeNum / x.tradeNum)
                    bill.tradeProfit = round(bill.tradeProfit, 2)
                    x.tradeNum_Stock = 0  
                    self._Add(bill_New, False)              #添加拆分项
                    dSum -= bill.tradeNum
                    bill = bill_New 
            if(dSum > 0):
                self.usrDB.pop(bill.tradeID)                #删除记录
                self.indLst.pop(nID)                        #删除索引记录
                return "账单信息无该项买入记录，无法登记。"

            #校检错误
            if(1 == 1):
                nTradeNum = 0               #总买入量
                nTradeMoney = 0             #总买总价
                nTradePoundage = 0          #总买入手续费
                nTradeNum_Stock = 0         #总剩余量
                nTradeMoney_Stock = 0       #总买总价-剩余
                nTradePoundage_Stock = 0    #总买入手续费-剩余
                for x in bills_Last:
                    nTradeNum = nTradeNum + x.tradeNum  
                    nTradeMoney = nTradeMoney + x.tradeMoney   
                    nTradePoundage = nTradePoundage + x.tradePoundage        
                    nTradeNum_Stock = nTradeNum_Stock + x.tradeNum_Stock 
                    nTradeMoney_Stock = nTradeMoney_Stock + x.tradeMoney * (x.tradeNum_Stock / x.tradeNum)
                    nTradePoundage_Stock = nTradePoundage_Stock + x.tradePoundage * (x.tradeNum_Stock / x.tradeNum)

                #统计卖出项目
                nTradeMoney_Sell = 0        #总卖总价
                nTradeNum_Sell = 0          #总卖出量
                nTradePoundage_Sell = 0     #总卖出手续费
                nTradeProfit = 0            #卖出收益
                lstValues_Sell = self.Query(startTime, bill.tradeTime, 36, bill.tradeParty, myBileType.卖出, bill.tradeTarget, bill.tradeType, bill.tradeTypeTarget)
                for x in lstValues_Sell[0]:
                    nTradeNum_Sell = nTradeNum_Sell + x.tradeNum  
                    nTradeMoney_Sell = nTradeMoney_Sell + x.tradeMoney 
                    nTradePoundage_Sell = nTradePoundage_Sell + x.tradePoundage  
                    nTradeProfit = nTradeProfit + x.tradeProfit    
  
                #对比判断(收益==已卖 - 买价 - 双向手续费)
                if(nTradeNum - nTradeNum_Stock != nTradeNum_Sell):
                    print("买入卖出量不一致")
                if(nTradeMoney_Sell - (nTradeMoney - nTradeMoney_Stock) - (nTradePoundage - nTradePoundage_Stock) - nTradePoundage_Sell - nTradeProfit >= 0.01):
                    print("卖出收益不一致")
                    
        #保存--排序
        if(bAppend == False or len(self.usrDB) == 1):
            self.Save_DB()
        else:
            self.dtDB.Save_csv_append(self.pathData, bill.ToList(), True, row_end = len(self.usrDB)-1 )   
        return "添加成功，账单信息如下：\n" + bill.ToString(4)
     
    def Query(self, startTime = '', endTime = '', nMonth = 1, tradeParty = '', usrBillType = "", tradeTarget = "", tradeType = "", tradeTypeTarget = "", exceptDeault = False, exceptBillTypes = [], exceptTradeTypes = [], bNoRelation = False): 
        #查询参数校正
        if(type(startTime) != datetime.datetime): startTime = self._Trans_Time_moth(datetime.datetime.now(), nMonth) 
        if(type(endTime) != datetime.datetime): endTime = datetime.datetime.now()
        
        #循环查询
        nLen_BillTypes = len(exceptBillTypes)
        nLen_TradeTypes = len(exceptTradeTypes)
        lstBill = []
        ind_S = self._Find_ind(startTime, True)
        ind_E = self._Find_ind(endTime)
        for x in range(ind_S, ind_E):
            bill = self._Find(self.indLst[x])   
            if(bill.isDel): continue    
            if(exceptDeault and bill.tradeParty == "未记名"): continue 
            if(tradeParty != "" and tradeParty != bill.tradeParty): continue
            if(usrBillType != "" and usrBillType != bill.usrBillType): continue
            if(tradeType != "" and tradeType != bill.tradeType): continue
            if(tradeTypeTarget != "" and tradeTypeTarget != bill.tradeTypeTarget): continue
            if(tradeTarget != "" and tradeTarget != bill.tradeTarget): continue
            if(bNoRelation and bill.tradeID_Relation != ""): continue
            if(nLen_BillTypes > 0):
                if(bill.usrBillType in exceptBillTypes): continue  
            if(nLen_TradeTypes > 0):
                if(bill.tradeType in exceptTradeTypes): continue  
            lstBill.append(bill)
        return lstBill, startTime, endTime 
    def Static(self, startTime = '', endTime = '', nMonth = 1, tradeParty = '', usrBillType = "", tradeTarget = "", tradeType = "", tradeTypeTarget = ""): 
        if(tradeType != ""):
            if(type(startTime) == str and startTime != ""): startTime = myData_Trans.Tran_ToDatetime(startTime, "%Y-%m-%d")
            if(type(endTime) == str and endTime != ""): endTime = myData_Trans.Tran_ToDatetime(endTime, "%Y-%m-%d")
            lstBill, startTime, endTime  = self.Query(startTime, endTime, nMonth, tradeParty, usrBillType, tradeTarget, tradeType, tradeTypeTarget)
        else:
            #单独查询投资所有
            startTime2 = startTime
            if(len(self.indLst) > 0): startTime2 = self._Trans_Time_year(self._Find(self.indLst[0]).tradeTime) 
            lstBill2, startTime2, endTime2  = self.Query(startTime2, endTime, nMonth, tradeParty, usrBillType, tradeTarget, myTradeType.投资, tradeTypeTarget)
            lstBill, startTime, endTime  = self.Query(startTime, endTime, nMonth, tradeParty, usrBillType, tradeTarget, tradeType, tradeTypeTarget, False, [], [myTradeType.投资])
            lstBill = lstBill + lstBill2
        
        #统计项目初始
        lstCount = {}
        for x in myBileType: 
            lstCount_Type = {}
            lstCount[x] = lstCount_Type
            for xx in myTradeType:
                lstCount_Type[xx] = {}

        #统计
        dSum_收益 = 0
        for x in lstBill:
            lstCount_Bill = lstCount[x.usrBillType] 
            lstCount_Type = lstCount_Bill[x.tradeType]
            lstCount_TypeTarget = lstCount_Type.get(x.tradeTypeTarget, None)
            if(lstCount_TypeTarget == None):
                lstCount_TypeTarget = {}
                lstCount_Type[x.tradeTypeTarget] = lstCount_TypeTarget

            dSum = lstCount_TypeTarget.get(x.tradeTarget, 0) + x.tradeMoney     #按名称累加
            lstCount_TypeTarget[x.tradeTarget] = dSum                           #子类累加
            lstCount_Type["SUM"] = lstCount_Type.get("SUM", 0) + x.tradeMoney   #金额累加
            lstCount_Bill["SUM"] = lstCount_Bill.get("SUM", 0) + x.tradeMoney   #金额累加-账单类型
            lstCount_Type["SUM_Poundage"] = lstCount_Type.get("SUM_Poundage", 0) + x.tradePoundage   #金额累加-手续费 
            lstCount_Bill["SUM_Poundage"] = lstCount_Bill.get("SUM_Poundage", 0) + x.tradePoundage   #金额累加-手续费-账单类型

            #投资卖出，需找到买入
            if(x.usrBillType == myBileType.卖出 and x.tradeType == myTradeType.投资):
                lstCount_Type["SUM_Profit"] = lstCount_Type.get("SUM_Profit", 0) + x.tradeProfit   #收益累加
                lstCount_Bill["SUM_Profit"] = lstCount_Bill.get("SUM_Profit", 0) + x.tradeProfit   #收益累加-账单类型

                #查询买入源
                if(x.tradeID_Relation != ""):
                    bill = self._Find(int(x.tradeID_Relation))
                    if(bill != None):
                        #lstCount_Bill["SUM_投资回笼"] = lstCount_Bill.get("SUM_投资回笼", 0) + x.tradeNum * bill.tradePrice   #收益原始投资-账单类型
                        bExist = False
                        for xx in lstBill:
                            if(xx.tradeID == bill.tradeID):
                                bExist = True
                                break
                        if(bExist == False): 
                            lstBill.append(bill)
                            
        #转账
        dSum_转入 = 0
        dSum_转出 = 0
        if(lstCount[myBileType.转账][myTradeType.投资].get("转入", None) != None):
            dSum_转入 = lstCount[myBileType.转账][myTradeType.投资]["转入"].get("现金", 0)
        if(lstCount[myBileType.转账][myTradeType.投资].get("转出", None) != None):
            dSum_转出 = lstCount[myBileType.转账][myTradeType.投资]["转出"].get("现金", 0)
        dSum_转帐 = dSum_转入 - dSum_转出

        #累加（自下向上）
        dSum_In_投资总计 = 0
        dSum_In_投资 = lstCount[myBileType.买入][myTradeType.投资].get("SUM", 0)       
        dSum_Out_投资 = lstCount[myBileType.卖出][myTradeType.投资].get("SUM", 0) 
        dSum_手续费 = lstCount[myBileType.买入].get("SUM_Poundage", 0) + lstCount[myBileType.卖出].get("SUM_Poundage", 0)
        dSum_分红 = lstCount[myBileType.分红].get("SUM", 0)
        dSum_收益 = lstCount[myBileType.卖出].get("SUM_Profit", 0)             #已去除手续费
        dSum_红包 = lstCount[myBileType.受赠][myTradeType.人际].get("SUM", 0)
        dSum_消费 = lstCount[myBileType.买入].get("SUM", 0) - dSum_In_投资
        dSum_收入 = lstCount[myBileType.卖出].get("SUM", 0) - dSum_Out_投资 
        dSum_In = dSum_收入 + lstCount[myBileType.受赠].get("SUM", 0) + dSum_收益
        dSum_Out = dSum_消费 + lstCount[myBileType.赠予].get("SUM", 0)  
        dSum_ALL = dSum_In - dSum_Out + dSum_转帐 + dSum_分红
        
        #输出信息
        strPerfix = "\n" + " " * 4
        strOut = "账单统计(" + self.usrID + ")："
        strOut += "\n" + "总资产：" + str(round(dSum_ALL, 2)) + "元"
        if(dSum_红包 > 0):
            strOut += strPerfix + "红包收入：" + str(round(dSum_红包, 2)) + "元"
        if(dSum_Out_投资 > 0):
            dSum_In_投资总计 = dSum_Out_投资 - dSum_In_投资 + dSum_收益 + dSum_分红     #加入分红的钱，收益股价未除权
            strOut += strPerfix + "投资收益：" + str(round(dSum_收益, 2)) + "元"
            strOut += strPerfix + "    " + "手续费：" + str(round(dSum_手续费, 2)) + "元"
            strOut += strPerfix + "    " + "分红累计：" + str(round(dSum_分红, 2)) + "元"
            strOut += strPerfix + "    " + "投资累计：" + str(round(dSum_In_投资, 2)) + "元" 
            strOut += strPerfix + "    " + "回笼累计：" + str(round(dSum_Out_投资 - myData.iif(dSum_收益 < 0,0, dSum_收益), 2)) + "元"
            strOut += strPerfix + "    " + "投资总计：" + str(round(dSum_In_投资总计, 0)) + "元"
        if(dSum_Out > 0):
            strOut += strPerfix + "消费总计：" + str(round(dSum_Out, 2)) + "元"
            #消费细分：
            lst消费 = lstCount[myBileType.买入]
            for x in lst消费.keys():
                if(x == "投资" or x == "SUM"): continue
                dSum = lst消费[x].get("SUM", 0)
                if(dSum > 0):  
                    strOut += strPerfix + "    " + x +"：" + str(round(dSum, 2)) + "元"

                    #子类型细分
                    lst消费类型 = lst消费[x]
                    for x in lst消费类型.keys():
                        if(x == "投资" or x == "SUM"): continue
                        dSum_C = lst消费类型[x].get("SUM", 0)
                        if(dSum_C > 0):  
                            strOut += strPerfix + "    " * 2 + x +"：" + str(round(dSum_C, 2)) + "元"

        #特殊指定类型处理
        if(usrBillType != "" and tradeType != ""):
            pLst = lstCount[usrBillType][tradeType]
            strOut += strPerfix + "总计：" + str(round(pLst['SUM'], 2)) + "元"
            strOut += strPerfix + "    " + "手续费" +"：" + str(round(pLst['SUM_Poundage'], 2)) + "元"
            for x in pLst.keys():
                if(x.count("SUM") == 1): continue

                #循环组装所有
                keys = pLst[x].keys()
                for xx in keys:
                    strOut += strPerfix + "    " + x + xx +"：" + str(round(pLst[x][xx], 2)) + "元"
        else:
            if(dSum_转帐 > 0):
                strOut += strPerfix + "转账累计：" + str(round(dSum_转帐, 2)) + "元"
                strOut += strPerfix + "    " + "手续费：" + str(round(lstCount[myBileType.转账]["SUM_Poundage"], 2)) + "元"
                strOut += strPerfix + "    " + "转入累计：" + str(round(dSum_转入, 2)) + "元" 
                strOut += strPerfix + "    " + "转出累计：" + str(round(dSum_转出, 2)) + "元"
                strOut += strPerfix + "    " + "净投资额：" + str(round(dSum_转帐, 2)) + "元"
            #当前账目余额
            strOut += strPerfix + "现金总计：" + str(round(dSum_ALL - dSum_In_投资总计, 2)) + "元"
                 
        if(usrBillType != ""): strOut += "\n账单类型：" + usrBillType    
        if(tradeTarget != ""): strOut += "\n交易品名：" + tradeTarget          
        if(tradeParty != ""): strOut += "\n交易方：" + tradeParty
        if(tradeType != ""): strOut += "\n交易品类：" + tradeType       
        if(tradeTypeTarget != ""): strOut += "\n交易品子类：" + tradeTypeTarget  
        strOut += "\n账单时间：" + strPerfix + myData_Trans.Tran_ToDatetime_str(startTime, "%Y-%m-%d") + " 至 " + myData_Trans.Tran_ToDatetime_str(endTime, "%Y-%m-%d") 
        return strOut
    def Static_max(self, startTime = '', endTime = '', nMonth = 1, tradeParty = '', usrBillType = "", tradeTarget = "", tradeType = "", tradeTypeTarget = "", bSum = False, nTop = 10, bMoney = True): 
        if(myTradeType.投资 != tradeType):
            lstBill, startTime, endTime  = self.Query(startTime, endTime, nMonth, tradeParty, usrBillType, tradeTarget, tradeType, tradeTypeTarget, True, [], [myTradeType.投资])
        else:   #投资相关需单独统计
            lstBill, startTime, endTime  = self.Query(startTime, endTime, nMonth, tradeParty, usrBillType, tradeTarget, tradeType, tradeTypeTarget, True, [], [])
        
        #统计        
        bReverse = True 
        if(tradeParty != ""): bSum = False
        if(bSum == False):      #最大金额统计
            if(bMoney):
                lstValues = sorted(lstBill, key=lambda myObj_Bill: myObj_Bill.tradeMoney, reverse=bReverse)   # sort by tradeMoney
            else:
                lstValues = sorted(lstBill, key=lambda myObj_Bill: myObj_Bill.tradeTime, reverse=bReverse)    # sort by tradeTime
        else:                   #累计统计
            dictSum = {}
            dictTimes = {}
            lstStatics = []
            for x in lstBill: 
                dSum = dictSum.get(x.tradeParty, 0)  
                dSum += x.tradeMoney
                dictSum[x.tradeParty] = dSum
                dictTimes[x.tradeParty] = dictTimes.get(x.tradeParty, 0) + 1

            keys = dictSum.keys()
            for x in keys:
                lstStatics.append((x, dictSum[x], dictTimes[x]))
            lstValues = sorted(lstStatics, key=itemgetter(1), reverse=bReverse)   # sort by tradeMoney

        #输出
        ind = 0
        strPerfix = "\n" + " " * 4
        strOut = "Top " + str(nTop) + " " + myData.iif(bSum, "累计金额", "单次金额") + "(" + self.usrID + ")："
        if(bSum):
            strOut += strPerfix + "排名，交易方，金额，次数"
        else:
            strOut += strPerfix +  "排名，交易方，金额"
            if(usrBillType == ""): strOut += "，分类"
            if(tradeTarget == ""): strOut += "，品名"  
            if(tradeType == ""): strOut += "，品类"  
            if(tradeTypeTarget == ""): strOut += "，子品类" 
            strOut += "，编号，时间" 

        for x in range(0, len(lstValues)):
            bill = lstValues[x]
            strTop = "Top " + str(ind + 1) + "："
            if(bSum == False): 
                strOut += strPerfix + strTop + bill.ToString(0, True, usrBillType, tradeTarget, tradeType, tradeTypeTarget)
            else:
                strOut += strPerfix + strTop + bill[0] + "，" + str(int(bill[1])) + "元，" + str(bill[2]) + "次"
            ind += 1
            if(ind >= nTop): break 
                 
        if(usrBillType != ""): strOut += "\n账单类型：" + usrBillType    
        if(tradeTarget != ""): strOut += "\n交易品名：" + tradeTarget          
        if(tradeParty != ""): strOut += "\n交易方：" + tradeParty
        if(tradeType != ""): strOut += "\n交易品类：" + tradeType       
        if(tradeTypeTarget != ""): strOut += "\n交易品子类：" + tradeTypeTarget  
        strOut += "\n账单时间：" + strPerfix + myData_Trans.Tran_ToDatetime_str(startTime, "%Y-%m-%d") + " 至 " + myData_Trans.Tran_ToDatetime_str(endTime, "%Y-%m-%d") 
        return strOut
    
    #查找
    def _Find_ind(self, usrTime, bIn = False): 
        #取ID号(usrTime排序)
        nID = len(self.indLst) - 1                      #索引最后一个序号
        if(nID >= 0):
            bill_Last = self._Find(self.indLst[nID])    #索引依次往前-usrTime排序
            if(bIn == False):
                while(nID >= 0 and bill_Last != None and bill_Last.tradeTime > usrTime):
                    nID -= 1
                    bill_Last = self._Find(self.indLst[nID])
            else:
                while(nID >= 0 and bill_Last != None and bill_Last.tradeTime >= usrTime):
                    nID -= 1
                    bill_Last = self._Find(self.indLst[nID])
        return nID + 1
    def _Find(self, id): 
        return self.usrDB.get(id, None)
    def _Get_ID(self):
        if(len(self.usrDB) == 0): return 1
        return len(self.usrDB) + 1

    #检查是否已经存在   
    def _Check(self, bill): 
        keys = self.usrDB.keys()
        for x in keys:
            billTemp = self.usrDB[x]
            if(billTemp.tradeTarget =="建设银行" and billTemp.tradeNum==5000):
                aa =0 
            if(bill.IsSame(billTemp, 1000)): 
                return False
        return True
    #时间转换为月初
    def _Trans_Time_moth(self, dtTime = '', nMonth = 1): 
        if(type(dtTime) != datetime.datetime): dtTime = datetime.datetime.now() 
        dtTime = dtTime - datetime.timedelta(days=(dtTime.day - 1))
        while(nMonth > 1):
            dtTime = self._Trans_Time_moth(dtTime - datetime.timedelta(days=1))
            nMonth -= 1
        strTime = myData_Trans.Tran_ToDatetime_str(dtTime, "%Y-%m-%d")
        return myData_Trans.Tran_ToDatetime(strTime, "%Y-%m-%d")
    #时间转换为年初
    def _Trans_Time_year(self, dtTime = "", nYears = 1): 
        if(type(dtTime) != datetime.datetime): dtTime = datetime.datetime.now() 
        nMonths = dtTime.month 
        if(nYears > 1): nMonths += (nYears -1) * 12
        return self._Trans_Time_moth(dtTime, nMonths)
    
    #生成信息字典
    def OnCreat_BillInfo(self): 
        pBill = myObj_Bill()
        return pBill.OnCreat_BillInfo()
    #当前数据进行保存   
    def Save_DB(self):  
        #组装行数据
        self.dtDB.dataMat = []
        for x in self.indLst:
            bill = self._Find(x) 
            self.dtDB.dataMat.append(bill.ToList())

        #保存
        self.dtDB.Save_csv(self.dir, self.usrID, True, 0, 0)
        
#管家功能--账单
class myManager_Bill():
    def __init__(self, dir = ""): 
        #初始根目录信息
        if(dir == ""):
            strDir, strName = myIO.getPath_ByFile(__file__)
            self.Dir_Base = os.path.abspath(os.path.join(strDir, "../../.."))  
            self.Dir_DataDB = self.Dir_Base + "/Data/DB_Bill/"
            myIO.mkdir(self.Dir_DataDB, False)
        else:
            self.Dir_DataDB = dir
        self._Init()            #初始参数信息等 
    #初始参数信息等   
    def _Init(self): 
        #提取所有用户DB文件
        lstFile = myIO.getFiles(self.Dir_DataDB, '.csv', True)

        #循环提取所有
        self.usrBills = {}      #当前用户账单信息字典
        for x in lstFile:
            usrID = myIO.getFileName(x)
            bills = myObj_Bills(usrID, self.Dir_DataDB)
            self.usrBills[usrID] = bills
        return True
    #查询、统计
    def _Find(self, usrID, bAuto_Creat = False): 
        bills = self.usrBills.get(usrID, None)
        if(bills == None and bAuto_Creat == True):
            bills = myObj_Bills(usrID, self.Dir_DataDB)
        return bills
    #用户账单
    def __getitem__(self, usrID):
        return self._Find(usrID, True)
              
#初始全局消息管理器
from myGlobal import gol 
gol._Init()     #先必须在主模块初始化（只在Main模块需要一次即可）
gol._Set_Setting('manageBills', myManager_Bill(""))     #实例 账单管理器 
         

#主启动程序
if __name__ == "__main__":
    #测试红包记录
    pManager = gol._Get_Setting('manageBills', None)
    pBills = pManager['Test']
    #pManager['朱美娜'].Save_DB()
    
    pBills.Add("", "门口超市", 10.2, "蔬菜", "", "", "", "")
    pBills.Add("", "门口超市", 20.4, "菜", "", "", "", "2018-8-20")
    pBills.Add("", "西边菜市场", 10.4, "菜", "", "", "","2018-8-22")
    pBills.Add("", "西边菜市场", 10.4, "菜", "", "", "", "2018-8-23")
    pBills.Add("", "西边菜市场", 10.4, "菜", "", "", "", "2018-8-16")
    pBills.Add("", "西边菜市场", 16.5, "猪肉", "", "", "", "2018-8-29")
  
    pBills.Add("", "国泰君安", 1000, "江苏银行", "买股票", "", "", "2018-5-16", "remark 2018-5-16", 10, 100,)
    pBills.Add("", "国泰君安", 800, "江苏银行", "买股票", "", "", "2018-6-16", "remark 2018-6-16 10:00:00", 8, 100)
    pBill = pBills.Query( "", "", 4, "", "", "江苏银行", "投资", "股票")
    pBills.Add("", "国泰君安", 120, "江苏银行", "卖股票", "", "", "2018-8-16", "remark 2018-8-16 10:00:00", 12, 10, pBill[0][0].tradeID) 
    pBills.Add("", "国泰君安", 1200, "江苏银行", "卖股票", "", "", "2018-8-17", "remark 2018-8-17 10:00:00", 12, 100, pBill[0][0].tradeID) 
    pBills.Add("", "老豆", 100, "红包", "", "", "", "2018-8-18")
    pBills.Add("", "老豆", 100, "红包", "", "", "", "2018-1-18")

    #查询统计测试
    myDebug.Debug(pBills.Static())
    myDebug.Debug(pBills.Static( "", "", 3, "", "", "", "", ""))
    myDebug.Debug(pBills.Static( "", "", 6, "", "", "", "", ""))
    myDebug.Debug(pBills.Static( "", "", 12, "", "", "", "", ""))
    myDebug.Debug(pBills.Static(pBills._Trans_Time_year("", 1), "", 12, "", "", "", "", ""))
    
    myDebug.Debug(pBills.Static(pBills._Trans_Time_year("", 1), "", 0, "", "", "红包", "", ""))
    myDebug.Debug(pBills.Static(pBills._Trans_Time_year("", 1), "", 0, "老豆", "", "红包", "", "红包"))
    print()


    #复杂统计
    pBills = pManager['多多']
    myDebug.Debug(pBills.Static(pBills._Trans_Time_year("", 1), "", 0, "", "", "", "", ""))
    
    myDebug.Debug(pBills.Static(pBills._Trans_Time_year("", 1), "", 0))
    myDebug.Debug(pBills.Static(pBills._Trans_Time_year("", 2), "", 0))
    myDebug.Debug(pBills.Static(pBills._Trans_Time_year("", 3), "", 0))

    myDebug.Debug(pBills.Static_max(pBills._Trans_Time_year("", 3), "", 0, "", "受赠", "红包", "", "", False, 10))
    print()
    myDebug.Debug(pBills.Static_max(pBills._Trans_Time_year("", 3), "", 0, "", "受赠", "红包", "", "", True, 10))
    print()
    myDebug.Debug(pBills.Static_max(pBills._Trans_Time_year("", 3), "", 0, "爸爸", "受赠", "红包", "", "", True, 10))
    print()
    myDebug.Debug(pBills.Static_max(pBills._Trans_Time_year("", 3), "", 0, "爸爸", "受赠", "红包", "", "", True, 10, False))
    

    exit()


    
