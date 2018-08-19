#-*- coding: utf-8 -*-
"""
Created on  张斌 2018-06-25 10:58:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com

    机器人-功能权限对象 
"""
import sys, os, datetime, mySystem 

#引用根目录类文件夹--必须，否则非本地目录起动时无法找到自定义类
mySystem.Append_Us("../Prjs", False, __file__)
mySystem.Append_Us("", False)    
import myIO, myIO_xlsx, myData, myImport
import myRoot_Usr, myRoot_GroupInfo, myRobot_Log
import myRoot_GroupInfo as group
from myGlobal import gol 


#功能权限对象
class myRoot_Prj():
    def __init__(self): 
        self.prjName = ""       #功能名
        self.prjClass = None    #功能对象实例
        self.fileName = ""      #文件名
        self.className = ""     #类名
        self.cmdStr = ""        #启动命令
        self.isRoot = False     #是否系统权限
        
        self.isRunSingle = False        #是否为单例使用(单例时每个用户专属) 
        self.isRunBack = False          #是否为后台运行(后台可运行多个，一般为系统级功能，如日志)  
        self.isRunning = False          #是否运行中（允许中非统一启用，全员有权限）
        self.isEnable = False           #是否可启用
        self.isEnable_All = False       #是否统一启用(登陆账户启用，否则单个用户启用)
        self.isEnable_one = False       #一对一有效
        self.isEnable_group = False     #群有效
        self.isEnable_groupAll = False  #群同时有效
        self.rootUsers = myRoot_Usr.myRoot_Usrs("", "")                 #根权限用户集
        self.rootUsers_up = myRoot_Usr.myRoot_Usrs("", "")              #提升权限用户集
        self.rootGroups = myRoot_GroupInfo.myRoot_GroupsInfo("", "")    #已启用群集
        self.plantsEnable = []          #平台列表
        self.registedUsrs = []          #当前授权功能开启用户
        self.registedGroups = []        #当前授权功能开启的群
        self.startUser = ""             #功能开启用户
        self.isNoOwner = False    #功能处理对启用者无效
        #self.infoLogs = {}              #日志消息
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
    #def Log(self, usrName, usrInfo):  
    #    self.infoLogs[datetime.datetime.now] = usrName + "::" + usrInfo
    #实例功能对象
    def creatIntance(self, usrName, usrID):      
        self.prjClass = myImport.Import_Class(self.fileName, self.className)(usrName, usrID)
        self.isRoot = self.prjClass.isRootUse           #是否为系统级使用(系统内置功能) 
        self.isRunSingle = self.prjClass.isSingleUse    #是否为单例使用(单例时每个用户专属) 
        self.isRunBack = self.prjClass.isBackUse        #是否为后台使用(后台可运行多个，一般为系统级功能，如日志)  
        self.isNoOwner = self.prjClass.isNoOwner        #是否为所有者除外不回复
        return self.prjClass
    #功能用户注册
    def registUser(self, usrID, usrName, nickName, groupInfo = None, nameSelf = ""):   
        #检查用户是否已经注册
        if(groupInfo == None):
            if(usrName != "" and (usrName in self.registedUsrs) == False):
                self.registedUsrs.append(usrName)
            if(nickName != "" and (nickName in self.registedUsrs) == False):
                self.registedUsrs.append(nickName)
        else:
            if(groupInfo.groupName != "" and (groupInfo.groupName in self.registedGroups) == False):
                self.registedGroups.append(groupInfo.groupName)
            if(groupInfo.groupID != "" and (groupInfo.groupID in self.registedGroups) == False):
                self.registedGroups.append(groupInfo.groupID)
        return True 
    def registoutUser(self, usrID, usrName, nickName, groupInfo = None, nameSelf = ""):   
        #检查用户是否已经注册
        if(groupInfo == None):
            if(usrName != "" and (usrName in self.registedUsrs)):
                self.registedUsrs.remove(usrName)
            if(nickName != "" and (nickName in self.registedUsrs)):
                self.registedUsrs.remove(nickName)
        else:
            if(groupInfo.groupName != "" and (groupInfo.groupName in self.registedGroups)):
                self.registedGroups.remove(groupInfo.groupName)
            if(groupInfo.groupID != "" and (groupInfo.groupID in self.registedGroups)):
                self.registedGroups.remove(groupInfo.groupID)
        return True 
    
    #功能开启与关闭
    def Start(self, usrID, usrName, nickName):  
        self.startUser = usrName
    def Close(self):  
        self.startUser = ""

    #命令权限检查
    def IsRoot_user(self, usr):  
        if(self.rootUsers._Find(usr.usrID, usr.usrName, usr.usrName_Nick, "") != None):
            return True
        return (self.rootUsers_up._Find(usr.usrID, usr.usrName, usr.usrName_Nick, "") != None)
    def IsRunning(self): return self.isRunning; 
    def IsRunSingle(self): return self.isRunSingle; 
    def IsEnable(self): return self.isEnable; 
    def IsEnable_All(self): return self.IsEnable() and self.isEnable_All; 
    def IsEnable_one(self): return self.IsEnable() and self.isEnable_one; 	 
    def IsEnable_group(self, pGroup): 
        if(self.IsEnable_groupAll()): return True
        if(self.IsEnable() and self.isEnable_group):
            if(len(self.rootGroups.groupInfos) < 1): return True        #未设置群则全部有效
            pGroup = self.rootGroups._Find_Group(pGroup)
            if(pGroup != None): return True
        return False
    def IsEnable_groupAll(self): return self.IsEnable() and self.isEnable_group and self.isEnable_groupAll;
    def IsRegist_user(self, usrName, nickName, pGroup): 
        #用户是否已经注册（单一注册）
        if(pGroup != None): return self.IsRegist_group(pGroup)
        if(usrName in self.registedUsrs): return True
        if(nickName in self.registedUsrs): return True
        if(self.isRunBack == True):         #后台运行默认为已注册
            return True
        if(self.startUser == usrName or self.startUser == nickName):    #当前用户为启动用户    
            return True
        return False
    def IsRegist_group(self, pGroup): 
        if(self.IsEnable_group(pGroup) == False): return False
        #用户是否已经注册（单一注册）
        if(pGroup.groupID in self.registedGroups): return True
        if(pGroup.groupName in self.registedGroups): return True
        if(self.isRunBack == True):         #后台运行默认为已注册
            return True
        return False
    def IsEnable_plant(self, plantName): 
        if(plantName == ""):
            return self.IsEnable(); 	
        else:
            return self.IsEnable() and (plantName in self.plantsEnable); 	 
