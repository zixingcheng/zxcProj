# -*- coding: utf-8 -*-
"""
Created on  张斌 2016-09-02 16:30:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com

    IO操作 
"""
import os, time, codecs
import shutil

 
#创建文件夹，存在则忽略
def mkdir(path, bTitle = True, bNew = False): 
    # 去除首位空格
    path = path.strip()
    
    # 去除尾部 \ 符号
    path = path.rstrip("\\")
 
    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    isExists = os.path.exists(path)
 
    #删除已存在文件
    if(isExists and bNew):
        shutil.rmtree(path)
        time.sleep(0.1)
        isExists = False

    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        # 创建目录操作函数
        os.makedirs(path) 
 
        if(bTitle): print (path + ' 创建成功')
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        if(bTitle): print (path + ' 目录已存在')
        return False
    
    
#提取文件名集(递归子文件)
def getFiles(path, wildcard = "", iswalk = True):
    #提取文件后缀
    suffixs = wildcard.split(" ")

    #循环识别所有
    list_Files = []
    if(iswalk == False):
        files = os.listdir(path)
        for name in files:
            for suffix in suffixs:
                if(name.endswith(suffix)):
                    list_Files.append(Trans_NoBOM(path) + "\\" + Trans_NoBOM(name))
                    break
        return list_Files
    
    #递归子文件
    for root, subdirs, files in os.walk(path):
        lstFile = getFiles(root, wildcard, False)
        for x in lstFile:
            list_Files.append(x)
    return list_Files
def getFileName(path, isNosuffix = True):
    #提取文件后缀
    name = os.path.basename(path)

    if(isNosuffix):
        name = name.split(".")[0]
    return name


#提取文件信息
def getContent(path, noBOM = False, bList = False, isUtf = True):
    #提取文件Json串
    if (os.path.exists(path) == False):
        if(bList): return None
        else: return ""
    if(isUtf):
        f = codecs.open(path, 'r', 'utf-8')  
    else:
        f = codecs.open(path, 'r') 
    if(bList == False):
        content = f.read() 
        if(noBOM):
            content = Trans_NoBOM(content)
    else:
        lists = f.readlines()
        if(noBOM and len(lists)>0 and len(lists[0]) > 0):
            lists[0] = Trans_NoBOM(lists[0])
            
        content = []
        for strLine in lists: 
            strLine = Trans_NoBOM(strLine)
            content.append(strLine)

    #关闭文件      
    f.close()
    return content
#提取文件信息
def getContents(path, noBOM = False, isUtf = True):
    #提取文件Json串
    if (os.path.exists(path) == False):
        return ""
    if(isUtf):
        f = codecs.open(path, 'r', 'utf-8')  
    else:
        f = codecs.open(path, 'r')  
    lists = f.readlines()
    if(noBOM and len(lists[0]) > 0):
        lists[0] = Trans_NoBOM(lists[0])
        
    bEnd = False;
    list_content = []
    content = ""
    for strLine in lists: 
        strLine = Trans_NoBOM(strLine)
        list_content.append(strLine)
                
    #关闭文件      
    f.close()
    return list_content 
#提取文件信息, 指定标识处终止
def getContent_EndByTag(path, strTag = "@@", noBOM = False, isUtf = True):
    #打开文件提取数据
    if (os.path.exists(path) == False):
        return "",[] 
    if(isUtf):
        f = codecs.open(path, 'r', 'utf-8')  
    else:
        f = codecs.open(path, 'r')    
    lists = f.readlines()
    if(noBOM and len(lists[0]) > 0):
        lists[0] = Trans_NoBOM(lists[0])
        
    bEnd = False;
    list_content = []
    content = ""
    for strLine in lists:
        #print(strLine)
        strTemp = strLine.strip() 
        if len(strTemp) > 2:
            nIndex = strTemp.find(strTag)  
            if nIndex == 0:
                bEnd = True
             
        if(bEnd):
            list_content.append(strLine)
        else:
            content += strLine
 
    #关闭文件      
    f.close()
    return (content,list_content)
 

#获取代码文件路径函数 2017-10-18
def getPath_ByFile(file):
    strDir = os.path.split(os.path.realpath(file))[0]
    strName = os.path.split(os.path.realpath(file))[1]
    return (strDir, strName)


#定义文件拷贝函数 2017-10-18
def copyFile(scrPath,  targetDir, name = ""):
    #组装目标文件路径
    fileName = os.path.basename(scrPath)
    if(name != ""):
        fileName = name
    destPath = targetDir + os.path.sep + fileName  

    #目标文件夹检测
    if (os.path.exists(targetDir) == False):
        mkdir(targetDir)
        
    #源文件存在则拷贝
    if (os.path.exists(scrPath)): 
        shutil.copy(scrPath, destPath)
        print("copy %s %s" % (scrPath, destPath))
#定义文件加内拷贝函数 2017-10-18
def copyFiles(scrDir, targetDir, wildcard = "", iswalk = False):
    #目标文件夹检测
    if (os.path.exists(targetDir) == False):
        mkdir(targetDir)
        
    #源文件存在则拷贝
    if (os.path.exists(scrDir)): 
        files = getFiles(scrDir, wildcard, iswalk)
        for file in files:
            copyFile(file, targetDir)

#去除BOM头
def Trans_NoBOM(strBom):
    #去除BOM头
    if strBom.startswith(u'\ufeff'): 
        strBom = strBom.encode('utf8')[3:].decode('utf8')
    return strBom

#保存文件信息
def Save_File(path, text, isUtf = True, isNoBoom = True):
    if(isUtf):
        pFile = codecs.open(path, 'w', 'utf-8')
    else:
        pFile = codecs.open(path, 'w')
        
    if(isNoBoom):
        text = Trans_NoBOM(text)

    pFile.write(text)
    pFile.close()


# 定义要创建的目录
#mkpath="d:\\qttc\\web\\"
# 调用函数
#mkdir(mkpath)
