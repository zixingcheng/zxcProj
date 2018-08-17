# -*- coding: utf-8 -*-
"""
Created on  张斌 2016-09-02 16:30:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com

    Error操作 
"""
import os
import myDebug

    
#自定义错误
class myEx(Exception):
    def __init__(self, msg):
        self.msg = msg


def Error(msg, ErrType = "Error"):
    print("ErrorInfo: %s, Type(%s)" %(msg, ErrType))


    
if __name__ == '__main__':   
    try:
        a = 1/ 0 
    except (myEx):
        myDebug.Error(myError.myEx.msg)
