#-*- coding: utf-8 -*-
"""
Created on  张斌 2017-11-17 15:16:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com

    Weixin网页版消息处理接口（功能库）--机器人类--消息回撤
"""
import sys, string, ast, os, time, random, mySystem
from urllib.parse import quote

#引用根目录类文件夹--必须，否则非本地目录起动时无法找到自定义类 
mySystem.Append_Us("", False) 
import myDebug, myData, myData_Json, myRobot, myIO, myWeb_urlLib
import myRobot_Robot, myManager_Msg
from myGlobal import gol   

    
#机器人类--消息处理(默认)
class myRobot_Msg(myRobot.myRobot):
    def __init__(self, usrID = "", usrName = ""):
        super().__init__(usrID, usrName)
        self.doTitle = "Robot_Note"     #说明 
        self.prjName = "消息处理"       #功能名
        self.doCmd = "@@zxcRobot_Msg"   #启动命令 
        self.isBackUse = True           #后台运行
        self.maxTime = -1               #永久有效 

        #初始全局操作对象
        #self.webQuote = myWeb_urlLib.myWeb("http://127.0.0.1:8669/zxcAPI/robot", "", False)   
        self.myRobot = myRobot_Robot.myRobot_Robot()
        self.myRobot.isRunning = True
                
    #消息处理接口
    def _Done(self, Text, msgID = "", msgType = "TEXT", usrInfo = {}):
        #按消息类型处理
        msgType = msgType.upper()
        strReturn = ""
        if(msgType == "TEXT") :
            strReturn = self._Done_Text(Text, msgID, usrInfo)
        return strReturn 
    
    #消息处理接口-Text
    def _Done_Text(self, Text, msgID = "", usrInfo = {}):
        #提取命令内容
        if(Text.count("@*") != 1): return ""
        cmds = Text.strip()[2:].split(" ")
        cmd = cmds[0].strip()
        nNum = len(cmds)
        myDebug.Print(Text.strip())
        
        #账单命令处理
        strReturn = ""
        if(cmd == "帮助"):
            return self._Title_Helper()
        elif(cmd == ""):
            #机器人
            return self.myRobot._Done(Text, msgID, "TEXT", usrInfo)
        elif(cmd == "股票"):
            #发送股票设置界面链接
            usrPlat = usrInfo.get('usrPlat', 'wx')
            usrID = myData.iif(usrInfo['groupName'] != "", "@*" + usrInfo['groupName'], usrInfo['usrNameNick'])
            url = 'http://39.105.196.175:8668/zxcWebs/stock/quoteset/' + usrID + "/" + usrPlat
            strReturn =  quote(url, safe = string.printable)   # unquote
        return strReturn

    #消息撤回通知        
    def _Done_Revoke(self, msg, msgID, msgType, usrInfo = {}):
        strReturn = ""
        pMsgs = self.usrMMsg._Find_Log_ByDict(usrInfo, False)
        if(pMsgs != None): 
            msgID_old = msg.get('old_msg_id', "")
            pMsg = pMsgs.Find(msgID_old)
            if(pMsg != None):
                #组装撤回描述个人消息发送到文件助手
                if(usrInfo.get('groupName', "") == ""):
                    usrInfo['to_usrName'] = "Self"          #调整的转发用户名(自己"self")
                    strReturn = pMsg.usrFrom + " "    
                else:
                    #组装随机前缀
                    indPrefix = random.randint(0, len(self.perfixRevoke) - 1)
                    strPrefix = self.perfixRevoke[indPrefix]
                    strReturn = strPrefix + " @" + pMsg.usrFrom + " "
                strReturn += "撤回了条消息。\n"

                #按消息内容组装 
                msgType_old = pMsg.msgType.upper()
                if(msgType_old == "TEXT"):
                    strReturn += "消息内容：\"" + pMsg.msg + "\""
                elif(msgType_old == "SHARING"):
                    strReturn += "分享链接：\"" + pMsg.msgUrl + "\""
        return strReturn  
    
    def _Title_User_Opened(self): 
        return "自动处理所有通知消息..."
    def _Title_Helper(self): 
        strReturn = "消息命令提示："
        strReturn += self.perfix + "@*帮助：输出所有命令说明"
        strReturn += self.perfix + "@*：机器人聊天，可咨询问题" 
        strReturn += self.perfix + "@*股票：股票设置，推送用户设置"  
        strReturn += "\n命令参数以空格区分，如：\"@* 光山天气\""
        return strReturn
        

#主启动程序
if __name__ == "__main__": 
    #消息处理
    pRobot_Msg = myRobot_Msg()
    pRobot_Msg.Done("@@zxcRobot_Msg")
    
    #组装请求
    usrInfo = {}
    noteMsg = {}
    if(True):
        usrInfo["usrID"] = "zxcID"
        usrInfo["usrName"] = "zxcName"
        usrInfo["usrNameNick"] = "茶叶一主号"
        usrInfo['usrNameSelf'] = ""             #自己发自己标识 
        usrInfo["groupID"] = ""
        usrInfo["groupName"] = "" 

    #回撤请求
    myDebug.Debug(pRobot_Msg.Done("@*帮助", usrNameNick='茶叶一主号')['msg']) 
    myDebug.Debug(pRobot_Msg.Done("@* 光山天气")['msg']) 
    myDebug.Debug(pRobot_Msg.Done("@* 附近商场")['msg']) 
    
    myDebug.Debug(pRobot_Msg.Done("@*股票", usrNameNick='茶叶一主号')['msg'])  

    pRobot_Msg.Done("@@zxcRobot_Msg")
    print()
    
