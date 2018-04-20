#-*- coding: utf-8 -*-
"""
Created on  张斌 2016-09-16 15:56:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com

    Gsafety行政管理系统特定操作，配合md文件自动化提交日报。
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
import mySetting_Note, myWebFun_gsafety, myWebFun_gsafety_prj


#定义参数信息：用户名密码等
dt = myDataSet.loadDataSet("mySetting/Setting.txt", 1)
strUrl = dt[0][1] 
strUser = dt[1][1] 
strUserPwd = dt[2][1]

#初始web操作对象
clsWeb = myWeb(strUrl ,"")

#登录信息  
strLoginInfo = { 
    'method':'login', 
    'username':strUser, 
    'pwd':strUserPwd 
}


#登录操作-简化 
r = clsWeb.Do_Post("util/sys/login.do", strLoginInfo, "登录", True, True)
#print(r.decode("UTF8"))

#跳转到浏览页面
r = clsWeb.Do_Post("ams_weekly/AnaphaseTreatmentBrowse.do", "", "浏览")
#print(r.decode("UTF8"))


#写考勤外出--特殊(并删除，这里不创建相关方法报错，特殊处理方式)
myWebFun_gsafety.__add_考勤外出__(clsWeb, "python-address-autotag", "python-gsafety")
myWebFun_gsafety.__delet_All_外出__(clsWeb, "python-address-autotag", "python-gsafety")
 

#获取最新项目信息
x,y = myWebFun_gsafety_prj.__get_prjinfo_all__(clsWeb)
pDict = y


#获取日志信息  
baseDir_Root = os.path.abspath(os.path.join(os.getcwd(), ""))
pathNote = baseDir_Root + "/mySetting/Note_Now.md"    #Note_Now配置文件路径，py脚本上级目录 
dirNotes = baseDir_Root + "/myNotes"                  #Note备份文件，Note_Now中记录后会复制一份备份

pNotes = mySetting_Note._Get_Notes_(pathNote)
nNotes = len(pNotes)
if(nNotes < 1):
    exit()
else:      
    #日志填写--循环所有日志记录
    for i in range(0, nNotes):  
        pNote = pNotes[i]

        #条用添加日报
        myWebFun_gsafety.__add_日报_byNote__(clsWeb, pNote) 

        #写入日志记录
        tTime_Day = time.strptime(pNote.Time, "%Y-%m-%d %H:%M")
        dirNote_Now = dirNotes + "/" + time.strftime("%Y", tTime_Day) + "/" + time.strftime("%m", tTime_Day) + "月日志/"
        myIO.mkdir(dirNotes)
            
        pathNote2 = dirNote_Now + time.strftime("%Y-%m-%d", tTime_Day) + ".md"    #Note_Now配置文件路径，py脚本上级目录
        print("备份日志：" +  pathNote2)
        mySetting_Note._Write_Note_(pathNote2, pNotes[i])


#检索--模糊
#print(len(pDict))
#pDict2 = myWebFun_gsafety_prj.__get_prj__('核事故应急关键技术研究')
#print(pDict2)


exit()




 
