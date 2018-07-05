#-*- coding: utf-8 -*-
"""
Created on  张斌 2018-07-04 15:58:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com

    机器人-平台对象 
"""
import sys, os, datetime, uuid, mySystem 

#引用根目录类文件夹--必须，否则非本地目录起动时无法找到自定义类 
mySystem.Append_Us("", False)    

 
#平台对象
class myRoot_Plant():
    def __init__(self): 
        self.plantName = ""     #平台名
        self.usrName = ""       #平台用户名（登录）
        self.usrID = ""         #平台用户ID（登录） 
        self.usrTime_Regist = datetime.datetime.now()          #注册时间
        self.usrTime_Logined_Last = datetime.datetime.now()    #最后登录时间（请求）
        self.usrToken = str(uuid.uuid1())                      #用于验证，暂时为请求获取
        
#平台对象集
class myRoot_Plants():
    def __init__(self, usrName, userID): 
        self.usrName = usrName      #归属用户
        self.usrID_sys = userID     #归属用户ID
        self.usrPlants = {}         #平台集

    #注册平台
    def Regist(self, usrName, usrID, usrType):
        pPlant = self.Find(usrType)
        if(pPlant == None):
            pPlant = myRoot_Plant()
            pPlant.plantName = usrType
            pPlant.usrName = usrName
            pPlant.usrID = usrID
            self.usrPlants[pPlant.plantName.lower()] = pPlant
        return pPlant
    #查找平台
    def Find(self, usrType, token = ""):
        pPlant = self.usrPlants.get(usrType.lower(), None)
        if(token != ""):
            if(token != pPlant.usrToken): return None
        return pPlant
    #合法性(时效)
    def Check(self):
        return True
    

#主启动程序
if __name__ == "__main__":
    pPlants = myRoot_Plants("zxcTest", "@Test")
    pPlant = pPlants.Regist("墨紫", "@aafsaf", "wx")
    print(pPlant.usrToken)

    print(pPlants.Find("wx").usrName)
    print(pPlants.Find("wx", pPlant.usrToken).usrName)
    print(pPlants.Find("wx", "sd"))

