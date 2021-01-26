# -*- coding: utf-8 -*-
"""
Created on  张斌 2018-11-26 15:58:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com

    Rest API --行情操作
"""
import os, copy, ast, time, threading 
import mySystem 
from flask import jsonify, request, make_response
from flask_restful import reqparse, abort, Api, Resource
    
#引用根目录类文件夹--必须，否则非本地目录起动时无法找到自定义类
mySystem.Append_Us("../zxcPy.APIs", False, __file__)
mySystem.Append_Us("../zxcPy.DataSwap", False, __file__)
mySystem.Append_Us("../zxcPy.Setting", False, __file__)
mySystem.Append_Us("../zxcPy.Quotation", False, __file__) 
mySystem.Append_Us("", False)    
import myIO, myWeb, myData_SwapWx, myDebug, myManager_Msg
from myGlobal import gol   
gol._Init()     #先必须在主模块初始化（只在Main模块需要一次即可）



#API-消息接口-Wx
class myAPI_Robot_msgWx(myWeb.myAPI): 
    def get(self, msgInfo):
        pMsg = copy.deepcopy(gol._Get_Setting('Return_strFormat', {}))
        if(msgInfo == ""): return pMsg

        #初始消息处理对象
        usrMMsg = gol._Get_Setting('manageMsgs', None)      #提取消息管理器
        if(usrMMsg == None): return pMsg
        
        #消息处理(应为异步处理)
        msg = ast.literal_eval(msgInfo) 
        msg['msg'] = msg['msg'].replace("※r※", "\r").replace("※n※", "\n").replace("※t※", "\t")
        usrMMsg.OnHandleMsg(msg, 'wx', True)
        pMsg['result'] = True
        pMsg['text'] = "Swap Cached!"
        myDebug.Debug("API Msg-->>", str(msg))
        return pMsg 

#集中添加所有API
def add_APIs(pWeb):  
    # 创建Web API
    pWeb.add_API(myAPI_Robot_msgWx, '/zxcAPI/robot/msg/<msgInfo>')
    
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
    print()
    