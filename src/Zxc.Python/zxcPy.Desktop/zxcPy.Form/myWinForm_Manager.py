# -*- coding: utf-8 -*-
"""
Created on  张斌 2020-05-15 11:00:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com

    窗体管理器, 基于pyqt5
    @依赖库： pyqt5
"""
import sys, ast, os, time, threading
import mySystem 

#引用根目录类文件夹--必须，否则非本地目录起动时无法找到自定义类
mySystem.Append_Us("/zxcPy.APIs", False, __file__)
mySystem.Append_Us("", False)    
import myData, myData_Trans, myIO, myDebug, myError
import myMQ_Rabbit, myManager_Msg
import myWinForm_QT, myWinForm_Set
from myGlobal import gol 



# 透明悬浮窗口-行情
class myWinForm_Quote(myWinForm_QT.myWinForm):
    def __init__(self, type = "", name = "", parent=None, icoUrl = "", imgDir = "", alpha = 0.8, randomXY = True, autoMove = True, typeMove = 0, range = [200,900,200,650], pos = [300, 300, 99, 99]):  
        super(myWinForm_Quote, self).__init__(type, name, parent, icoUrl, imgDir, alpha, randomXY, autoMove, typeMove, range, pos)
    #初始窗口
    def _initForm_urs(self, msg):
        # 临时调整窗口信息
        # self.imgDir = "D:/myCode/zxcProj/src/Zxc.Python/zxcPy.All.Base/Data/" + "Images/imgQuote/"
        if(self.icoUrl == ""):
            self.icoUrl = "windy.png"
        pass
    #初始窗口信息
    def initHwnd(self, strText = '', icoUrl = "", isShow = True, infCmd = None):
        #提取命令信息
        super().initHwnd(strText, icoUrl, isShow)
        if(infCmd != None):
            typeCmd = infCmd.get("typeCmd", "")
            if(typeCmd != "quote"): return

            #按照行情匹配图标
            value = myData_Trans.To_Int(str(infCmd.get("value", "")))
            self.icoUrl = myData.iif(value >= 0, "Rise-", "Fall-") + str(abs(value)) + ".png"
            self.strText = infCmd.get("msg", strText)
            super().initHwnd(self.strText, self.icoUrl, isShow)

