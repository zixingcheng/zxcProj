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
from collections import OrderedDict

#引用根目录类文件夹--必须，否则非本地目录起动时无法找到自定义类
mySystem.Append_Us("../zxcPy.DataSwap", False, __file__)
#mySystem.Append_Us("/Weixin_Reply/myWxDo", False, __file__)
mySystem.Append_Us("", False)  
import myError, myIO, myDebug, myMMap, myThread, myDebug, myData, myData_Trans, myMQ_Rabbit, myData_Swap, myData_SwapWx, myManager_Msg
import myReply_Factory   
from myGlobal import gol 



#webWeixin接口封装类
class myWeixin_ItChat(myThread.myThread):
    def __init__(self, Tag = "zxcWeixin", useCmdMMap = True, useSwap = True):
        super().__init__("", 0) # 必须调用
        self.usrTag = Tag       # 类实例标识
        self.usrName = ""       # 类实例用户名
        self.wxReply = myReply_Factory.myWx_Reply(Tag)      #
        self.pMMsg = gol._Get_Setting('manageMsgs')         #消息管理类
        self.usrDefault = {'UserName' : ""}
        self.Init()             # 文件初始
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
        self.useSwap = useSwap          #消息通询使用数据交换
        self.swapRecv = None            #接收消息数据交换 
        self.Init_MsgCache(useCmdMMap)  #创建消息通讯缓存
    def Init(self, dir = "", pathPicDir = ""):
        if (dir == ""):
            strDir, strName = myIO.getPath_ByFile(__file__)
            self.dirBase = os.path.abspath(os.path.join(strDir, "..")).replace("\\", "/")  
        else:
            self.dirBase = dir
            
        #初始根目录信息
        self.dirSetting = self.dirBase + "/Setting/"
        self.dirData = self.dirBase + "/Data/"
        if(pathPicDir == ""): pathPicDir = self.dirData
        self.dirPic = pathPicDir + "Pic/"
        self.dirFile = pathPicDir + "File/"
        myIO.mkdir(self.dirPic, False)
        myIO.mkdir(self.dirPic + "Temps", False, True)
        myIO.mkdir(self.dirFile, False)
        myIO.mkdir(self.dirFile + "Temps", False, True)

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
        if(gol._Get_Value("msgSet_usrMQ", False) == False):
            self.Init_Swap(bStart)
            return 

        #初始消息接收队列
        self.mqName = 'zxcMQ_wx'
        if(self.mqRecv == None):
            self.mqRecv = myMQ_Rabbit.myMQ_Rabbit(False)
            self.mqRecv.Init_Queue(self.mqName, True)
            self.mqRecv.Init_callback_RecvMsg(self.callback_RecvMsg)    #消息接收回调
            myDebug.Print("消息队列(" + self.mqName + ")创建成功...")
            
        #接收消息 
        if(bStart): 
            self.mqRecv.Start()
            self.mqTimeNow = myData_Trans.Tran_ToTime_int()   #接收开始时间

        #接收消息--x线程方式
        #self.thrd_MQ = threading.Thread(target = self.mqRecv.Start)
        #self.thrd_MQ.setDaemon(False)
        #if(bStart): 
        #    self.thrd_MQ.start()
        #    self.mqTimeNow = myData_Trans.Tran_ToTime_int()   #接收开始时间
        
    #创建消息队列 
    def Init_Swap(self, bStart = False):
        #初始消息接收-Swap
        self.swapName = 'zxcSwap_wx'
        if(self.swapRecv == None):
            self.swapRecv = gol._Get_Value('dataSwap_msgWx')
            self.swapOut = gol._Get_Value('dataSwap_msgWx_out')
            
            @self.swapRecv.changeDataSwap()
            def Reply(lstData): 
                for x in lstData:
                    if(self.Done_Swap(x)):
                        self.swapRecv.ackDataSwap(x)
                    pass
            myDebug.Print("消息Swap(" + self.swapName + ")创建成功...")
            
        #接收消息 
        if(bStart): 
            self.swapOut.startSwap()
            self.swapRecv.startSwap()
            self.mqTimeNow = myData_Trans.Tran_ToTime_int()   #接收开始时间
    #处理交换消息集
    def Done_Swap(self, msgSwaps):
        lstData = msgSwaps['data']['fileInfo']
        bRes = 0
        for x in lstData:
            if(self._Send_Msg(x)):
                bRes += 1
        if(bRes > 0): return True
        return False
    #处理交换消息集-缓存已收消息
    def Done_Swap_MsgOut(self, msg, isGroup = False):
        if(msg or len(msg) > 1):
            myDebug.Debug("消息接收::", msg['Text'])
            if(str(msg['Text']) == '[]'): return 
            if(msg.get('Type', "") == 'System'): return

            #特殊消息处理
            try:
                destPath = ""
                dtTime = myData_Trans.Tran_ToTime_byInt(myData_Trans.To_Int(str(msg.get('CreateTime', 0))))
                msgType = msg['MsgType']
                if(msgType == 3):       # 图片 
                    destPath = self.dirPic + "Temps/" + msg.fileName
                    msg.download(destPath); time.sleep(1);
                elif(msgType == 49):    # 文件
                    destPath = self.dirFile + "Temps/" + msg.fileName
                    msg.download(destPath); time.sleep(1);

                #组装消息内容
                wxMsg = self.pMMsg.OnCreatMsg();
                wxMsg['usrID'] = msg['User']['UserName']
                wxMsg['usrName'] = msg['User']['NickName']
                wxMsg['usrNameNick'] = msg['User']['RemarkName']
                wxMsg['groupID'] = myData.iif(isGroup, msg['User']['UserName'], "")
                if(wxMsg['groupID'] != ""):
                    wxMsg['usrNameNick'] = msg['ActualNickName']
                    if(wxMsg['usrNameNick'] == ""):
                        if(msg['FromUserName'] == self.usrName):
                            wxMsg['usrNameNick'] = self.usrName_Alias
                wxMsg['msgID'] = msg['MsgId']
                wxMsg['msgType'] = msg['Type'].upper()
                wxMsg['msg'] = msg['Text']
                wxMsg['msgContent'] = msg.get('Content', '')
                wxMsg['usrPlat'] = "wx"
                wxMsg['msgTime'] = myData_Trans.Tran_ToTime_str(dtTime)
                if(destPath != ""):
                    wxMsg['msg'] = destPath

                #保存
                if(msgType == 1 or msgType == 10002): 
                    if(wxMsg['msg'] != ""):  
                        self.swapOut.SwapData_Out(wxMsg)
            except Exception as ex:
                myError.Error(ex)  
        return

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
        if(True):
            #记录为文件格式，便于其他识别
            dictUsr = {'UserName': self.usrName, 'NickName': self.usrName_Alias}
            myIO.Save_File(self.dirData + 'zxcWeixin.cache', str(dictUsr), True, True)

        #更新用户信息（回复消息处理工厂对象类）
        self.wxReply._Init(self.usrName, self.usrName_Alias)
        

        #消息发送测试
        #self.Send_Msg("", "茶叶一主号", "测试消息1", "SHARING", 0)
        #self.Send_Msg("", "测试", "测试消息22", "TEXT", 1)
        #self.Send_Msg("", "股票行情监测群", "测试消息33", "TEXT", 1)
        #self.Send_Msg("", "filehelper", "/root/Public/myPrjs/zxcProj/src/Zxc.Python/zxcPy.Weixin/Data/Pic/Temps/191008-203316.png", "Image", 1)
         
 
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
            if(roupID[0:2] == "@*"): roupID = roupID[2:]
            pUsers = itchat.search_chatrooms(name = roupID)
            if(pUsers != None and len(pUsers) == 1): return pUsers[0]
        if(groupName != ""):
            if(groupName[0:2] == "@*"): groupName = groupName[2:]
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
        elif(type(msgInfo)== OrderedDict):
            msg = msgInfo
        elif(type(msgInfo)== myData_Json.Json_Object):
            msg = msgInfo
        else:
            return False

        #增加记录日志--消息管理器实现 

        #调用 消息发送
        msgR = msg 
        msgR['msg'] = msgR['msg'].replace("※r※", "\r").replace("※n※", "\n").replace("※i※", '"').replace("※t※", "\t")
        if(msgR.get('groupID', '') != '' or msgR.get('groupName', '') != ''):       #区分群、个人
            return self.Send_Msg(msgR['groupID'], msgR['groupName'], msgR['msg'], msgR['msgType'], 1)
        else:
            return self.Send_Msg(msgR['usrID'], msgR['usrName'], msgR['msg'], msgR['msgType'])
    #发送消息接口(typeUser, 0: 好友 1：群 2：公众号)
    def Send_Msg(self, usrID, usrName = "", msgInfo = "" , typeMsg = "TEXT", typeUser = 0):
        #用户检测(@开头为用户名，filehelper，其他需要检索实际用户名)
        userName = usrName
        if(usrID == None): usrID = ""
        if(userName != "filehelper"):
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
        elif(typeMsg == "IMAGE"):   #未实现
            itchat.send_image(msgInfo, userName)
            if (os.path.exists(msgInfo) == False):
                myDebug.Error("No this Image" + msgInfo + ".")
        elif(typeMsg == "CARD1"): 
            Content = "<?xml version=\"1.0\"?>\n<msg bigheadimgurl=\"http://wx.qlogo.cn/mmhead/ver_1/UuYfjibTFM2RFQsy5hvdojN8qeSqghGeONUBib34ucEWpztQOM18xFicVYK02lfNYLFdiaYZww71H6oDgiaBPhVm9vCgXXB1bP9XoPgE8jOibJcko/0\" smallheadimgurl=\"http://wx.qlogo.cn/mmhead/ver_1/UuYfjibTFM2RFQsy5hvdojN8qeSqghGeONUBib34ucEWpztQOM18xFicVYK02lfNYLFdiaYZww71H6oDgiaBPhVm9vCgXXB1bP9XoPgE8jOibJcko/132\" username=\"v1_cd9b652b5b54d225963c03833cef2f27e2a1e7b9b55f5659ac9210eb315cca20@stranger\" nickname=\"MlNA\"  shortpy=\"MLNA\" alias=\"\" imagestatus=\"3\" scene=\"17\" province=\"广东\" city=\"广州\" sign=\"\" sex=\"2\" certflag=\"0\" certinfo=\"\" brandIconUrl=\"\" brandHomeUrl=\"\" brandSubscriptConfigUrl=\"\" brandFlags=\"0\" regionCode=\"CN_Guangdong_Guangzhou\" antispamticket=\"v2_2ced7b6604ee323f392d80574d0de3db9f4b52048d9bb0a3c231dc36f9285c02212ad1a52bcf0968b17bde1e4d8c167a153b52d5b9ff638a1cdf560d5f9d5e1a014792f12a7a6189768f049d47ca18ebb66e0bc34578bef58ce3602817a355f07c891384ee03a11f5639f39ba61ccac48bdaeaf0e3ebf06b707af8c6328d3de5834a7a89f03601ae0bc8fb5d0e8216acd0d50b8bd8e3fac6c9dad59253b829f74688d6fa701259f7ded3a108304cd7cd@stranger\" />\n"
            itchat.send_raw_msg(42, Content, userName)

            '''
                MsgType: 42
    FromUserName: 发送方ID
    ToUserName: 接收方ID
    Content:
        <?xml version="1.0"?>
        <msg bigheadimgurl="" smallheadimgurl="" username="" nickname=""  shortpy="" alias="" imagestatus="3" scene="17" province="" city="" sign="" sex="1" certflag="0" certinfo="" brandIconUrl="" brandHomeUrl="" brandSubscriptConfigUrl="" brandFlags="0" regionCode="" />
    RecommendInfo:
        {
            "UserName": "xxx", # ID
            "Province": "xxx",
            "City": "xxx",
            "Scene": 17,
            "QQNum": 0,
            "Content": "",
            "Alias": "xxx", # 微信号
            "OpCode": 0,
            "Signature": "",
            "Ticket": "",
            "Sex": 0, # 1:男, 2:女
            "NickName": "xxx", # 昵称
            "AttrStatus": 4293221,
            "VerifyFlag": 0
        }
        '''
        elif(typeMsg == "SHARING1"): 
            Content = '<?xml version="1.0"?>\n<msg>\n\t<appmsg appid="" sdkver="0">\n\t\t<title>【生活·吃·01】叹茶，一盅两件！曾经，我们插肩而过。10年后的重逢，才发现，你是这样的广式早茶！</title>\n\t\t<des>为名忙，为利忙，忙里偷闲，饮杯茶去；劳心苦，劳力苦，苦中作乐，拿壶酒来。</des>\n\t\t<username />\n\t\t<action>view</action>\n\t\t<type>5</type>\n\t\t<showtype>0</showtype>\n\t\t<content />\n\t\t<url>http://mp.weixin.qq.com/s?__biz=MzAxMDQ3MTk4Nw==&amp;mid=2247483741&amp;idx=1&amp;sn=8fb62dd901ca3f1eb1a89566af3abb53&amp;chksm=9b4e9e01ac391717ed0c9d726f7a66d2d7ce1e84aa052995997cabf21fb6db96040a60747062&amp;mpshare=1&amp;scene=1&amp;srcid=&amp;sharer_sharetime=1575551329214&amp;sharer_shareid=d369241c24472101fffbbbe1df71790e#rd</url>\n\t\t<lowurl />\n\t\t<dataurl />\n\t\t<lowdataurl />\n\t\t<contentattr>0</contentattr>\n\t\t<streamvideo>\n\t\t\t<streamvideourl />\n\t\t\t<streamvideototaltime>0</streamvideototaltime>\n\t\t\t<streamvideotitle />\n\t\t\t<streamvideowording />\n\t\t\t<streamvideoweburl />\n\t\t\t<streamvideothumburl />\n\t\t\t<streamvideoaduxinfo />\n\t\t\t<streamvideopublishid />\n\t\t</streamvideo>\n\t\t<canvasPageItem>\n\t\t\t<canvasPageXml><![CDATA[]]></canvasPageXml>\n\t\t</canvasPageItem>\n\t\t<appattach>\n\t\t\t<attachid />\n\t\t\t<cdnthumburl>305d0201000456305402010002044a17792502033d11fe020432f516d202045de90173042f6175706170706d73675f303961666430663738306163343663375f313537353535313334363837375f3236343734320204010400030201000400</cdnthumburl>\n\t\t\t<cdnthumbmd5>36cca8f5a144a3ef508a2d041b17237e</cdnthumbmd5>\n\t\t\t<cdnthumblength>32522</cdnthumblength>\n\t\t\t<cdnthumbheight>120</cdnthumbheight>\n\t\t\t<cdnthumbwidth>120</cdnthumbwidth>\n\t\t\t<cdnthumbaeskey>a8ff2b1290888ee1aa0653469b609ab8</cdnthumbaeskey>\n\t\t\t<aeskey>a8ff2b1290888ee1aa0653469b609ab8</aeskey>\n\t\t\t<encryver>1</encryver>\n\t\t\t<fileext />\n\t\t\t<islargefilemsg>0</islargefilemsg>\n\t\t</appattach>\n\t\t<extinfo />\n\t\t<androidsource>3</androidsource>\n\t\t<sourceusername></sourceusername>\n\t\t<sourcedisplayname>简易生活号</sourcedisplayname>\n\t\t<commenturl />\n\t\t<thumburl />\n\t\t<mediatagname />\n\t\t<messageaction><![CDATA[]]></messageaction>\n\t\t<messageext><![CDATA[]]></messageext>\n\t\t<emoticongift>\n\t\t\t<packageflag>0</packageflag>\n\t\t\t<packageid />\n\t\t</emoticongift>\n\t\t<emoticonshared>\n\t\t\t<packageflag>0</packageflag>\n\t\t\t<packageid />\n\t\t</emoticonshared>\n\t\t<designershared>\n\t\t\t<designeruin>0</designeruin>\n\t\t\t<designername>null</designername>\n\t\t\t<designerrediretcturl>null</designerrediretcturl>\n\t\t</designershared>\n\t\t<emotionpageshared>\n\t\t\t<tid>0</tid>\n\t\t\t<title>null</title>\n\t\t\t<desc>null</desc>\n\t\t\t<iconUrl>null</iconUrl>\n\t\t\t<secondUrl>null</secondUrl>\n\t\t\t<pageType>0</pageType>\n\t\t</emotionpageshared>\n\t\t<webviewshared>\n\t\t\t<shareUrlOriginal>http://mp.weixin.qq.com/s?__biz=MzAxMDQ3MTk4Nw==&amp;mid=2247483741&amp;idx=1&amp;sn=8fb62dd901ca3f1eb1a89566af3abb53&amp;chksm=9b4e9e01ac391717ed0c9d726f7a66d2d7ce1e84aa052995997cabf21fb6db96040a60747062&amp;scene=0&amp;xtrack=1&amp;clicktime=1575551321&amp;enterid=1575551321#rd</shareUrlOriginal>\n\t\t\t<shareUrlOpen>https://mp.weixin.qq.com/s?__biz=MzAxMDQ3MTk4Nw==&amp;mid=2247483741&amp;idx=1&amp;sn=8fb62dd901ca3f1eb1a89566af3abb53&amp;chksm=9b4e9e01ac391717ed0c9d726f7a66d2d7ce1e84aa052995997cabf21fb6db96040a60747062&amp;scene=0&amp;xtrack=1&amp;clicktime=1575551321&amp;enterid=1575551321&amp;ascene=7&amp;devicetype=android-27&amp;version=27000934&amp;nettype=WIFI&amp;abtest_cookie=AAACAA%3D%3D&amp;lang=zh_CN&amp;exportkey=AUVRoLcGAshgpownvyOek%2Bg%3D&amp;pass_ticket=H3X23ZwHOD05zFxqyys3F3YWCRWy5%2BRN%2B%2BFoP3lJfZW6PrO5vamVdlYXLm4XlGv2&amp;wx_header=1</shareUrlOpen>\n\t\t\t<jsAppId />\n\t\t\t<publisherId>msg_8659705440921183578</publisherId>\n\t\t</webviewshared>\n\t\t<template_id />\n\t\t<md5>36cca8f5a144a3ef508a2d041b17237e</md5>\n\t\t<weappinfo>\n\t\t\t<username />\n\t\t\t<appid />\n\t\t\t<appservicetype>0</appservicetype>\n\t\t\t<videopageinfo>\n\t\t\t\t<thumbwidth>120</thumbwidth>\n\t\t\t\t<thumbheight>120</thumbheight>\n\t\t\t\t<fromopensdk>0</fromopensdk>\n\t\t\t</videopageinfo>\n\t\t</weappinfo>\n\t\t<statextstr />\n\t\t<mmreadershare>\n\t\t\t<itemshowtype>0</itemshowtype>\n\t\t</mmreadershare>\n\t\t<directshare>0</directshare>\n\t\t<websearch>\n\t\t\t<rec_category>0</rec_category>\n\t\t\t<channelId>0</channelId>\n\t\t</websearch>\n\t</appmsg>\n\t<fromusername></fromusername>\n\t<scene>0</scene>\n\t<appinfo>\n\t\t<version>1</version>\n\t\t<appname></appname>\n\t</appinfo>\n\t<commenturl></commenturl>\n</msg>\n'
            params = {"AppMsgType": 5, "Url": 'http://mp.weixin.qq.com/s?__biz=MzAxMDQ3MTk4Nw==&amp;mid=2247483741&amp;idx=1&amp;sn=8fb62dd901ca3f1eb1a89566af3abb53&amp;chksm=9b4e9e01ac391717ed0c9d726f7a66d2d7ce1e84aa052995997cabf21fb6db96040a60747062&amp;mpshare=1&amp;scene=1&amp;srcid=&amp;sharer_sharetime=1575551329214&amp;sharer_shareid=d369241c24472101fffbbbe1df71790e#rd', "FileName": "【生活·吃·01】叹茶，一盅两件！........"}
            itchat.send_raw_msg(49, Content, userName, params)
        else:
            myDebug.Print("No this type.")
            return False
        return True
    #提取格式化返回信息 
    def Get_Msg_Back(self, msg, isGroup = False):
        return None         #强制关闭，调整为文件交换方式

        #回复操作调用 
        msgR = self.wxReply.Done_ByMsg(msg, isGroup)    #兼容API方式，消息队列无返回        
        if(msgR == None): return None
        
        #回复自己判断(调整为目标用户)
        myDebug.Debug("消息回复::", msgR)
        if(msgR.get('groupName', '') == ''):            #区分群、个人
            self.Send_Msg(msgR['usrID'], msgR['usrName'], msgR['msg'], msgR['msgType'])
        else:
            self.Send_Msg(msgR['groupID'], msgR['groupName'], msgR['msg'], msgR['msgType'], 1)
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
        
        #掉线重连
        if(True):
            #登录微信网页版(二维码扫码)
            self.Logion();
 
            #运行 
            pWeixin.Run_ByThread();
         
        
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
            #@itchat.msg_register([TEXT, PICTURE, RECORDING, ATTACHMENT, VIDEO, SYSTEM, CARD, NOTE, SHARING], isFriendChat=True) 
            @itchat.msg_register([TEXT, PICTURE, RECORDING, ATTACHMENT, VIDEO, SYSTEM, NOTE], isFriendChat=True) 
            def Reply_Text(msg): 
                self.Done_Swap_MsgOut(msg);     #缓存信息

                if self.Auto_RreplyText:  
                    #提取回复消息内容
                    return self.Get_Msg_Back(msg)               #格式化提取(兼容API方式，消息队列无返回)
            self.funStatus_RText = self.Auto_RreplyText
            
            #注册普通文本消息回复                 
            @itchat.msg_register([TEXT, SYSTEM, SHARING], isMpChat=True) 
            def Reply_Text(msg): 
                self.Done_Swap_MsgOut(msg);     #缓存信息 

                if self.Auto_RreplyText:  
                    #提取回复消息内容
                    return self.Get_Msg_Back(msg)               #格式化提取(兼容API方式，消息队列无返回)
            self.funStatus_RText = self.Auto_RreplyText


        #注册普通文本消息回复(群消息)    
        if self.Auto_RreplyText_G != self.funStatus_RText_G:
            #注册普通文本消息回复                 
            #@itchat.msg_register([TEXT, PICTURE, FRIENDS, SYSTEM, CARD, NOTE, SHARING], isGroupChat=True)
            @itchat.msg_register([TEXT, PICTURE, RECORDING, ATTACHMENT, VIDEO, SYSTEM, NOTE], isGroupChat=True)
            def Reply_Text_Group(msg): 
                self.Done_Swap_MsgOut(msg, True);     #缓存信息

                if self.Auto_RreplyText_G: 
                    #提取回复消息内容
                    return self.Get_Msg_Back(msg, True)         #格式化提取(兼容API方式，消息队列无返回)
            self.funStatus_RText_G = self.Auto_RreplyText_G

        # 收到note通知类消息，判断是不是撤回并进行相应操作
        #@itchat.msg_register([NOTE], isMpChat=True)
        #def send_msg_helper(msg):
        #    def Reply_Text_Group(msg): 
        #        if self.Auto_RreplyText_G: 
        #            #提取回复消息内容
        #            return self.Get_Msg_Back(msg, True, True)   #格式化提取(兼容API方式，消息队列无返回)
        #
        #    global face_bug
        #    if re.search(r"\<\!\[CDATA\[.*撤回了一条消息\]\]\>", msg['Content']) is not None:
        #        # 获取消息的id
        #        old_msg_id = re.search("\<msgid\>(.*?)\<\/msgid\>", msg['Content']).group(1)
        #        old_msg = msg_dict.get(old_msg_id, {})
        #        if len(old_msg_id) < 11:
        #            itchat.send_file(rev_tmp_dir + face_bug, toUserName='filehelper')
        #            os.remove(rev_tmp_dir + face_bug)
        #        else:
        #            msg_body = "告诉你一个秘密~" + "\n" \
        #                       + old_msg.get('msg_from') + " 撤回了 " + old_msg.get("msg_type") + " 消息" + "\n" \
        #                       + old_msg.get('msg_time_rec') + "\n" \
        #                       + "撤回了什么 ⇣" + "\n" \
        #                       + r"" + old_msg.get('msg_content')
        #            # 如果是分享存在链接
        #            if old_msg['msg_type'] == "Sharing": msg_body += "\n就是这个链接➣ " + old_msg.get('msg_share_url')
        #
        #            # 将撤回消息发送到文件助手
        #            itchat.send(msg_body, toUserName='filehelper')
        #            # 有文件的话也要将文件发送回去
        #            if old_msg["msg_type"] == "Picture" \
        #                    or old_msg["msg_type"] == "Recording" \
        #                    or old_msg["msg_type"] == "Video" \
        #                    or old_msg["msg_type"] == "Attachment":
        #                file = '@fil@%s' % (rev_tmp_dir + old_msg['msg_content'])
        #                itchat.send(msg=file, toUserName='filehelper')
        #                os.remove(rev_tmp_dir + old_msg['msg_content'])
        #            # 删除字典旧消息
        #            msg_dict.pop(old_msg_id)
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
            msgR = ast.literal_eval(strMsg) 
            
            #时间校检, 十分钟内缓存数据有效(过早时间数据忽略)
            if(self.wxReply.Check_TimeOut(msgR)):
                myDebug.Debug("--队列消息已超时wx::", strMsg)  
                return True

            #消息发送
            if(msgR.get('groupID', '') != '' or msgR.get('groupName', '') != ''):       #区分群、个人
                self.Send_Msg(msgR['groupID'], msgR['groupName'], msgR['msg'], msgR['msgType'], 1)
            else:
                self.Send_Msg(msgR['usrID'], msgR['usrName'], msgR['msg'], msgR['msgType'])
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
    #单例运行检测
    if(gol._Run_Lock(__file__) == False):
       exit(0)

    #声明Weixin操作对象
    pWeixin = myWeixin_ItChat('zxcWx', False, gol._Get_Value("msgSet_usrMQ", False))
    
    #登录微信网页版(二维码扫码)
    pWeixin.Logion();
 
    #消息测试
    #pWeixin.Send_Msg("", "茶叶一主号","登陆")

    #运行 
    #pWeixin.Run();
    pWeixin.Run_ByThread();

    #退出
    gol._Run_UnLock(__file__)
    exit(0)

