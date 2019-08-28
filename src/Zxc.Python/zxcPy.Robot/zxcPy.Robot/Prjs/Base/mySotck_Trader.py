#-*- coding: utf-8 -*-
"""
Created on  张斌 2019-08-27 15:58:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com
    
    股票交易员--买卖操作(记录、查询、统计等)
"""
import sys, os, time, copy, datetime, mySystem
from operator import itemgetter, attrgetter

#引用根目录类文件夹--必须，否则非本地目录起动时无法找到自定义类
mySystem.Append_Us("../Prjs", False, __file__)
mySystem.Append_Us("../../../../zxcPy.Quote/zxcPy.Quotation", False, __file__)
mySystem.Append_Us("", False) 
import myEnum, myIO, myIO_xlsx, myData, myData_Trans, myDebug 
import myQuote
from myGlobal import gol 


#定义交易类型枚举
myOrderType = myEnum.enum('买入', '卖出', '受赠', '赠予', '分红', '转账')
myTradeType_投资 = ['活期', '定期', '股票', '基金', '可转债', '国债逆回购', '理财', '转入', '转出']



# 交易信息
class myObj_Trade():
    def __init__(self): 
        self.usrID = ""             #用户名
        self.usrOrderType = ""      #用户操作类型(买入/卖出/看涨/看跌)
        self.recordTime = None      #记录时间
        self.recorder = None        #记录人
        
        self.targetID = ""          #标的代码
        self.targetName = ""        #标的名称
        self.targetMarket = ""      #标的所属市场
        self.targetMarketBoard = "" #标的所属市场板块
        self.targetIndustries = []  #标的行业分类
        self.targetConcepts = []    #标的概念分类
        self.targetPrice = 0        #标的价格-当前
        self.targetPrice_Ex = 0     #标的价格-期望值
        self.targetPosition = 0     #标的仓位-该股相对全部资金

        self.infoID = 0             #信息编号
        self.tradeType = "投资"     #交易分类(投资)
        self.tradeType_sub = "股票" #交易内容分类(股票、基金)
        self.tradeNum = 0           #交易数量
        self.tradeMoney = 0         #交易金额
        self.tradePosition = 0      #交易仓位-单笔相对全部资金
        self.tradeProfit = 0        #交易收益-单笔涨幅
        self.tradeProfit_total = 0  #交易收益-年度总涨幅
        self.tradeTime = None       #交易时间

        self.isDel = False          #是否已删除
        self.remark = ""            #备注
    def Init(self, usrID, targetID, targetPrice, tradePosition, usrOrderType = "", tradeType = "", tradeType_sub = "", targetName = "", targetPosition = 0, targetPrice_Ex = 0, tradeNum = 0, tradeMoney = 0, tradeProfit = 0, tradeProfit_total = 0, tradeTime = "", remark = "", recorder = ""):
        self.usrID = usrID 
        self.usrOrderType = usrOrderType
        
        self.targetID = targetID 
        self.targetName = targetName 
        self.targetPrice = targetPrice 
        self.targetPrice_Ex = targetPrice_Ex 
        self.targetPosition = targetPosition 
        
        self.tradeType = tradeType 
        self.tradeType_sub = tradeType_sub 
        self.tradeNum = tradeNum 
        self.tradeMoney = tradeMoney 
        self.tradePosition = tradePosition 
        self.tradeProfit = tradeProfit 
        self.tradeProfit_total = tradeProfit_total 
        self.tradeTime = tradeTime
        self.remark = remark
        self.recorder = myData.iif(recorder == "", "zxcRobot", recorder)
        
        tradeInfo = self.OnCreat_TradeInfo()
        return self.Init_ByDict(tradeInfo) 
    def Init_ByDict(self, tradeInfo = {}): 
        self.usrID = tradeInfo.get("usrID", "")
        self.usrOrderType = tradeInfo.get("usrOrderType", "")
        self.recordTime = tradeInfo.get("recordTime", datetime.datetime.now())
        if(self.recordTime == None): self.recordTime = datetime.datetime.now()
        self.recorder = tradeInfo.get("recorder", "zxcRobot")
        if(self.recorder == ''): self.recorder = 'zxcRobot'

        self.targetID = tradeInfo.get("targetID", 0)
        self.targetName = tradeInfo.get("targetName", "")
        self.targetMarket = tradeInfo.get("targetMarket", "")
        self.targetMarketBoard = tradeInfo.get("targetMarketBoard", "")
        self.targetIndustries = tradeInfo.get("targetIndustries", [])
        self.targetConcepts = tradeInfo.get("targetConcepts", [])
        self.targetPrice = tradeInfo.get("targetPrice", 0)
        self.targetPrice_Ex = tradeInfo.get("targetPrice_Ex", 0)
        self.targetPosition = tradeInfo.get("targetPosition", 0)

        self.infoID = tradeInfo.get("infoID", 0)
        self.tradeType = tradeInfo.get("tradeType", "")
        self.tradeType_sub = tradeInfo.get("tradeType_sub", "")
        self.tradeNum = tradeInfo.get("tradeNum", 0)
        self.tradeMoney = tradeInfo.get("tradeMoney", 0)
        self.tradePosition = tradeInfo.get("tradePosition", 0)
        self.tradeProfit = tradeInfo.get("tradeProfit", 0)
        self.tradeProfit_total = tradeInfo.get("tradeProfit_total", 0)

        dateTime = tradeInfo.get("tradeTime", "")
        self.tradeTime = myData.iif(dateTime == "", datetime.datetime.now(), dateTime)
        if(type(self.tradeTime) == str): 
            if(self.tradeTime.count(":") == 2):
                self.tradeTime =  myData_Trans.Tran_ToDatetime(dateTime)
            else:
                self.tradeTime =  myData_Trans.Tran_ToDatetime(dateTime, "%Y-%m-%d")
        
        self.isDel = tradeInfo.get("isDel", False)
        self.remark = tradeInfo.get("remark", "")
        return self.Init_CheckInfo(self.usrOrderType, self.tradeType, self.tradeType_sub)
    #初始类型信息检查修正
    def Init_CheckInfo(self, usrOrderType, tradeType = "", tradeType_sub = ""): 
        # 基础信息修正
        self.usrOrderType = myData.iif(usrOrderType == "" or usrOrderType.count("买") == 1, myOrderType.买入, usrOrderType) 
        self.usrOrderType = myData.iif(usrOrderType == "" or usrOrderType.count("卖") == 1, myOrderType.卖出, usrOrderType) 
        self.tradeType = myData.iif(tradeType == "" or tradeType in myTradeType_投资, "投资", tradeType) 
        self.tradeType_sub = myData.iif(tradeType == "", "股票", tradeType) 

        # 股票信息补全
        targets = self.targetID.split('.')
        pStocks = gol._Get_Value('setsStock', None)
        stocks = pStocks._Find(targets[1], exType = targets[0])
        if(len(stocks) != 1):
            stocks = pStocks._Find(self.targetName)
            if(len(stocks) != 1): return False

        pStock = stocks[0]
        self.tradeType_sub = myQuote.stockTypes.get(pStock.type.lower(), '股票')
        self.targetID = pStock.code_id
        self.targetName = pStock.code_name
        self.targetMarket = pStock.exName
        self.targetMarketBoard = pStock.getMarketBoard()
        self.targetIndustries = pStock.getIndustries()
        self.targetConcepts = pStock.getConcepts()
        return True
    #生成信息字典
    def OnCreat_TradeInfo(self): 
        tradeInfo = {}
        tradeInfo['usrID'] = self.usrID
        tradeInfo['usrOrderType'] = self.usrOrderType
        tradeInfo['recordTime'] = self.recordTime
        tradeInfo['recorder'] = self.recorder
        
        tradeInfo['targetID'] = self.targetID
        tradeInfo['targetName'] = self.targetName
        tradeInfo['targetMarket'] = self.targetMarket
        tradeInfo['targetMarketBoard'] = self.targetMarketBoard
        tradeInfo['targetIndustries'] = self.targetIndustries
        tradeInfo['targetConcepts'] = self.targetConcepts
        tradeInfo['targetPrice'] = self.targetPrice
        tradeInfo['targetPrice_Ex'] = self.targetPrice_Ex
        tradeInfo['targetPosition'] = self.targetPosition

        tradeInfo['infoID'] = self.infoID
        tradeInfo['tradeType'] = self.tradeType 
        tradeInfo['tradeType_sub'] = self.tradeType_sub 
        tradeInfo['tradeNum'] = self.tradeNum
        tradeInfo['tradeMoney'] = self.tradeMoney
        tradeInfo['tradePosition'] = self.tradePosition
        tradeInfo['tradeProfit'] = self.tradeProfit
        tradeInfo['tradeProfit_total'] = self.tradeProfit_total

        tradeInfo['tradeTime'] = self.tradeTime
        tradeInfo['isDel'] = self.isDel
        tradeInfo['remark'] = self.remark
        return tradeInfo
    #生成list
    def ToList(self): 
        lstValue = [self.infoID, self.usrID, self.usrOrderType, self.targetID, self.targetName, self.targetMarket, self.targetMarketBoard, self.targetPrice, self.targetPrice_Ex, self.targetPosition, myData_Trans.Tran_ToStr(self.targetIndustries, symbol = '、'), myData_Trans.Tran_ToStr(self.targetConcepts, symbol = '、'), self.tradeType, self.tradeType_sub, self.tradeNum, self.tradeMoney, self.tradePosition, self.tradeProfit, self.tradeProfit_total, self.tradeTime.strftime("%Y-%m-%d %H:%M:%S"), self.isDel, self.recorder, self.recordTime.strftime('%Y-%m-%d %H:%M:%S'), self.remark]
        return lstValue
    #生成提示信息
    def ToTitlestr(self, nSpace = 0, isSimple = False, usrOrderType = "", tradeTarget = "", tradeType = "", tradeTypeTarget = ""): 
        if(isSimple == False):
            strSpace = " " * nSpace
            strTrade = strSpace + "编号: " + str(self.infoID) + "\n"
            strTrade += strSpace + "用户名: " + self.usrID + "\n"
            strTrade += strSpace + "交易类型: " + self.usrOrderType + "\n"
            strTrade += strSpace + "标的信息: " + self.targetID + "  " + self.targetName + "\n"
            strTrade += strSpace + "标的价格: " + str(round(self.targetPrice, 2)) + "元 \n"
            strTrade += strSpace + "交易金额: " + str(round(self.tradeMoney, 2)) + "元 \n" 
            strTrade += strSpace + "账单时间: " + myData_Trans.Tran_ToDatetime_str(self.tradeTime, "%Y-%m-%d") + "\n"
            strTrade += strSpace + "备注: " + self.remark 
        else:
            strTrade = self.tradeParty
            strTrade += "，" + str(round(self.tradeMoney, 2)) + "元" 
            if(usrTradeType == ""): strTrade += "，" + self.usrTradeType
            if(tradeTarget == ""): strTrade += "，" + self.tradeTarget
            if(tradeType == ""): strTrade += "，" + self.tradeType
            if(tradeTypeTarget == ""): strTrade += "，" + self.tradeTypeTarget
            strTrade += "，" + str(self.infoID) 
            strTrade += "，" + myData_Trans.Tran_ToDatetime_str(self.tradeTime, "%Y-%m-%d") 
        return strTrade
    #是否相同
    def IsSame(self, trade, mseconds = 1000): 
        if(trade.usrOrderType == self.usrOrderType and trade.tradeType == self.tradeType):
            if(trade.targetID == self.targetID):
                timeDelta = myData.iif(trade.tradeTime > self.tradeTime, trade.tradeTime - self.tradeTime, self.tradeTime - trade.tradeTime)
                nMiniSeconds = (timeDelta.days * 3600 * 24 + timeDelta.seconds) * 1000 + timeDelta.microseconds
                if((datetime.datetime.now() - trade.recordTime).days < 1):         #一天内算相同
                    return True
        return False
