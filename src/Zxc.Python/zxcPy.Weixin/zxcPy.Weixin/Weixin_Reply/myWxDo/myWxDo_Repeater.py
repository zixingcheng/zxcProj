#-*- coding: utf-8 -*-
"""
Created on  张斌 2017-11-17 15:16:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com

    Weixin网页版消息处理接口（功能库）
"""

import sys, os, time #,mySystem
from myWxDo import myWxDo 


#引用根目录类文件夹--必须，否则非本地目录起动时无法找到自定义类
#mySystem.m_strFloders.append('/myAPIs')
#mySystem.Append_Us("", True) 
#import myError, myData_Json #myDataSet, myData, myData_Trans 


    
#消息处理--复读机(回复相同消息)
class myWxDo_Repeater(myWxDo):
    def __init__(self, usrName_F, Text, prjRoot):
        myWxDo.__init__(self)
        self.usrType = "Cmd_@@"   #类型   
        self.usrTag = "Repeater"  #标识
        if(self.usrTag in Text):
            self.usrTag = Text 
        self.usrTitle = "复读机"  #说明  
        self.usrName = usrName_F  #用户名称(对方)
        self.strText_L = Text     #标识  
        self.msg['FromUserName'] = usrName_F 
        self.msg['Type'] = "TEXT"  
   
    
    #消息处理接口
    def _Done(self, Text, isGroup = False, idGroup = ""):        
        #复读机(回复相同消息)
        return Text 
    
    def _Title_User_Opened(self): 
        return "发送任何消息均同声回复..."
        

#主启动程序
if __name__ == "__main__":
    pR = myWxDo_Repeater("zxc", "@@Repeater");
    pp = pR.Done("@@Repeater")
    print(pp)
    print(pR.Done("Hello"))
    print(pR.Done("@@Repeater"))

    time.sleep (2)
    pp = pR.Done("Hello")
    print(pp)

    
