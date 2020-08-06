# -*- coding: utf-8 -*-
"""
Created on  张斌 2020-08-05 11:58:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com

    pyWeb --大气扩散API测试
""" 
import sys, os, urllib, datetime, threading, string, mySystem  

mySystem.Append_Us("", False)  
import myIO, myWeb, myWeb_urlLib, myDebug, myData_Trans
from myGlobal import gol



#调用webAPI
def run_WebAPI(isPrint = True):      
    #strUrl = "http://127.0.0.1:8686/zxcAPI/Model/Leak"
    strUrl = "http://120.197.152.99:18686/zxcAPI/Model/Leak"
    strPath = '{"tag": "东莞铭晋家具有限公司", "infoLeak": {"longitude": 113.8, "latitude": 23.0478, "height_leak": 5, "massrate_leak": 4407.661085743278, "timestart_leak": "2020-08-04 16:05:57"}, "infoTarget": [{"id": "441900403", "longitude": 113.7819, "latitude": 23.0536, "height": 15}], "infoEnvironment": {"wind_speed": 1.1, "wind_direction": "ESE", "wind_height": 15, "temperature": 27.6, "cloudy_is": true}}'

    #设置查询接口执行
    pWeb = myWeb_urlLib.myWeb(strUrl, bPrint=False)
    strReturn = pWeb.Do_API_get(strPath, "zxcAPI-py")
    if(isPrint):
        print(myData_Trans.Tran_ToDatetime_str() , "查询结果：\n", strUrl, "--\n", strReturn, "\n")

    # 使用 urllib 方式获取
    #response = urllib.request.urlopen(F'{strUrl}/{strPath}')
    # read() 读取的是服务器的原始返回数据 decode() 后会进行转码
    #print(datetime.datetime.now(), response.read().decode())

    
if(True):
    print("多线程测试::")
    dtStart = datetime.datetime.now()
    print(dtStart)
    for x in range(0, 2000):
        #创建线程
        thrd_Run = threading.Thread(target = run_WebAPI,  args=[False])
        thrd_Run.setDaemon(False)
        thrd_Run.start()
    dtEnd = datetime.datetime.now()
    print(dtEnd)
    print((dtEnd-dtStart).seconds)


if(True):
    print("单线程测试::")
    dtStart = datetime.datetime.now()
    print(dtStart)
    for x in range(0, 2000):
        run_WebAPI(False)
    dtEnd = datetime.datetime.now()
    print(dtEnd)
    print((dtEnd-dtStart).seconds)

