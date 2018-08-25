#-*- coding: utf-8 -*-
"""
Created on  张斌 2018-08-24 15:58:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com
    
    管家功能--账单(记录、查询)
"""
import sys, os, time , datetime, mySystem

#引用根目录类文件夹--必须，否则非本地目录起动时无法找到自定义类
mySystem.Append_Us("../Prjs", False, __file__)
mySystem.Append_Us("", False) 
import myEnum, myIO, myIO_xlsx, myData, myData_Trans 


#定义账单类型枚举
myBillType = myEnum.enum('投资', '红包', '买菜', '买衣服', '购物')

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
        self.idDel = False      #是否已删除
        self.remark = ""        #备注
    def Init(self, usrID, usrMoney, usrSrc, usrBillType = "", dateTime = "", remark = "", recordTime = datetime.datetime.now()): 
        self.usrID = usrID 
        self.usrSrc = usrSrc 
        self.usrBillType = usrBillType
        self.usrTime = myData.iif(dateTime == "", datetime.datetime.now(), dateTime)
        if(type(self.usrTime) == str): self.usrTime =  myData_Trans.Tran_ToDatetime(dateTime, "%Y-%m-%d")
        self.recordTime = recordTime
        self.remark = remark

        #收支判断
        if(self.IsInCome):
            self.usrMoney = usrMoney
        else:
            self.usrMoney = usrMoney * -1
    def ToList(self): 
        lstValue = [self.recordTime.strftime('%Y-%m-%d %H:%M:%S'), self.id, self.usrID, self.usrMoney, self.usrBillType, self.usrSrc, self.usrTime.strftime("%Y-%m-%d"), self.idDel, self.remark]
        return lstValue
    def ToString(self, nSpace = 0): 
        strSpace = " " * nSpace
        strBill = strSpace + "编号: " + str(self.id) + "\n"
        strBill += strSpace + "账单人: " + self.usrID + "\n"
        strBill += strSpace + "账单金额: " + str(self.usrMoney) + "元 \n"
        if(self.usrMoney > 0):
            strBill += strSpace + "收入来源: " + self.usrSrc + "\n"
        else:
            strBill += strSpace + "支出目标: " + self.usrSrc + "\n"
        strBill += strSpace + "账单类型: " + self.usrBillType + "\n"
        strBill += strSpace + "账单时间: " + myData_Trans.Tran_ToDatetime_str(self.usrTime, "%Y-%m-%d") + "\n"
        strBill += strSpace + "备注: " + self.remark 
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
        if(self.usrBillType == myBillType.投资 or self.usrBillType == myBillType.投资):
            return True
        return False
    def IsSame(self, bill, days = 3): 
        if(bill.usrBillType == self.usrBillType):
            if(abs((bill.usrTime - self.usrTime).days) < days):    #7天内算相同
                if(self.usrSrc == bill.usrSrc): return True
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

        lstFields = ["记录时间","编号","用户名","账单金额","账单分类","账单来源","账单时间","是否删除","备注"]
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
            bill.usrID = dtRow[lstFields_ind["用户名"]]
            bill.usrMoney = float(dtRow[lstFields_ind["账单金额"]])
            bill.usrSrc = dtRow[lstFields_ind["账单来源"]] 
            bill.usrBillType = dtRow[lstFields_ind["账单分类"]]
            bill.usrTime = myData_Trans.Tran_ToDatetime(dtRow[lstFields_ind["账单时间"]], "%Y-%m-%d")
            bill.recordTime = myData_Trans.Tran_ToDatetime(dtRow[lstFields_ind["记录时间"]])
            bill.remark = dtRow[lstFields_ind["备注"]]
            bill.idDel = myData.iif(dtRow[lstFields_ind["是否删除"]] == True, True, False) 
            self.usrDB[bill.id] = bill
            self.indLst.append(bill.id)     # 顺序记录索引
        self.dtDB = dtDB
             
    #添加账单记录
    def Add(self, usrMoney, usrSrc, usrCause = "", remark = "", dateTime = ""): 
       bill = myObj_Bill()
       bill.Init(self.usrID, usrMoney, usrSrc, usrCause, dateTime, remark, datetime.datetime.now())
       return self._Add(bill)
    def _Add(self, bill): 
        if(bill.usrID == "" or bill.usrMoney <= 0 or bill.usrSrc == ""):
            return "用户名、账单金额、账单来源，输入不全。"
        if(self._Check(bill) == False): return "账单信息已经存在。"
        
        #添加(记录索引)
        bill.id = len(self.usrDB) + 1
        self.usrDB[bill.id] = bill 

        #取ID号(usrTime排序)
        bAppend = True
        nID = len(self.indLst) - 1                      #索引最后一个序号
        if(nID >= 0):
            bill_Last = self._Find(self.indLst[nID])    #索引依次往前-usrTime排序
            while(nID >= 0 and bill_Last != None and bill_Last.usrTime > bill.usrTime):
                nID -= 1
                bill_Last = self._Find(self.indLst[nID])
                bAppend = False
        self.indLst.insert(nID + 1, bill.id)    # 记录索引

        #保存--排序
        bill_Last = self._Find(bill.id - 1)
        if(bAppend == False):
            self.Save_DB()
        else:
            self.dtDB.Save_csv_append(self.pathData, bill.ToList())   
        return "添加成功，账单信息如下：\n" + bill.ToString(4)
    
    #查询、统计
    def _Find(self, id): 
        return self.usrDB.get(id, None)
    #检查是否已经存在   
    def _Check(self, bill): 
        keys = self.usrDB.keys()
        for x in keys:
            billTemp = self.usrDB[x]
            if(bill.IsSame(billTemp)): return False
        return True
    
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
            

#主启动程序
if __name__ == "__main__":
    #测试红包记录
    pManager = myManager_Bill("")
    pBills = pManager['Test']

    pBills.Add(10.2, "门口超市", "购物")
    pBills.Add(20.4, "门口超市", "买菜", "", "2018-8-20")
    pBills.Add(10.4, "西边菜市场", "买菜", "", "2018-8-22")
    pBills.Add(10.4, "西边菜市场", "买菜", "", "2018-8-23")
    pBills.Add(10.4, "西边菜市场", "买菜", "", "2018-8-16")

    exit()


    
