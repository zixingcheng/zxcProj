# -*- coding: utf-8 -*-
"""
Created on  张斌 2018-04-03 11:30:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com

    Debug操作 
"""
import os, math, time, datetime
import myData_Trans
from myGlobal import gol   

#定义全局方法集并缓存
gol._Init()             #先必须在主模块初始化（只在Main模块需要一次即可）
ms_Msgs = gol._Get_Value('golMsgs')


#打印调试信息并记录时间
def Debug_byTag(tag, msg = "", bRecord = False, bTitle = True):
    nTime = time.time()
    ms_Deepth = gol._Get_Setting('Debug_Depth') 
    if(bRecord):        #记录信息
        ms_Msgs[tag] = nTime
        Debug(tag, "", msg, "\n              ", "--Start at", datetime.datetime.fromtimestamp(nTime).strftime('%H:%M:%S.%f')) 
        ms_Deepth += 1
        gol._Set_Setting('Debug_Depth', ms_Deepth) 
         
    elif(ms_Msgs.__contains__(tag)):
        nInterval = nTime - ms_Msgs[tag]
        ms_Deepth -= 1
        gol._Set_Setting('Debug_Depth', ms_Deepth) 
        if(bTitle):
            Debug(tag, "", msg, "\n              ", "--End at", datetime.datetime.fromtimestamp(nTime).strftime('%H:%M:%S.%f'), "\n      ", "--耗时:", round(nInterval, 3), "秒")  
        return nInterval

#打印调试信息并记录时间
def Error(*args):
    if(gol._Get_Setting('CanPrint_Error')):
        Print(*args, type="E")
def Warnning(*args):
    if(gol._Get_Setting('CanPrint_Warnning')):
        Print(*args, type="W")
def Debug(*args):
    if(gol._Get_Setting('CanPrint_Debug')):
        Print(*args, type="D")
def Print(*args, type = "T"):
    if(gol._Get_Setting('CanPrint')):
        strText = ""
        for x in args:
            strText += str(x)
    
        strDepth = _Depth_str()
        if(strDepth == ""):
            print(type + "->>", strText) 
        else:
            print(type + "->>", strDepth, strText) 


#提取depth字符串
def _Depth_str(strSeg = "->>", nSeg = 1):
    nDeepth = gol._Get_Setting('Debug_Depth') 
    strDepth = ""
    while(nDeepth > 0):
        strDepth += strSeg * nSeg + " "
        nDeepth -= 1
    return strDepth.strip() 


def main(): 
    Print("a", "b", 1)
    Debug_byTag("Test", "测试", True, False)
    time.sleep(1)
    Debug("Test0", "测试结束")
    time.sleep(0.2)
    Debug("Test", "测试结束")
    Debug_byTag("Test", "测试")
if __name__ == '__main__':
     exit(main())
