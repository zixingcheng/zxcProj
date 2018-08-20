#-*- coding: utf-8 -*-
"""
Created on  张斌 2018-06-25 10:58:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com

    机器人-权限对象操作 
"""
import sys, os, mySystem 

#引用根目录类文件夹--必须，否则非本地目录起动时无法找到自定义类
mySystem.Append_Us("../Prjs", False, __file__) 
mySystem.Append_Us("", False) 
import myRoot_Prj, myRoot_Usr, myRoot_GroupInfo, myRoot_Plat
from myGlobal import gol   


#权限对象操作
class myRoot():
    def __init__(self):
        self.usrName = "zxcRobot"       #归属用户
        self.usrNameNick = "zxcRobot"   #归属用户昵称
        self.usrID = "zxcRobot"         #归属用户ID
        self.rootPrjs = None            #功能集 
        self.usrInfos = None            #用户集 
        self.usrGroups = None           #用户群组集
        self.usrPlats = None           #平台集

        self.Init()                     #信息初始
    def Init(self):  
        self.usrName = gol._Get_Setting('usrName', "zxcRobot")          #归属用户
        self.usrNameNick = gol._Get_Setting('usrNameNick', "zxc机器人") #归属用户昵称
        self.usrID = gol._Get_Setting('usrID', "zxcRobotID")            #归属用户ID
        
        #用户集 
        if(self.usrInfos == None):
            self.usrInfos = myRoot_Usr.myRoot_Usrs(self.usrID,self.usrName)   
            gol._Set_Value('rootRobot_usrInfos', self.usrInfos)
        else:
            self.usrInfos.usrName = self.usrName
            self.usrInfos.usrID = self.usrID

        #群组集
        if(self.usrGroups == None):
            self.usrGroups = myRoot_GroupInfo.myRoot_GroupsInfo(self.usrName, self.usrID)   
            gol._Set_Value('rootRobot_usrGroups', self.usrGroups)
        else:
            self.usrGroups.usrName = self.usrName
            self.usrGroups.usrID = self.usrID

        #功能集
        if(self.rootPrjs == None):
            self.rootPrjs = myRoot_Prj.myRoots_Prj(self.usrName, self.usrID)   
        else:
            self.rootPrjs.usrName = self.usrName
            self.rootPrjs.usrID = self.usrID
        
        #平台集   
        if(self.usrPlats == None):
            self.usrPlats = myRoot_Plat.myRoot_Plats(self.usrName, self.usrID)   
        else:
            self.usrPlats.usrName = self.usrName
            self.usrPlats.usrID = self.usrID
        self.Init_Plats()  #初始平台             
    def Init_Plats(self, plat = "wx"):  
        self.usrPlats.Regist(self.usrName, self.usrID, plat)
    def Init_UserInfo(self, usrName, usrNameNick, usrID):  
        gol._Set_Setting('usrName', usrName)
        gol._Set_Setting('usrNameNick', usrNameNick)
        gol._Set_Setting('usrID', usrID)
        self.Init();
             
#定义全局方法集并缓存
gol._Init()         #先必须在主模块初始化（只在Main模块需要一次即可）
gol._Set_Value('rootRobot', myRoot())


#主启动程序
if __name__ == "__main__":
    pRoot = gol._Get_Value('rootRobot', myRoot())
    print(pRoot.usrName)

    gol._Set_Setting('usrName', "zxcRobot2")
    gol._Set_Setting('usrNameNick', "zxc机器人2")
    gol._Set_Setting('usrID', "zxcRobotID2")
    pRoot.Init()
    print(pRoot.usrName)
