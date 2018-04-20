# -*- coding: utf-8 -*-
"""
Created on  张斌 2018-01-05 10:30:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com

    自定义python类安装脚本, 运行该脚本将相关自定义类复制到python默认库路径下
"""

import sys, io, os, shutil, string 
import mySystem


#获取路径信息
baseDir_Root = ""                           #环境路径
baseDir = os.getcwd()                       #改为读取文件路径，保证各种调用引用路径正确  


#提取Lib\site-packages路径作为自定义类安装路径
def getRootPath():
    strRoot = "/lib/site-packages"
    nLen = len(strRoot)

    #提取所有环境路径
    sysPahts = sys.path
    for path in sysPahts:
        path = path.replace("\\", "/") 
        if(len(path) > nLen and path[-nLen:] == strRoot):
            strRoot = path
            break
    return strRoot

#定义文件拷贝函数
def copyFile(scrPath,  targetDir):
    #组装目标文件路径
    fileName = os.path.basename(scrPath)
    destPath = targetDir + os.path.sep + fileName

    #目标文件夹检测
    if (os.path.exists(targetDir) == False):
        os.makedirs(targetDir)    

    #源文件存在则拷贝 
    if (os.path.exists(scrPath)): 
        print("copy %s %s" % (scrPath, destPath))
        shutil.copy(scrPath, destPath)


#解析配置文件      
def main():    
    #增加配置文件
    lists = []
    lists.append("mySystem.py=")
    lists.append("zxcPy.Base=/myPy_Libs")

    #提取根环境路径
    baseDir_Root = getRootPath()

    #解析配置文件
    for i in lists:
        #以=进行分割，前面为项目名称，后面为项目路径        
        strTemps = i.split('=')        
        strSrcPath = baseDir + "/" + strTemps[0].strip() 
        strDestPath = baseDir_Root + "/" + strTemps[1].strip()          
        
        #拷贝生成文件
        if (os.path.isfile(strSrcPath) == True):
            copyFile(strSrcPath, strDestPath)
        else:
            #拷贝文件夹
            List = os.listdir(strSrcPath)
            for path in List:
                srcPath = strSrcPath + "/" + path
                if os.path.isfile(srcPath) == True: 
                    copyFile(srcPath, strDestPath)

     
if __name__ == '__main__': 
    main()

