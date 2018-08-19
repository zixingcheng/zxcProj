#-*- coding: utf-8 -*-
"""
Created on  张斌 2018-07-04 15:58:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com
    
    机器人（功能库）  --红包(记录、查询)
"""
import sys, os, time , datetime, mySystem

#引用根目录类文件夹--必须，否则非本地目录起动时无法找到自定义类
mySystem.Append_Us("../Roots", False, __file__)
mySystem.Append_Us("", False) 
import myIO, myIO_xlsx, myData, myData_Trans
import myRoot, myRobot
from myGlobal import gol 


#红包对象
class myObj_gift():
    def __init__(self): 
        self.id = -1            #编号
        self.usrID = ""         #用户名
        self.usrMoney = 0       #红包金额
        self.usrSrc = ""        #红包来源
        self.usrCause = ""      #红包事由
        self.usrTime = None    #红包时间
        self.recordTime = None  #记录时间
        self.idDel = False      #是否已删除
        self.remark = ""        #备注
    def Init(self, usrID, usrMoney, usrSrc, usrCause = "", dateTime = "", remark = "", recordTime = datetime.datetime.now()): 
       self.usrID = usrID 
       self.usrMoney = usrMoney
       self.usrSrc = usrSrc
       self.usrCause = usrCause
       self.usrTime = myData.iif(dateTime == "", datetime.datetime.now(), dateTime)
       self.recordTime = recordTime
       self.remark = remark
    def ToString(self, nSpace = 0): 
        strSpace = " " * nSpace
        strGift = strSpace + "编号: " + str(self.id) + "\n"
        strGift += strSpace + "红包归属: " + self.usrID + "\n"
        strGift += strSpace + "红包金额: " + str(self.usrMoney) + "元 \n"
        strGift += strSpace + "红包来源: " + self.usrSrc + "\n"
        strGift += strSpace + "红包事由: " + self.usrCause + "\n"
        strGift += strSpace + "红包时间: " + myData_Trans.Tran_ToDatetime_str(self.usrTime, "%Y-%m-%d") + "\n"
        strGift += strSpace + "备注: " + self.remark 
        return strGift
