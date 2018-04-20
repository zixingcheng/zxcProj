# -*- coding: utf-8 -*-
"""
Created on  张斌 2016-09-16 15:56:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com

    Gsafety行政管理系统特定操作方法集，md记录的日志信息提取

日志Md文件格式如下：(@@为特殊字符，除时间必须设置外，其他可忽略)
    
# 2017-09-20 09:00

## 生命线云平台 @@(3h)@@10

	1.测试工作内容1；
	2.测试工作内容2； 
	3.测试工作内容3； 

## 生命线云平台 @@(3h)

	1.测试工作内容21；
	2.测试工作内容22； 
	3.测试工作内容23；
	
## 生命线云平台 @@(3h)

	1.测试工作内容31；
	2.测试工作内容32； 
	3.测试工作内容33；
	
## @@其他

### @@下周安排
	测试安排，可无，可无"下周安排"节点

### @@问题

    测试问题，可无，可无"问题"节点
   
### @@备注

	测试备注，可无，可无"备注"节点
"""

#定义结构体--单项（##）
class Item_Note_Child:
    def __init__(self):
        self.Name = ""      #节点名称
        self.ID = ""        #节点项目编号
        self.Hours = 0      #节点花费时间
        self.Computed = 1   #节点完成度
        self.List = []      #节点完成内容
        self.IsSys = False  #节点是否默认
       
#定义结构体--Note 
class Item_Note:
    def __init__(self):     
        self.Name = ""      #日志名称 
        self.Time = ""      #日志对应时间字符串 2017-09-20 09:00
        self.Title = ""     #日志说明
        self.List = []      #节点完成内容
        self.Tag = 0        #标识当前级别 
        self.IsOverTime = False     #标识是否加班时间
        

import os
import sys
import shutil
import string
import time,  datetime
#import Item_Note_Child 
#import Item_Note


#引用根目录类文件夹
#sys.path.append(r'D:/我的工作/学习/MyProject/日报提交/myFunction')
sys.path.append(r'../myFunction')


#获取路径信息
baseDir = os.getcwd()
baseDir_Root = os.path.abspath(os.path.join(os.getcwd(), ".."))

pathNote = baseDir_Root + "/Note_Now.md"    #Note_Now配置文件路径，py脚本上级目录 
dirNotes = baseDir_Root + "/Notes"          #Note备份文件，Note_Now中记录后会复制一份备份
#print("test %s" % (pathNote))




#是否为Note节点(通用) --单个#,子节点##,子子节点####     
def __IsNote__(strNode, strFirt ="#" ,strSec = "#" ,nCount =1):    
    strInfo = strNode.strip()
    if(strInfo.count(strSec) != nCount):
        return False
    
    strInfo = strInfo[0: strInfo.find(strFirt)]
    if(strInfo == strFirt):
        #print(strInfo[0:2])
        return False
    return True
 
#生成Note节点对象(通用) --单个#,子节点##,子子节点#### ,系统@@  
def __Get_NoteInfo__(strNode, strFirt ="#" ,strSec = "@@"):
    #解析数据
    strInfo = strNode.strip()
    strTemps = strInfo.split(strFirt)
    if(len(strTemps)<1):
        return
    
    strSets = strTemps[1].split(strSec)
    nSets = len(strSets)
    if(len(strSets)<1):
        return
        
    #依次塞入List 
    List = []
    for i in range(0, nSets): 
        List.append(strSets[i].strip()) 
    return List


#生成Note节点对象
def __CreateNote__(strNode):
    #解析数据
    List = __Get_NoteInfo__(strNode, "#") 
    
    #初始对象
    pNote = Item_Note()
    pNote.Time = List[0] 
    pNote.Name = ""
    pNote.Title = "" 
    pNote.List = [] 
    pNote.Tag = 0
    pNote.IsOverTime = False


    #获取名称
    nLen =len(List)
    if(nLen > 1):
        pNote.Name = List[1]
        
    #是否全天加班
    if(nLen > 2):
        pOver = List[2]
        if(pOver.strip() == "加班"):
            pNote.IsOverTime = True
    
    return pNote
