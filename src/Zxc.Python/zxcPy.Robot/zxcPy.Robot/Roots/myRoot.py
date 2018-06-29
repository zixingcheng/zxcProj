#-*- coding: utf-8 -*-
"""
Created on  张斌 2018-06-25 10:58:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com

    机器人-权限对象操作 
"""
import sys, os, mySystem 

#引用根目录类文件夹--必须，否则非本地目录起动时无法找到自定义类
mySystem.Append_Us("/zxcPy.APIs", False, __file__)
mySystem.Append_Us("", False)    
import myRoot_GroupInfo as group


#权限对象操作
class myRoot():
    def __init__(self): 
        self.prjName = ""       #功能名
        self.fileName = ""      #文件名
        self.className = ""     #类名
        self.cmdStr = ""        #启动命令
        self.isNoReply = False  #是否无回复操作--功能自带    
        self.isRoot = False     #是否根标识 ??

        self.isRegisted = False         #是否注册
        self.isEnable = False           #是否启用
        self.isEnable_All = False       #是否统一启用(登陆账户启用，否则单个用户启用)
        self.isEnable_one = False       #一对一有效
        self.isEnable_group = False     #群有效
        self.isEnable_groupAll = False  #群同时有效
        self.goupsEnable = {}           #已启用群集

    def _Init(self, prjName, fileName, className, cmdStr, isEnable, isEnable_All, isEnable_one, isEnable_group, isEnable_groupAll): 
        self.prjName = prjName
        self.fileName = fileName
        self.className = className
        self.cmdStr = cmdStr
        self.isEnable = isEnable
        self.isEnable_All = isEnable_All
        self.isEnable_one = isEnable_one
        self.isEnable_group = isEnable_group
        self.isEnable_groupAll = isEnable_groupAll

    #命令权限检查
    def IsEnable(self): return self.isEnable; 
    def IsEnable_All(self): return self.IsEnable() and self.isEnable_All; 
    def IsEnable_one(self): return self.IsEnable() and self.isEnable_one; 	
    def IsEnable_group(self): return self.IsEnable() and self.isEnable_group; 
    def IsEnable_groupAll(self): 
        return self.IsEnable_group() and self.isEnable_groupAll; 		 

#权限对象信息(单人)
class myRoot_Info():
    def __init__(self, usrName, userID): 
        self.usrName = usrName  #用户名
        self.userID = userID    #用户名
        self.prjRoots = {}      #功能权限集
        self.prjCmds = {}       #功能命令集
        # self.prjRoots_user = {} #功能权限用户集
          
         


#主启动程序
if __name__ == "__main__":
    pData = Data_Stock()
    pData.Print()
