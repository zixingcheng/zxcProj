# -*- coding: utf-8 -*-
"""
Created on  张斌 2018-07-23 11:00:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com

    消息处理器--通用消息处理器
"""
import sys, os, copy, time, datetime, threading
import myEnum, myData, myData_Trans, myDebug, myIO, myWeb_urlLib, myMQ_Rabbit #, myVoice 


#定义消息类型枚举
myMsgType = myEnum.enum('TEXT', 'PICTURE', 'VOICE', 'VIDEO', 'NOTE')
myMsgPlat = myEnum.enum('robot', 'wx')

#自定义消息对象
class myMsg():
    def __init__(self, msg, msgID, msgType = myMsgType.TEXT, usrFrom = '', usrPlat = ''): 
        self.msg = msg              #消息内容
        self.msgID = str(msgID)     #消息标识
        self.msgType = msgType      #消息类型
        self.usrFrom = usrFrom      #消息来源用户
        self.usrPlat = usrPlat      #消息来源平台
        self.msgUrl = ""            #消息链接(多媒体)
        self.msgTime = datetime.datetime.now()  #消息示例时间 
    def toCSVString(self):
        strCSV = "\n" + myData_Trans.Tran_ToDatetime_str(self.msgTime)
        strCSV += "," + self.usrFrom
        strCSV += "," + self.msg
        strCSV += "," + self.msgType
        return strCSV
#自定义消息对象集
class myMsgs():
    def __init__(self, userID, usrName, usrNameNick, dirLog = ""): 
        self.usrName = usrName          #归属用户
        self.usrNameNick = usrNameNick  #归属用户昵称
        self.userID = userID            #归属用户ID
        self.usrID_sys = userID         #归属用户ID_sys
        self.usrMsgs = []               #消息集
        self.pathLog = ""
        if(dirLog != ""):
            nameFile = myData.iif(self.usrNameNick == '', self.usrName, self.usrNameNick)
            self.pathLog = dirLog + nameFile + ".csv"
            if(os.path.exists(self.pathLog) == False):
                myIO.Save_File(self.pathLog, "时间,用户名,消息,消息类型", False, True) 

    #添加消息
    def Add(self, msg, msgID = '', msgType = myMsgType.TEXT, usrFrom = '', usrPlat = ''):
        if(msg == ""): return False
        pMsg = myMsg(msg, msgID, msgType, usrFrom, usrPlat)
        return self._Add(pMsg, True)
    def _Add(self, msg, bSave = False):
        if(msg == None): return False
        self.usrMsgs.append(msg)

        #文件追加数据内容
        if(self.pathLog != ""):
            with open(self.pathLog, 'a+') as f:
                f.write(msg.toCSVString())   
        return True
    
    #查找消息
    def Find(self, msgID):
        nLen = len(self.usrMsgs)
        for ind in range(nLen - 1, -1, -1):
            pMsg = self.usrMsgs[ind]
            if(pMsg.msgID == msgID):
                return pMsg
        return None

