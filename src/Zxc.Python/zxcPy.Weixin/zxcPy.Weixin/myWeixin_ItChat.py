#-*- coding: utf-8 -*-
"""
Created on  张斌 2017-11-17 12:16:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com

    Python的Weixin网页版接口封装(使用itchat封装)
"""
import sys, os, time, re, ast, threading, mySystem 
import itchat
from itchat.content import *
from atexit import register

#引用根目录类文件夹--必须，否则非本地目录起动时无法找到自定义类
#mySystem.Append_Us("/Weixin_Reply", False, __file__)
#mySystem.Append_Us("/Weixin_Reply/myWxDo", False, __file__)
mySystem.Append_Us("", False) 
import myError, myIO, myDebug, myMMap, myThread, myDebug, myData_Trans, myMQ_Rabbit
import myReply_Factory    
from myGlobal import gol 


#webWeixin接口封装类
class myWeixin_ItChat(myThread.myThread):
    def __init__(self, Tag = "zxcWeixin", useCmdMMap = True):
        super().__init__("", 0) # 必须调用
        self.usrTag = Tag       #类实例标识
        self.usrName = ""       #类实例用户名
        self.wxReply = myReply_Factory.myWx_Reply(Tag)     #回复消息处理工厂对象类
        self.usrDefault = {'UserName' : ""}
        self.Init()             #文件初始
        self.ind = 0
        self.max = 5
        #self.cmdWeixin = None
        
        self.isRuning = False           #是否运行中
        self.Auto_RreplyText = True     #是否开启自动回复--文本
        self.Auto_RreplyText_G = True   #是否开启自动回复--文本-群
        self.funStatus_RText = False    #状态自动回复--文本
        self.funStatus_RText_G = False  #状态自动回复--文本-群
        self.managerMMap = None         #接收共享内存
        self.mqRecv = None              #接收消息队列     
        self.mqTimeNow = 0              #接收时间--当前
        self.Init_MsgCache(useCmdMMap)  #创建消息通讯缓存
    def Init(self, dir = "", pathPicDir = ""):
        if (dir == ""):
            strDir, strName = myIO.getPath_ByFile(__file__)
            self.dirBase = os.path.abspath(os.path.join(strDir, ".."))  
        else:
            self.dirBase = dir
            
        #初始根目录信息
        self.dirSetting = self.dirBase + "/Setting/"
        self.dirData = self.dirBase + "/Data/"
        if(pathPicDir == ""): pathPicDir = self.dirData
        self.dirPic = pathPicDir + "Pic/"
        myIO.mkdir(self.dirPic, False)

    #初始消息通讯缓存    
    def Init_MsgCache(self, useCmdMMap = True):
        self.useCmdMMap = useCmdMMap
        if(useCmdMMap): return self.Init_MMap()
        return True
    #创建命令内存映射 
    def Init_MMap(self, useCmdMMap = True):
        # 创建内存映射（读）
        try:
            self.managerMMap = myMMap.myMMap_Manager(self.dirData + "zxcMMap.dat")
            pMMdata_M2, ind2 = self.managerMMap.Read(0)
            if(pMMdata_M2 != None):
                myDebug.Print(pMMdata_M2.value, ind2)
            return True
        except:
            print()
            myDebug.Print("创建内存映射失败.")
            return False
    #创建消息队列 
    def Init_MQ(self, bStart = False):
        #初始消息接收队列
        self.mqName = 'zxcMQ_wx'
        if(self.mqRecv == None):
            self.mqRecv = myMQ_Rabbit.myMQ_Rabbit(False)
            self.mqRecv.Init_Queue(self.mqName, True, False)
            self.mqRecv.Init_callback_RecvMsg(self.callback_RecvMsg)    #消息接收回调
            myDebug.Print("消息队列(" + self.mqName + ")创建成功...")
            
        #接收消息--x线程方式
        self.thrd_MQ = threading.Thread(target = self.mqRecv.Start)
        self.thrd_MQ.setDaemon(False)
        if(bStart): 
            self.thrd_MQ.start()
            self.mqTimeNow = myData_Trans.Tran_ToTime_int()   #接收开始时间

    #运行
    def run(self): 
        self.Run_ByThread();
  
    #登陆
    def Logion(self, bSave = True, bSave_HeadImg = False): 
        #二维码路径组装
        pathPic = self.dirPic + "QR.png" 
        patStatusStorage = self.dirData + 'zxcWeixin.pkl'

        #登录微信网页版(二维码扫码)
        myDebug.Print('登陆验证中...')
        itchat.auto_login(hotReload = True, enableCmdQR = False, statusStorageDir = patStatusStorage, picDir = pathPic,
                           qrCallback = None, loginCallback = self._Logioned, exitCallback = self._LogionOuted)

        #获取所有好友信息
        #friends = itchat.get_friends() 
        friends = itchat.get_friends(update = True)[0:]   # 核心：得到frieds列表集，内含很多信息
        groups  = itchat.get_chatrooms(update = True)
        
        #获取自己的UserName
        self.usrFriends = friends
        self.usrName = friends[0]['UserName']
        self.usrName_Alias = friends[0]['NickName']
        gol._Set_Value('zxcWx_usrName', self.usrName)
        gol._Set_Value('zxcWx_usrName_Alias', self.usrName_Alias)
        myDebug.Print("    --授权微信用户为：" + self.usrName_Alias + self.usrName)

        #更新用户信息（回复消息处理工厂对象类）
        self.wxReply._Init(self.usrName, self.usrName_Alias)
        

        #消息发送测试
        #self.Send_Msg("", "茶叶一主号", "测试消息", "TEXT", 0)
        #self.Send_Msg("", "测试", "测试消息", "TEXT", 1)
 
        #将friends列表存下来，看看内容
        if(bSave):
            #创建文件夹用于装载所有好友头像
            self.dirPic_Head = self.dirPic + "Head/" + self.usrName_Alias + "/"
            myIO.mkdir(self.dirPic_Head, False)

            #创建主信息文件
            self.dirFriends = self.dirData + "Firends" + "/"  
            myIO.mkdir(self.dirFriends, False)
            w = open(self.dirFriends + self.usrName_Alias + "_friends", 'a', encoding = 'utf-8', errors = 'ignore')  
            
            #循环写入所有
            num = 0
            for user in friends:
                w.write(str(user))

                #用户图像
                if(bSave_HeadImg):
                    img = itchat.get_head_img(userName = user["UserName"])
                    fileImage = open(self.dirPic_Head + "/" + str(num) + ".jpg",'wb')
                    fileImage.write(img)
                    fileImage.close()
                    num += 1
            
            #得到user目录下的所有文件，即各个好友头像
            pics = os.listdir(self.dirPic_Head)    
            numPic = len(pics)
            myDebug.Print("    --微信好友图像数：" + str(numPic) + "\n")  
    #查找用户       
    def Get_User(self, usrID = "", usrName = ""):
        if(usrID[0:1] == "@"):
            pUsers = itchat.search_friends(userName = usrID)
            if(pUsers != None and len(pUsers) == 1): return pUsers[0]

        #统配查询所有
        if(usrID != ""):
            pUsers = itchat.search_friends(name = usrID)
            if(pUsers != None and len(pUsers) == 1): return pUsers[0]
        if(usrName != ""):
            pUsers = itchat.search_friends(name = usrName)
            if(pUsers != None and len(pUsers) == 1): return pUsers[0]

        myDebug.Error("用户未找到::", usrID, usrName)
        return self.usrDefault  
    #查找群       
    def Get_User_group(self, roupID = "测试", groupName = ""):
        if(roupID[0:2] == "@@"):
            pUsers = itchat.search_chatrooms(userName = roupID)
            if(pUsers != None and len(pUsers) == 1): return pUsers[0]

        #统配查询所有
        if(roupID != ""):
            pUsers = itchat.search_chatrooms(name = roupID)
            if(pUsers != None and len(pUsers) == 1): return pUsers[0]
        if(groupName != ""):
            pUsers = itchat.search_chatrooms(name = groupName)
            if(pUsers != None and len(pUsers) == 1): return pUsers[0]

        myDebug.Error("用户群未找到::", roupID, groupName)
        return self.usrDefault    

    #发送消息接口(Json的msg)
    def _Send_Msg(self, msgInfo): 
        if(type(msgInfo)== str):
            msg = myData_Json.Trans_ToJson(msgInfo)
        elif(type(msgInfo)== dict):
            msg = msgInfo
        elif(type(msgInfo)== myData_Json.Json_Object):
            msg = msgInfo
        else:
            return False

        #增加记录日志--消息管理器实现 

        #调用 
        return self.Send_Msg(msg.get('usrID', ""), msg['usrName'], msg['msg'], msg['msgType'])
    #发送消息接口(typeUser, 0: 好友 1：群 2：公众号)
    def Send_Msg(self, usrID, usrName = "", msgInfo = "" , typeMsg = "TEXT", typeUser = 0):
        #用户检测(@开头为用户名，filehelper，其他需要检索实际用户名)
        if(typeUser == 0):
            pUser = self.Get_User(usrID, usrName)
        else:
            pUser = self.Get_User_group(usrID, usrName)
        userName = pUser['UserName']
        if(userName == ""): return 

        #发送消息
        typeMsg = typeMsg.upper()
        if(typeMsg == "TEXT"):
            itchat.send('%s' % (msgInfo), userName)
        elif(typeMsg == "IMage"):   #未实现
            itchat.send_image('%s: %s' % (typeMsg, msgInfo), userName)
        else:
            myDebug.Print("No this type.")
    #提取格式化返回信息 
    def Get_Msg_Back(self, msg, isGroup = False):
        #回复操作调用 
        msgR = self.wxReply.Done_ByMsg(msg, isGroup)    #兼容API方式，消息队列无返回        
        if(msgR == None): return None
        
        #回复自己判断(调整为目标用户)
        myDebug.Debug("消息回复::", msgR)
        if(msgR.get('isSelf', False) == True):          #自己时，主动发送个对方处理信息(无法自动回复给自己)
            self.Send_Msg(msgR['usrID'], msgR['usrName'], msgR['msg'], msgR['msgType'])
        else:
            self.Send_Msg(msgR['usrID'], msgR['usrName'], msgR['msg'], msgR['msgType'])
        return None
    #定义消息接收方法回调
    def callback_RecvMsg(self, body):
        if(self.isRuning):   
            return self.Run_Monitor_Cmd_ByMQ(body)
        return False

            
    #二维码信息下载完回调函数
    def _DownloadQRed(self, uuid, status, qrcode): 
        myDebug.Print('二维码下载本地完毕')
        myDebug.Print(uuid)
        myDebug.Print(status)
        myDebug.Print(qrcode)  
    #登陆后回调函数
    def _Logioned(self):
        myDebug.Print('登陆验证完成')
    #登出后回调函数
    def _LogionOuted(self):
        myDebug.Print('系统已退出')
         
        
    #运行（单线程）
    def Run2(self):
        #文本消息处理
        @itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING])
        def text_reply(msg):
            pReply = self.wxReply.Done(msg['FromUserName'],msg['Text'])
            if(pReply != None): 
                return pReply['Text']
        itchat.run() 
    #运行-停止
    def Stop(self):
        self.isRuning = False
            
    #运行（线程检测）
    def Run_ByThread(self, nSleep = 0.1):
        try:
            #创建微信线程
            self.thrd_Replay = threading.Thread(target = itchat.run)
            self.thrd_Replay.setDaemon(False)
            self.thrd_Replay.start()
            
            #创建消息队列 
            self.isRuning = True
            self.Init_MQ(bStart = True)

                    
            #线程循环
            while self.isRuning:
                try:
                    #运行（监测, 用于线程内部） 
                    self.Run_Monitor()  
            
                    #命令监测--共享内存方式 
                    if(self.useCmdMMap):
                        self.Run_Monitor_Cmd_ByMMP()
                    time.sleep(nSleep)
                except :
                    myDebug.Error("Err:: Run_Monitor... ")
        except :
            myDebug.Error("Err:: Run_ByThread... Restart...")
        myDebug.Print('Thread is exiting...')
    #运行（监测, 用于线程内部） 
    def Run_Monitor(self):
        #注册普通文本消息回复(一对一)
        if self.Auto_RreplyText != self.funStatus_RText:
            #注册普通文本消息回复                 
            @itchat.msg_register([NOTE, TEXT], isFriendChat=True)
            def Reply_Text(msg): 
                if self.Auto_RreplyText: 
                    #提取回复消息内容
                    myDebug.Debug("消息接收::", msg['Content'])
                    return self.Get_Msg_Back(msg)               #格式化提取(兼容API方式，消息队列无返回)
            self.funStatus_RText = self.Auto_RreplyText

        #注册普通文本消息回复(群消息)    
        if self.Auto_RreplyText_G != self.funStatus_RText_G:
            #注册普通文本消息回复                 
            @itchat.msg_register([NOTE, TEXT, FRIENDS], isGroupChat=True)
            def Reply_Text_Group(msg): 
                if self.Auto_RreplyText_G: 
                    #提取回复消息内容
                    return self.Get_Msg_Back(msg, True)         #格式化提取(兼容API方式，消息队列无返回)
            self.funStatus_RText_G = self.Auto_RreplyText_G
       
        # 收到note通知类消息，判断是不是撤回并进行相应操作
        @itchat.msg_register([NOTE], isMpChat=True)
        def send_msg_helper(msg):
            def Reply_Text_Group(msg): 
                if self.Auto_RreplyText_G: 
                    #提取回复消息内容
                    return self.Get_Msg_Back(msg, True, True)   #格式化提取(兼容API方式，消息队列无返回)

            global face_bug
            if re.search(r"\<\!\[CDATA\[.*撤回了一条消息\]\]\>", msg['Content']) is not None:
                # 获取消息的id
                old_msg_id = re.search("\<msgid\>(.*?)\<\/msgid\>", msg['Content']).group(1)
                old_msg = msg_dict.get(old_msg_id, {})
                if len(old_msg_id) < 11:
                    itchat.send_file(rev_tmp_dir + face_bug, toUserName='filehelper')
                    os.remove(rev_tmp_dir + face_bug)
                else:
                    msg_body = "告诉你一个秘密~" + "\n" \
                               + old_msg.get('msg_from') + " 撤回了 " + old_msg.get("msg_type") + " 消息" + "\n" \
                               + old_msg.get('msg_time_rec') + "\n" \
                               + "撤回了什么 ⇣" + "\n" \
                               + r"" + old_msg.get('msg_content')
                    # 如果是分享存在链接
                    if old_msg['msg_type'] == "Sharing": msg_body += "\n就是这个链接➣ " + old_msg.get('msg_share_url')

                    # 将撤回消息发送到文件助手
                    itchat.send(msg_body, toUserName='filehelper')
                    # 有文件的话也要将文件发送回去
                    if old_msg["msg_type"] == "Picture" \
                            or old_msg["msg_type"] == "Recording" \
                            or old_msg["msg_type"] == "Video" \
                            or old_msg["msg_type"] == "Attachment":
                        file = '@fil@%s' % (rev_tmp_dir + old_msg['msg_content'])
                        itchat.send(msg=file, toUserName='filehelper')
                        os.remove(rev_tmp_dir + old_msg['msg_content'])
                    # 删除字典旧消息
                    msg_dict.pop(old_msg_id)
    #命令监测--共享内存方式 
    def Run_Monitor_Cmd_ByMMP(self):     
        if(self.managerMMap == None): 
            return False
        nNum = 0
        pMMdata_M, self.ind = self.managerMMap.Read(self.ind, True)
        while(pMMdata_M != None):
            #调用发送消息
            nNum += 1
            msg = pMMdata_M.value
            if(msg != None and msg != 0):
                self.Send_Msg(msg['usrID'], msg['usrName'], msg['msg'], msg['msgType'])
                myDebug.Print(msg)

                #再次提取命令
                if(nNum >= self.max): return 
                pMMdata_M, self.ind = self.managerMMap.Read(self.ind, True)
    #命令监测--消息队列方式 
    def Run_Monitor_Cmd_ByMQ(self, strMsg):  
        try:
            myDebug.Debug("接收队列消息wx::", strMsg)  
            msg = ast.literal_eval(strMsg) 
            
            #时间校检, 十分钟内缓存数据有效(过早时间数据忽略)
            if(self.wxReply.Check_TimeOut(msg)):
                myDebug.Debug("--队列消息已超时wx::", strMsg)  
                return True

            #消息发送
            if(msg.get('groupID', "") != ""):
                self.Send_Msg(msg['usrID'], msg['groupID'], msg['msg'], msg['msgType'], 1)
            else:
                self.Send_Msg(msg['usrID'], msg['usrName'], msg['msg'], msg['msgType'])
            return True
        except Exception as ex:
            myError.Error(ex)  
            return True

            