#生成Note子节点对象
def __CreateNote_Child__(strNode, strFirt ="##"):
    #解析数据
    List = __Get_NoteInfo__(strNode, strFirt)
    nCount = len(List)
    if(nCount<2):
        return       
    
    #初始对象
    pChild = Item_Note_Child()
    pChild.List = []
    pChild.Computed =1
    if(List[0] == ""):
        pChild.Name = List[1]
        pChild.Hours = 0
        pChild.IsSys = True  
    else: 
        pChild.Name = List[0]
        pChild.Hours = List[1] 
        pChild.IsSys = False
        if(nCount > 2):
            pChild.Computed = List[2]
    return pChild
 

#生成Note节点对象信息
def __CreateNote_Info__(pNote, strNode):
    #解析数据,不以#开头
    strInfo = strNode.strip()
    if(strInfo.find("#") == 0):
        #判断是否为子节点
        if(__IsNote__(strInfo, "##", "#", 2) == True): 
            #创建子节点
            pChild = __CreateNote_Child__(strNode)
            pNote.List.append(pChild)
            pNote.Tag = 1
            return True
        else:
            return False

    #记录节点Title
    if(pNote.Title == ""):        
        pNote.Title = strInfo
    else:
        pNote.Title = pNote.Title + strInfo 
    return True 
#生成Note子节点对象信息
def __CreateNote_ChildInfo__(pNote, strNode):
    #解析数据,不以#开头
    strInfo = strNode.strip()
    if(strInfo.find("#") == 0):
        #判断是否为子节点
        if(__IsNote__(strInfo, "##", "#", 2) == True):  
            #创建子节点
            return __CreateNote_Info__(pNote, strNode) 
        else:
            #判断是否为子子节点
            if(__IsNote__(strInfo, "###", "#", 3) == True):  
                #创建子节点
                pChild2 = __CreateNote_Child__(strNode, "###") 
                                
                nChild = len(pNote.List)
                pChild = pNote.List[nChild - 1] 
                pChild.List.append(pChild2)                
                pNote.Tag = 2
                return True
            else:
                return False 

    #记录节点信息
    nChild = len(pNote.List)
    pChild = pNote.List[nChild - 1]
    pChild.List.append(strInfo) 
    return True 
#生成Note子节点对象信息
def __CreateNote_ChildInfo2__(pNote, strNode):
    #解析数据,不以#开头
    strInfo = strNode.strip()
    if(strInfo.find("#") == 0):
        #判断是否为子子节点
        if(__IsNote__(strInfo, "###", "#", 3) == True):  
            #创建子节点
            pChild2 = __CreateNote_Child__(strNode, "###") 
                                
            nChild = len(pNote.List)
            pChild = pNote.List[nChild - 1] 
            pChild.List.append(pChild2)                
            pNote.Tag = 2
            return True
        else:
            return False  

    #记录节点信息
    nChild = len(pNote.List)
    pChild = pNote.List[nChild - 1]
    
    nChild2 = len(pChild.List)
    pChild2 = pChild.List[nChild2 - 1]
    pChild2.List.append(strInfo)     
    return True
#生成Note节点对象具体信息(逐行)
def __CreateNote_Infos__(pNote, strNode):
    #解析数据
    strInfo = strNode.strip()
    if(strInfo == ""):
        return True

    #按级别依次处理 0:Note 1:Note子节点 2:@@其他字节点
    if(pNote.Tag == 0):
        #Note根
        return __CreateNote_Info__(pNote, strNode)
    
    if(pNote.Tag == 1):
        #Note子节点
        return __CreateNote_ChildInfo__(pNote, strNode)
    
    if(pNote.Tag == 2):
        #Note子子节点
        return __CreateNote_ChildInfo2__(pNote, strNode)
         
    return False


#打印节点信息      
def OutPut(pNotes): 
    #循环输出结果 
    for i in range(0, len(pNotes)):                   
        pNote = pNotes[i]                   
        print("pNote.Time %s" % (pNote.Time))
        print("pNote.Name %s" % (pNote.Name))
        print("pNote.Title %s" % (pNote.Title))
 
        for j in range(0, len(pNote.List)):
            pChild = pNote.List[j]
            print("pChild.Name %s" % (pChild.Name))
            print("pChild.Hours %s" % (pChild.Hours))
            print("pChild.Computed %s" % (pChild.Computed))
            print("pChild.IsSys %s" % (pChild.IsSys))
                       
            for k in range(0, len(pChild.List)): 
                if(pChild.IsSys == False):
                    print("pChild.List %s: %s" % (k, pChild.List[k])) 
                else:                           
                    pChild2 = pChild.List[k]
                    print("pChild2.Name %s" % (pChild2.Name))
                    print("pChild2.Hours %s" % (pChild2.Hours))
                    print("pChild2.Computed %s" % (pChild2.Computed))
                    print("pChild2.IsSys %s" % (pChild2.IsSys))
                           
                    for m in range(0, len(pChild2.List)): 
                        print("pChild.List %s: %s" % (m, pChild2.List[m]))
                        