#消息处理器--通用消息处理器(转发需要主动初始平台对应消息队列及API)
class myManager_Msg():
    def __init__(self, dir = ""):
        self.usePrint = True
        self.useVoice = False  
        self.msgExramp = {"usrID":'', "usrName":'', "usrNameNick":'', "msg":'', "msgID":'', "msgType":'TEXT', "groupID":'', "usrPlat":''} #消息样例
        self.msgLogs = {}
        self.msgInd_Name = {}
        self.msgInd_Nick = {}
        self.usrWebs = {}           #在线消息集    
        self.usrMQs = {}            #消息队列  
        self.usrNameSelfs = {}      #各个平台标识的自己用户名（接收特殊消息）  
        self.usrMsgs_Buffer = []    #异步消息集    
        self.dirLog = dir

        #创建线程
        if(True):
            self.isRuning = True
            self.thrd_Handle = threading.Thread(target = self.OnHandleMsg_ByThread)
            self.thrd_Handle.setDaemon(False)
            self.thrd_Handle.start()
    #初始API、消息队列    
    def _Init(self, plat = myMsgPlat.wx, msgUrl_API = "http://127.0.0.1:8666/zxcAPI/weixin", msgMQ_Sender = None, usrHelper = ''):
        if(plat == None or plat == ""): return 
        self.usrNameSelfs[plat] = usrHelper      #自定义的特殊用户名(特殊发送目标)

        #消息队列
        if(msgMQ_Sender != None): 
            msgMQ_Sender.Init_Queue(msgMQ_Sender.nameQueue, True, True)     #消息持久化设置
            self.usrMQs[plat] = msgMQ_Sender
            
        #消息回调API
        if(msgUrl_API != ""):                 
            pWeb = myWeb_urlLib.myWeb(msgUrl_API, "", False)                #按消息分类标识初始对应web对象并存入dict
            self.usrWebs[plat] = pWeb
    #初始消息日志路径   
    def Init_LogDir(self, dir):
        self.dirLog = dir
        myIO.mkdir(self.dirLog, False)
    #关闭
    def _Close(self):
        self.isRuning = False
        
    #添加消息
    def Log(self, usrID, usrName, usrNameNick, msg, msgID, msgType = myMsgType.TEXT, usrPlat = '', idGroup = '', nameGroup = '', nameSelf = ''):
        usrInfo = self.OnCreatMsg_UsrInfo(usrID, usrName, usrNameNick, usrPlat, idGroup, nameGroup, nameSelf)
        return self.Log_ByDict(msg, msgID, msgType, usrInfo)
    def Log_ByDict(self, msg, msgID, msgType, usrInfo):
        pMsgs = self._Find_Log_ByDict(usrInfo, True)
        if(pMsgs != None):
            if(msg == ""): return False
            nameSelf = usrInfo.get('usrNameSelf', "")
            usrName = myData.iif(nameSelf == "", usrInfo.get('usrName', ""), nameSelf)
            usrPlat = usrInfo.get('usrPlat', "")
            pMsg = myMsg(msg, msgID, msgType, usrName, usrPlat)
            pMsgs._Add(pMsg, True) 
        return True
    def _Log(self, msg = {}):
        return self.Log_ByDict(msg.get('msg', ""), msg.get('msgID', ""), msg.get('msgType', ""), msg)
    def _Find_Log_ByDict(self, usrInfo, bCreatAuto = False):
        nameGroup = usrInfo.get('groupName', "")
        if(nameGroup != ""):
            usrID = usrInfo.get('groupID', "")
            usrName = nameGroup
            usrNameNick = ""
        else:
            usrID = usrInfo.get('usrID', "")
            usrName = usrInfo.get('usrName', "")
            usrNameNick = usrInfo.get('usrNameNick', "")
        return self._Find_Log(usrID, usrName, usrNameNick, bCreatAuto)
    def _Find_Log(self, usrID, usrName, usrNameNick, bCreatAuto = False):
        #依次查询
        pMsgs = None
        if(usrID == "" and usrName == "" and usrNameNick == ""): return pMsgs
        if(usrID != ""): pMsgs = self.msgLogs.get(usrID, None)
        if(pMsgs == None):
            if(usrName != ""): pMsgs = self.msgInd_Name.get(usrName, None)
            if(pMsgs == None):
                if(usrNameNick != ""):pMsgs = self.msgInd_Nick.get(usrNameNick, None)

        #创建新消息集
        if(pMsgs == None and bCreatAuto):
            pMsgs = myMsgs(usrID, usrName, usrNameNick, self.dirLog)
            self.msgLogs[usrID] = pMsgs
            if(usrName != ""): self.msgInd_Name[usrName] = usrID
            if(usrNameNick != ""): self.msgInd_Nick[usrNameNick] = usrID
        return pMsgs

    #消息处理（可指定plat）
    def OnHandleMsg(self, msg, plat = "", bCheck = False, nSleep = 0):
        if(msg == None): return
        strMsg = msg.get('msg')
        
        #异步延迟消息处理
        if(nSleep > 0):
            self.OnHandleMsg_Check(msg, plat)
            msg["timeLimit"] = datetime.datetime.now() + datetime.timedelta(seconds=nSleep)
            self.usrMsgs_Buffer.append(msg)
            return 

        #消息内容校正
        if(bCheck):
            self.OnHandleMsg_Check(msg, plat)


        #文字输出
        typePlatform = myData.iif(plat == "", msg.get("usrPlat", myMsgPlat.wx), plat)
        if(self.usePrint):
            myDebug.Print("消息管理器::", typePlatform + ">> ",strMsg)

        #声音输出
        #if(self.useVoice):
        #    myVoice.Say_thrd(msg["text"])

        #在线消息输出
        if(typePlatform != ""):
            pWeb = self.usrWebs.get(typePlatform, None)     #提取对应平台的web对象
            if(pWeb != None):   
                #格式化接口输出
                wxPath = msg["usrName"] + "/" + strMsg + "/" + msg["msgType"]
                pWeb.Do_API_get(wxPath, typePlatform + "API-py")

            usrMQ = self.usrMQs.get(typePlatform, None)
            if(usrMQ != None):
                #特殊消息处理
                toUser = msg.get('to_usrName', "")
                if(toUser != ""):
                    toUser = myData.iif(toUser.lower() != "self", toUser, self.usrNameSelfs.get(typePlatform, toUser))
                    msg['usrID'] = ""
                    msg['usrName'] = toUser     #调整toUser
                    msg['usrNameNick'] = ""
                #转发消息
                usrMQ.Send_Msg(usrMQ.nameQueue, str(msg))
                myDebug.Print("消息管理器转发::", usrMQ.nameQueue + ">> ",strMsg)
    #运行（线程检测, 异步延时发送）
    def OnHandleMsg_ByThread(self): 
        try:
            #线程循环
            while self.isRuning:
                try:
                    #循环所有缓存进行处理
                    for x in self.usrMsgs_Buffer:
                        bNeedSend = False
                        time = x.get("timeLimit", "")
                        if(time == "" and myData_Trans.Is_Numberic(time)):
                            bNeedSend = True
                        else:
                            if(type(time) != datetime.datetime):
                                time = myData_Trans.Tran_ToDatetime(time)
                            time_N = datetime.datetime.now() 
                            if(time_N >= time): 
                                bNeedSend = True

                        #消息发送
                        if(bNeedSend == False): continue
                        x['timeLimit'] = ""
                        self.OnHandleMsg(x, "")
                        self.usrMsgs_Buffer.remove(x)
                
                    # 延时
                    self.OnHandleMsg_ByThread_sleep(0.5)
                except :
                    myDebug.Error("Err:: Run_OnHandleMsg_ByThread... ")
        except :
            myDebug.Error("Err:: Run_OnHandleMsg_ByThread... Restart...")
        myDebug.Print('Thread Run_OnHandleMsg_ByThread is exiting...')
    #运行（线程延时，直接写报错）
    def OnHandleMsg_ByThread_sleep(self, nSleep): 
        time.sleep(nSleep)
    #消息内容校正
    def OnHandleMsg_Check(self, msg, plat = ""):
        if(msg == None): return
        usrName = msg.get('usrName', "")
        if(len(usrName) > 2 and usrName[0:2] == "@*"):      #用户为群用户
            if(msg.get('groupID', "") == "" and msg.get('groupName', "") == ""):
                msg['groupID'] = ""
                msg['groupName'] = usrName[2:]
                msg['usrID'] = ""
                msg['usrName'] = ""
                msg['usrNameNick'] = ""
        if(plat != ""): msg['usrPlat'] = plat
        return True
 
    #创建新消息
    def OnCreatMsg(self, bCreatTime = True):
        msg = copy.deepcopy(self.msgExramp)
        if(bCreatTime):
            msg['time'] = myData_Trans.Tran_ToTime_int()
        return msg
    #创建封装用户信息
    def OnCreatMsg_UsrInfo(self, usrID, usrName, nameNick, usrPlat, groupID, groupName, nameSelf):
        usrInfo = {}
        usrInfo['usrID'] = usrID
        usrInfo['usrName'] = usrName
        usrInfo['usrNameNick'] = nameNick
        usrInfo['usrPlat'] = usrPlat
        usrInfo['groupID'] = groupID
        usrInfo['groupName'] = groupName
        usrInfo['usrNameSelf'] = nameSelf      #自己发自己标识 
        return usrInfo

    #消息超时校检
    def Check_TimeOut(self, msg, nTimeOut = 600, nTimeNow = -1):  
        #时间校检, 十分钟内缓存数据有效(过早时间数据忽略)
        msgTime = msg.get('time', -1)
        if(nTimeNow < 0): nTimeNow = myData_Trans.Tran_ToTime_int()
        if(abs(msgTime - nTimeNow) >= 600): 
            myDebug.Warnning("已超时::", nTimeNow, ",", msgTime)
            return True
        return False
    
              
