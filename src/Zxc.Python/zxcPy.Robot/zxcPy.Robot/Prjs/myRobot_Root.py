#-*- coding: utf-8 -*-
"""
Created on  张斌 2017-11-17 15:16:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com

    Weixin网页版消息处理接口（功能库）--Root临时提升，以便有开启系统功能权限
"""
import sys, os, time ,mySystem

#引用根目录类文件夹--必须，否则非本地目录起动时无法找到自定义类 
mySystem.Append_Us("", False) 
import myRobot
from myGlobal import gol   

    
#机器人类--权限提升
class myRobot_Root(myRobot.myRobot):
    def __init__(self, usrName, usrID):
        super().__init__(usrName, usrID)
        self.doTitle = "Robot_Root"     #说明 
        self.prjName = "Robot_Root"     #功能名
        self.doCmd = "@@zxcRobot_Root"  #启动命令 
        self.rootPrjs = None            #功能集
        
    #消息处理接口
    def _Done(self, Text, msgID = "", msgType = "TEXT", usrInfo = {}):
        #命令权限提升()
        #print(Text)
        #bResult, pPrj = self.usrRoot.Add_Cmd(Text, isGroup, idGroup)
        #strText = "功能(" + pPrj.prjName + ")权限提升" + myData.iif(bResult, "成功！", "失败！")
        strText = ""
        return strText 
    
    def _Title_User_Opened(self): 
        strReturn = ">>发送功能名称，提升对应管理权限...\n"
        strReturn += "    功能列表：\n"
        
        #初始用户全局功能权限对象 
        if(self.rootPrjs != None):
            pRoot = gol._Get_Value('rootRobot')     #权限信息
            if(pRoot != None):
                self.rootPrjs = pRoot.rootPrjs

        #输出功能名
        if(self.rootPrjs != None):
            prjRoots = self.rootPrjs.prjRoots
            for key in prjRoots.keys():
                prj = prjRoots[key]
                if(prj.isRoot == False):
                    strReturn += "      " + prj.prjName + "  " + prj.cmdStr + "\n"
        strReturn += "    输入以上功能名，或命令名，均可提升该功能管理权限。\n"
        strReturn += "    输入\"@@\" + 以上功能名，或命令名，均可开启或关闭相关功能。"
        return strReturn
        

#主启动程序
if __name__ == "__main__":
    pR = myRobot_Root("zxc", "zxcID");
    pp = pR.Done("@@zxcRobot_Root")
    print(pp)
    print(pR.Done("Hello"))
    print(pR.Done("@@zxcRobot_Root"))

    time.sleep (2)
    pp = pR.Done("Hello")
    print(pp)

    
