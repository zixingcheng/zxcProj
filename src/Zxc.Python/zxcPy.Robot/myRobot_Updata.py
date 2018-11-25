#-*- coding: utf-8 -*-
"""
Created on  张斌 2018-11-25 17:16:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com

    Python的Robot功能updata，发布版本更新信息等
"""
import os, ast, time, threading  
import mySystem 
    
#引用根目录类文件夹--必须，否则非本地目录起动时无法找到自定义类
mySystem.Append_Us("", False)    
import myDebug, myIO, myIO_md, myManager_Msg

#初始全局消息管理器
from myGlobal import gol 
gol._Init()     #先必须在主模块初始化（只在Main模块需要一次即可）


#机器人功能--更新消息类 
class myRobot_Updata():
    def __init__(self):  
        self.usrTag = "" 
        self.usrMMsg = gol._Get_Setting('manageMsgs')     #消息管理器
        self._Init()             #按全局权限初始
    def _Init(self): 
        #初始根目录信息
        strDir, strName = myIO.getPath_ByFile(__file__)
        self.Dir_Base = os.path.abspath(os.path.join(strDir, ""))  

        self.mdUpdata = myIO_md.myMD(self.Dir_Base + "/Docs/Updata.md")
        pNode = self.mdUpdata[0]
        self.version = pNode.titleName
        self.verText = pNode.getContent().strip()
        self.mdUpdata = None

        self.Send_UpdataMsg()   #发送更新消息 

    #发送更新消息    
    def Send_UpdataMsg(self):
        #组装消息内容
        strText = "zxcRobot（" + self.version + "） --"

        #判断是否已经发送
        strVer = myIO.getContent(self.Dir_Base + "/Log/Updata.log", True)
        if(strVer != self.version):
            strText += "已启动."
            strText += "\n更新内容：\n" + self.verText
            myIO.Save_File(self.Dir_Base + "/Log/Updata.log", self.version)
        else:
            strText += "已重启."

        #发送所有
        msg = self.usrMMsg.OnCreatMsg()
        msg['usrName'] = "filehelper"
        msg["usrPlat"] = "wx"
        msg['msg'] = strText  
        self.usrMMsg.OnHandleMsg(msg)

        msg["usrName"] = ""
        msg["groupName"] = "测试群"
        self.usrMMsg.OnHandleMsg(msg) 
        
myUpdata = myRobot_Updata()     # 机器人功能--更新消息类 
#主启动程序
if __name__ == "__main__": 
    #机器人功能--更新消息类 
    #myUpdata.Send_UpdataMsg()  

    print() 
    exit()