#功能权限集对象
class myRoots_Prj():
    def __init__(self, usrName, usrID, bgetGol = True): 
        self.usrName = usrName  #用户名
        self.usrID = usrID      #用户名
        self.prjRoots = {}      #功能权限集
        self.prjCmds = {}       #功能命令集
        self.hasGol = bgetGol   #由全局提取
        # self.prjRoots_user = {} #功能权限用户集
        
        #初始根目录信息
        strDir, strName = myIO.getPath_ByFile(__file__)
        self.Dir_Base = os.path.abspath(os.path.join(strDir, "../.."))  
        self.Dir_Setting = self.Dir_Base + "/Setting/"
        self.Dir_Data = self.Dir_Base + "/Data/"
        self._Init()    #初始参数信息等 
    #初始参数信息等   
    def _Init(self):            
        dtSetting = myIO_xlsx.loadDataTable(self.Dir_Setting + "Setting.xlsx", 0, 1)            #外部参数设置 
        dtSetting_user = myIO_xlsx.loadDataTable(self.Dir_Setting + "Setting_User.xlsx", 0, 1)  #外部参数设置-权限用户 
        
        #提取字段信息 
        lstFields = ["功能名称","文件名","类名","启动命令","统一启用","是否启用","一对一有效","群有效","群同时有效","群列表","平台列表"]
        lstFields_ind = dtSetting.Get_Index_Fields(lstFields)

        #转换为功能权限对象集
        if(self.hasGol):
            pGroups = gol._Get_Value('rootRobot_usrGroups', None)     #群组信息
        for dtRow in dtSetting.dataMat:
            prjRoot = myRoot_Prj()
            prjRoot.prjName = dtRow[lstFields_ind["功能名称"]]
            prjRoot.fileName = dtRow[lstFields_ind["文件名"]]
            prjRoot.className = dtRow[lstFields_ind["类名"]]
            prjRoot.cmdStr = dtRow[lstFields_ind["启动命令"]]
            prjRoot.isEnable = myData.iif(dtRow[lstFields_ind["是否启用"]] == True, True, False)
            prjRoot.isEnable_All = myData.iif(dtRow[lstFields_ind["统一启用"]] == True, True, False)
            prjRoot.isEnable_one = myData.iif(dtRow[lstFields_ind["一对一有效"]] == True, True, False)
            prjRoot.isEnable_group = myData.iif(dtRow[lstFields_ind["群有效"]] == True, True, False)
            prjRoot.isEnable_groupAll = myData.iif(dtRow[lstFields_ind["群同时有效"]] == True, True, False)

            #平台集合
            lstGroup = dtRow[lstFields_ind["群列表"]].split(',')
            if(self.hasGol):
                for x in lstGroup:
                    pGroup = pGroups.Find_Group(x, x, "", True)
                    prjRoot.rootGroups.groupInfos[x] = pGroup
            prjRoot.plantsEnable = list(dtRow[lstFields_ind["平台列表"]])

            #实例功能对象并缓存索引
            prjRoot.creatIntance(self.usrName, self.usrID)
            self.prjRoots[prjRoot.prjName] = prjRoot
            self.prjCmds[prjRoot.cmdStr.lower()] = prjRoot.prjName

        #增加默认隐藏功能 
        if(True): 	 
            prjRoot = myRoot_Prj()
            prjRoot._Init("权限提升", "myRobot_Root", "myRobot_Root", "zxcRobot_Root", True, False, True, False, False)
            prjRoot.creatIntance(self.usrName, self.usrID)
            self.prjRoots[prjRoot.prjName] = prjRoot
            self.prjCmds[prjRoot.cmdStr.lower()] = prjRoot.prjName

            prjLog = myRoot_Prj()
            prjLog._Init("消息日志", "myRobot_Log", "myRobot_Log", "zxcRobot_Log", True, False, True, False, False)
            prjLog.creatIntance(self.usrName, self.usrID)
            prjLog.prjClass.Done("@@zxcRobot_Log", "")       #自启动
            self.prjRoots[prjLog.prjName] = prjLog
            self.prjCmds[prjLog.cmdStr.lower()] = prjLog.prjName
        
        #用户权限设置
        if(True): 	 
            #提取字段信息 
            lstFields_user = ["用户名","功能权限","功能列表"]
            lstFields_ind_user = dtSetting_user.Get_Index_Fields(lstFields_user)

            #转换为功能权限对象集
            if(self.hasGol):
                pUsers = gol._Get_Value('rootRobot_usrInfos', None)     #权限信息
                for dtRow in dtSetting_user.dataMat:
                    #提取用户对象
                    #prjRoot_user = myRoot_Usr.myRoot_Usr("", usrName, usrName, "", self)
                    usrName = dtRow[lstFields_ind_user["用户名"]] 
                    pUser = pUsers._Find(usrName, usrName, usrName, "", "", True)

                    #添加系统级权限用户 
                    bRoot = myData.iif(dtRow[lstFields_ind_user["功能权限"]] == True, True, False)
                    lstPrj = list(dtRow[lstFields_ind_user["功能列表"]])
                    if(bRoot):
                        if(len(lstPrj) < 1):    #所有有效
                            for x in self.prjRoots.keys():
                                self.prjRoots[x].rootUsers._Add(pUser)
                        else:
                            for x in self.prjRoots.keys():
                                if(x.prjName in lstPrj):
                                    self.prjRoots[x].rootUsers._Add(pUser) 
    #查找 
    def _Find(self, prjName): 
        prjName = prjName.lower()
        pPrj = self.prjCmds.get(prjName)    #cmd方式找项目
        if(pPrj != None):
            return self.prjRoots.get(pPrj)
        return self.prjRoots.get(prjName)

    #命令权限检查
    def IsEnable(self, prjName):
        pPrj = self._Find(prjName)
        if(pPrj == None): return False
        return pPrj.IsEnable()
    def IsEnable_All(self, prjName):
        pPrj = self._Find(prjName)
        if(pPrj == None): return False
        return pPrj.IsEnable_All()
    def IsEnable_one(self, prjName, usrName = ""): 
        pPrj = self._Find(prjName)
        if(pPrj == None): return False
        return pPrj.IsEnable_one(usrName)
    def IsEnable_group(self, prjName, groupName = ""): 
        pPrj = self._Find(prjName)
        if(pPrj == None): return False
        return pPrj.IsEnable_group(groupName)
    def IsEnable_groupAll(self, prjName): 
        pPrj = self._Find(prjName)
        if(pPrj == None): return False
        return pPrj.IsEnable_groupAll()


#主启动程序
if __name__ == "__main__":
    pRoots = myRoots_Prj("zxcTest", "@Test", False)
    print(pRoots.prjRoots)
