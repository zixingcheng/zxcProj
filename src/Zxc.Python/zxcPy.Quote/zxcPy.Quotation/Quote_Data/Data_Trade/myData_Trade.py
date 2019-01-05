#-*- coding: utf-8 -*-
"""
Created on  张斌 2018-08-24 15:58:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com
    
    管家功能--账单(记录、查询)
"""
import sys, os, time , datetime, mySystem
from operator import itemgetter, attrgetter

#引用根目录类文件夹--必须，否则非本地目录起动时无法找到自定义类
mySystem.Append_Us("../../../../zxcPy.Robot/zxcPy.Robot/Prjs/Base", False, __file__)
mySystem.Append_Us("", False) 
import myIO, myIO_xlsx, myData, myData_Trans, myDebug 
import myManager_Bill

 
#交易信息
class myData_Trade():
    def __init__(self, useID):  
        self.usrID = useID      #用户名
        self.usrTime = ""       #数据日期（月）
        self.remark = ""        #备注
        
        #初始数据路径
        strDir, strName = myIO.getPath_ByFile(__file__)
        self.Dir_Base = os.path.abspath(os.path.join(strDir, "../../.."))  
        self.Dir_DataDB = self.Dir_Base + "/Data/DB_Trade/"

        #初始全局账单管理器
        from myGlobal import gol 
        gol._Init()     #先必须在主模块初始化（只在Main模块需要一次即可）
        gol._Set_Setting('manageBills', myManager_Bill.myManager_Bill(self.Dir_DataDB))     #实例 账单管理器 
        self.billManager = gol._Get_Setting('manageBills', None)
        
    #初始对账单(所有)   
    def _Init_Trades(self): 
        #提取路径下所有文件信息
        strDir = self.Dir_DataDB + "Stock_Bills"
        lstFile = myIO.getFiles(strDir, '.csv', True)

        #循环提取所有
        for x in lstFile:
            self._Init_TradeDB(x)

    #初始对账单   
    def _Init_TradeDB(self, path): 
        #提取字段信息  
        dtDB = myIO_xlsx.DtTable()
        dtDB.Load_csv(path, 5, 0, True, 4, ',', isUtf = False) 

        lstFields = ["交收日期","合同号","资金账号","股东代码","证券代码","证券名称","交易类别","成交价格","成交数量","证券余额","成交金额","资金发生数","资金余额","费用合计","净佣金","规费","印花税","过户费","经手费","清算费","前台费用","交易规费","证管费","币种","交易市场"]
        if(dtDB.sheet == None): dtDB.dataField = lstFields
        lstFields_ind = dtDB.Get_Index_Fields(lstFields)

        #提取交易记录
        pBills = self.billManager._Find("Stock_" + self.usrID, True)    

        #装载账单记录
        nInd = 0
        for nTimes in range(0,1):   
            for dtRow in dtDB.dataMat:
                #解析有效数据内容
                bill = myManager_Bill.myObj_Bill()
                bill.usrID = self.usrID
                bill.recorder = self.usrID

                bill.tradeParty = dtRow[lstFields_ind["交易市场"]] 
                bill.tradeType = "投资"
                bill.tradeTypeTarget = "股票"
                bill.tradeTarget = dtRow[lstFields_ind["证券名称"]] 
                bill.tradePrice = float(dtRow[lstFields_ind["成交价格"]])
                bill.tradeNum = int(dtRow[lstFields_ind["成交数量"]])
                bill.tradeMoney = float(dtRow[lstFields_ind["成交金额"]])
                bill.tradePoundage = float(dtRow[lstFields_ind["费用合计"]]) 
                bill.tradeTime = myData_Trans.Tran_ToDatetime(dtRow[lstFields_ind["交收日期"]], "%Y%m%d") + datetime.timedelta(minutes=nInd)
                nInd = nInd + 1
            
                #区分类型，部分类型屏蔽
                strType = dtRow[lstFields_ind["交易类别"]] 
                if(strType.count('买入') == 1 or strType.count('配售缴款') == 1):
                    bill.usrBillType = '买入'
                elif(strType.count('卖出') == 1):
                    bill.usrBillType = '卖出'
                elif(strType.count('银行转证券') == 1):
                    bill.usrBillType = '转账'
                    bill.tradeTypeTarget = "转入"
                    bill.tradeTarget = "现金"
                    bill.tradeParty = "券商"
                    bill.tradeMoney = float(dtRow[lstFields_ind["资金发生数"]])
                elif(strType.count('证券转银行') == 1):
                    bill.usrBillType = '转账'
                    bill.tradeTypeTarget = "转出"
                    bill.tradeTarget = "现金"
                    bill.tradeParty = "券商"
                    bill.tradeMoney = abs(float(dtRow[lstFields_ind["资金发生数"]]))
                elif(strType.count('融券回购') == 1):
                    bill.usrBillType = '买入'
                    bill.tradeTypeTarget = "国债逆回购"
                elif(strType.count('融券购回') == 1):
                    bill.usrBillType = '卖出'
                    bill.tradeTypeTarget = "国债逆回购"
                    bill.tradeMoney = float(dtRow[lstFields_ind["资金发生数"]])
                elif(strType.count('利息归本') == 1 or strType.count('利息税代扣') == 1):
                    bill.usrBillType = '分红'
                    bill.tradeTypeTarget = "活期"
                    bill.tradeTarget = "利息"
                    bill.tradeParty = "券商"
                    bill.tradeMoney = float(dtRow[lstFields_ind["资金发生数"]])
                elif(strType.count('红利入账') == 1):
                    bill.usrBillType = '分红'
                    if(bill.tradeNum != 0):
                        pass  #价格变动。。
                    bill.tradeMoney = float(dtRow[lstFields_ind["资金发生数"]])
                else:
                    continue

                #部分特殊类型名称转换
                if(bill.usrBillType == "卖出"):
                    if(bill.tradeTarget.count("转债") == 1):
                        bill.tradeTarget = bill.tradeTarget.replace("转债", "发债")
                if(bill.tradeTarget.count("发债") == 1): bill.tradeTypeTarget = "可转债"
                if(bill.tradeTarget.count("发债") == 1): bill.tradeTypeTarget = "可转债"

                #@@Test  
                if(bill.usrBillType == "卖出" and bill.tradeTarget.count("五粮")==1):
                    aa =1

                #添加账单信息
                strReturn = pBills._Add(bill)
                myDebug.Print(strReturn)
    

#主启动程序
if __name__ == "__main__":
    #对账单转换测试
    pTrade = myData_Trade("张斌")
    pTrade._Init_Trades()

    #查询统计
    pBills = pTrade.billManager["Stock_张斌"]
    
    myDebug.Debug(pBills.Static("2007-1-1", "2018-12-31", 0, "", "", "", "", ""))
    myDebug.Debug(pBills.Static("2007-1-1", "2018-12-31", 0, "", "转账", "", "投资", ""))


    exit()



    
