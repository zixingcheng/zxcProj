# -*- coding: utf-8 -*-
"""
Created on  张斌 2018-07-04 15:58:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com

    Rest API --平台注册
"""
import os, copy, ast 
import mySystem 
from flask import jsonify, request, make_response
    
#引用根目录类文件夹--必须，否则非本地目录起动时无法找到自定义类
mySystem.Append_Us("../zxcPy.APIs", False, __file__)
mySystem.Append_Us("../zxcPy.Robot", False, __file__)
mySystem.Append_Us("../zxcPy.Robot/Prjs", False, __file__)
mySystem.Append_Us("../zxcPy.Robot/Reply", False, __file__)
mySystem.Append_Us("../zxcPy.Robot/Roots", False, __file__)
mySystem.Append_Us("", False)    
import myIO, myData_Trans, myWeb, myDebug, myRobot_Reply, myRobot_Reply_MQ, myManager_Msg
from myGlobal import gol   



#API-平台注册
class myAPI_Robot_RegistPlat(myWeb.myAPI): 
    def get(self, usrName, usrID, PlatName):
        pMsg = copy.deepcopy(gol._Get_Setting('Return_strFormat', {}))
        if(PlatName == ""): return pMsg
        
        #提取平台集 
        pRoot = gol._Get_Value('rootRobot')
        pPlats = pRoot.usrPlats
        pPlat = pPlats.Find(PlatName)
        if(pPlat == None):
            pPlat = pPlats.Regist(usrName, usrID, PlatName)
        
        pMsg['result'] = True
        pMsg['toke'] = pPlat.usrToken

        #初始消息处理对象
        init_Reply()._Init()
        return pMsg
    
#API-消息处理
class myAPI_Robot_Reply(myWeb.myAPI): 
    def get(self, msgInfo):
        #初始消息处理对象
        ms_Reply = init_Reply()
        
        #消息处理(应为异步处理)
        msg = ast.literal_eval(msgInfo) 
        pReutrn = ms_Reply.OnHandleMsg(msg) 
        myDebug.Debug("API-->>", pReutrn)
        try:
            return pReutrn
        except :
            return None

#API-验证码人工处理
class myAPI_Robot_Captcha(myWeb.myAPI): 
    def get(self, msgInfo):
        #提取消息内容
        msgInfo = myData_Trans.Tran_ToDict(msgInfo)
        imgPath = msgInfo.get('imgPath', "")
        usrName = msgInfo.get('usrName', "")
        urlCallback = msgInfo.get('urlCallback', "")

        #发送wx消息
        pMMsg = gol._Get_Setting('manageMsgs')
        if(pMMsg != None):
            bufMsgs = gol._Get_Setting('bufferMsgs')        #消息缓存
            id = len(bufMsgs.usrMsgs) + 1
            msgID = "*" + str(id)

            msg = pMMsg.OnCreatMsg()
            msg["usrPlat"] = "wx"
            msg["usrName"] = usrName
            msg["bufTimes"] = 2

            #发送标识信息
            msg["msgType"] = "TEXT"
            msg["msg"] = "@*" + msgID + " "
            pMMsg.OnHandleMsg(msg)
            
            #发送验证码图片信息
            imgPath = "E:\\myCode\\zxcProj\\src\\Zxc.Python\\zxcPy.gsLog_Submits\\code.jpg"
            msg["msgType"] = "IMage"
            msg["msg"] = imgPath
            pMMsg.OnHandleMsg(msg)

            return {"res": "OK", "msgID": msgID}
        else:
            return {"err": 0} 
class myAPI_Robot_Captcha_Code(myWeb.myAPI): 
    def get(self, msgID):
        #提取消息内容
        bufMsgs = gol._Get_Setting('bufferMsgs')        #消息缓存
        pMsg = bufMsgs.Find(msgID)  
        if(pMsg == None): 
            return ""
        return str(pMsg.msg['value'])


#初始消息处理对象
def init_Reply():     
    #全局对象提取
    ms_Reply = gol._Get_Setting('robotReply', None)
    return ms_Reply
#集中添加所有API
def add_APIs(pWeb):     
    #初始消息处理对象
    init_Reply()

    # 创建Web API
    pWeb.add_API(myAPI_Robot_RegistPlat, '/zxcAPI/robot/regist/Plat/<usrName>/<usrID>/<PlatName>')
    pWeb.add_API(myAPI_Robot_Reply, '/zxcAPI/robot/reply/<msgInfo>')
    pWeb.add_API(myAPI_Robot_Captcha, '/zxcAPI/robot/captcha/<msgInfo>')
    pWeb.add_API(myAPI_Robot_Captcha_Code, '/zxcAPI/robot/captcha/code/<msgID>')
    
    
    # 显示登录二维码图片
    @pWeb.app.route('/zxcAPI/robot/wechat/login', methods=['GET'])
    def login_WeChat():
        strDir, strName = myIO.getPath_ByFile(__file__)    
        strDirBase = os.path.abspath(os.path.join(strDir, "../..")) + "/zxcPy.Weixin/Data/Pic/"
        if request.method == 'GET':
            image_data = open(os.path.join(strDirBase, "QR.png"), "rb").read()
            response = make_response(image_data)
            response.headers['Content-Type'] = 'image/png'
            return response
        else:
            pass


#主程序启动
if __name__ == '__main__': 
    gol._Init()     #先必须在主模块初始化（只在Main模块需要一次即可）
    #gol._Set_Setting("CanPrint_Debug", False)
    init_Reply()
    print()

    #测试
    namePlat = "wx"
    token = ""

    #注册平台, 取token
    pReg = myAPI_Robot_RegistPlat()
    token = pReg.get("myTest", "@zxcv", "wx")
    print("token::", token)
    print()


    #消息处理借接口
    # {'msg': '@@Repeater', 'usrName': '墨紫_0', 'usrNameNick': '墨紫', 'groupID': '', 'usrPlat': 'wx', 'msgType': 'TEXT', 'usrID': 'zxc_0', 'msgID': ''}
    pMMsg = gol._Get_Setting('manageMsgs', None)
    msg = pMMsg.OnCreatMsg()
    msg["usrID"] = "zxc_0"
    msg["usrName"] = "墨紫"
    msg["usrNameNick"] = ""
    msg["msg"] = "Repeater"
    msg["usrPlat"] = "wx"
    myDebug.Debug("消息结构：", msg)
    print()
    

    #API测试
    pReply = myAPI_Robot_Reply()
    pReply.get(str(msg))
    print()
    
    #测试功能 
    msg["msg"] = "@@Repeater"
    myDebug.Debug(pReply.get(str(msg)))

    msg["msg"] = "Hi Repeater"
    myDebug.Debug(pReply.get(str(msg)))
    print()
    
    msg["msg"] = "@@Repeater"
    pReply.get(str(msg))
    print()