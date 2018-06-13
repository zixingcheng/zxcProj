# -*- coding: utf-8 -*-
"""
Created on  张斌 2018-04-03 11:30:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com

    Debug操作 
"""
import os, math, time, datetime
import myData_Trans

#全局变量
global ms_Msgs 
ms_Msgs = {}


#打印调试信息并记录时间
def Debug(tag, msg, bRecord = False, bTitle = True, ErrType = "Error"):
    nTime = time.time()
    if(bRecord):        #记录信息
        ms_Msgs[tag] = nTime
        print("->>", tag, "", msg, "\n              ", "--Start at", datetime.datetime.fromtimestamp(nTime).strftime('%H:%M:%S.%f')) 
        
    elif(ms_Msgs.__contains__(tag)):
        nInterval = nTime - ms_Msgs[tag]
        if(bTitle):
            print("->>", tag, "", msg, "\n              ", "--End at", datetime.datetime.fromtimestamp(nTime).strftime('%H:%M:%S.%f'), "\n      ", "--耗时:", round(nInterval, 3), "秒")  
        return nInterval

#打印调试信息并记录时间
def Debug(msg, ErrType = "Debug"):
    #if(ms_Msgs["Can_Debug"] == True):
    print("->>", ErrType, "::", msg)  

def main(): 
    Debug("Test", "测试", True, False, "Info")
    time.sleep(1)
    Debug("Test0", "测试结束")
    time.sleep(0.2)
    Debug("Test", "测试结束")
     
if __name__ == '__main__':
     exit(main())
