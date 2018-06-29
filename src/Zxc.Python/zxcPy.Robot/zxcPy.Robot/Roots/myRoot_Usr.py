#-*- coding: utf-8 -*-
"""
Created on  张斌 2018-06-25 10:58:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com

    机器人-用户对象 
"""
import sys, os, datetime, mySystem 

#引用根目录类文件夹--必须，否则非本地目录起动时无法找到自定义类
mySystem.Append_Us("", False)    
import myIO, myIO_xlsx, myData_Trans, myRoot


#用户对象
class myRoot_Usr():
    def __init__(self, usrName, usrName_Nick = "", usrID = "", usrRoot = None): 
        self.usrID = ""         #用户ID
        self.usrName = usrName  #用户名
        self.usrName_Nick = ""  #用户名--昵称
        self.usrTag = ""        #标签
        self.usrRamak = ""      #备注
        self.usrPhone = ""      #电话号码
        self.usrNotes = ""      #描述信息
        self.usrTime_Regist = datetime.datetime.now()          #注册时间
        self.usrTime_Logined_Last = datetime.datetime.now()    #最后登录时间（请求）
        self.usrRoot = usrRoot
        self.usrLoaded = False  
        self._Init(usrName_Nick, usrID)
    # 初始用户信息
    def _Init(self, usrName_Nick = "", usrID = ""): 
        self.usrName_Nick = usrName_Nick
        self.usrID = usrID
        return True

