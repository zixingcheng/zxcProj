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

    
#机器人类--权限提升
class myRobot_Root(myRobot):
    def __init__(self, usrName_F, Text, usrRoot):
        myRobot.__init__(self)
        self.doTitle = "Robot_Root"     #说明 
        self.doCmd = "@@zxcRobot_Root"  #启动命令 
        
        self.usrTag = "zxcWeixin_Root"  #标识
        if(self.usrTag in Text):
            self.usrTag = Text 
        self.usrTitle = "命令权限提升"  #说明  
        self.usrName = usrName_F        #用户名称(对方)
        self.strText_L = Text           #标识  
        self.msg['FromUserName'] = usrName_F 
        self.msg['Type'] = "TEXT"  
        self.usrRoot = usrRoot	        #用户功能权限对象
        

    #消息处理接口
    def _Done(self, Text, isGroup = False, idGroup = ""):     
        #命令权限提升()
        #print(Text)
        bResult, pPrj = self.usrRoot.Add_Cmd(Text, isGroup, idGroup)
        strText = "功能(" + pPrj.prjName + ")权限提升" + myData.iif(bResult, "成功！", "失败！")
        return strText 
    
    def _Title_User_Opened(self): 
        strReturn = ">>发送功能名称，提升对应管理权限...\n"
        strReturn += "    功能列表：\n"
        prjRoots = self.usrRoot.prjRoots.prjRoots
        for key in prjRoots:
            prj = prjRoots[key]
            if(prj.isRoot == False):
                strReturn += "      " + prj.prjName + "  " + prj.cmdStr + "\n"
        strReturn += "    输入以上功能名，或命令名，均可提升该功能管理权限。\n"
        strReturn += "    输入\"@@\" + 以上功能名，或命令名，均可开启或关闭相关功能。"
        return strReturn
        

#主启动程序
if __name__ == "__main__":
    pR = myWxDo_Repeater("zxc", "@@zxcWeixin");
    pp = pR.Done("@@zxcWeixin")
    print(pp)
    print(pR.Done("Hello"))
    print(pR.Done("@@zxcWeixin"))

    time.sleep (2)
    pp = pR.Done("Hello")
    print(pp)

    
