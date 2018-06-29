#-*- coding: utf-8 -*-
"""
Created on  张斌 2018-06-25 10:58:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com

    机器人-功能权限对象 
"""
import sys, os, mySystem 

#引用根目录类文件夹--必须，否则非本地目录起动时无法找到自定义类
mySystem.Append_Us("/zxcPy.APIs", False, __file__)
mySystem.Append_Us("", False)    
import myRoot_GroupInfo as group


#功能权限对象
class myRoot_Prj():
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

#功能权限集对象
class myRoots_Prj():
    def __init__(self, usrName, userID): 
        self.usrName = usrName  #用户名
        self.userID = userID    #用户名
        self.prjRoots = {}      #功能权限集
        self.prjCmds = {}       #功能命令集
        # self.prjRoots_user = {} #功能权限用户集
        
        #初始根目录信息
        strDir, strName = myIO.getPath_ByFile(__file__)
        self.Dir_Base = os.path.abspath(os.path.join(strDir, ".."))  
        self.Dir_Setting = self.Dir_Base + "/Setting/"
        self.Dir_Data = self.Dir_Base + "/Data/"

    #初始参数信息等   
    def _Init(self):            
        dtSetting = myIO_xlsx.loadDataTable(self.Dir_Setting + "Setting.xlsx", 0, 1)            #外部参数设置 
        dtSetting_user = myIO_xlsx.loadDataTable(self.Dir_Setting + "Setting_User.xlsx", 0, 1)  #外部参数设置-权限用户 
        
        #提取字段信息 
        lstFields = ["功能名称","文件名","类名","启动命令","统一启用","是否启用","一对一有效","群有效","群同时有效"]
        lstFields_ind = dtSetting.Get_Index_Fields(lstFields)

        #转换为功能权限对象集
        for dtRow in dtSetting.dataMat:
            prjRoot = myPrj_Root()
            prjRoot.prjName = dtRow[lstFields_ind["功能名称"]]
            prjRoot.fileName = dtRow[lstFields_ind["文件名"]]
            prjRoot.className = dtRow[lstFields_ind["类名"]]
            prjRoot.cmdStr = dtRow[lstFields_ind["启动命令"]]
            prjRoot.isEnable = myData.iif(dtRow[lstFields_ind["是否启用"]] == True, True, False)
            prjRoot.isEnable_All = myData.iif(dtRow[lstFields_ind["统一启用"]] == True, True, False)
            prjRoot.isEnable_one = myData.iif(dtRow[lstFields_ind["一对一有效"]] == True, True, False)
            prjRoot.isEnable_group = myData.iif(dtRow[lstFields_ind["群有效"]] == True, True, False)
            prjRoot.isEnable_groupAll = myData.iif(dtRow[lstFields_ind["群同时有效"]] == True, True, False)
            self.prjRoots[prjRoot.prjName] = prjRoot
            self.prjCmds[prjRoot.cmdStr.lower()] = prjRoot.prjName

        #用户权限设置
        if(True): 	 
            #提取字段信息 
            lstFields_user = ["用户名","功能权限"]
            lstFields_ind_user = dtSetting_user.Get_Index_Fields(lstFields_user)

            #转换为功能权限对象集
            for dtRow in dtSetting_user.dataMat:
                prjRoot_user = myPrj_Root_user()
                prjRoot_user.usrName = dtRow[lstFields_ind_user["用户名"]]
                prjRoot_user.prjRoot = myData.iif(dtRow[lstFields_ind_user["功能权限"]] == True, True, False)
                self.prjRoots_user[prjRoot_user.usrName.lower()] = prjRoot_user

        #增加默认隐藏功能 
        prjRoot = myPrj_Root()
        prjRoot._Init("权限提升", "myWxDo_Root", "myWxDo_Root", "zxcWeixin_Root", True, False, True, False, False)
        prjRoot.isRoot = True
        self.prjRoots[prjRoot.prjName] = prjRoot
        self.prjCmds["zxcWeixin_Root".lower()] = prjRoot.prjName

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
    def IsEnable_one(self, prjName): 
        pPrj = self._Find(prjName)
        if(pPrj == None): return False
        return pPrj.IsEnable_one()
    def IsEnable_group(self, prjName): 
        pPrj = self._Find(prjName)
        if(pPrj == None): return False
        return pPrj.IsEnable_group()
    def IsEnable_groupAll(self, prjName): 
        pPrj = self._Find(prjName)
        if(pPrj == None): return False
        return pPrj.IsEnable_groupAll()


#主启动程序
if __name__ == "__main__":
    pData = Data_Stock()
    pData.Print()
