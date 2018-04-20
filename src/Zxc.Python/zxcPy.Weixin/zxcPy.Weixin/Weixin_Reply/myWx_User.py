#-*- coding: utf-8 -*-
"""
Created on  张斌 2017-11-17 12:16:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com

    Python的Weixin网页版消息处理接口(用户对象，记录用户设置及消息)
"""

import sys, os, time, mySystem   


#引用根目录类文件夹--必须，否则非本地目录起动时无法找到自定义类 
mySystem.m_strFloders.append('/myWxDo')
mySystem.Append_Us("", False) 
import myWx_UserRoot  #myError, myData_Json #myDataSet, myData, myData_Trans 



#消息回复用户类
class myWx_User():
    def __init__(self, usrName, nickName, wxRoot):
        self.usrName = usrName
        self.nickName = nickName
        self.wxDos = {}         #消息处理类集合
        self.wxDos_sys = {}     #消息处理类集合--系统级
        self.wxDo = None		#消息处理类当前
        self.usrRoot = myWx_UserRoot.myWx_UserRoot(usrName, wxRoot)	#用户权限对象


    #新消息处理
    def Done(self, pWxdo, Text, isGroup = False, idGroup = ""):         
        #增加功能 
        self._Add_WxDo(pWxdo)

        #None表示无命令，忽略 
        if(self.wxDo == None): 
            return None

        #调用处理命令对象
        pReturn = self.wxDo.Done(Text, isGroup, idGroup)

		#命令有效性检查，失效则初始状态
        if(self.wxDo._Check() == False): 
            self._Close_WxDo(self.wxDo)
            self.wxDo = None
        return pReturn;

    #增加功能
    def _Add_Root(self, pWxdo): 
        pWxdo_Find = self.wxDos_sys.get(pWxdo.usrTag)
        if(pWxdo_Find == None):
            self.wxDos_sys[pWxdo.usrTag] = pWxdo
        return True

    #查找功能
    def _Find_WxDo(self, prjName):
        #按消息生成对应对象
        for key in self.wxDos: 
            if(key == prjName): 
                return self.wxDos[prjName]
        return None
    
    #增加功能
    def _Add_WxDo(self, pWxdo): 
        if(pWxdo == None): return True		#非命令，直接返回
        if(self.wxDo == None):				#当前无命令，查找更新命令
            self.wxDo = None
        elif(pWxdo.usrTag != self.wxDo.usrTag):	#命令变更，关闭当前功能
            self._Close_WxDo(self.wxDo)
        else: 
            return True							#命令相同，直接返回
            
        #查找功能并添加
        pWxdo_Now = self._Find_WxDo(pWxdo.usrTag)
        if(pWxdo_Now == None):					#无历史命令，直接添加
            self.wxDos[pWxdo.usrTag] = pWxdo
            self.wxDo = pWxdo
        else: 
            self.wxDo = pWxdo_Now 
        return True
    
    #关闭功能
    def _Close_WxDo(self, pWxdo): 
        if(pWxdo == None): return False

        #查找功能并关闭
        pWxdo_Now = self._Find_WxDo(pWxdo.usrTag)
        if(pWxdo_Now != None): 
            self.wxDos.pop(pWxdo.usrTag)
        return True
 
