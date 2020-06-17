# -*- coding: utf-8 -*-
"""
Created on  张斌 2020-05-15 11:00:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com

    窗体管理器，消息发送测试, 基于pyqt5
    @依赖库： pyqt5
"""
import sys, ast, time, threading
import myWinForm_Manager


if __name__ == '__main__':
    pWinManager = myWinForm_Manager.myWinForm_Manager()
    
    usrID = "茶叶一主号"
    usrName = "茶叶一主号"
    nameNick = "茶叶一主号"
    usrPlat = "wx"
    groupID = ""
    groupName = ""
    nameSelf = False

    num = 100
    while(num > 0):
        infCmd = {"tag": "Test_0", "value": 0.5, "msg": "上涨5%--" + str(num)}
        pWinManager.sendMsg("quote", infCmd, usrID, usrName, nameNick, usrPlat, groupID, groupName, nameSelf)
        num -= 1
        time.sleep(4)

