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
    def __init__(self): 
        self.typeName = ""      #群组类型
        self.groupName = ""     #群组名
        self.groupID = ""       #群组ID  

#功能权限 群组信息对象
class myRoot_GroupsInfo():
    def __init__(self, typeName): 
        self.typeName = typeName.lower()    #群组类型
        self.groupInfos = {}                #群组对象集

    # 添加群组
    def Add_Group(self, groupName, groupID): 
        pGroup = self.Find_Group(groupName, groupID)
        if(pGroup != None): return False

        pGroup = myRoot_GroupInfo() 
        pGroup.typeName = self.typeName
        pGroup.groupName = groupName.lower()
        pGroup.groupID = groupID.lower() 
        self.groupInfos[pGroup.groupName] = pGroup
    # 移除群组
    def Del_Group(self, groupName, groupID): 
        pGroup = self.Find_Group(groupName, groupID)
        if(pGroup == None): return False
        self.groupInfos.pop(pGroup.groupName)   # 移除字典项 
        
    # 查找群组
    def Find_Group(self, groupName, groupID = ""): 
        pGroup = self.groupInfos.get(groupName.lower(), None)
        if(pGroup != None): return pGroup
        groupID = groupID.strip().lower()
        if(groupID == ""): return pGroup

        #查找ID
        keys = self.groupInfos.keys()
        for x in keys:
            if(self.groupInfos[x].groupID == groupID):
                return self.groupInfos[x]
        return pGroup

    
#主启动程序
if __name__ == "__main__":
    pGroups = myRoot_GroupsInfo("Wx")
    pGroups.Add_Group("Test", "@asadafs")
    pGroups.Add_Group("test", "@")
    pGroups.Add_Group("test2", "")
    pGroups.Del_Group("test", "@")
    pGroup = pGroups.Find_Group("Test")

    print(pGroup)
