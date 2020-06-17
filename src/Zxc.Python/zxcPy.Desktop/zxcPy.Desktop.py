# -*- coding: utf-8 -*-
"""
Created on  张斌 2020-06-16 11:00:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com

    窗体管理器，启动程序
    @依赖库： pyqt5
"""
import sys, ast, time, threading
import mySystem 

#引用根目录类文件夹--必须，否则非本地目录起动时无法找到自定义类
mySystem.Append_Us("/zxcPy.Form", False, __file__)
mySystem.Append_Us("", False)    
from myGlobal import gol  
import myWinForm_QT, myWinForm_Manager



if __name__ == '__main__':
    gol._Init()             #先必须在主模块初始化（只在Main模块需要一次即可）
    #单例运行检测
    if(gol._Run_Lock(__file__) == False):
       exit(0)

       
    
    #初始窗体管理器
    app = myWinForm_QT._initApp()
    frmManager = myWinForm_Manager.myWinForm_Manager(True)
    frmManager._initForms("quote", "Tag", 0, 10, 600, 600, True)
    frmManager._initForms("", "Tag", 0, 10, 600, 600, True)
   
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

