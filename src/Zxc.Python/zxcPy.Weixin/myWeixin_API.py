# -*- coding: utf-8 -*-
"""
Created on  张斌 2017-11-19 14:58:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com

    Rest API --Weixin API操作 
"""
import os, time  
import mySystem 
    
#引用根目录类文件夹--必须，否则非本地目录起动时无法找到自定义类
mySystem.Append_Us("/zxcPy.APIs", False, __file__)
mySystem.Append_Us("/zxcPy.Weixin", False, __file__)
mySystem.Append_Us("/zxcPy.Weixin/Weixin_Reply", False, __file__)
mySystem.Append_Us("/zxcPy.Weixin/Weixin_Reply/myWxDo", False, __file__)
mySystem.Append_Us("", False)    
import myWeb, myDebug, myMMap, myMQ_Rabbit, myWeixin_Cmd
from myGlobal import gol 



#主程序启动
if __name__ == '__main__': 
    gol._Init()     #先必须在主模块初始化（只在Main模块需要一次即可）
    useCmdMMap = False

    errStr = ""
    try:
        # 创建内存映射（写）
        if(useCmdMMap):
            pMMap_Manager = myMMap.myMMap_Manager("Data/zxcMMap.dat")
            gol._Set_Value('manageMMap', pMMap_Manager, True)
            errStr = "创建内存映射失败."
        else:
            # 创建消息队列
            nameMQ = 'zxcMQ_wx'
            pMQ_Sender = myMQ_Rabbit.myMQ_Rabbit(True)
            pMQ_Sender.Init_Queue(nameMQ, True, True)
            gol._Set_Value('zxcMQ_Wx_Sender', pMQ_Sender, True)
            errStr = "创建消息队列失败."

        #测试
        #users = ['茶叶一主号', '老婆']
        #pAPI = myWeixin_Cmd.myAPI_Weixin_Cmd()
        #for i in range(0, 15):
        #    for x in users:
        #        strMsg = "Hello " + x 
        #        pAPI.get(x, strMsg)
        #    time.sleep(1)
        #print()
    except:
        myDebug.Error(errStr)
        exit()

    # 创建新线程
    pWeb = myWeb.myWeb("0.0.0.0", 8666)
    pWeb.add_API(myWeb.myAPI, '/test')
    pWeb.add_API(myWeb.myAPI_p, '/test1/<param>')
    if(useCmdMMap):
        pWeb.add_API(myWeixin_Cmd.myAPI_Weixin_Cmd_ByMMP, '/zxcAPI/weixin/<user>/<text>/<type>')
    else:
        pWeb.add_API(myWeixin_Cmd.myAPI_Weixin_Cmd_ByMQ, '/zxcAPI/weixin/<user>/<text>/<type>')
    
    #运行API
    pWeb.run()
        
exit()