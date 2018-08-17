#-*- coding: utf-8 -*-
"""
Created on  张斌 2017-11-17 12:16:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com

    Python的Weixin网页版接口(使用itchat封装)--测试用
"""
import sys, os, time, mySystem 
import itchat
from itchat.content import *

#引用根目录类文件夹--必须，否则非本地目录起动时无法找到自定义类
mySystem.m_strFloders.append('/myAPIs')
mySystem.Append_Us("", True) 
import myError, myData_Json #myDataSet, myData, myData_Trans 

 
#发送消息接口(Json的msg)
def Send_Msg(msgInfo): 
    if(type(msgInfo)== str):
        msg = myData_Json.Trans_ToJson(msgInfo)
    elif(type(msgInfo)== dict):
        msg = msgInfo
    elif(type(msgInfo)== myData_Json.Json_Object):
        msg = msgInfo
    else:
        return False

    #调用 
    return Send_Ms(msg['FromUserName'], msg['Text'], msg['Type'])
 
#发送消息接口
def Send_Msg(userFrom = "", msgInfo = "" , typeMsg = "TEXT"):
    #用户检测(@开头为用户名，filehelper，其他需要检索实际用户名)
    if(userFrom == ""): return
    if(userFrom[0] != "@" and userFrom != "filehelper"):      
        #查找用户
        #user = itchat.search_friends(userName = '@minazhu')
        #user = itchat.search_friends(wechatAccount = 'littlecodersh') 
        user = itchat.search_friends(name = userFrom)
        if(len(user) != 1):
            print("用户未找到")
            return
        userFrom = user[0]['UserName']

    #组装消息字典
    msg = {}
    msg['Type'] = typeMsg
    msg['Text'] = msgInfo
    msg['FromUserName'] = userFrom
    text_reply(msg)
    #print(msg)
    return True

    
@itchat.msg_register
def general_reply(msg):
    return 'I received a %s' % msg['Type']

@itchat.msg_register
def simple_reply(msg):
    if msg['Type'] == TEXT:
        return 'I received: %s' % msg['Content']

@itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING])
def text_reply(msg):
    itchat.send('%s: %s' % (msg['Type'], msg['Text']), msg['FromUserName'])

# 以下四类的消息的Text键下存放了用于下载消息内容的方法，传入文件地址即可
@itchat.msg_register([PICTURE, RECORDING, ATTACHMENT, VIDEO])
def download_files(msg):
    msg['Text'](msg['FileName'])
    return '@%s@%s' % ({'Picture': 'img', 'Video': 'vid'}.get(msg['Type'], 'fil'), msg['FileName'])

# 收到好友邀请自动添加好友
@itchat.msg_register(FRIENDS)
def add_friend(msg):
    itchat.add_friend(**msg['Text']) # 该操作会自动将新好友的消息录入，不需要重载通讯录
    itchat.send_msg('Nice to meet you!', msg['RecommendInfo']['UserName'])

# 在注册时增加isGroupChat=True将判定为群聊回复
@itchat.msg_register(TEXT, isGroupChat = True)
def groupchat_reply(msg):
    if msg['isAt']:
        itchat.send(u'@%s\u2005I received: %s' % (msg['ActualNickName'], msg['Content']), msg['FromUserName'])
 

if __name__ == "__main__": 
    #登录微信网页版(二维码扫码)
    itchat.auto_login(enableCmdQR = -1, hotReload = True)
    
    #获取所有好友信息
    account = itchat.get_friends() 
    
    # #获取自己的UserName
    userName = account[0]['UserName']
    #print (account[0]) 
    #print (account[1])  


    #测试消息发送
    #Send_Msg("MlNA", "Test Python Winxin API...", "TEXT" )
    Send_Msg("filehelper", "Test Python Winxin API...", "TEXT" )

    #运行 
    itchat.run()
exit()

import thread
import itchat
from itchat.content import *

replyToGroupChat = True
functionStatus = False

def change_function():
    if replyToGroupChat != functionStatus:
        if replyToGroupChat:
            @itchat.msg_register(TEXT, isGroupChat = True)
            def group_text_reply(msg):
                if u'关闭' in msg['Text']:
                    replyToGroupChat = False
                    return u'已关闭'
                elif u'开启' in msg['Text']:
                    return u'已经在运行'
                return u'输入"关闭"或者"开启"测试功能'
        else:
            @itchat.msg_register(TEXT, isGroupChat = True)
            def group_text_reply(msg):
                if u'开启' in msg['Text']:
                    replyToGroupChat = True
                    return u'重新开启成功'
        functionStatus = replyToGroupChat
thread.start_new_thread(itchat.run, ())

while 1:
    change_function()
    time.sleep(.1)



 
