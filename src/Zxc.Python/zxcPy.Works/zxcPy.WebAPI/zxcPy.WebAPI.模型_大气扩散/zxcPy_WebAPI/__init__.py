# -*- coding: utf-8 -*-
"""
Created on  张斌 2020-06-08 10:58:00 
    @author: zhang bin
    @email:  zhangbin@qq.com

    Rest Server --服务启动初始 
"""
import mySystem

mySystem.Append_Us("", False)    
import myWeb, zxcPy_WebAPI.myWebAPI_Model
from myGlobal import gol 
gol._Init()             #先必须在主模块初始化（只在Main模块需要一次即可）


#提取端口号(环境变量)
HOST, PORT, dirBase = myWeb.get_InfoServer(__file__, 'SERVER_HOST', 'SERVER_PORT', 8686)  
gol._Set_Setting("serverUrl", "http://" + HOST + ":" + str(PORT))
gol._Set_Setting("serverBaseDir", dirBase)


#初始Web程序
appWeb = myWeb.myWeb("0.0.0.0", PORT, webFolder = dirBase + "/" )

#启用-模型-大气扩散WebAPI
appWeb.add_API(myWebAPI_Model.myAPI_Model_Atmospheric_Diffusion, '/zxcAPI/Model/Leak/<param>')

