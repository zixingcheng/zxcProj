# -*- coding: utf-8 -*-
"""
Created on  张斌 2018-05-03 14:58:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com

    Rest API --Quote API操作 
"""
import os  
import mySystem 
from flask import Flask
from flask_restful import reqparse, abort, Api, Resource

    
#引用根目录类文件夹--必须，否则非本地目录起动时无法找到自定义类
mySystem.m_strFloders.append('/zxcPy.Test')
mySystem.m_strFloders.append('/zxcPy.Quoation')
mySystem.Append_Us("", True)    
import myWeb, myWeixin_ItChat


#主程序启动
if __name__ == '__main__': 
    myWeixin_ItChat.main()

    # 创建新线程
    pWeb = myWeb.myWeb("0.0.0.0", 8080)
    pWeb.add_API(myWeb.myAPI, '/test')
    pWeb.add_API(myWeixin_ItChat.myAPI_p, '/test/<param>')
    pWeb.run()

    
    #声明Weixin操作对象
    pWeixin = myWeixin_ItChat.myWeixin_ItChat()
    
    #登录微信网页版(二维码扫码)
    pWeixin.Logion();
 
    #运行 
    #pWeixin.Run();
    pWeixin.Run_ByThread();
    
exit()