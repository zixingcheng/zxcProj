# -*- coding: utf-8 -*-
"""
Created on  张斌 2016-10-07 14:05:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com

    枚举类型操作
"""
from collections import namedtuple 
 
def enum(*keys):
    return namedtuple('Enum', keys)(*keys)
 
# 带字符数字映射的，像C/C++
def enum_index(*keys):
    return namedtuple('Enum', keys)(*range(len(keys)))
 
# 带字典映射的，可以映射出各种类型，不局限于数字
def enum_values(**kwargs):
    return namedtuple('Enum', kwargs.keys())(*kwargs.values())


#字符串转enum
def Tran_ToEnum(strKey, enum):
    nIndex = 0
    List = list(enum)
    if(strKey in List):
        nIndex = List.index(strKey)
        
    if(nIndex < 0):
        nIndex = 0 
    return enum[nIndex]
