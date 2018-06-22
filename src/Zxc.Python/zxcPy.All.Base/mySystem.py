# -*- coding: utf-8 -*-
"""
Created on  张斌 2017-10-16 11:30:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com

    mySystem, 置于Python系统环境下，便于直接引用
"""

import sys, os 

#定义全局默认路径
m_strFloders = ["/myPy_Libs"]


#定义默认的系统目录引用(文件引用或shell时的系统路径缺失补全，补全自定义的myPy_Libs、GModel_Py_Base等路径，其中GModel_Py_Base为模型原始数据，并拷贝到myPy_Libs，位于python库\Lib\site-packages下)
def Append_Us(path = "", bPrint = False, file = None):
    #获取文件路径信息
    rootDir = path.strip()
    if(rootDir == "") :
        rootDir = sys.path[0]

    #定义系统文件夹myPy_Libs、GModel_Py_Base
    strFloders = m_strFloders   

    #调用添加引用
    Append(rootDir, strFloders, bPrint)

    
    #获取当前根目录路径信息，并调用添加引用
    baseDir = os.getcwd() 
    if(rootDir != baseDir):
        Append(baseDir, strFloders, bPrint)
        

    #系统目录，并调用添加引用
    sysDir = os.path.split(os.path.realpath(__file__))[0]
    if(rootDir != sysDir):
        Append(sysDir, strFloders, bPrint)


    #其他自定义路径
    if(file != None):
        if(os.path.exists(path) == False):
            strDir = os.path.split(os.path.realpath(file))[0]
            Append_Dir(strDir, bPrint)
            Append_Dir(strDir + "/" + path, bPrint)
        else:
            Append_Dir(path, bPrint)

    #返回当前文件路径
    return sysDir
    
#定义默认的系统目录引用，路径下的相对文件夹自由定义为系统引用
def Append(path, floders = [], bPrint = False):
    #获取文件路径信息
    strFile = path
    strDir = os.path.abspath(os.path.join(strFile, "")) 
        
    #引用根目录类文件夹
    for i in floders: 
        pDir = strDir + i
        Append_Dir(pDir, bPrint)
        
#增加的系统目录引用
def Append_Dir(strDir, bPrint = False):        
    #引用根目录类文件夹
    if(os.path.exists(strDir) == False): return
    sys.path.append(strDir)
    if(bPrint):
        print(strDir) 
    
     
if __name__ == '__main__':   
    #添加当前默认路径到系统目录
    Append_Us("", True)




