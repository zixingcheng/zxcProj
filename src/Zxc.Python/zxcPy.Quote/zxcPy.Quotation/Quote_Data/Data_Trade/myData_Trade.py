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
        for dtRow in dtDB.dataMat:
            #区分类型，部分类型屏蔽
            strType = dtRow[lstFields_ind["交易类别"]] 
            if(strType.count('买入') == 1 or strType.count('配售缴款') == 1):
                strType = '买入'
            elif(strType.count('卖出') == 1):
                strType = '卖出'
            elif(strType.count('利息归本') == 1):
                strType = '分红'
            else:
                continue

            #解析有效数据内容
            bill = myManager_Bill.myObj_Bill()
            bill.usrID = self.usrID
            bill.usrBillType = strType
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

            #部分特殊类型名称转换
            if(bill.usrBillType == "卖出"):
                if(bill.tradeTarget.count("转债") == 1):
                    bill.tradeTarget = bill.tradeTarget.replace("转债", "发债")
            if(bill.tradeTarget.count("发债") == 1): bill.tradeTypeTarget = "可转债"

            #@@Test  
            if(bill.usrBillType == "卖出" and bill.tradeTarget == "航电发债"):
                aa =1

            #添加账单信息
            strReturn = pBills._Add(bill)
            myDebug.Print(strReturn)
    

#主启动程序
if __name__ == "__main__":
    #对账单转换测试
    pTrade = myData_Trade("张斌")
    pTrade._Init_Trades()

    exit()


    pBills = pManager['Test']

    pBills.Add("门口超市", 10.2, "购物")
    pBills.Add("门口超市", 20.4, "买菜", "2018-8-20")
    pBills.Add("西边菜市场", 10.4, "买菜","2018-8-22")
    pBills.Add("西边菜市场", 10.4, "买菜", "2018-8-23")
    pBills.Add("西边菜市场", 10.4, "买菜", "2018-8-16")
    
    pBills.Add("股票", 1000, "投资", "2018-5-16")
    pBill = pBills.Query("股票", "投资", "", "", 4)
    pBills.Add(str(pBill[0][0].id), 1200, "投资回笼","2018-8-16")
    pBills.Add("老豆", 100, "红包", "2018-8-18")
    pBills.Add("老豆", 100, "红包", "2018-1-18")

    #查询统计测试
    myDebug.Debug(pBills.Static())
    myDebug.Debug(pBills.Static("", "", "", "", 3))
    myDebug.Debug(pBills.Static("", "", "", "", 6))
    myDebug.Debug(pBills.Static("", "", "", "", 12))
    myDebug.Debug(pBills.Static("", "", pBills._Trans_Time_year("", 1), "", 12))

    myDebug.Debug(pBills.Static("", "红包", pBills._Trans_Time_year("", 1), "", 12))
    myDebug.Debug(pBills.Static("老豆", "红包", pBills._Trans_Time_year("", 1), "", 12))
    print()


    #复杂统计
    pBills = pManager['多多']
    myDebug.Debug(pBills.Static("", "", pBills._Trans_Time_year("", 1), "", 0))
    myDebug.Debug(pBills.Static("", "", pBills._Trans_Time_year("", 2), "", 0))
    myDebug.Debug(pBills.Static("", "", pBills._Trans_Time_year("", 3), "", 0))

    myDebug.Debug(pBills.Static_max("", "红包", False, 10, pBills._Trans_Time_year("", 3), "", 0))
    print()
    myDebug.Debug(pBills.Static_max("", "红包", True, 10, pBills._Trans_Time_year("", 3), "", 0))
    print()
    myDebug.Debug(pBills.Static_max("爸爸", "红包", True, 10, pBills._Trans_Time_year("", 3), "", 0))
    

    exit()


    
