#-*- coding: utf-8 -*-
"""
Created on  张斌 2018-06-25 10:58:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com

    机器人-群组对象 
"""
import sys, os, mySystem 

#引用根目录类文件夹--必须，否则非本地目录起动时无法找到自定义类 
mySystem.Append_Us("", False)    

 
#功能权限 群组信息对象
class myRoot_GroupInfo():
    def __init__(self, groupName, groupID = "", typeName = ""): 
        self.typeName = typeName    #群组类型
        self.groupName = groupName  #群组名
        self.groupID = groupID      #群组ID  
#功能权限 群组信息对象
class myRoot_GroupsInfo():
    def __init__(self, usrName, userID): 
        self.usrName = usrName      #归属用户
        self.usrID_sys = userID     #归属用户ID
        self.groupInfos = {}        #群组对象集

    # 添加群组
    def Add_Group(self, groupName, groupID, typeName = "", bUpdata = True): 
        pGroup = self.Find_Group(groupName, groupID)
        if(pGroup != None): 
            if(bUpdata):
                pGroup.groupID = groupID
                pGroup.groupName = groupName
                return pGroup
            else: return None

        pGroup = myRoot_GroupInfo(groupName, groupID, typeName) 
        self.groupInfos[pGroup.groupName] = pGroup
        return pGroup
    # 移除群组
    def Del_Group(self, groupName, groupID): 
        pGroup = self.Find_Group(groupName, groupID)
        if(pGroup == None): return False
        self.groupInfos.pop(pGroup.groupName)   # 移除字典项 
        return True
    # 查找群组
    def _Find_Group(self, pGroup):
        return Find_Group(pGroup.groupName, pGroup.groupID, pGroup.typeName)
    def Find_Group(self, groupName, groupID = "", typeName = "", bCreate_Auto = False): 
        pGroup = self.groupInfos.get(groupName, None)
        if(pGroup != None): return pGroup
        if(groupID == ""): return pGroup

        #查找ID
        keys = self.groupInfos.keys()
        for x in keys:
            if(self.groupInfos[x].groupID == groupID):
                return self.groupInfos[x]
            
        # 不存在
        if(bCreate_Auto):
            pGroup = myRoot_GroupInfo(groupName, groupID, typeName)
            self.groupInfos[pGroup.groupName] = pGroup
        return pGroup

    
#主启动程序
if __name__ == "__main__":
    pGroups = myRoot_GroupsInfo("WxGroup")
    pGroups.Add_Group("Test", "@asadafs")
    pGroups.Add_Group("test", "@001")
    pGroups.Add_Group("test2", "")
    pGroups.Del_Group("test", "@")
    pGroups.Add_Group("Test2", "@0012")
    pGroup = pGroups.Find_Group("Test")
    print(pGroup)

    pGroup2 = pGroups.Find_Group("Test2")
    print(pGroup2.groupID, pGroup2.groupName, pGroup2.typeName)
