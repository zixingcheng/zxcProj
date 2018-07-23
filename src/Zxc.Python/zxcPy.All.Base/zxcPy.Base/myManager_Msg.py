# -*- coding: utf-8 -*-
"""
Created on  张斌 2018-07-23 11:00:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com

    消息处理器--通用消息处理器
"""
import sys, os, copy
import myWeb_urlLib, myVoice


#消息处理器--通用消息处理器
class myManager_Msg():
    def __init__(self, msgUrls ={"weixin": "http://127.0.0.1:8668"}):
        self.usePrint = True
        self.useVoice = False
        self.useLineMsg = True
        self.msgExramp = {"user":'', "text":'', "type":'TEXT', "plat":'weixin'} #消息样例

        self.usrWebs = {}           #在线消息集       
        if(self.useLineMsg):
            keys = msgUrls.keys()
            for x in keys:          #按消息分类标识初始对应web对象并存入dict
                pWeb = myWeb_urlLib.myWeb(msgUrls[x])
                self.usrWebs[x] = pWeb
        
    #消息处理
    def OnHandleMsg(self, msg):
        strMsg = msg["text"]

        #文字输出
        if(self.usePrint): print(strMsg)

        #声音输出
        if(self.useVoice):
            myVoice.Say_thrd(msg["text"])

        #在线消息输出
        typePlatform = msg.get("plat", "weixin")
        if(typePlatform != ""):
            pWeb = self.usrWebs.get(typePlatform, None)     #提取对应平台的web对象
            if(pWeb != None):   
                #微信输出
                if(typePlatform == "weixin"):    
                    wxPath = "weixin/" + msg["user"] + "/" + strMsg + "/" + msg["type"]
                    pWeb.Do_API_get(wxPath, "微信API-py")
                else:
                    pass
    #创建新消息
    def OnCreatMsg(self):
        return copy.deepcopy(self.msgExramp)
              
#初始全局消息管理器
from myGlobal import gol 
gol._Init()     #先必须在主模块初始化（只在Main模块需要一次即可）
gol._Set_Setting('manageMsgs', myManager_Msg())


if __name__ == '__main__':
   pMMsg = gol._Get_Setting('manageMsgs')

   #组装消息 
   msg = {}
   msg["user"] = "茶叶一主号"
   msg["text"] = "测试消息py"
   msg["type"] = "TEXT"
   msg["plat"] = "weixin"
   pMMsg.OnHandleMsg(msg)

   print()
    