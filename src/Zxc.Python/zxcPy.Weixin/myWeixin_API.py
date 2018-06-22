# -*- coding: utf-8 -*-
"""
Created on  张斌 2017-11-19 14:58:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com

    Rest API --Weixin API操作 
"""
import os  
import mySystem 
    
#引用根目录类文件夹--必须，否则非本地目录起动时无法找到自定义类
mySystem.m_strFloders.append('/zxcPy.APIs')
mySystem.m_strFloders.append('/zxcPy.Weixin')
mySystem.m_strFloders.append('/zxcPy.Weixin/Weixin_Reply')
mySystem.m_strFloders.append('/zxcPy.Weixin/Weixin_Reply/myWxDo')
mySystem.Append_Us("", False)    
import myWeb, myMMap, myWeixin_Cmd
from myGlobal import gol 



#主程序启动
if __name__ == '__main__': 
    gol._Init()     #先必须在主模块初始化（只在Main模块需要一次即可）
    
    # 创建内存映射（写）
    try:
        pMMap_Manager = myMMap.myMMap_Manager("Data/zxcMMap.dat")
        gol._Set_Value('manageMMap', pMMap_Manager)
    except:
        print("创建内存映射失败.")
        exit()

    # 创建新线程
    pWeb = myWeb.myWeb("127.0.0.1", 8668)
    pWeb.add_API(myWeb.myAPI, '/test')
    pWeb.add_API(myWeb.myAPI_p, '/test1/<param>')
    pWeb.add_API(myWeixin_Cmd.myAPI_Weixin_Cmd, '/weixin/<user>/<text>/<type>')
    pWeb.run()
        
exit()