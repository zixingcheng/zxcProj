#-*- coding: utf-8 -*-
"""
Created on  张斌 2018-08-12 19:16:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com

    Python的Weixin网页版消息处理接口(文本消息)--调整为调用Robot消息接口方法 
"""
import sys, ast, re, mySystem   

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
        self.usrMMsg = gol._Get_Setting('manageMsgs')   #消息管理对象
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

        #提取消息内容（可能随wx版本变更） 参见 https://blog.csdn.net/zhizunyu2009/article/details/79000190
        usrName_To = msg['ToUserName']
        msgID = msg.get('NewMsgId',"")              #消息ID
        msgType = msg['Type'].upper()               #消息类型
        msgTime = msg.get('CreateTime', 0)          #消息时间
        strText = msg['Text']                       #消息内容

        #区分群与个人
        idGroup = "" 
        nameGroup = ""
        nameSelf = ""
        isFromSelf = False
        if(isGroup):
            usrID = msg.get('ActualUserName',"")        #发消息人ID
            usrName = msg.get('ActualNickName',"")      #发消息人昵称
            nickName = msg.get('ActualNickName',"")     #发消息人昵称

            idGroup = msg['User'].get('UserName',"")    #群ID
            nameGroup = msg['User'].get('NickName',"")  #群名称
            if(self.usrID == usrID):
                nameSelf = self.usrName                 #发消息人名称，调整为自己
                usrName = self.usrName                   
                nickName = usrName
        else:
            #区分自己发送
            usrID = msg.get('FromUserName',"")          #发消息人ID
            usrName = msg['User'].get('RemarkName',"")  #发消息人备注名称
            nickName = msg['User'].get('NickName',"")   #发消息人昵称
            if(self.usrID == usrID):
                usrID = msg.get('ToUserName',"")        #发消息ID，调整为目标用户
                nameSelf = self.usrName                 #发消息人名称，调整为自己
        if(usrName == ""): usrName = nickName           #无MarkName使用nickName
        myDebug.Debug(nameSelf,",", usrID,",", usrName,",", nickName, ",", msgID, ",",strText, ",", idGroup, ",",nameGroup)

        #Note信息(增加Note标识及提取信息)
        noteMsg = self.get_NoteTag(msgType, msg)


        #消息测试 
        #msgR = {}
        #msgR["msgType"] = "TEXT"
        #msgR["msg"] = "msg:" + strText
        #msgR["usrName"] = usrID
        #msgR["isSelf"] = isFromSelf
        #return msgR
        
        #调用 
        return self.Done(usrID, usrName, nickName, strText, msgID, msgType, msgTime, idGroup, nameGroup, nameSelf, noteMsg)         
    #按命令处理返回消息(按标识内容处理)
    def Done(self, usrID, usrName, usrNameNick, strText, msgID = "", msgType = "TEXT", msgTime = 0, idGroup = "", nameGroup = '', nameSelf = '', noteMsg = None):
        #组装请求参数字典
        # {'msg': '@@Repeater', 'usrName': '墨紫_0', 'usrNameNick': '墨紫', 'groupID': '', 'usrPlat': 'wx', 'msgType': 'TEXT', 'usrID': 'zxc_0', 'msgID': ''}
        msg = self.usrMMsg.OnCreatMsg()
        msg["usrID"] = usrID
        msg["usrName"] = usrName
        msg["usrNameNick"] = usrNameNick
        msg['usrNameSelf'] = nameSelf       #自己发自己标识 
        msg["groupID"] = idGroup
        msg["groupName"] = nameGroup

        msg["msg"] = strText
        msg["msgID"] = msgID
        msg["msgType"] = msgType
        if(msgTime > 0): msg['time'] = msgTime 
        msg["usrPlat"] = "wx"
        if(noteMsg != None): 
            msg['noteInfo'] = noteMsg       #加入通知信息 noteMsg  
            msg["msg"] = str(noteMsg)       #调整消息内容为noteMsg
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
    
    #处理封装返回消息(按标识内容处理)
    def get_NoteTag(self, msgType, msg):
        if(msgType != "NOTE"): return None
        strText = msg['Text']   #消息内容

        noteMsg = {}
        if(strText.count("撤回了一条消息") == 1):
            noteMsg['noteTag'] = "REVOKE"
            noteMsg['old_msg_id'] = re.search("\<msgid\>(.*?)\<\/msgid\>", msg['Content']).group(1)     # 获取消息的id
        return noteMsg
    
    #消息超时校检
    def Check_TimeOut(self, msg, nTimeOut = 600): 
        return self.usrMMsg.Check_TimeOut(msg, nTimeOut)


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

     

 
 
