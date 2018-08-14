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
mySystem.Append_Us("", False)    
import myWeb, myMMap, myDebug, myMQ_Rabbit
from myGlobal import gol   
gol._Init()     #先必须在主模块初始化（只在Main模块需要一次即可）


#API-命令--共享内存
class myAPI_Weixin_Cmd_ByMMP(myWeb.myAPI): 
    def get(self, user, text, type = "Text"):
        pMMap_Manager = gol._Get_Value('manageMMap')
        if(pMMap_Manager == None):
            return False
        #myDebug.Debug(user, text, type)

        #生成并写入命令
        msg = {'FromUserName': user, 'Text': text, 'Type': type}        
        pMMdata = myMMap.myMMap_Data(msg, 0)      #生成命令--共享内存数据对象
        ind = pMMap_Manager.Write(pMMdata)          #写入命令--共享内存
        
        #读取测试
        pMMdata_M2, ind2 = pMMap_Manager.Read(ind)  
        #myDebug.Debug(str(ind) + ":", pMMdata_M2.value)
        #if(ind>1):
        #    pMMdata_M3, ind3 = pMMap_Manager.Read(ind - 1)  
        #    if(pMMdata_M3 != None):
        #        print("Last::" + str(ind - 1) + ":", pMMdata_M3.value)
        return ind
    
#API-命令--消息队列
class myAPI_Weixin_Cmd_ByMQ(myWeb.myAPI): 
    def get(self, user, text, type = "Text"):
        pMQ_Sender = gol._Get_Value('zxcMQ_Wx_Sender')
        if(pMQ_Sender == None):
            return False 

        #生成命令并推送消息队列
        msg = {'usrName': user, 'msg': text, 'msgType': type}    
        pMQ_Sender.Send_Msg(pMQ_Sender.nameQueue, str(msg))
        myDebug.Debug(pMQ_Sender.nameQueue, msg) 
        try:
            return True
        except :
            return False


#主程序启动 
if __name__ == '__main__': 
    # 创建消息队列
    gol._Init()     #先必须在主模块初始化（只在Main模块需要一次即可）
    nameMQ = 'zxcMQ_Wx'
    pMQ_Sender = myMQ_Rabbit.myMQ_Rabbit(True)
    pMQ_Sender.Init_Queue(nameMQ, True, True)
    gol._Set_Value('zxcMQ_Wx_Sender', pMQ_Sender, True)
    errStr = "创建消息队列失败."

    pMQ = myAPI_Weixin_Cmd_ByMQ()
    pMQ.get('茶叶一主号','text--登陆')


    # 创建内存映射
    try:
        pMMap_Manager = myMMap.myMMap_Manager("D:\myGit\zxcProj\src\Zxc.Python\zxcPy.Weixin\Data/zxcMMap.dat")
        
        ind = 0
        while(True):
            dict0 = {'FromUserName': '茶叶一主号', 'Text': 'text--登陆', 'Type': 'Text'}        
            pMMdata = myMMap.myMMap_Data(dict0, 0)
            #ind = pMMap_Manager.Write(pMMdata)
            
            pMMdata_M2, ind = pMMap_Manager.Read(ind, True)
            if(pMMdata_M2 != None):
                print(pMMdata_M2.value)
            time.sleep(1)
    except:
        bWrite = False
    exit()