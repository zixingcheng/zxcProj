#-*- coding: utf-8 -*-
"""
Created on  张斌 2017-11-17 15:16:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com

    Weixin网页版消息处理接口（功能库）--机器人类--消息回撤
"""
import sys, ast, os, time, random, mySystem

#引用根目录类文件夹--必须，否则非本地目录起动时无法找到自定义类 
mySystem.Append_Us("", False) 
import myDebug, myData, myRobot, myManager_Msg, myIO
from myGlobal import gol   

    
#机器人类--消息回撤
class myRobot_Note(myRobot.myRobot):
    def __init__(self, usrID = "", usrName = ""):
        super().__init__(usrID, usrName)
        self.doTitle = "Robot_Note"     #说明 
        self.prjName = "通知消息"       #功能名
        self.doCmd = "@@zxcRobot_Note"  #启动命令 
        self.isBackUse = True           #后台运行
        self.maxTime = -1               #永久有效 
        self.perfixRevoke = ['告诉你一个秘密，', '偷偷告诉你哦，', '哈哈，发现你了！', '万能的机器人告诉我，', '小样，被我发现了吧。', '别想跑哦，我看到你了，']
                
    #消息处理接口
    def _Done(self, Text, msgID = "", msgType = "NOTE", usrInfo = {}):
        #必须为NOTE类型 
        strReturn = ""
        if(msgType.upper() != "NOTE"): return strReturn

        #解析通知
        msg = ast.literal_eval(Text) 

        #按通知标签处理
        noteTag = msg.get('noteTag', "").upper()
        if(noteTag == "REVOKE"):    #消息撤回通知
            strReturn = self._Done_Revoke(msg, msgID, msgType, usrInfo)
        elif(noteTag == "PAY"):     #消息撤回通知
            strReturn = self._Done_Pay(msg, msgID, msgType, usrInfo)
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
                    usrInfo['to_usrName'] = "self"          #调整的转发用户名(自己"self")
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
    #转账通知        
    def _Done_Pay(self, msg, msgID, msgType, usrInfo = {}):
        strReturn = "" 
        if(msg['paySubType'] == '1'): 
            if(msg['payUser'] == "Self"):
                strReturn = f"已发转账 ￥{msg['payMoney']}。"
            else:
                strReturn = f"待收转账 ￥{msg['payMoney']}。"
        elif(msg['paySubType'] == '3'): 
            if(msg['payUser'] == "Self"):
                strReturn = f"已成转账 ￥{msg['payMoney']}。"
            else:
                strReturn = f"已收转账 ￥{msg['payMoney']}。" 
        return strReturn  
    
    def _Title_User_Opened(self): 
        return "自动处理所有通知消息..."
        

#主启动程序
if __name__ == "__main__":
    from myRobot_Log import myRobot_Log
    pR = myRobot_Log("zxcID", "zxcName");
    pR.Done("@@zxcRobot_Log")
    myDebug.Debug(pR.Done("Hello"))
    pR.Done("Test", "@zxcvbnm", "TEXT", "zxcID", 'zxcName', "zxcNameNick")
    pR.Done("Bye")
    pR.Done("@@zxcRobot_Log")
    print()
    time.sleep (1)
    
    #回复消息
    pRevoke = myRobot_Note()
    
    #组装请求
    usrInfo = {}
    noteMsg = {}
    if(True):
        usrInfo["usrID"] = "zxcID"
        usrInfo["usrName"] = "zxcName"
        usrInfo["usrNameNick"] = "zxcNameNick"
        usrInfo['usrNameSelf'] = ""             #自己发自己标识 
        usrInfo["groupID"] = ""
        usrInfo["groupName"] = ""

        noteMsg["noteTag"] = "REVOKE"
        noteMsg["old_msg_id"] = "@zxcvbnm"

    #回撤请求
    pRevoke.Done("@@zxcRobot_Note")
    myDebug.Debug(pRevoke.Done_ByDict(str(noteMsg), "", "NOTE", usrInfo)["msg"])

    pRevoke.Done("@@zxcRobot_Note")
    print()
    