#解析配置文件      
def _Get_Notes_(path):    
    #提取配置文件
    if (os.path.exists(path) == False):
        print(path)
        return 
    f = open(path, 'r', encoding = 'utf-8')  
    lists = f.readlines()
    pNotes = []
    bStart = False

    #解析，以#为主节点进行分割
    nLines = len(lists) 
    for i in range(0, nLines):
        #忽略空字符串
        if(lists[i].strip() == ""): 
            continue
        
        #Note节点
        if(__IsNote__(lists[i]) == True):
            #生成Note对象
            pNote = __CreateNote__(lists[i])
            pNotes.append(pNote)
            bStart = True
        else:
            if(bStart):
                if(pNote):
                    __CreateNote_Infos__(pNote, lists[i])        
        
    #关闭文件      
    f.close() 
    return pNotes

#截取符号后数据     
def _Get_Content_(strInfo, strFlit = '.'):
    nIndex = strInfo.find('.')
    if(nIndex > 0 and nIndex < 3):
        strInfo = strInfo[nIndex + 1: -1]
    return strInfo

    
import codecs
def _Write_Note_(path, pNote):    
    #提取配置文件  
    f = codecs.open(path, 'wb+', 'utf-8')
    

    #循环输出结果
    strNote = ''
    strNote_Else = ''
    nIndex = 1

    if(pNote):
        f.write('# %s @@%s \r\n\r\n' % (pNote.Time, pNote.Name))   
        f.write('%s \r\n\r\n' % (pNote.Title))
        
        strNote += ('\r\n\r\n工作内容：\r\n\r\n') 

        #循环所有子节点
        for j in range(0, len(pNote.List)):
            pChild = pNote.List[j]
            if(pChild.IsSys == True):
                f.write('## @@%s \r\n\r\n' % (pChild.Name)) 
            else:
                f.write('## %s  @@%s  @@%s \r\n\r\n' % (pChild.Name, pChild.Hours ,pChild.Computed))
                
            #循环所有子子节点
            strWork = ''
            for k in range(0, len(pChild.List)): 
                if(pChild.IsSys == False):
                    f.write('\t%s \r\n' % (pChild.List[k]))
                    strWork = _Get_Content_(pChild.List[k])
                    strNote += ('    %d. %s@@%s(项目工时：%s 完成度：%s%s) \r\n\r\n' % (nIndex ,strWork, pChild.Name, pChild.Hours, pChild.Computed, "%"))
                    nIndex += 1
                else:                           
                    pChild2 = pChild.List[k]
                    f.write('### @@%s \r\n\r\n' % (pChild2.Name))                    
                    strNote_Else += ('%s: \r\n' % (pChild2.Name))
                           
                    for m in range(0, len(pChild2.List)): 
                        f.write('\t%s \r\n' % (pChild2.List[m]))
                        strNote_Else += ('    %s \r\n\r\n' % (pChild2.List[m]))
                        
                    #子子节点数据写完增加换行
                    f.write('\r\n')    
                        
            #子节点数据写完增加换行
            f.write('\r\n')  
            

    #输出OneNote格式
    strNote += ('\r\n\r\n其他内容：\r\n')
    strNote += ('上班时间：%s \r\n\r\n' % (pNote.Time))
    strNote += ('%s \r\n\r\n' % (strNote_Else))
    #print (strNote)
    f.write('%s \r\n' % (strNote))  
        
    #关闭文件      
    f.close()
    return True
 
        
     
if __name__ == '__main__':
    print(pathNote)
    pNotes = _Get_Notes_(pathNote)

    #循环输出结果      
    OutPut(pNotes)


    #pathNote2 = baseDir_Root + "/Note_Now2.md"    #Note_Now配置文件路径，py脚本上级目录 
    #_Write_Note_(pathNote2, pNotes[0])
