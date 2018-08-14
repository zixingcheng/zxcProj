#-*- coding: utf-8 -*-
"""
Created on  张斌 2017-11-17 12:16:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com

    Python的Robot消息处理接口(文本消息)
"""
import os, ast, time, threading  
import mySystem 
    
#引用根目录类文件夹--必须，否则非本地目录起动时无法找到自定义类
mySystem.Append_Us("../Prjs", False, __file__)
mySystem.Append_Us("../Roots", False, __file__)
mySystem.Append_Us("", False)    
import myWeb, myImport, myData, myDebug, myManager_Msg, myMQ_Rabbit
import myRoot, myRoot_Usr
from myGlobal import gol 


#机器人消息处理工厂类（所有消息从此处走）
class myRobot_Reply():
    def __init__(self, useMQ = True): 
        self.usrTag = ""
        self.usrName = ""
        self.usrNameNick = ""
        self.usrReplys = myRoot_Usr.myRoot_Usrs("", "")   #消息用户集
        self.usrMQ_Recv = None   #消息队列队形       
        self.isUseMQ = useMQ     #是否允许使用消息队列
        self._Init()             #按全局权限初始
        self._Init_MQ()          #初始消息队列
        #self.wxDos = {}         #消息处理类
        #self.wxUser_Root = None #当前授权用户对象(避免频繁查找)
        myDebug.Print("消息处理工厂--已初始 (%s::%s--%s)" % (self.usrName, self.usrNameNick, self.usrTag))
    def _Init(self): 
        #初始用户全局功能权限对象 
        self.root = gol._Get_Value('rootRobot')     #权限信息
        if(self.root != None):
            self.usrName = self.root.usrName
            self.usrNameNick =self.root.usrNameNick
            self.usrTag =self.root.usrID
            self.usrReplys = myRoot_Usr.myRoot_Usrs(self.usrName, self.usrTag)   #消息用户集
    def _Init_MQ(self): 
        if(self.isUseMQ == False): return

        #初始消息接收队列
        self.usrMQ_Name = 'zxcMQ_Robot'
        self.usrMQ_Recv = myMQ_Rabbit.myMQ_Rabbit(False)
        self.usrMQ_Recv.Init_Queue(self.usrMQ_Name, True, False)
        self.usrMQ_Recv.Init_callback_RecvMsg(self.callback_RecvMsg)    #消息接收回调
            
        #接收消息--x线程方式
        self.thrd_MQ = threading.Thread(target = self.usrMQ_Recv.Start)
        self.thrd_MQ.setDaemon(False)
        self.thrd_MQ.start()
        #self.usrMQ_Recv.Start()
        myDebug.Print("消息队列创建成功...")
        
    #处理封装返回消息(按标识内容处理)
    def Done_ByMsg(self, msg):
        myDebug.Print("请求消息:: ", msg)
        if(msg == None): return None

        #提取消息内容（自定义格式类型 myManager_Msg.OnCreatMsg）
        usrID = msg.get('usrID', "")
        usrName = msg.get('usrName', "")
        usrNameNick = msg.get('usrNameNick', "")

        msgText = msg.get('msg', "")
        msgID = msg.get('msgID', "")
        msgType = msg.get('msgType', "")
        plat = msg.get('plat', "")
        groupID = msg.get('groupID', "")
        isGroup = myData.iif(groupID == "", False, True)

        #按消息类型进一步处理('TEXT', 'IMAGE', 'VOICE', 'VIDEO')
        if(msgType == myManager_Msg.myMsgType.TEXT):
            msgText = msgText
        else:
            return None 

        #调用 
        return self.Done(usrID, usrName, usrNameNick, msgText, msgID, plat, isGroup, groupID)
    #按命令处理返回消息(按标识内容处理)
    def Done(self, usrID, usrName, nickName, strText, msgID = "", usrPlant = "", isGroup = False, idGroup = ""):
        #命令识别
        pPrj = None 
        pUser = None 
        if(strText[0:2] == "@@"):
            pPrj, pUser = self._Create_Cmd(usrID, usrName, nickName, strText[2:], isGroup, idGroup, usrPlant)
        else:
            #查找用户
            pUser = self._Find_Usr(usrID, usrName, nickName, "", usrPlant)
      
        #查找用户, 调用消息处理方法调用
        if(pUser != None):
            return pUser.Done(pPrj, strText, msgID, isGroup, idGroup)
        return None
    #定义消息接收方法回调
    def callback_RecvMsg(self, body):
        msg = ast.literal_eval(body) 
        #myDebug.Debug("接收队列消息::", msg['msg'])  
        myDebug.Debug("处理消息::", self.Done_ByMsg(msg)['Text'])

    #查找用户（不存在则自动创建）
    def _Find_Usr(self, usrID, usrName, usrName_Nick, usrID_sys = "", usrPlant = ""): 
        #按消息生成对应对象 
        pUser = self.root.usrInfos._Find(usrName_Nick, usrName, usrID, usrID_sys, usrPlant, False)
        if(pUser == None):      #非参与用户，于全局用户集信息提取，不存在的自动生成
            pUser = self.root.usrInfos._Find(usrName_Nick, usrName, usrID, usrID_sys, usrPlant, True)
            pUser.usrPrj._Add_prjDos(self.root.rootPrjs)
            self.usrReplys._Add(pUser)
        return pUser
    #是否管理员账户（直接提升权限）
    def _IsRoot_Usr(self, usrName):
        pRoot = self.wxRoot.prjRoots_user.get(usrName.lower()) 
        if pRoot == None : return False
        if pRoot.prjRoot == False : return False
        return True
    #是否可启动命令用户
    def _IsEnable_Usr(self, pUser, pPrj, isGroup, pGroup = None):
        #必须可用
        if(pPrj.IsEnable() == False): return False

        #区分是否运行状态，非运行，必须root用户启用
        bIsRoot = pPrj.IsRoot_user(pUser)   #查找用户权限 
        if(pPrj.IsRunning() == False):
            if(bIsRoot == False): return False 
        else:   #运行时，仅非统一启动时，需要个人启动
            if(pPrj.IsEnable_All() == False): return False
            
        #群有效区分
        if(isGroup):                     #群有效，且为设置群
            return pPrj.IsEnable_group(pGroup)
        else:
            return pPrj.IsEnable_one()   #单人有效(一对一)
            
    #命令处理（@@命令，一次开启，再次关闭）
    def _Create_Cmd(self, usrID, usrName, nickName, prjCmd, isGroup, idGroup, usrPlant = ""):    
        #查找功能权限对象
        pPrj = self.root.rootPrjs._Find(prjCmd)
        if(pPrj == None):
            print(">>Create Prj(%s) Faield" % (prjCmd))
            return None, None, None
        if(pPrj.IsEnable() == False): return None, None     #必须启用

        #查找用户（功能开启全部可用则当前用户）  
        pUser = self._Find_Usr(usrID, usrName, nickName, "", usrPlant)   
        if(pUser == None): return None, None

        #功能权限验证 
        bEnable = self._IsEnable_Usr(pUser, pPrj, isGroup, idGroup)
        if(bEnable == False): return None, None             #必须可用

        #动态实例 (非单例，单独实例并缓存) 
        if(pPrj.IsRunSingle() == False):      
            prjClass = pPrj.creatIntance()          #实例对象--专有      
            prjClass.isRunning = pPrj.isRunning     #同步运行状态
            pUser.usrPrj._Change_prjDo(prjClass)    #切换功能 
        return pPrj, pUser  
     

