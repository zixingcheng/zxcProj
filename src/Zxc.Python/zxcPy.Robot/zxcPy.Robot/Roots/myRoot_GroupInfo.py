#-*- coding: utf-8 -*-
"""
Created on  张斌 2018-06-25 10:58:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com

    机器人-群组对象 
"""
import sys, os, datetime, mySystem

#引用根目录类文件夹--必须，否则非本地目录起动时无法找到自定义类 
mySystem.Append_Us("", False)    
import myIO, myIO_xlsx, myData_Trans

 
#功能权限 群组信息对象
class myRoot_GroupInfo():
    def __init__(self, groupID = "", groupName = "", typeName = ""): 
        self.typeName = typeName    #群组类型
        self.groupName = groupName  #群组名
        self.groupID = groupID      #群组ID  
        self.groupDesc = ""         #群组描述  
        self.groupTime_Regist = datetime.datetime.now()          #注册时间
        self.groupTime_Logined_Last = datetime.datetime.now()    #最后登录时间（请求）
        self.usrInd = -1     
#功能权限 群组信息对象
class myRoot_GroupsInfo():
    def __init__(self, userID, usrName): 
        self.usrName = usrName      #归属用户
        self.usrID_sys = userID     #归属用户ID
        self.groupList = {}         #群组集(按顺序索引)
        self.groupList_Name = {}    #群组集--(按名称索引)
        self.groupList_usrID = {}   #群组集--(按ID索引)

        #初始根目录信息
        strDir, strName = myIO.getPath_ByFile(__file__)
        self.Dir_Base = os.path.abspath(os.path.join(strDir, "../.."))  
        self.Dir_Setting = self.Dir_Base + "/Setting"
        self.Path_SetUser = self.Dir_Setting + "/UserInfo_Group.csv"
        self.lstFields = ["ID","群组名","来源平台","描述","注册时间","最后登录时间"]
        if(userID != "" and usrName != ""):
            self._Init() 
    def _Init(self):            
        #提取字段信息 
        #dtGroup = myIO_xlsx.loadDataTable(self.Path_SetUser, 0, 1)            #用户信息
        dtGroup = myIO_xlsx.DtTable() 
        dtGroup.Load_csv(self.Path_SetUser, 1, 0, isUtf = True)
         
        if(len(dtGroup.dataMat) < 1 or len(dtGroup.dataField) < 1): return
        lstFields_ind = dtGroup.Get_Index_Fields(self.lstFields)

        #转换为功能权限对象集
        for dtRow in dtGroup.dataMat:
            pGroup = myRoot_GroupInfo("", dtRow[lstFields_ind["群组名"]])
            pGroup.groupID = dtRow[lstFields_ind["ID"]]
            pGroup.typeName = dtRow[lstFields_ind["来源平台"]].split('、')
            pGroup.groupDesc = dtRow[lstFields_ind["描述"]]
            pGroup.groupTime_Regist = myData_Trans.Tran_ToDatetime(dtRow[lstFields_ind["注册时间"]])
            pGroup.groupTime_Logined_Last = myData_Trans.Tran_ToDatetime(dtRow[lstFields_ind["最后登录时间"]])
            self._Index(pGroup)      #索引用户信息

    # 添加群组
    def Add_Group(self, groupID, groupName, typeName = "", bUpdata = True): 
        pGroup = self.Find_Group(groupID, groupName)
        if(pGroup != None): 
            if(bUpdata):
                pGroup.groupID = groupID
                pGroup.groupName = groupName
                return pGroup
            else: return None

        pGroup = myRoot_GroupInfo(groupID, groupName, typeName) 
        self._Index(pGroup)
        return pGroup
    # 用户群组
    def _Index(self, pGroup): 
        ind = len(self.groupList.keys()) 
        self.groupList[ind] = pGroup
        pGroup.usrInd = ind        #用户集中的序号

        #用户集--(按名称索引)
        if(pGroup.groupName != ""):
            if(self.groupList_Name.get(pGroup.groupName, None) == None):
                self.groupList_Name[pGroup.groupName] = pGroup
                
        #用户集--(按ID索引)
        if(pGroup.groupID != ""):
            if(self.groupList_usrID.get(pGroup.groupID , None) == None):
                self.groupList_usrID[pGroup.groupID ] = pGroup
    # 移除群组
    def Del_Group(self, groupID, groupName): 
        pGroup = self.Find_Group(groupID, groupName)
        if(pGroup == None): return False
        self.groupList.pop(pGroup.usrInd)
        self.groupList_Name.pop(pGroup.groupName)   # 移除字典项 
        self.groupList_usrID.pop(pGroup.groupID)    # 移除字典项 
        return True
    # 查找群组
    def _Find_Group(self, pGroup):
        return self.Find_Group(pGroup.groupID, pGroup.groupName, pGroup.typeName) 
    def Find_Group(self, groupID = "", groupName = "", typeName = "", bCreate_Auto = False, bAdd = True): 
        #按名称查找
        pGroup = self.groupList_Name.get(groupID, None)
        if(pGroup == None):
            pGroup = self.groupList_Name.get(groupName, None)
        if(pGroup != None): return pGroup
            
        # 不存在
        if(bCreate_Auto):
            pGroup = myRoot_GroupInfo(groupID, groupName, typeName)
            if(bAdd): self._Index(pGroup)
        return pGroup

    
#主启动程序
if __name__ == "__main__":
    pGroups = myRoot_GroupsInfo("zxc", "WxGroup")
    pGroups.Add_Group("@asadafs", "Test")
    pGroups.Add_Group("@001", "test")
    pGroups.Add_Group("", "test2")
    pGroups.Del_Group("@", "test")
    pGroups.Add_Group("@0012", "Test2")
    pGroup = pGroups.Find_Group("", "Test")
    print(pGroup)

    pGroup2 = pGroups.Find_Group("", "Test2")
    print(pGroup2.groupID, pGroup2.groupName, pGroup2.typeName)
