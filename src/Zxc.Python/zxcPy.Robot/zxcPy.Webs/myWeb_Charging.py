# -*- coding: utf-8 -*-
"""
Created on  张斌 2020-09-09 20:58:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com

    pyWeb --充电桩接口
""" 
import sys, os, string, time, mySystem  

#导入模块
from flask import jsonify, request, flash, render_template, redirect    #导入模块

mySystem.Append_Us("", False)   
import myIO, myWeb, myWeb_urlLib, myDebug, myData_Json, myRoot_Usr
from myGlobal import gol



#集中添加所有Web
def add_Webs(pWeb):      
    #添加接口--充电启动接口 
    @pWeb.app.route('/zxcAPI/robot/charging/start')
    def chargingStart(): 
        # 模拟启
        res = {"success": 1, "data": "", "msg": ""}
        state = gol._Get_Value('chargingState', 0)
        typeDone = gol._Get_Value('chargingDone', '')
        if(typeDone == '启动'):
            res['success'] = 0
            res['msg'] = "充电启动中"
        elif(state < 10):
            res['msg'] = "尝试启动充电"
            gol._Set_Value('chargingDone', '启动', True)
        else:
            res['success'] = 0
            res['msg'] = "错误"
        return myData_Json.Trans_ToJson_str(res)

    #添加接口--充电停止接口
    @pWeb.app.route('/zxcAPI/robot/charging/stop')
    def chargingStop(): 
        # 模拟停
        res = {"success": 1, "data": "", "msg": ""}
        state = gol._Get_Value('chargingState', 0)
        typeDone = gol._Get_Value('chargingDone', '')
        if(typeDone == '启动'):
            res['success'] = 0
            res['msg'] = "充电停止中"
        elif(state > 0):
            res['msg'] = "尝试停止充电"
            gol._Set_Value('chargingDone', '停止', True)
        else:
            res['success'] = 0
            res['msg'] = "错误"
        return myData_Json.Trans_ToJson_str(res)     
     
    #添加接口--充电状态查询接口
    @pWeb.app.route('/zxcAPI/robot/charging/queryState/<ID>', methods = ['GET', 'POST'])
    def queryState(ID): 
        res = {"success": 1, "data": 0, "msg": ""}
        typeDone = gol._Get_Value('chargingDone', '启动')
        state = gol._Get_Value('chargingState', 0)
        times = gol._Get_Value('chargingTimes', 0)
        
        # 模拟状态调整
        time.sleep(1)
        if(times < 5):
            times += 1
            gol._Set_Value('chargingTimes', times, True)
            if(typeDone == "启动"):
                res['msg'] = "充电启动中"
            elif(typeDone == "停止"):
                res['msg'] = "充电停止中"
        else:
            gol._Set_Value('chargingTimes', 0, True)

            if(typeDone == "启动"):
                gol._Set_Value('chargingState', 11, True)
                res['success'] = 1
                res['data'] = 11
                res['msg'] = "充电已启动"
            elif(typeDone == "停止"):
                gol._Set_Value('chargingState', -1, True)
                res['success'] = 1
                res['data'] = -1
                res['msg'] = "充电已停止"
        return myData_Json.Trans_ToJson_str(res)
    
    #添加接口--充电详情查询接口
    @pWeb.app.route('/zxcAPI/robot/charging/queryDetail/<ID>', methods = ['GET', 'POST'])
    def queryDetail(ID): 
        res = {"success": 1, "data": 0, "msg": ""}
        details = {'duration': "15分钟", 'power': "0.6kWh", 'cost': "1元"}

        res['data'] = details
        return myData_Json.Trans_ToJson_str(res)