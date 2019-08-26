# -*- coding: utf-8 -*-
"""
Created on  张斌 2018-08-12 23:58:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com

    Rest API --myBlockChain 操作
"""
import os, copy  
import mySystem 
    
#引用根目录类文件夹--必须，否则非本地目录起动时无法找到自定义类
mySystem.Append_Us("/zxcPy.APIs", False, __file__)
mySystem.Append_Us("/zxcPy.BlockChain", False, __file__)
mySystem.Append_Us("", False)    
import myWeb, myAPI_BlockChain, myBlockChain
from myGlobal import gol 



#主程序启动
if __name__ == '__main__': 
    gol._Init()             #先必须在主模块初始化（只在Main模块需要一次即可）  
    
    # 创建新线程
    pWeb = myWeb.myWeb("127.0.0.1", 5016)
    pWeb.add_API(myWeb.myAPI, '/test')

    # 添加接口并启动API
    myAPI_BlockChain.add_APIs(pWeb)
    pWeb.run()
    