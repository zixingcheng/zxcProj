#-*- coding: utf-8 -*-
"""
Created on  张斌 2018-08-12 19:16:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com

    Python的Weixin网页版消息处理接口(文本消息)--调整为调用Robot消息接口方法 
"""
import sys, ast, mySystem   

#引用根目录类文件夹--必须，否则非本地目录起动时无法找到自定义类  
mySystem.Append_Us("", False) 
import myWeb, myWeb_urlLib, myManager_Msg, myDebug, myData
from myGlobal import gol 


#消息处理工厂类
class myWx_Reply():
    def __init__(self, tag, bUseMQ = True, robot_API = "http://127.0.0.1:8668/zxcAPI/robot"):
        self.usrTag = tag
        self.usrID = "zxcID"
        self.usrName = "墨紫"
        self.nickName = ""
        self.robotAPI = myWeb_urlLib.myWeb(robot_API)   #WebAPI
        self.routeReply = "reply/"                      #消息处理接口路由名
        self.MMsg = gol._Get_Setting('manageMsgs')      #消息管理对象
        self.useMQ = bUseMQ
    def _Init(self, usrID, usrName, nickName = ""): 
        self.usrID = usrID
        self.usrName = usrName
        self.nickName = myData.iif(nickName == "", usrName, nickName)
        self.usrMMsg = gol._Get_Setting('manageMsgs')
        myDebug.Print("    --消息工厂(%s)初始: %s--%s" % (self.usrTag, nickName, usrID))
                 
    #处理封装返回消息(按标识内容处理)
    def Done_ByMsg(self, msg, isGroup = False):
        if(msg == None): return None

        #提取消息内容（可能随wx版本变更）
        usrName_To = msg['ToUserName']
        strText = msg['Text'] 
        idGroup = "" 
        isFromSelf = False
        if(isGroup):
            idGroup = msg['User'].get('UserName',"")
            nickName = msg.get('ActualNickName',"")
            usrName = msg.get('ActualNickName',"")
            usrID = msg.get('ActualUserName',"")
            msgID = msg.get('NewMsgId',"")
        else:
            #区分自己发送
            usrID = msg.get('FromUserName',"")
            nickName = msg['User'].get('NickName',"")
            msgID = msg.get('msgID',"")
            if(self.usrID == usrID):
                usrID = msg.get('ToUserName',"")    #调整为目标用户
                usrName = self.usrName              #调整为自己
                isFromSelf = True
                myDebug.Debug(nickName, msgID, strText, usrID)
            else:
                usrName = msg['User'].get('RemarkName',"")

        #消息测试 
        #msgR = {}
        #msgR["msgType"] = "TEXT"
        #msgR["msg"] = "msg:" + strText
        #msgR["usrName"] = usrID
        #msgR["isSelf"] = isFromSelf
        #return msgR
        
        #调用 
        return self.Done(usrID, usrName, nickName, strText, msgID, isGroup, idGroup, isFromSelf)         
    #按命令处理返回消息(按标识内容处理)
    def Done(self, usrID, usrName, usrNameNick, strText, msgID = "", isGroup = False, idGroup = "", isFromSelf = False):
        #组装请求参数字典
        # {'msg': '@@Repeater', 'usrName': '墨紫_0', 'usrNameNick': '墨紫', 'groupID': '', 'plat': 'wx', 'msgType': 'TEXT', 'usrID': 'zxc_0', 'msgID': ''}
        msg = self.MMsg.OnCreatMsg()
        msg["usrID"] = usrID
        msg["usrName"] = usrName
        msg["usrNameNick"] = usrNameNick
        msg["msg"] = strText
        msg["plat"] = "wx"
        msg["isSelf"] = isFromSelf
        print("请求消息:: ", msg)

        #请求robotAPI
        robotPath = self.routeReply + str(msg) 
        strReturn = ""
        try:
            if(self.useMQ):
                self.usrMMsg.OnHandleMsg(msg, 'robot')     #消息处理--推送至消息处理器
                return None
            else:
                strReturn = self.robotAPI.Do_API_get(robotPath, "zxcAPI-py") 
                #处理返回结果 
                if(strReturn == "null" or strReturn == ""): return None
                if(strReturn != None):
                    msgRe = ast.literal_eval(strReturn) 
                    return msgRe
        except :
            pass
        return None

    
#主启动程序
if __name__ == "__main__":
    gol._Init()             #先必须在主模块初始化（只在Main模块需要一次即可）
    gol._Set_Setting("CanPrint_Debug", False)

    #消息处理
    pWxReply = myWx_Reply("zxcc")
    pWxReply._Init("zxc", "墨紫")

    #权限初始
    pWxReply.Done('zxc_ID','zxc_0',"墨紫",'@@Repeater')
    pWxReply.Done('zxc_ID','zxc_0',"墨紫",'@@Repeater')
    print()

     

 
 
