#encoding: utf-8 
# -*- coding: utf-8 -*-
"""
Created on  张斌 2016-09-23 16:00:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com

    广东省厅后台行政区划数据自动填写
"""

import sys, os, time
import re, requests
import urllib,urllib.parse,urllib.request,http.cookiejar 
import mySystem


#引用根目录类文件夹--必须，否则非本地目录起动时无法找到自定义类
sysDir = mySystem.Append_Us("")
sysDir = mySystem.Append_Dir("myFunction")
import myIO, myDataSet 
from myWeb_urlLib import myWeb  


#定义参数信息：用户名密码等
dt = myDataSet.loadDataSet("mySetting/Setting.txt", 1)
strUrl = "http://19.16.40.226:7001"


#登录信息  
strLoginInfo = { 
    'username': 'gsafety', 
    'password': 'Gsafety@321#'
}


#添加数据-机构
def addGroup(pWeb, reqP):
    #组装参数
    #reqP = {
    #        "districtCode": districtCode,
    #        "orgName": "广州市交通运输局4446",
    #        "orgShortName": "广州市交通运输局 4446",
    #        "parentCode": "0860860025",
    #        "perception": "",
    #        "orgEntity": 1
    #    }

    #调用
    r = pWeb.Do_Post("gdst-sa/admin/basedata/org/save?", reqP, "添加数据-机构", useJson = False)
    rr = r.decode(encoding = "utf8")
 
    

#主启动程序 
if __name__ == "__main__":    
    # 初始web操作对象
    pWeb = myWeb('http://19.16.40.226:7001' ,"")
    
    # 登录操作-简化 
    r = pWeb.Do_Post("gdst-sa/login", strLoginInfo, "登录", bUseHeaders = True, bInitCookie = True, useJson = False)
    
    # 读取省市信息
    txtLines = myIO.getContents("E:\\myCode\\zxcProj\\src\\Zxc.Python\\zxcPy.gsLog_Submits\\mySetting\\揭阳.txt", noBOM = False, isUtf = False)
    
    # 循环添加数据-机构
    for x in txtLines:
        name = x.replace(" ", "").replace("\n", "")
        if(name == ""): continue

        # 组装参数
        reqP = {
                "districtCode": 445100,
                "orgName": name,
                "orgShortName": name,
                "parentCode": "0860860083",
                "perception": "",
                "orgEntity": 1
            }
        addGroup(pWeb, reqP)
        print(reqP)

    print()
     