# 窗体管理器
class myWinForm_Manager():
    def __init__(self, recv = False):  
        self.usrMMsg = gol._Get_Setting('manageMsgs')       #消息管理对象
        self.manager = {}
        self.managerTemp = []
        self.mqRecv = None
        self.isRuning = True
        self.init_MQ(recv)
        
        #初始根目录信息
        strDir, strName = myIO.getPath_ByFile(__file__)
        self.baseDir = os.path.abspath(os.path.join(strDir, ".."))  
        self.imgDir = self.baseDir + "/Data/Images/imgQuote/"
        self.setWinForm = gol._Get_Value('zxcWinForm_Control', None)
    #初始窗口集（缓存备用，避免线程问题）
    def _initForms(self, type, tag, indMin = 0, indMax = 10, x = 300, y = 300, w = 86, h = 86, randomXY = False, rangeRect = None, saveXY = False, isShow = False):
        #初始行情窗口备用
        for xx in range(indMin, indMax):
            self._initForm(type, tag + "_" + str(xx), "", x, y, w, h, rangeRect, randomXY, saveXY, isShow)
    #初始窗口
    def _initForm(self, type, tag, icoUrl = "", x = 300, y = 300, w = 86, h = 86, rangeRect = None, randomXY = False, saveXY = False, isShow = True):
        frm = self._findForm(type, tag)
        if(frm == None):             
            #显示窗口
            pos = [x, y, w, h]
            _tag = self._getTag(type, tag) 
            pSet = self.setWinForm.getSet("", "", _tag)
            if(pSet != None):
                pos = pSet.formPos
                saveXY = pSet.formRePos
                randomXY = False
            self._showForm(type, tag, icoUrl, randomXY, rangeRect, pos, isShow, saveXY)
        pass

    #显示窗口   
    def _showForm_thrd(self, type, tag, icoUrl, randomXY, rangeRect, isShow, saveXY = False): 
        randomXY = True
        thrdForm = threading.Thread(target = self._showForm, args=(type, tag, icoUrl, randomXY, rangeRect, isShow, saveXY))
        thrdForm.setDaemon(False)
        thrdForm.start() 
    #显示窗口-线程 
    def _showForm(self, type, tag, icoUrl, randomXY, rangeRect, pos, isShow, saveXY = False): 
        _tag = self._getTag(type, tag) 
        if(type == "quote"):
            frm = myWinForm_Quote(type, _tag, icoUrl=icoUrl, imgDir=self.imgDir, randomXY=randomXY, range=rangeRect, pos=pos)
        else:
            frm = myWinForm_QT.myWinForm(type, _tag, icoUrl=icoUrl, imgDir=self.imgDir, randomXY=randomXY, range=rangeRect, pos=pos, parent=None)

        #窗体必须显示出来，否则窗体会卡死
        frm.initHwnd("", icoUrl, isShow)
        frm.savePos = saveXY
        frm.show()
        if(isShow):
            self.manager[frm.name] = frm
        self.managerTemp.append(frm)
    #查询窗体
    def _findForm(self, type, tag, autoCreate = False, autoChange = False):
        _tag = self._getTag(type, tag) 
        winFrom = self.manager.get(_tag, None)
        if(winFrom == None):
            if(autoCreate):
                self._initForm(type, tag, randomXY = True)
                winFrom = self.manager.get(_tag, None)
            elif(autoChange):
               # 去除空闲窗体记录
                for x in self.manager.keys():
                    frm = self.manager[x]
                    if(frm.isUsed == False):
                        self.manager.pop(x)

                # 提取空闲窗体备用
                for x in self.managerTemp:
                    if(x.isUsed == False and x.type == type):
                        winFrom = x; winFrom.tag = _tag
                        self.manager[_tag] = winFrom
                        break;
        return winFrom
    #提取标签
    def _getTag(self, type, tag):
        return type + "_" + tag
     
    #初始窗口信息
    def initHwnd(self, type, tag, strText = '', icoUrl = ""):
        frm = self._findForm(type, tag, autoChange = True)
        if(frm != None):
            frm.initHwnd(strText, icoUrl)

            #记录窗体信息
            if(frm.savePos):
                pSet = self.setWinForm.getSet("", "", frm.name)
                if(pSet == None or (pSet.formPos[0] != frm.x and pSet.formPos[1] != frm.y)):
                    self.setWinForm.initSet("", "", frm.name, type, formRange = frm.rangHwnd, formPos = [frm.x, frm.y, frm.w, frm.h], formRePos = frm.savePos, remark = '')
        return frm
    #创建消息队列 
    def init_MQ(self, bStart = False):
        #初始消息接收队列
        self.mqName = 'zxcMQ_usrWin'
        if(self.mqRecv == None):
            self.mqRecv = myMQ_Rabbit.myMQ_Rabbit(False)
            self.mqRecv.Init_Queue(self.mqName, True)
            self.mqRecv.Init_callback_RecvMsg(self.callback_RecvMsg)    #消息接收回调
            myDebug.Print("消息队列(" + self.mqName + ")创建成功...")
            
        #接收消息 
        if(bStart): 
            self.mqRecv.Start()
            self.mqTimeNow = myData_Trans.Tran_ToTime_int()   #接收开始时间


    #定义消息接收方法回调
    def callback_RecvMsg(self, body):
        if(self.isRuning):   
            thrdHandel_Msg = threading.Thread(target = self.checkMsg, args=(body,))
            thrdHandel_Msg.setDaemon(False)
            thrdHandel_Msg.start() 
            return True
        return False
    #消息检查修正--消息队列方式 
    def checkMsg(self, strMsg):  
        try:
            myDebug.Debug("接收队列消息window::", strMsg)  
            msgR = ast.literal_eval(strMsg) 
            
            #时间校检, 十分钟内缓存数据有效(过早时间数据忽略)
            if(self.checkTimeOut(msgR)):
                myDebug.Debug("--队列消息已超时window::", strMsg)  
                return True

            #消息处理
            return self.handelMsg(msgR)
        except Exception as ex:
            myError.Error(ex)  
            return True
    #消息超时校检
    def checkTimeOut(self, msg, nTimeOut = 600, nTimeNow = -1):  
        #时间校检, 十分钟内缓存数据有效(过早时间数据忽略)
        msgTime = msg.get('time', -1)
        if(nTimeNow < 0): nTimeNow = myData_Trans.Tran_ToTime_int()
        if(abs(msgTime - nTimeNow) >= 600): 
            myDebug.Warnning("已超时::", nTimeNow, ",", msgTime)
            return True
        return False

    #处理窗口信息
    def handelMsg(self, msg):
        #提取信息
        typeCmd = msg.get("typeCmd", "")
        infCmd = msg.get("infCmd", {})
        tagCmd = infCmd.get("tag", "")

        #分类处理
        return self.handelMsg_Quote(typeCmd, tagCmd, infCmd, msg)
    #处理窗口信息-行情
    def handelMsg_Quote(self, typeCmd, tagCmd, infCmd, msg):
        #提取窗体
        frm = self.initHwnd(typeCmd, tagCmd, "", "")
        if(frm != None):
            infCmd['typeCmd'] = typeCmd
            frm.initHwnd("", "", True, infCmd)
        return True
    #初始窗口信息
    def sendMsg(self, typeCmd, infCmd, usrID, usrName, nameNick, usrPlat, groupID, groupName, nameSelf):
        #创建消息信息
        msg = self.usrMMsg.OnCreatMsg()
        msg['usrID'] = usrID
        msg['usrName'] = usrName
        msg['usrNameNick'] = nameNick
        msg['usrPlat'] = usrPlat
        msg['groupID'] = groupID
        msg['groupName'] = groupName
        msg['usrNameSelf'] = nameSelf      #自己发自己标识 
        
        msg['typeCmd'] = typeCmd
        msg['infCmd'] = infCmd
        
        #消息发送
        self.usrMMsg.OnHandleMsg(msg, "usrWin", True)

        

if __name__ == '__main__':
    #初始窗体管理器
    app = myWinForm_QT._initApp()
    frmManager = myWinForm_Manager(True)
    frmManager._initForms("quote", "Tag", 0, 10, 600, 600, randomXY = True)
    frmManager._initForms("", "Tag", 0, 10, 600, 600, randomXY = True)
   
    #消息模拟线程   
    def _thrdSet_Msg(): 
        thrdSet_Msg = threading.Thread(target = _Set_Msg)
        thrdSet_Msg.setDaemon(False)
        thrdSet_Msg.start() 
    #消息模拟线程-实现
    def _Set_Msg():
        ind = 0
        while(True):
            ind += 1
            frmManager.initHwnd("", "Tag_" + str(1), "Tag" + str(ind), "Rise-1.png")
            #frmManager.initHwnd("quote", "Tag_1", "quote_Tag" + str(ind), "aa2.png")
            time.sleep(2)     #延时
    _thrdSet_Msg()
    
    myWinForm_QT._exitApp(app)
