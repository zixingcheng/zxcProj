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
        super().__init__(self) #初始化父类
        self.msg = str(msg)
    def ToString(self):
        return self.msg

def Error(ex, bSave = True):
    pEx = myEx(ex)
    myDebug.Error(pEx.msg)

    
if __name__ == '__main__':   
    try:
        a = 1/ 0 
    except Exception as e:
        Error(e)
