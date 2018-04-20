#-*- coding: utf-8 -*-
"""
Created on  张斌 2017-11-17 12:16:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com

    Python的Weixin网页版接口封装(使用itchat封装)
"""

import sys, os, time, threading, mySystem 
import itchat
from itchat.content import *


#引用根目录类文件夹--必须，否则非本地目录起动时无法找到自定义类
mySystem.m_strFloders.append('/Weixin_Reply')
mySystem.m_strFloders.append('/Weixin_Reply/myWxDo')
mySystem.Append_Us("", False) 
import myWeb, myError, myData_Json, myIO, myThread, myReply_Factory  #myDataSet, myData, myData_Trans 


#webWeixin接口封装类
class myWeixin_ItChat(myThread.myThread):
    def __init__(self, Tag = "zxcWeixin"):
        super().__init__("", 0) # 必须调用
        self.usrTag = Tag       #类实例标识
        self.usrName = ""       #类实例用户名
        self.wxReply = myReply_Factory.myWx_Reply(Tag)     #回复消息处理工厂对象类
        self.dirData = self.wxReply.wxRoot.Dir_Data
        self.dirPic = self.wxReply.wxRoot.Dir_Data + "Pic/" 
        
        self.Runing = False             #是否运行中
        self.Auto_RreplyText = True     #是否开启自动回复--文本
        self.Auto_RreplyText_G = True   #是否开启自动回复--文本-群
        self.funStatus_RText = False    #状态自动回复--文本
        self.funStatus_RText_G = False  #状态自动回复--文本-群
        self.Init()        
    def Init(self, pathPicDir = ""):
        if (pathPicDir == ""):
            self.dirData = self.wxReply.wxRoot.Dir_Data
            self.dirPic = self.wxReply.wxRoot.Dir_Data + "Pic/"
            myIO.mkdir(self.dirPic)
    #运行
    def run(self): 
        self.Run_ByThread();
  
    #登陆
    def Logion(self, bSave = True, bSave_HeadImg = False): 
        #二维码路径组装
        pathPic = self.dirPic + "QR.png" 
        patStatusStorage = self.dirData + 'zxcWeixin.pkl'

        #登录微信网页版(二维码扫码)
        print('\n>>登陆验证中...')
        itchat.auto_login(hotReload = True, enableCmdQR = False, statusStorageDir = patStatusStorage, picDir = pathPic,
                           qrCallback = None, loginCallback = self._Logioned, exitCallback = self._LogionOuted)

        #获取所有好友信息
        #friends = itchat.get_friends() 
        friends = itchat.get_friends(update = True)[0:]   # 核心：得到frieds列表集，内含很多信息
        
        #获取自己的UserName
        self.usrFriends = friends
        self.usrName = friends[0]['UserName']
        self.usrName_Alias = friends[0]['NickName']
        print("    --授权微信用户为：" + self.usrName_Alias + self.usrName)

        #更新用户信息（回复消息处理工厂对象类）
        self.wxReply._Init(self.usrName, self.usrName_Alias)
        

        #将friends列表存下来，看看内容
        if(bSave):
            #创建文件夹用于装载所有好友头像
            self.dirPic_Head = self.dirPic + "Head/" + self.usrName_Alias + "/"
            myIO.mkdir(self.dirPic_Head, False)

            #创建主信息文件
            w = open(self.dirData + self.usrName + "_friends", 'a', encoding = 'utf-8', errors = 'ignore')  
            
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
            print("    --微信好友图像数：" + str(numPic) + "\n")  
            
    #发送消息接口(Json的msg)
    def Send_Msg(self, msgInfo): 
        if(type(msgInfo)== str):
            msg = myData_Json.Trans_ToJson(msgInfo)
        elif(type(msgInfo)== dict):
            msg = msgInfo
        elif(type(msgInfo)== myData_Json.Json_Object):
            msg = msgInfo
        else:
            return False

        #调用 
        return Send_Ms(msg['FromUserName'], msg['Text'], msg['Type'])
    #发送消息接口
    def Send_Msg(self, userFrom = "", msgInfo = "" , typeMsg = "TEXT"):
        #用户检测(@开头为用户名，filehelper，其他需要检索实际用户名)
        if(userFrom == ""): return
        if(userFrom[0] != "@" and userFrom != "filehelper"):      
            #查找用户
            user = itchat.search_friends(name = userFrom)
            if(len(user) != 1):
                myError.Error("用户(" + userFrom + ")未找到.")
                return
            userFrom = user[0]['UserName']

        #发送消息
        itchat.send('%s: %s' % (typeMsg, msgInfo), userFrom)
            
    #二维码信息下载完回调函数
    def _DownloadQRed(self, uuid, status, qrcode): 
        print('\n>>二维码下载本地完毕')
        print(uuid)
        print(status)
        print(qrcode)  
    #登陆后回调函数
    def _Logioned(self):
        print('\n>>登陆验证完成')
    #登出后回调函数
    def _LogionOuted(self):
        print('\n>>系统已退出')
         
        
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
        self.Runing = False
            
    #运行（线程检测）
    def Run_ByThread(self, nSleep = 0.1):
        thrd_Replay = threading.Thread(target = itchat.run)
        thrd_Replay.setDaemon(False)
        thrd_Replay.start()
        
        #线程循环
        self.Runing = True
        while self.Runing:
            self.Run_Monitor()
            time.sleep(nSleep)

        print('Thread is exiting...')
    #运行（监测, 用于线程内部） 
    def Run_Monitor(self):
        #注册普通文本消息回复(一对一)
        if self.Auto_RreplyText != self.funStatus_RText:
            #注册普通文本消息回复                 
            @itchat.msg_register(TEXT, isGroupChat = False)
            def Reply_Text_(msg): 
                if self.Auto_RreplyText: 
                    #提取回复消息内容
                    pReply = self.wxReply.Done_ByMsg(msg)
                    if(pReply != None): return pReply['Text']   #返回消息
            self.funStatus_RText = self.Auto_RreplyText

        #注册普通文本消息回复(群消息)    
        if self.Auto_RreplyText_G != self.funStatus_RText_G:
            #注册普通文本消息回复                 
            @itchat.msg_register(TEXT, isGroupChat = True)
            def Reply_Text_Group(msg): 
                if self.Auto_RreplyText_G: 
                    #提取回复消息内容
                    pReply = self.wxReply.Done_ByMsg(msg, True)
                    if(pReply != None): return pReply['Text']   #返回消息
            self.funStatus_RText_G = self.Auto_RreplyText_G
           

class myAPI_p(myWeb.myAPI):
    def get(self, param):
        strReturn = "参数：" + param
        ps_Weixin.Send_Msg("茶叶一主号",strReturn)
        return strReturn

   
#主启动程序
if __name__ == "__main__":
    #声明Weixin操作对象
    pWeixin = myWeixin_ItChat()
    
    #登录微信网页版(二维码扫码)
    pWeixin.Logion();
 
    #消息测试
    pWeixin.Send_Msg("茶叶一主号","登陆")
    pWeixin.run()

    #运行 
    #pWeixin.Run();
    pWeixin.Run_ByThread();
      

    exit()




 
