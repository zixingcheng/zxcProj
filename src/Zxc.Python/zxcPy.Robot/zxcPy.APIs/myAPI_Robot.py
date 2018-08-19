# -*- coding: utf-8 -*-
"""
Created on  张斌 2018-07-04 15:58:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com

    Rest API --平台注册
"""
import os, copy, ast 
import mySystem 
    
#引用根目录类文件夹--必须，否则非本地目录起动时无法找到自定义类
mySystem.Append_Us("../zxcPy.APIs", False, __file__)
mySystem.Append_Us("../zxcPy.Robot", False, __file__)
mySystem.Append_Us("../zxcPy.Robot/Prjs", False, __file__)
mySystem.Append_Us("../zxcPy.Robot/Reply", False, __file__)
mySystem.Append_Us("../zxcPy.Robot/Roots", False, __file__)
mySystem.Append_Us("", False)    
import myWeb, myDebug, myRobot_Reply, myRobot_Reply_MQ, myManager_Msg
from myGlobal import gol   



#API-平台注册
class myAPI_Robot_RegistPlant(myWeb.myAPI): 
    def get(self, usrName, usrID, plantName):
        pMsg = copy.deepcopy(gol._Get_Setting('Return_strFormat', {}))
        if(plantName == ""): return pMsg
        
        #提取平台集 
        pRoot = gol._Get_Value('rootRobot')
        pPlants = pRoot.usrPlants
        pPlant = pPlants.Find(plantName)
        if(pPlant == None):
            pPlant = pPlants.Regist(usrName, usrID, plantName)
        
        pMsg['result'] = True
        pMsg['toke'] = pPlant.usrToken

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
        pReutrn = ms_Reply.Done_ByMsg(msg, True) 
        myDebug.Debug("API-->>", pReutrn)
        try:
            return pReutrn
        except :
            return None


#初始消息处理对象
def init_Reply():     
    #全局对象提取
    ms_Reply = gol._Get_Value('robotReply', None)
    return ms_Reply
#集中添加所有API
def add_APIs(pWeb):     
    #初始消息处理对象
    init_Reply()

    # 创建Web API
    pWeb.add_API(myAPI_Robot_RegistPlant, '/zxcAPI/robot/regist/plant/<usrName>/<usrID>/<plantName>')
    pWeb.add_API(myAPI_Robot_Reply, '/zxcAPI/robot/reply/<msgInfo>')


#主程序启动
if __name__ == '__main__': 
    gol._Init()     #先必须在主模块初始化（只在Main模块需要一次即可）
    #gol._Set_Setting("CanPrint_Debug", False)
    init_Reply()
    print()

    #测试
    namePlant = "wx"
    token = ""

    #注册平台, 取token
    pReg = myAPI_Robot_RegistPlant()
    token = pReg.get("myTest", "@zxcv", "wx")
    print("token::", token)
    print()


    #消息处理借接口
    # {'msg': '@@Repeater', 'usrName': '墨紫_0', 'usrNameNick': '墨紫', 'groupID': '', 'plat': 'wx', 'msgType': 'TEXT', 'usrID': 'zxc_0', 'msgID': ''}
    pMMsg = myManager_Msg.myManager_Msg()
    msg = pMMsg.OnCreatMsg()
    msg["usrID"] = "zxc_0"
    msg["usrName"] = "墨紫"
    msg["usrNameNick"] = ""
    msg["msg"] = "Repeater"
    msg["plat"] = "wx"
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