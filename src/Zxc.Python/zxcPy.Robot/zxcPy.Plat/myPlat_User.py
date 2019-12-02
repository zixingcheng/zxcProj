#encoding: utf-8 
# -*- coding: utf-8 -*-
"""
Created on  张斌 2019-12-02 16:00:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com

    我的管理平台-用户管理平台
"""
import sys, os, time, datetime
import mySystem

#引用根目录类文件夹--必须，否则非本地目录起动时无法找到自定义类
sysDir = mySystem.Append_Us("")
sysDir = mySystem.Append_Dir("myFunction")
import myIO, myData_DB, myData_Trans, myDebug
from myData_DB_Mysql import myData_Table



# 用户管理平台
class myPlat_User(): 
    def __init__(self, host = "127.0.0.1"):        
        #初始根目录信息
        strDir, strName = myIO.getPath_ByFile(__file__)
        self._Dir_Base = os.path.abspath(os.path.join(strDir, ".."))  

        #初始数据库对象
        self._dbUser = myData_Table("zxcDB_User", self._Dir_Base + "/Data/DB_Data/", params = {"host": host})

    # 创建用户
    def Add_User(self, usrName = "", urlDoLogin = "", url_img_code = "", cookie_str = ""):  
        usrInfo = {"用户名": "用户名","姓名": "姓名","性别": "男","电话": "136**","微信ID": "微信ID","微信名": "微信名"}
        self._dbUser.add(usrInfo, tableName = "zxcUserInfo")
        aa =0
 
                 



#主启动程序 
if __name__ == "__main__":    
    # 模拟登录
    pPlat = myPlat_User() 


    exit(0)