#用户对象集
class myRoot_Usrs():
    def __init__(self, usrName, userID): 
        self.usrName = usrName  #归属用户
        self.usrID = userID     #归属用户ID
        self.usrList = {}       #用户集
        self.usrRoot = myRoot.myRoot_Info(usrName, userID)

        #初始根目录信息
        strDir, strName = myIO.getPath_ByFile(__file__)
        self.Dir_Base = os.path.abspath(os.path.join(strDir, "../.."))  
        self.Dir_Setting = self.Dir_Base + "/Setting"
        self.Path_SetUser = self.Dir_Setting + "/UserInfo.xls"
        self.lstFields = ["用户名","用户昵称","用户ID","电话","标签","备注","描述","注册时间","最后登录时间"]
        self._Init()
    #初始参数信息等   
    def _Init(self):            
        dtUser = myIO_xlsx.loadDataTable(self.Path_SetUser, 0, 1)            #用户信息
        
        #提取字段信息 
        lstFields_ind = dtUser.Get_Index_Fields(self.lstFields)

        #转换为功能权限对象集
        for dtRow in dtUser.dataMat:
            pUser = myRoot_Usr(dtRow[lstFields_ind["用户名"]])
            pUser.usrName_Nick = dtRow[lstFields_ind["用户昵称"]]
            pUser.usrID = dtRow[lstFields_ind["用户ID"]]
            pUser.usrPhone = dtRow[lstFields_ind["电话"]]
            pUser.usrTag = dtRow[lstFields_ind["标签"]]
            pUser.usrRamak = dtRow[lstFields_ind["备注"]]
            pUser.usrNotes = dtRow[lstFields_ind["描述"]]
            pUser.usrTime_Regist = myData_Trans.Tran_ToDatetime(dtRow[lstFields_ind["注册时间"]])
            pUser.usrTime_Logined_Last = myData_Trans.Tran_ToDatetime(dtRow[lstFields_ind["最后登录时间"]])
            pUser.usrRoot = self.usrRoot
            pUser.usrLoaded = True  
            self.usrList[pUser.usrName] = pUser
    def _Save(self):            
        dtUser = myIO_xlsx.DtTable()    #用户信息表
        dtUser.dataName = "dataName"
        dtUser.dataField = self.lstFields
        dtUser.dataFieldType = ['string', 'string', 'string', 'string', 'string', 'string', 'string', 'datetime', 'datetime']
       
        # 组装行数据
        keys = self.usrList.keys()
        for x in self.usrList:
            pUser = self.usrList[x]
            pValues = []
            pValues.append(pUser.usrName)
            pValues.append(pUser.usrName_Nick)
            pValues.append(pUser.usrID)
            pValues.append(pUser.usrPhone)
            pValues.append(pUser.usrTag)
            pValues.append(pUser.usrRamak)
            pValues.append(pUser.usrNotes)
            pValues.append(pUser.usrTime_Regist.strftime("%Y-%m-%d %H:%M:%S"))
            pValues.append(pUser.usrTime_Logined_Last.strftime("%Y-%m-%d %H:%M:%S"))
            dtUser.dataMat.append(pValues)

        # 保存
        dtUser.Save(self.Dir_Setting,  "UserInfo", 0, 0, True, "用户信息表")

    #查找 
    def _Find(self, usrName, usrName_Nick, usrID, bCreate_Auto = False): 
        usrName = usrName.strip().lower()
        if(usrName != ""):
            pUsr = self.usrList.get(usrName)   
            if(pUsr != None): 
                self._Refresh(pUsr) # 信息更新
                return pUsr

        #查找
        pUser = None
        usrName_Nick = usrName_Nick.strip().lower()
        usrID = usrID.strip().lower()
        keys = self.usrList.keys()
        for x in keys:
            pUser = self.usrList[x]
            if(usrName != ""):
                if(pUser.usrName == usrName):
                    break
            elif(usrName_Nick != ""):
                if(pUser.usrName_Nick == usrName_Nick):
                    break
            elif(usrID != ""):
                if(pUser.usrID == usrID):
                    break
        
        # 不存在
        if(bCreate_Auto):
            pUser = myRoot_Usr(usrName, usrName_Nick, usrID, self.usrRoot)
            if(self._Add(pUser) == False): return None

        # 信息更新, 并返回
        self._Refresh(pUser)
        return pUser
    # 添加用户
    def _Add(self, pUser): 
        if(pUser == None): return False
        if(pUser.usrName == ""): 
            pUser.usrName = pUser.usrName_Nick

        # 不存在才可添加    
        if(self.usrList.get(pUser.usrName, None) == None):
            self.usrList[pUser.usrName] = pUser
            return True
        return False 
    # 刷新更新部分信息
    def _Refresh(self, pUser): 
        # 信息更新
        if(pUser != None):
            pUser.usrTime_Logined_Last = datetime.datetime.now()
    
    # 用户是否存在
    def IsExist(self, usrName, usrName_Nick, usrID): 
        pUser = self._Find(usrName, usrName_Nick, usrID, False) 
        if(pUser == None): return False
        return True
    # 添加用户
    def Add(self, msgInfo = {}, canUpdata = False): 
        usrName = msgInfo.get("usrName", "")
        usrName_Nick = msgInfo.get("usrName_Nick", "")
        usrID = msgInfo.get("usrID", "")
        if(usrName == None): return False

        # 新用户
        pUser = self._Find(usrName, usrName_Nick, usrID, True)
        if(pUser.usrLoaded and canUpdata == False): return False

        # 信息更新
        pUser.usrPhone = msgInfo.get("usrPhone", "")  
        pUser.usrTag = msgInfo.get("usrTag", "")  
        pUser.usrRamak = msgInfo.get("usrRamak", "")  
        pUser.usrNotes = msgInfo.get("usrNotes", "")  
        return True
    # 添加用户
    def Del(self, usrName): 
        usrName = usrName.strip().lower()
        pUser = self._Find(usrName, usrName, usrName, False) 
        if(pUser == None): return False
        return self.usrList.pop(pUser.usrName)
    

#主启动程序
if __name__ == "__main__":
    pUsers = myRoot_Usrs("zxcPy", "@@zxcPy")
    pUser = pUsers.Add({'usrName': "Test",'usrName_Nick': "测试",'usrID': "@@1" })
    pUser = pUsers.Add({'usrName': "Test3",'usrName_Nick': "测试3",'usrID': "@@3" })
    pUsers.Del("测试3")

    pUsers._Save()
    print(pUser)
