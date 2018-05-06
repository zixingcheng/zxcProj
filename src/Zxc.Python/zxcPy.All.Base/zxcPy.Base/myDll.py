# -*- coding: utf-8 -*-
"""
Created on  张斌 2018-04-02 18:00:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com

    动态库接口操作
"""
import sys, string, re, ctypes
import time
 

#转换为str由char* 
def Create_Dll(pathDll): 
    return ctypes.CDLL(pathDll);  

#转换为str由char* 
def To_Str_ByChar(ptr, strEncod = 'gb2312'): 
    return ctypes.string_at(ptr, -1).decode(encoding = strEncod)

#转换为char*参数    
def To_Char(strValue, strEncod = "gb2312"):
    return ctypes.c_char_p(bytes(strValue, encoding = strEncod))
