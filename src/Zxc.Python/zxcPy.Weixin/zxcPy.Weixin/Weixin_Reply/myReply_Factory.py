#-*- coding: utf-8 -*-
"""
Created on  张斌 2017-11-17 12:16:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com

    Python的Weixin网页版消息处理接口(文本消息)
"""

import sys, os, time, mySystem   


#引用根目录类文件夹--必须，否则非本地目录起动时无法找到自定义类 
mySystem.m_strFloders.append('/myWxDo')
mySystem.Append_Us("", False) 
import myImport, myDataSet, myIO, myWx_User, myWx_UserRoot #myError, myData_Json #myDataSet, myData, myData_Trans 



#消息处理工厂类
class myWx_Reply():
    def __init__(self, tag): 
        self.usrTag = tag
        self.usrName = ""
        self.nickName = ""
        self.wxUsers = {}       #消息用户类
        self.sysUsers = {}      #管理员用户列表
        #self.wxDos = {}         #消息处理类
        self.wxUser_Root = None #当前授权用户对象(避免频繁查找)

        #初始用户全局功能权限对象 
        self.wxRoot = myWx_UserRoot.myWx_Root(self.usrName)
        self.wxRoot._Init()
        print(">>实例消息处理工厂(%s)" % (tag))

    def _Init(self, usrName, nickName = ""): 
        self.usrName = usrName
        self.nickName = nickName
        self.wxRoot.usrName = usrName
        self.wxUser_Root = self._Find_Usr(usrName, nickName)

        self.sysUsers[self.usrName] = "墨紫"
        self.sysUsers["@cffee2f4531ac21cbfa3fec6180cf21f33178e37919952fb53f38c661feb4caf"] = "墨紫2"
        print("    --消息工厂(%s)初始: %s--%s" % (self.usrTag, nickName, usrName))

        
    #处理封装返回消息(按标识内容处理)
    def Done_ByMsg(self, msg, isGroup = False):
        if(msg == None): return None

        #提取消息内容（可能随wx版本变更）
        usrName = msg['FromUserName']
        usrName_To = msg['ToUserName']
        nickName = msg['User']['NickName']
        strText = msg['Text'] 
        idGroup = ""
        pWxdo = None 
        if(isGroup):
            idGroup = msg['User']['UserName']

        #调用 
        return self.Done(usrName, nickName, strText, isGroup, idGroup)
     
    #按命令处理返回消息(按标识内容处理)
    def Done(self, usrName, nickName, strText, isGroup = False, idGroup = ""):
        #命令识别
        pWxdo = None 
        if(strText[0:2] == "@@"):
            pWxdo, pPrj, pUser = self._Create_Cmd(usrName, nickName, strText[2:], isGroup, idGroup)
            if(pWxdo != None):
                print( "--Create WxDo: %s " % pPrj.prjName)
                return pUser.Done(pWxdo, pPrj.cmdStr, isGroup, idGroup)    #直接消息处理方法调用
            
        #查找用户  
        pUser = self._Find_Usr(usrName, nickName)       
        if(pUser == None): return None

        #消息处理方法调用
        return pUser.Done(pWxdo, strText, isGroup, idGroup)

    #查找用户（不存在则自动创建）
    def _Find_Usr(self, usrName, nickName):
        #按消息生成对应对象 
        for key in self.wxUsers:
            if(key == usrName): 
                return self.wxUsers[usrName]

        #新建用户对象
        pUser = myWx_User.myWx_User(usrName, nickName, self.wxRoot)
        self.wxUsers[usrName] = pUser
        return pUser
    #是否管理员账户（直接提升权限）
    def _IsRoot_Usr(self, usrName):
        return self.sysUsers.get(usrName) != None;
            
    #命令处理（@@命令，一次开启，再次关闭）
    def _Create_Cmd(self, usrName, nickName, prjCmd, isGroup, idGroup):    
        #查找功能权限对象
        pPrj = self.wxRoot._Find(prjCmd)
        if(pPrj == None):
            print(">>Create Prj(%s) Faield" % (prjCmd))
            return None, None, None
        if(pPrj.IsEnable() == False): return None, None, None     #必须启用

        #查找用户（功能开启全部可用则当前用户）  
        pUser = self._Find_Usr(usrName, nickName)   

        #功能权限验证 
        bEnable = pUser.usrRoot.IsEnable(pPrj.prjName, isGroup, idGroup)
        if(bEnable == False): bEnable = self._IsRoot_Usr(usrName)              
        if(bEnable == False): return None, None, None             #必须可用


        #动态实例
        pWxdo = myImport.Import_Class(pPrj.fileName, pPrj.className)(self.usrName, "@@" + pPrj.prjName, pUser.usrRoot)
        if(pPrj.IsEnable_All()):    #系统级功能，全部用户更新
            for key in self.wxUsers:
                self.wxUsers[key]._Add_Root(pWxdo)
        return pWxdo, pPrj, pUser 

    
    
#主启动程序
if __name__ == "__main__":
    #sys.path.append("C:\Python35-32\Lib\site-packages\myPy_Libs")
    print(sys.path)

    #动态实例测试
    pWxdo2 = myImport.Import_Class("myWxDo_Repeater","myWxDo_Repeater")('zxc','@@Repeater',None);
    print( pWxdo2.Done("@@Repeater"))
    print( pWxdo2.Done("Hello"))
    print( pWxdo2.Done("@@Repeater"))
    print("\n\n")

    #消息处理
    pWxReply = myWx_Reply("zxcc")
    pWxReply._Init("zxc", "墨紫")

    #权限初始
    print(pWxReply.Done('zxc_0',"墨紫_0",'@@zxcWeixin_Root'))
    print(pWxReply.Done('zxc_0',"墨紫_0",'Repeater'))

    #功能开关
    print(pWxReply.Done('zxc_0',"墨紫_0",'@@Repeater'))
    print(pWxReply.Done('zxc_0',"",'@@Repeater'))


    print(pWxReply.Done('zxc', "墨紫",'@@Repeater'))
    print(pWxReply.Done('zxc', "",'Hello'))
    print(pWxReply.Done('zxc', "",'@@Repeater'))

    time.sleep(2)
    print(pWxReply.Done('zxc', "",'@@Repeater'))

 
 
