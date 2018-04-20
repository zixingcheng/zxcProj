# -*- coding: utf-8 -*-
"""
Created on  张斌 2017-11-19 19:30:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com

    Import操作（含部分反射操作） 
"""
import sys, os 


#导入模块名类名，反射创建
def Import_Class(module_name, class_name):
    module_meta = Import_Module(module_name, class_name)
    class_meta = getattr(module_meta, class_name)
    return class_meta

#导入模块名类名，反射创建模块元数据对象
def Import_Module(module_name, class_name):
    module_meta = __import__(module_name, globals(), locals(), [class_name])
    return module_meta


    
#主启动程序
if __name__ == "__main__":
    sys.path.append("myPy_Libs")
    sys.path.append("C:\Python35-32\Lib\site-packages\myPy_Libs")
    print(sys.path)
    
    pField = Import_Class('myPy_Libs.myDict_Field','Item_Field')()
    pField.Name = "Test"  
    pField.Name_En = "Test"
    pField.Value_Default = "Test_Value"
    print(pField.To_String(False))  
