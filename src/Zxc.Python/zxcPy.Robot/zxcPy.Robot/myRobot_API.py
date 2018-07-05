# -*- coding: utf-8 -*-
"""
Created on  张斌 2018-07-04 15:58:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com

    Rest API --Robot API操作 
"""
import os  
import mySystem 
    
#引用根目录类文件夹--必须，否则非本地目录起动时无法找到自定义类
mySystem.Append_Us("../zxcPy.Robot", False, __file__)
mySystem.Append_Us("../zxcPy.APIs", False, __file__)
mySystem.Append_Us("/Prjs", False, __file__)
mySystem.Append_Us("/Roots", False, __file__)
mySystem.Append_Us("", False)    
import myWeb, myRoot, myAPI_Robot
from myGlobal import gol 


#主程序启动
if __name__ == '__main__': 
    #gol._Init()     #先必须在主模块初始化（只在Main模块需要一次即可） 
     
    # 创建Web
    pWeb = myWeb.myWeb("127.0.0.1", 8666)
    pWeb.add_API(myWeb.myAPI, '/test')
    pWeb.add_API(myWeb.myAPI_p, '/test1/<param>')
    
    myAPI_Robot.add_APIs(pWeb)
    pWeb.run()
        
exit()