#主启动程序
if __name__ == "__main__":
    #sys.path.append("C:\Python35-32\Lib\site-packages\myPy_Libs")

    #动态实例测试
    pWxdo2 = myImport.Import_Class("myRobot_Repeater","myRobot_Repeater")('zxc', 'zxcID');
    print( pWxdo2.Done("@@Repeater"))
    print( pWxdo2.Done("Hello"))
    print( pWxdo2.Done("Bye"))
    print( pWxdo2.Done("@@Repeater"))
    print("\n\n")

    #机器人消息处理
    pWxReply = myRobot_Reply()
    pWxReply._Init()
    pWxReply._Init_MQ
    
    #用户信息
    usrID = "zxc_0"
    usrName = "墨紫_0"
    nickName = "墨紫"
    usrPlant = "wx"
    msgID = ""

    
    #复读机功能测试
    pWxReply.Done(usrID, usrName, nickName, '@@Repeater', msgID, usrPlant)
    print(pWxReply.Done(usrID, usrName, nickName, 'Hello Rep', msgID, usrPlant))
    print(pWxReply.Done(usrID, usrName, nickName, 'zxczxc', "@zxcvbnm", usrPlant))
    print(pWxReply.Done(usrID, usrName, nickName, 'Bye Repeater', msgID, usrPlant))
    pWxReply.Done(usrID, usrName, nickName, '@@Repeater', msgID, usrPlant) 
    print()

    #复读功能再次开启与关闭
    pWxReply.Done(usrID, usrName, nickName, '@@Repeater', msgID, usrPlant) 
    pWxReply.Done(usrID, usrName, nickName, '@@Repeater', msgID, usrPlant)  
    print()


    #聊天机器人测试
    pWxReply.Done(usrID, usrName, nickName, '@@ChatRobot', msgID, usrPlant) 
    print(pWxReply.Done(usrID, usrName, nickName, 'Hello Robot', msgID, usrPlant))
    print(pWxReply.Done(usrID, usrName, nickName, 'God Job...', msgID, usrPlant))
    print(pWxReply.Done(usrID, usrName, nickName, 'Bye Robot', msgID, usrPlant))
    pWxReply.Done(usrID, usrName, nickName, '@@ChatRobot', msgID, usrPlant) 
    print()


    #交互启动测试 
    pWxReply.Done(usrID, usrName, nickName, '@@Repeater', msgID, usrPlant) 
    pWxReply.Done(usrID, usrName, nickName, '@@ChatRobot', msgID, usrPlant) 
    print(pWxReply.Done(usrID, usrName, nickName, 'Hello ChatRobot...', msgID, usrPlant))
    
   #队列消息测试
    if(True):
        nameMQ = 'zxcMQ_Robot'
        pMQ_Send = myMQ_Rabbit.myMQ_Rabbit(True)
        pMQ_Send.Init_Queue(nameMQ, True)
         
        pMQ_Recv = myMQ_Rabbit.myMQ_Rabbit(False)
        pMQ_Recv.Init_Queue(nameMQ, True, False)
        pMQ_Recv.Init_callback_RecvMsg(pWxReply.callback_RecvMsg)
        #pMQ_Recv.Init_callback_RecvMsg(pMQ_Recv.Recv_Msg)
    
        #接收消息线程
        thrdMQ = threading.Thread(target = pMQ_Recv.Start)
        thrdMQ.setDaemon(False)
        #thrdMQ.start()  

        #循环测试
        nTimes = 5
        pMMsg = myManager_Msg.myManager_Msg()
        msg = pMMsg.OnCreatMsg()
        msg["usrID"] = usrID
        msg["usrName"] = usrName
        msg["usrNameNick"] = nickName
        msg["plat"] = usrPlant
    
        for x in range(0, nTimes):
            #发送消息
            msg["msg"] = "hello world " + str(x)
            pMQ_Send.Send_Msg(nameMQ, str(msg))
            print("[生产者] send '", msg)

            #myDebug.Debug(pWxReply.Done_ByMsg(msg))
            time.sleep(0.01) 

    pWxReply.Done(usrID, usrName, nickName, '@@ChatRobot', msgID, usrPlant) 
    print()



    #消息提取测试
    #pMsg = pR.msgLogs._Find_Log("zxcID").Find("@zxcvbnm")

    exit()

 
 