#管家功能--红包
class myManager_Gift():
    def __init__(self, usrID, dir = ""): 
        #初始根目录信息
        if(dir == ""):
            strDir, strName = myIO.getPath_ByFile(__file__)
            self.Dir_Base = os.path.abspath(os.path.join(strDir, "../.."))  
            self.Dir_Setting = self.Dir_Base + "/Setting/"
            dir = self.Dir_Setting
        self.pathData = dir + "DB_gift.xls"  
        self.usrID = usrID      #当前红包归属用户
        self.giftDB = None      #红包库(全局缓存)
        self.usrGifts = {}      #当前用户红包信息集
        self.ind_IDs = {}       #当前用户红包ID索引
        self._Init()    #初始参数信息等 
    #初始参数信息等   
    def _Init(self): 
        #检查加载红包库
        if(self.usrID == ""): return False
        self._Init_DB()
        if(self.giftDB != None): return False

        #循环提取当前用户红包集
        self.usrGifts = {}
        self.ind_IDs = {}
        keys = self.giftDB.keys()
        for x in keys:
            gift = self.giftDB[x]
            if(gift.usrID == self.usrID):
                self.usrGifts[x] = gift
                self.ind_IDs[gift.id] = x
        return True
    #初始红包库   
    def _Init_DB(self):  
        #红包库已加载则忽略
        self.giftDB = gol._Get_Value('DB_gift', None)
        if(self.giftDB != None): return 

        #提取字段信息 
        dtDB = myIO_xlsx.loadDataTable(self.pathData, 0, 1)            #红包记录 
        lstFields = ["ID","用户ID","红包金额","红包来源","红包事由","是否删除","红包时间","记录时间","备注"]
        lstFields_ind = dtDB.Get_Index_Fields(lstFields)
        self.lstFields = lstFields

        #装载红包记录
        self.giftDB = {}
        for dtRow in dtDB.dataMat:
            gift = myObj_gift()
            gift.id = int(dtRow[lstFields_ind["ID"]])
            gift.usrID = dtRow[lstFields_ind["用户ID"]]
            gift.usrMoney = float(dtRow[lstFields_ind["红包金额"]])
            gift.usrSrc = dtRow[lstFields_ind["红包来源"]]
            gift.usrCause = dtRow[lstFields_ind["红包事由"]]
            gift.usrTime = dtRow[lstFields_ind["红包时间"]]
            gift.recordTime = dtRow[lstFields_ind["记录时间"]]
            gift.remark = dtRow[lstFields_ind["备注"]]
            gift.idDel = myData.iif(dtRow[lstFields_ind["是否删除"]] == True, True, False)
            self.giftDB[gift.recordTime] = gift
        gol._Set_Value('DB_gift', self.giftDB)
             
    #添加红包记录
    def Add(self, usrMoney, usrSrc, usrCause = "", dateTime = "", remark = ""): 
       gift = myObj_gift()
       gift.Init(self.usrID, usrMoney, usrSrc, usrCause, dateTime, remark)
       return self._Add(gift)
    def _Add(self, gift): 
        if(gift.usrID == "" or gift.usrMoney <= 0 or gift.usrSrc == ""):
            return "用户名、红包金额、红包来源，输入不全。"
        if(self._Check(gift) == False): return "红包信息已经存在。"

        #添加(记录索引)
        gift.id = len(self.giftDB)
        self.giftDB[gift.recordTime] = gift
        self.usrGifts[gift.recordTime] = gift
        self.ind_IDs[gift.id] = gift.recordTime
        return "添加成功，红包信息如下：\n" + gift.ToString(4)
    
    #查询、统计
    def _Find(self, id): 
        ind = self.ind_IDs.get(id, None)
        if(ind == None): return None
        return self.usrGifts[ind]

    #检查是否已经存在   
    def _Check(self, gift): 
        keys = self.usrGifts.keys()
        for x in keys:
            giftTemp = self.usrGifts[x]
            if(giftTemp.usrSrc == gift.usrSrc): 
                if(giftTemp.usrCause == gift.usrCause):
                    if((giftTemp.usrTime - gift.usrTime).day < 7):    #7天内算相同
                        return False
        return True
    
    #当前数据进行保存   
    def Save_DB(self): 
        dtDB = myIO_xlsx.DtTable()    #用户信息表
        dtDB.dataName = "dataName"
        dtDB.dataField = self.lstFields
        dtDB.dataFieldType = ['int', 'string', 'float', 'string', 'string', 'bool', 'datetime', 'datetime', 'string']
       
        # 组装行数据
        #keys = list(self.giftDB.keys())
        #keys.sort(key = None, reverse = True) #字典排序
        keys = self.giftDB.keys()
        for x in keys:
            gift = self.giftDB[x]
            pValues = []
            pValues.append(gift.id)
            pValues.append(gift.usrID)
            pValues.append(gift.usrMoney)
            pValues.append(gift.usrSrc)
            pValues.append(gift.usrCause)
            pValues.append(gift.idDel)
            pValues.append(gift.usrTime.strftime("%Y-%m-%d"))
            pValues.append(gift.recordTime.strftime("%Y-%m-%d %H:%M:%S"))
            pValues.append(gift.remark)
            dtDB.dataMat.append(pValues)

        # 保存
        name = myIO.getFileName(self.pathData)
        dir = self.pathData.split(name)[0]
        dtDB.Save(dir, name, 0, 0, True, "红包记录")

#机器人类----红包(记录、查询)
class myRobot_Repeater(myRobot.myRobot):
    def __init__(self, usrName, usrID):
        super().__init__(usrName, usrID)
        self.doTitle = "复读机"     #说明 
        self.prjName = "复读机"     #功能名
        self.doCmd = "@@Repeater"   #启动命令 
        self.msg['FromUserName'] = self.usrName 

    #消息处理接口
    def _Done(self, Text, msgID = "", msgType = "TEXT", usrInfo = {}):
        #复读机(回复相同消息)
        usrName = usrInfo['usrName']
        return "@" + usrName + " "+ Text 
    def _Title_User_Opened(self): 
        return "发送任何消息均同声回复..."
        

#主启动程序
if __name__ == "__main__":
    #测试红包记录
    pManager = myManager_Gift("zxcID", "")
    print(pManager.Add(100, "老豆", "六一红包"))
    print(pManager.Add(200, "老豆", "十一红包"))
    pManager.Save_DB()

    exit()


    pR = myRobot_Repeater("zxc", "zxcID");
    print(pR.Done("@@Repeater")["Text"])
    print(pR.Done("Hello")["Text"])
    print(pR.Done("@@Repeater")["Text"])

    time.sleep (2)
    print(pR.Done("Hello"))

    pR = myRobot_Repeater("zxc", "zxcID");
    print(pR.Done("@@zxcWeixin")["Text"])
    print(pR.Done("Hello")["Text"])
    print(pR.Done("@@zxcWeixin")["Text"])

    
