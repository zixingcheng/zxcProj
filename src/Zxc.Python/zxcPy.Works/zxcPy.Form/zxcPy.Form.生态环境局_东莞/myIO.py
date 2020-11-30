# -*- coding: utf-8 -*-
"""
Created on  张斌 2016-09-02 16:30:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com

    IO操作 
"""
import os, time, codecs, base64, zipfile
import shutil, random, datetime
 

#检查路径    
def checkPath(path):
    if(path.count("\\")):
        path = path.replace("\\", "/")
    while(path.count("//") > 0):
        path = path.replace("//", "/")
    return path
#删除文件夹
def deldir(path): 
    # 去除首位空格
    path = checkPath(path)
    path = path.strip()
    
    # 去除尾部 \ 符号
    path = path.rstrip("\\")

    #删除已存在文件
    if(os.path.exists(path)):
        shutil.rmtree(path)
#创建文件夹，存在则忽略
def mkdir(path, bTitle = True, bNew = False): 
    # 去除首位空格
    path = checkPath(path)
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
                    list_Files.append(checkPath(Trans_NoBOM(path) + "/" + Trans_NoBOM(name)))
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
    path = checkPath(path)
    name = os.path.basename(path)

    if(isNosuffix):
        name = name.split(".")[0]
    return name


#提取文件信息
def getContent(path, noBOM = False, bList = False, isUtf = True):
    #提取文件Json串
    path = checkPath(path)
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
    path = checkPath(path)
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
    path = checkPath(path)
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


# 将图片读入，对byte进行str解码
def getImage_Str(path):
    with open(path, 'rb') as f:
        img_byte = base64.b64encode(f.read())

    img_str = img_byte.decode('ascii')
    return img_str
# 将str解码，返回byte
def getImage_Byte(img_str):
    # 解码得到图像并保存 
    img_decode_ = img_str.encode('ascii')       # ascii编码
    img_decode = base64.b64decode(img_decode_)  # base64解码 
    return img_decode


#获取代码文件路径函数 2017-10-18
def getPath_ByFile(file):
    file = checkPath(file)
    strDir = os.path.split(os.path.realpath(file))[0]
    strName = os.path.split(os.path.realpath(file))[1]
    return (strDir, strName)


#定义文件拷贝函数 2017-10-18
def copyFile(scrPath, targetDir, name = "", recover = True):
    #组装目标文件路径
    scrPath = checkPath(scrPath)
    fileName = os.path.basename(scrPath)
    if(name != ""):
        fileName = name.split('.')[0] + "." + fileName.split(".")[1]
    destPath = targetDir + os.path.sep + fileName  
    destPath = checkPath(destPath)

    #目标文件夹检测
    if (os.path.exists(targetDir) == False):
        mkdir(targetDir)
        
    #源文件存在则拷贝
    if (os.path.exists(scrPath)): 
        if(recover):
            shutil.copy(scrPath, destPath)
            return destPath
        else:
            if (os.path.exists(destPath) == False): 
                shutil.copy(scrPath, destPath)
                return destPath
        print("copy %s %s" % (scrPath, destPath))
    return ""

#定义文件加内拷贝函数 2017-10-18
def copyFiles(scrDir, targetDir, wildcard = "", iswalk = False, bSameFloder = False):
    #目标文件夹检测
    if (os.path.exists(targetDir) == False):
        mkdir(targetDir)
        
    #源文件存在则拷贝
    if (os.path.exists(scrDir)): 
        files = getFiles(scrDir, wildcard, iswalk)
        for file in files:
            if(not os.path.isdir(file)):
                #文件夹深度处理
                dirTarget = targetDir
                if(bSameFloder):
                    dirTarget = os.path.dirname(file).replace(scrDir, targetDir)
                copyFile(file, dirTarget)

#去除BOM头
def Trans_NoBOM(strBom):
    #去除BOM头
    if strBom.startswith(u'\ufeff'): 
        strBom = strBom.encode('utf8')[3:].decode('utf8')
    return strBom

#保存文件信息
def Save_File(path, text, isUtf = True, isNoBoom = True):
    #文件夹初始
    path = checkPath(path)
    strDir, strName = getPath_ByFile(path)
    mkdir(strDir, False, False)

    if(isUtf):
        pFile = codecs.open(path, 'w', 'utf-8')
    else:
        pFile = codecs.open(path, 'w')
        
    text = Trans_NoBOM(text) 
    if(isNoBoom == False):
        text = u'\ufeff' + text
    pFile.write(text)
    pFile.close()

#保存压缩文件
def Save_Files_zip(files, newfiles, filedir, zip_name):
    filepath = checkPath(filedir + "/" + zip_name + '.zip')
    zp = zipfile.ZipFile(filepath,'w', zipfile.ZIP_DEFLATED)

    for x in range(0, len(files)):
        zp.write(files[x], newfiles[x])
    zp.close()
    time.sleep(3)
    print(zip_name + '-压缩完成。') 
    return True

#保存压缩文件夹
def Save_Floders_zip(floderdir, filedir, zip_name):
    filepath = checkPath(filedir + "/" + zip_name + '.zip')
    zp = zipfile.ZipFile(filepath,'w', zipfile.ZIP_DEFLATED)

    # 压缩文件的名字 
    for dirpath, dirmanes, filenames in os.walk(floderdir): 
        fpath = dirpath.replace(floderdir,'')   # 这一句很重要，不replace的话，就从根目录开始复制
        fpath = fpath and fpath + os.sep or ''

        # 当前文件夹以及包含的所有文件的压缩
        for filename in filenames: 
            zp.write(os.path.join(dirpath, filename), fpath + filename)
    zp.close()
    time.sleep(3)
    print(zip_name + '-压缩完成。') 
    return True

    
#生成唯一名称字符串
def create_UUID(): 
    nowTime = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")  # 生成当前时间
    randomNum = random.randint(0, 100)                          # 生成的随机整数n，其中0<=n<=100
    if randomNum <= 10:
        randomNum = str(0) + str(randomNum)
    uniqueNum = str(nowTime) + str(randomNum)
    return uniqueNum

