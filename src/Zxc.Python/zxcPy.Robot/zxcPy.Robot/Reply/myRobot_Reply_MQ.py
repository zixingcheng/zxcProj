#-*- coding: utf-8 -*-
"""
Created on  张斌 2017-11-17 12:16:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com

    Python的Robot消息处理接口(文本消息)（消息队列方式实现）
"""
import os, ast, time, threading  
import mySystem 
    
#引用根目录类文件夹--必须，否则非本地目录起动时无法找到自定义类
mySystem.Append_Us("../Prjs", False, __file__)
mySystem.Append_Us("../Roots", False, __file__)
mySystem.Append_Us("", False)    
import myWeb, myImport, myData, myDebug, myManager_Msg, myMQ_Rabbit, myRobot_Reply
import myRoot, myRoot_Usr
from myRobot_Reply  import myRobot_Reply


#机器人消息处理工厂类（消息队列方式实现）
class myRobot_Reply_MQ(myRobot_Reply):
    def __init__(self, bStart = True): 
        super().__init__()
        self.mqRecv = None          #消息队列(接收)
        if(bStart): self.Start()    #自动开始运行
    def _Init_MQ(self, bStart = True):     
        #初始消息接收队列
        self.mqName = 'zxcMQ_robot'
        if(self.mqRecv == None):
            self.mqRecv = myMQ_Rabbit.myMQ_Rabbit(False)
            self.mqRecv.Init_Queue(self.mqName, True, False)
            self.mqRecv.Init_callback_RecvMsg(self.callback_RecvMsg)    #消息接收回调
            myDebug.Print("消息队列(" + self.mqName + ")创建成功...")
            
        #接收消息--x线程方式
        self.thrd_MQ = threading.Thread(target = self.mqRecv.Start)
        self.thrd_MQ.setDaemon(False)
        if(bStart): self.thrd_MQ.start()

    #定义消息接收方法回调
    def callback_RecvMsg(self, body):
        if(self.isRunning):
            try:
                msg = ast.literal_eval(body) 
                myDebug.Debug("接收队列消息robot::", msg['msg'])  

                #调用消息处理(并推送消息管理器)
                self.Done_ByMsg(msg, True)
                return True
            except :
                return False
        return False
    
    #运行-开始
    def Start(self):
        self.isRunning = True
        self._Init_MQ(self.isRunning)


#主启动程序
if __name__ == "__main__":
    #机器人消息处理
    pWxReply = myRobot_Reply_MQ(True)
    
    #实例生产者、消费者
    from myGlobal import gol 
    pMMsg = gol._Get_Setting('manageMsgs')
    
    #用户信息 
    msg = {"usrID":'zxc_0', "usrName":'墨紫', "usrNameNick":'', "msg":'', "msgType":'TEXT', "plat":'wx'} #消息样例
    plat = 'robot'
       

    #复读机功能测试
    msg["msg"] = "@@Repeater" 
    pMMsg.OnHandleMsg(msg, plat)
    msg["msg"] = "@@Hello Rep"
    pMMsg.OnHandleMsg(msg, plat)
    msg["msg"] = "@@Repeater"
    pMMsg.OnHandleMsg(msg, plat)
    print()
    

    #功能测试 
    pMMsg.OnHandleMsg(msg, plat)
    
   #队列消息测试
    if(True == True): 
        #循环测试
        nTimes = 3
        msg["usrName"] = "茶叶一主号"
        msg["usrNameNick"] = ""    

        #启动自己功能
        for x in range(0, nTimes):
            #发送消息
            msg["msg"] = "hello world " + str(x)
            print("[生产者] send '", msg)
            pMMsg.OnHandleMsg(msg, plat)
            time.sleep(0.01) 
    
    #关闭交互
    msg["usrName"] = "墨紫"
    msg["msg"] = "@@Repeater"
    pMMsg.OnHandleMsg(msg, plat)
    print()


    exit()

 
 