#webWeixin接口--命令封装类--未使用
#线程
class myWeixin_CmdThread (threading.Thread):  #继承父类threading.Thread
    def __init__(self, managerMMap):
        super().__init__()              #必须调用
        self.managerMMap = managerMMap  #内存映射
        self.ind = 0
        self.exitFlag = False

    #把要执行的代码写到run函数里面 线程在创建后会直接运行run函数 
    def run(self):                   #把要执行的代码写到run函数里面 线程在创建后会直接运行run函数 
        myDebug.Print("Starting " + self.name)
        i = 0
        while not self.exitFlag: 
            self.ind = 0
            pMMdata_M, self.ind = self.managerMMap.Read(0, False)
            if(pMMdata_M != None):
                #发送消息
                dict0 = pMMdata_M.value
                itchat.send(dict0["Text"], dict0["FromUserName"])
                #itchat.send('%s: %s' % (typeMsg, msgInfo), userFrom)
        myDebug.Print("Exiting Manager MMap.")

    #退出接口
    def _stop(self):   
        threading.Thread._stop(self)     
        self.exitFlag = True     
   

#主启动程序
if __name__ == "__main__":
    #声明Weixin操作对象
    pWeixin = myWeixin_ItChat('zxcWx', False)
    
    #登录微信网页版(二维码扫码)
    pWeixin.Logion();
 
    #消息测试
    #pWeixin.Send_Msg("", "茶叶一主号","登陆")

    #运行 
    #pWeixin.Run();
    pWeixin.Run_ByThread();

    #退出
    exit()

