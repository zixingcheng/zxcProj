# -*- coding: utf-8 -*-
"""
Created on  张斌 2020-05-20 09:58:00 
    @author: zhang bin
    @email:  zhangbin@qq.com

    Rest Server --服务启动，
"""    
import mySystem

mySystem.Append_Us("", False)    
import myWeb
from myGlobal import gol 
gol._Init()             #先必须在主模块初始化（只在Main模块需要一次即可）


#提取端口号(环境变量)
HOST, PORT, dirBase = myWeb.get_InfoServer(__file__, 'SERVER_HOST', 'SERVER_PORT', 5555)  
gol._Set_Setting("serverUrl", "http://" + HOST + ":" + str(PORT))
gol._Set_Setting("serverBaseDir", dirBase)

#初始Web程序
appWeb = myWeb.myWeb("0.0.0.0", PORT, webFolder = dirBase + "/" )
appWeb.add_Web()
appWeb.add_API(myWeb.myAPI, '/test') 

import zxcPy_Form.myWeb_Test
#myWeb_Test.add_Webs(appWeb) 
