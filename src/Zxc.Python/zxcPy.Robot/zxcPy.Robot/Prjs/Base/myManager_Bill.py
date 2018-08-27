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
mySystem.Append_Us("../Prjs", False, __file__)
mySystem.Append_Us("", False) 
import myEnum, myIO, myIO_xlsx, myData, myData_Trans, myDebug 


#定义账单类型枚举
myBillType = myEnum.enum('购物', '买菜', '买衣服', '投资', '红包', '投资回笼')

#账单对象
class myObj_Bill():
    def __init__(self): 
        self.id = -1            #编号
        self.usrID = ""         #用户名
        self.usrMoney = 0       #金额
        self.usrSrc = ""        #来源（交易人或单位）
        self.usrBillType = ""   #账单类型
        self.usrTime = None     #发生时间
        self.recordTime = None  #记录时间
        self.isDel = False      #是否已删除
        self.remark = ""        #备注
    def Init(self, usrID, usrSrc, usrMoney, usrBillType = "", dateTime = "", remark = "", recordTime = datetime.datetime.now()): 
        self.usrID = usrID 
        self.usrSrc = usrSrc 
        self.usrBillType = usrBillType
        self.usrTime = myData.iif(dateTime == "", datetime.datetime.now(), dateTime)
        if(type(self.usrTime) == str): self.usrTime =  myData_Trans.Tran_ToDatetime(dateTime, "%Y-%m-%d")
        self.recordTime = recordTime
        self.remark = remark

        #收支判断
        if(self.IsInCome()):
            self.usrMoney = usrMoney
        else:
            self.usrMoney = usrMoney * -1
    def ToList(self): 
        lstValue = [self.recordTime.strftime('%Y-%m-%d %H:%M:%S'), self.id, self.usrBillType, self.usrMoney, self.usrSrc, self.usrTime.strftime("%Y-%m-%d"), self.isDel, self.remark]
        return lstValue
    def ToString(self, nSpace = 0, isSimple = False): 
        if(isSimple == False):
            strSpace = " " * nSpace
            strBill = strSpace + "编号: " + str(self.id) + "\n"
            strBill += strSpace + "账单人: " + self.usrID + "\n"
            strBill += strSpace + "账单金额: " + str(round(self.usrMoney, 2)) + "元 \n"
            if(self.usrMoney > 0):
                if(self.usrBillType == myBillType.投资回笼):
                    strBill += strSpace + "收入来源: 投资回笼，投资账单编号（" + str(self.usrSrc) + "）\n"
                else:
                    strBill += strSpace + "收入来源: " + self.usrSrc + "\n"
            else:
                strBill += strSpace + "支出目标: " + self.usrSrc + "\n"
            strBill += strSpace + "账单类型: " + self.usrBillType + "\n"
            strBill += strSpace + "账单时间: " + myData_Trans.Tran_ToDatetime_str(self.usrTime, "%Y-%m-%d") + "\n"
            strBill += strSpace + "备注: " + self.remark 
        else:
            strBill = self.usrSrc
            strBill += "，" + str(round(self.usrMoney, 2)) + "元"
            strBill += "，" + self.usrBillType
            strBill += "，" + str(self.id) 
            strBill += "，" + myData_Trans.Tran_ToDatetime_str(self.usrTime, "%Y-%m-%d") 
        return strBill
    def ToString2(self, nSpace = 0): 
        strSpace = " " * nSpace
        strBill = strSpace + "编号: " + str(self.id) + "\n"
        strBill += strSpace + "红包归属: " + self.usrID + "\n"
        strBill += strSpace + "红包金额: " + str(self.usrMoney) + "元 \n"
        strBill += strSpace + "红包来源: " + self.usrSrc + "\n"
        strBill += strSpace + "红包事由: " + self.usrBillType + "\n"
        strBill += strSpace + "红包时间: " + myData_Trans.Tran_ToDatetime_str(self.usrTime, "%Y-%m-%d") + "\n"
        strBill += strSpace + "备注: " + self.remark 
        return strBill
    #是否收入（是为正支出为负）
    def IsInCome(self): 
        if(self.usrBillType == myBillType.红包 or self.usrBillType == myBillType.投资回笼):
            return True
        return False
    def IsSame(self, bill, days = 3): 
        if(bill.usrBillType == self.usrBillType):
            if(abs((bill.usrTime - self.usrTime).days) < days):    #7天内算相同
                if(self.usrSrc == bill.usrSrc): 
                    if(self.isDel == bill.isDel):
                        return True
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
        dtDB.Load_csv(path, 1, 0, True, 0, ',')

        lstFields = ["记录时间","编号","账单分类","账单金额","账单来源","账单时间","是否删除","备注"]
        if(dtDB.sheet == None): dtDB.dataField = lstFields
        lstFields_ind = dtDB.Get_Index_Fields(lstFields)
        self.lstFields = lstFields
        self.pathData = path

        #装载账单记录
        self.usrDB = {} 
        self.indLst = []
        for dtRow in dtDB.dataMat:
            bill = myObj_Bill()
            bill.id = int(dtRow[lstFields_ind["编号"]])
            bill.usrID = self.usrID
            bill.usrMoney = float(dtRow[lstFields_ind["账单金额"]])
            bill.usrSrc = dtRow[lstFields_ind["账单来源"]] 
            bill.usrBillType = dtRow[lstFields_ind["账单分类"]]
            bill.usrTime = myData_Trans.Tran_ToDatetime(dtRow[lstFields_ind["账单时间"]], "%Y-%m-%d")
            bill.recordTime = myData_Trans.Tran_ToDatetime(dtRow[lstFields_ind["记录时间"]])
            bill.remark = dtRow[lstFields_ind["备注"]]
            bill.isDel = myData.iif(dtRow[lstFields_ind["是否删除"]] == True, True, False) 
            self.usrDB[bill.id] = bill
            self.indLst.append(bill.id)     # 顺序记录索引
        self.dtDB = dtDB
             
    #添加账单记录
    def Add(self, usrSrc, usrMoney, usrBillType = "", remark = "", dateTime = ""): 
       bill = myObj_Bill()
       bill.Init(self.usrID, usrSrc, usrMoney, usrBillType, dateTime, remark, datetime.datetime.now())
       return self._Add(bill)
    def _Add(self, bill): 
        if(bill.usrID == "" or bill.usrMoney == 0 or bill.usrSrc == ""):
            return "用户名、账单金额、账单来源，输入不全。"
        if(self._Check(bill) == False): return "账单信息已经存在。"
        
        #添加(记录索引)
        bill.id = len(self.usrDB) + 1
        self.usrDB[bill.id] = bill 

        #取ID号(usrTime排序)
        bAppend = True
        nID = self._Find_ind(bill.usrTime)
        if(nID != len(self.indLst) - 1):        #索引最后一个序号
            bAppend = False 
        self.indLst.insert(nID, bill.id)        # 记录索引

        #保存--排序
        bill_Last = self._Find(bill.id - 1)
        if(bAppend == False):
            self.Save_DB()
        else:
            self.dtDB.Save_csv_append(self.pathData, bill.ToList())   
        return "添加成功，账单信息如下：\n" + bill.ToString(4)
    
    #查询、统计
    def Query(self, usrSrc = '', usrBillType = "", startTime = '', endTime = '', nMonth = 1): 
        #查询参数校正
        if(type(startTime) != datetime.datetime): startTime = self._Trans_Time_moth(datetime.datetime.now(), nMonth) 
        if(type(endTime) != datetime.datetime): endTime = datetime.datetime.now()

        #循环查询
        lstBill = []
        ind_S = self._Find_ind(startTime)
        ind_E = self._Find_ind(endTime)
        for x in range(ind_S, ind_E):
            bill = self._Find(self.indLst[x])   
            if(bill.isDel): continue     
            if(usrSrc != "" and usrSrc != bill.usrSrc): continue
            if(usrBillType != "" and usrBillType != bill.usrBillType): continue
            lstBill.append(bill)
        return lstBill, startTime, endTime 
    def Static(self, usrSrc = '', usrBillType = "", startTime = '', endTime = '', nMonth = 1): 
        lstBill, startTime, endTime  = self.Query(usrSrc, usrBillType, startTime, endTime, nMonth)
        
        #统计项目初始
        lstSum = {}
        for x in myBillType: lstSum[x] = 0

        #统计
        dSum_Out = 0 
        dSum_Out_投资 = 0 
        dSum_In_投资 = 0 
        dSum_In = 0 
        for x in lstBill:
            if(x.usrBillType == myBillType.投资回笼):       #投资收益单独计算
                bill = self._Find(int(x.usrSrc))            #查找投资编号,计算收益
                lstSum[x.usrBillType] += x.usrMoney + bill.usrMoney
                dSum_In_投资 += bill.usrMoney               #投资已回收项  
                if(startTime > bill.usrTime):              #投资在当前时间前，累加投资项，否则计算有误
                    lstSum[myBillType.投资] += bill.usrMoney
            else:
                lstSum[x.usrBillType] += x.usrMoney
                
        keys = lstSum.keys()
        for x in keys:
            dSum = lstSum[x]
            if(dSum > 0): dSum_In += dSum
            elif(dSum < 0): dSum_Out += dSum
        dSum_Out -= lstSum[myBillType.投资]       #剔除投资(投资记负但非消费)
        dSum_Out_投资 = lstSum[myBillType.投资] - dSum_In_投资
        
        #输出信息
        strPerfix = "\n" + " " * 4
        strOut = "账单统计(" + self.usrID + ")："
        strOut += "\n" + "总资产：" + str(round(dSum_Out + dSum_In, 2)) + "元"
        if(lstSum[myBillType.红包] > 0):
            strOut += strPerfix + "红包收入：" + str(round(lstSum[myBillType.红包], 2)) + "元"
        if(lstSum[myBillType.投资回笼] > 0):
            strOut += strPerfix + "投资收益：" + str(round(lstSum[myBillType.投资回笼], 2)) + "元"
            if(dSum_In_投资 < 0):
                strOut += strPerfix + "    " + "投资回笼：" + str(round(-dSum_In_投资, 2)) + "元"

        if(dSum_Out_投资 < 0):
            strOut += strPerfix + "投资总计：" + str(-round(dSum_Out_投资, 2)) + "元"
        if(dSum_Out < 0):
            strOut += strPerfix + "消费总计：" + str(round(-dSum_Out, 2)) + "元"
            #消费细分：
            for x in keys:
                if(lstSum[x] < 0 and x != myBillType.投资):
                    strOut += strPerfix + "    " + x +"：" + str(round(-lstSum[x], 2)) + "元"
        strOut += "\n账单时间：" + myData_Trans.Tran_ToDatetime_str(startTime, "%Y-%m-%d") + " 至 " + myData_Trans.Tran_ToDatetime_str(endTime, "%Y-%m-%d") 
        if(usrBillType != ""): 
            strOut += "\n账单分类：" + usrBillType      
        if(usrSrc != ""): 
            strOut += "\n账单来源：" + usrSrc
        return strOut

  
    def Static_max(self, usrSrc = '', usrBillType = "", bSum = False, nTop = 10, startTime = '', endTime = '', nMonth = 1): 
        lstBill, startTime, endTime  = self.Query(usrSrc, usrBillType, startTime, endTime, nMonth)

        #统计         
        if(usrSrc != ""): bSum = False
        if(bSum == False):      #最大金额统计
            lstValues = sorted(lstBill, key=lambda myObj_Bill: myObj_Bill.usrMoney, reverse=True)   # sort by usrMoney
        else:                   #累计统计
            dictSum = {}
            dictTimes = {}
            lstStatics = []
            for x in lstBill:
                if(x.usrSrc == "未记名"): continue
                dSum = dictSum.get(x.usrSrc, 0)  
                dSum += x.usrMoney
                dictSum[x.usrSrc] = dSum
                dictTimes[x.usrSrc] = dictTimes.get(x.usrSrc, 0) + 1

            keys = dictSum.keys()
            for x in keys:
                lstStatics.append((x, dictSum[x], dictTimes[x]))
            lstValues = sorted(lstStatics, key=itemgetter(1), reverse=True)   # sort by usrMoney

        #输出
        ind = 0
        strPerfix = "\n" + " " * 4
        strOut = myData.iif(bSum, "累计最高", "单次最高") + "(Top" + str(nTop) + ")" 
        strOut += strPerfix + "排名，来源，金额，类型，编号，时间"
        for x in range(0, len(lstValues)):
            bill = lstValues[x]
            strTop = "Top " + str(ind + 1) + "："
            if(bSum == False):
                if(bill.usrSrc == "未记名"): continue
                strOut += strPerfix + strTop + bill.ToString(0, True)
            else:
                strOut += strPerfix + strTop + bill[0] + "，" + str(round(bill[1], 2)) + "元，" + str(bill[2]) + "次"
            ind += 1
            if(ind >= nTop): break 
        strOut += "\n账单时间：" + myData_Trans.Tran_ToDatetime_str(startTime, "%Y-%m-%d") + " 至 " + myData_Trans.Tran_ToDatetime_str(endTime, "%Y-%m-%d") 
        if(usrBillType != ""): 
            strOut += "\n账单分类：" + usrBillType      
        if(usrSrc != ""): 
            strOut += "\n账单来源：" + usrSrc
        return strOut
    
    #查找
    def _Find_ind(self, usrTime): 
        #取ID号(usrTime排序)
        nID = len(self.indLst) - 1                      #索引最后一个序号
        if(nID >= 0):
            bill_Last = self._Find(self.indLst[nID])    #索引依次往前-usrTime排序
            while(nID >= 0 and bill_Last != None and bill_Last.usrTime > usrTime):
                nID -= 1
                bill_Last = self._Find(self.indLst[nID])
        return nID + 1
    def _Find(self, id): 
        return self.usrDB.get(id, None)

    #检查是否已经存在   
    def _Check(self, bill): 
        keys = self.usrDB.keys()
        for x in keys:
            billTemp = self.usrDB[x]
            if(bill.IsSame(billTemp)): return False
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

    #当前数据进行保存   
    def Save_DB(self):  
        #组装行数据
        self.dtDB.dataMat = []
        for x in self.indLst:
            bill = self._Find(x) 
            self.dtDB.dataMat.append(bill.ToList())

        #保存
        self.dtDB.Save_csv(self.dir, self.usrID, False, 0, 0)
        
#管家功能--账单
class myManager_Bill():
    def __init__(self, dir = ""): 
        #初始根目录信息
        if(dir == ""):
            strDir, strName = myIO.getPath_ByFile(__file__)
            self.Dir_Base = os.path.abspath(os.path.join(strDir, "../../.."))  
            self.Dir_DataDB = self.Dir_Base + "/Data/DB_Bill/"
            myIO.mkdir(self.Dir_DataDB, False)
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

    pBills.Add("门口超市", 10.2, "购物")
    pBills.Add("门口超市", 20.4, "买菜", "", "2018-8-20")
    pBills.Add("西边菜市场", 10.4, "买菜", "", "2018-8-22")
    pBills.Add("西边菜市场", 10.4, "买菜", "", "2018-8-23")
    pBills.Add("西边菜市场", 10.4, "买菜", "", "2018-8-16")
    
    pBills.Add("股票", 1000, "投资", "", "2018-5-16")
    pBill = pBills.Query("股票", "投资", "", "", 4)
    pBills.Add(str(pBill[0][0].id), 1200, "投资回笼", "", "2018-8-16")
    pBills.Add("老豆", 100, "红包", "", "2018-8-18")
    pBills.Add("老豆", 100, "红包", "", "2018-1-18")

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


    