#初始全局消息管理器
from myGlobal import gol 
gol._Init()     #先必须在主模块初始化（只在Main模块需要一次即可）
gol._Set_Setting('bufferMsgs', myMsgs("zxc", "zxc", "", ""))    #实例 消息缓存
gol._Set_Setting('manageMsgs', myManager_Msg())                 #实例 消息管理器并初始消息api及消息队列 
gol._Get_Setting('manageMsgs', None)._Init(plat = myMsgPlat.robot, msgMQ_Sender = myMQ_Rabbit.myMQ_Rabbit(True, 'zxcMQ_robot'), msgUrl_API = "")    #不使用api回调
gol._Get_Setting('manageMsgs', None)._Init(plat = myMsgPlat.wx, msgMQ_Sender = myMQ_Rabbit.myMQ_Rabbit(True, 'zxcMQ_wx'), msgUrl_API = "", usrHelper = 'filehelper')    #不使用api回调


if __name__ == '__main__':
   pMMsg = gol._Get_Setting('manageMsgs')
   pMMsg.Init_LogDir("D:/myGit/zxcProj/src/Zxc.Python/zxcPy.Robot/Log/Msgs/")

   #组装消息 
   msg = pMMsg.OnCreatMsg()
   msg["usrName"] = "茶叶一主号"
   msg["usrID"] = "zxcID"
   msg["msg"] = "测试消息py"
   msg["msgID"] = "msgID-***"
   msg["msgType"] = "TEXT"
   msg["usrPlat"] = "wx"
   pMMsg.OnHandleMsg(msg)

   #msg["usrName"] = "@*股票行情监测群"
   pMMsg.OnHandleMsg(msg)
   pMMsg.OnHandleMsg(msg, '', True)     #必须check
   msg["msg"] = "测试消息py--延时"
   msg["usrName"] = "@*测试群"
   msg["msg"] = "测试股票: 10.37 元, 回撤逾1.4%.\r\n操作策略: 建议止盈, 操作2.0成仓, 卖出2000股.\r\n策略收益: 7.0%, 总收益 9.0%, 涨幅前高 10.5%, 最高13.5%."
   pMMsg.OnHandleMsg(msg, '', False, 5)
   
   msg["usrName"] = "@*测试群"
   msg["msgType"] = "IMage"
   msg["msg"] = "E:\\myCode\\zxcProj\\src\\Zxc.Python\\zxcPy.Weixin/Data/Pic/QR.png"
   pMMsg.OnHandleMsg(msg, '', True)
   print()

    

   #消息日志
   pMMsg.Log("zxcID", "茶叶一主号", "", "测试消息py-00", "")
   pMMsg._Log(msg)
   print(pMMsg._Find_Log("zxcID", "茶叶一主号", "").Find(msg["msgID"]))
   
   time.sleep(13)
   gol._Close()
   print()
    