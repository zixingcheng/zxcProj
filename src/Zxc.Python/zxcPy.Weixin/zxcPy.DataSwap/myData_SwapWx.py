#-*- coding: utf-8 -*-
"""
Created on  张斌 2021-01-24 12:16:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com

    Python的数据交换接口实现
"""
import sys, os, ast, re, mySystem   

#引用根目录类文件夹--必须，否则非本地目录起动时无法找到自定义类  
mySystem.Append_Us("", False) 
import myWeb, myIO
from myGlobal import gol 
gol._Init()     #先必须在主模块初始化（只在Main模块需要一次即可）
gol._Set_Value("msgSet_usrMQ", False)

strDir, strName = myIO.getPath_ByFile(__file__)
dirBase = os.path.abspath(os.path.join(strDir, ".."))  
gol._Set_Setting('dirMsgsSwaps', dirBase + "/Data/Swaps")    #实例 消息缓存




#初始数据教会对象
import myData_Swap
pDataSwap_In = myData_Swap.myData_Swap_FileIO("msgWx", dirBase + "/Data/Swaps/SwapMsg", isSender = True, stepSwaps = 1, delayedTime = 0, useAck = True, nameSwap = "zxcSwap_wx")
pDataSwap_Out = myData_Swap.myData_Swap_FileIO("msgWx", dirBase + "/Data/Swaps/SwapMsg_Out")
gol._Set_Value('dataSwap_msgWx', pDataSwap_In, True)
gol._Set_Value('dataSwap_msgWx_out', pDataSwap_Out, True)




#主启动程序
if __name__ == "__main__":
    gol._Set_Setting("CanPrint_Debug", True)
    dataSwap = gol._Get_Value('dataSwap_msgWx')

    @dataSwap.changeDataSwap()
    def Reply(lstData): 
        for x in lstData:
            print(lstData)
            #pDataSwap.ackDataSwap(x)
            pass

    #文件交换处理
    dataSwap.startSwap();

    print()

     

 
 