# 交易信息对象集
class myObj_Trades():
    def __init__(self, usrID = "zxcTradeInfos", dir = ""):  
        self.usrID = usrID      #当前账单归属用户
        self.usrDB = {}         #当前账包信息集 
        self.dir = dir

        #初始根目录信息
        if(self.dir == ""):
            strDir, strName = myIO.getPath_ByFile(__file__)
            self.dirBase = os.path.abspath(os.path.join(strDir, "../../.."))  
            self.dir = self.dirBase + "/Data/DB_Trade/"
            myIO.mkdir(self.dir, False)
        self._Init_DB(self.dir + usrID + ".csv"  )    #初始参数信息等 
    #初始信息库   
    def _Init_DB(self, path): 
        #提取字段信息  
        dtDB = myIO_xlsx.DtTable()
        dtDB.Load_csv(path, 1, 0, True, 0, ',', isUtf = True)
        
        lstFields = ["编号","用户名","操作类型","标的代码","标的名称","标的所属市场","标的所属市场板块","标的价格","标的价格-期望","标的仓位","标的所属行业","标的所属概念","交易类型","交易子类型","交易数量","交易金额","交易量仓位占比","交易收益","交易收益-总计","交易时间","是否删除","记录人","记录时间","备注"]
        if(dtDB.sheet == None): dtDB.dataField = lstFields
        lstFields_ind = dtDB.Get_Index_Fields(lstFields)
        self.lstFields = lstFields
        self.pathData = path

        #装载账单记录
        self.usrDB = {} 
        self.indLst = []
        for dtRow in dtDB.dataMat:
            trade = myObj_Trade()
            if(dtRow[lstFields_ind["记录时间"]] == ""): continue
            trade.recordTime = myData_Trans.Tran_ToDatetime(dtRow[lstFields_ind["记录时间"]])
            trade.recorder = dtRow[lstFields_ind["记录人"]]    

            trade.usrID = dtRow[lstFields_ind["编号"]]
            trade.usrOrderType = dtRow[lstFields_ind["操作类型"]]
            
            trade.targetID = dtRow[lstFields_ind["标的代码"]]
            trade.targetName = dtRow[lstFields_ind["标的名称"]] 
            trade.targetMarket = dtRow[lstFields_ind["标的所属市场"]] 
            trade.targetMarketBoard = dtRow[lstFields_ind["标的所属市场板块"]]  
            trade.targetIndustries = dtRow[lstFields_ind["标的所属行业"]].split("、") 
            trade.targetConcepts = dtRow[lstFields_ind["标的所属概念"]].split("、") 
            trade.targetPrice = float(dtRow[lstFields_ind["标的价格"]]) 
            trade.targetPrice_Ex = float(dtRow[lstFields_ind["标的价格-期望"]]) 
            trade.targetPosition = float(dtRow[lstFields_ind["标的仓位"]]) 

            trade.infoID = int(dtRow[lstFields_ind["编号"]])
            trade.tradeType = dtRow[lstFields_ind["交易类型"]]
            trade.tradeType_sub = dtRow[lstFields_ind["交易子类型"]]
            trade.tradeNum = float(dtRow[lstFields_ind["交易数量"]])
            trade.tradeMoney = float(dtRow[lstFields_ind["交易金额"]])
            trade.tradePosition = float(dtRow[lstFields_ind["交易量仓位占比"]])
            trade.tradeProfit = float(dtRow[lstFields_ind["交易收益"]])
            trade.tradeProfit_total = float(dtRow[lstFields_ind["交易收益-总计"]])
            trade.tradeTime = myData_Trans.Tran_ToDatetime(dtRow[lstFields_ind["交易时间"]])

            trade.isDel = myData.iif(dtRow[lstFields_ind["是否删除"]] == "TRUE", True, False)
            trade.remark = dtRow[lstFields_ind["备注"]] 
            self.usrDB[trade.infoID] = trade
            self.indLst.append(trade.infoID)     # 顺序记录索引
        self.dtDB = dtDB
             
    #添加交易记录
    def Add(self, usrID, targetID, targetPrice, tradePosition, usrOrderType = "", tradeType = "", tradeType_sub = "", targetName = "", targetPosition = 0, targetPrice_Ex = 0, tradeNum = 0, tradeMoney = 0, tradeProfit = 0, tradeProfit_total = 0, tradeTime = "", remark = "", recorder = ""): 
       trade = myObj_Trade()
       if(trade.Init(usrID, targetID, targetPrice, tradePosition, usrOrderType, tradeType, tradeType_sub, targetName, targetPosition, targetPrice_Ex, tradeNum, tradeMoney, tradeProfit, tradeProfit_total, tradeTime, remark, recorder)):
        return self._Add(trade)
        return False
    def Add_ByDict(self, tradeInfo = {}): 
       trade = myObj_Trade()
       trade.Init_ByDict(tradeInfo)
       return self._Add(trade)
    def _Add(self, trade, bCheck = True): 
        if(trade.usrID == "" or trade.targetID == ""):
            return "用户名或标的信息输入不全。"
        if(self._Check(trade) == False): return "信息已经存在。"
        
        #添加(记录索引)
        trade.infoID = self._Get_ID()
        self.usrDB[trade.infoID] = trade 
        if(trade.recordTime == "" or trade.recordTime == None):
            trade.recordTime = datetime.datetime.now()
          
        #校正存量
        bAppend = True 
            
        #取ID号(usrTime排序)
        nID = self._Find_ind(trade.tradeTime)
        if(nID < len(self.indLst)):                 #索引最后一个序号
            bAppend = False 
        self.indLst.insert(nID, trade.infoID)       #记录索引
        
        
        #保存--排序
        if(bAppend == False or len(self.usrDB) == 1):
            self.Save_DB()
        else:
            self.dtDB.Save_csv_append(self.pathData, trade.ToList(), True, row_end = len(self.usrDB)-1 )   
        return "添加成功，账单信息如下：\n" + trade.ToTitlestr(4)
     
    #查询
    #def Query(self, startTime = '', endTime = '', nMonth = 1, tradeParty = '', usrTradeType = "", tradeTarget = "", tradeType = "", tradeTypeTarget = "", exceptDeault = False, exceptTradeTypes = [], exceptTradeTypes = [], bNoRelation = False):
    
    #查找
    def _Find_ind(self, usrTime, bIn = False): 
        #取ID号(usrTime排序)
        nID = len(self.indLst) - 1                      #索引最后一个序号
        if(nID >= 0):
            trade_Last = self._Find(self.indLst[nID])    #索引依次往前-usrTime排序
            if(bIn == False):
                while(nID >= 0 and trade_Last != None and trade_Last.tradeTime > usrTime):
                    nID -= 1
                    trade_Last = self._Find(self.indLst[nID])
            else:
                while(nID >= 0 and trade_Last != None and trade_Last.tradeTime >= usrTime):
                    nID -= 1
                    trade_Last = self._Find(self.indLst[nID])
        return nID + 1
    def _Find(self, id): 
        return self.usrDB.get(id, None)
    def _Get_ID(self):
        if(len(self.usrDB) == 0): return 1
        return len(self.usrDB) + 1

    #检查是否已经存在   
    def _Check(self, trade): 
        keys = self.usrDB.keys()
        for x in keys:
            tradeTemp = self.usrDB[x]
            if(trade.IsSame(tradeTemp, 1000)): 
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
    def OnCreat_TradeInfo(self): 
        pTrade = myObj_Trade()
        return pTrade.OnCreat_TradeInfo()
    #当前数据进行保存   
    def Save_DB(self):  
        #组装行数据
        self.dtDB.dataMat = []
        for x in self.indLst:
            trade = self._Find(x) 
            self.dtDB.dataMat.append(trade.ToList())

        #保存
        self.dtDB.Save_csv(self.dir, self.usrID, True, 0, 0)



#主启动程序
if __name__ == "__main__":
    #测试交易记录
    zxcTrades = myObj_Trades()

    # 添加
    print(zxcTrades.Add("成功", "sh.600060", 6.6, 0, "看涨"))
    


    print()
