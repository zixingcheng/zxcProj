#encoding: utf-8 
# -*- coding: utf-8 -*-
"""
Created on  张斌 2016-09-23 16:00:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com

    Gsafety行政管理系统特定操作方法集，项目信息提取更新及ID检索
"""

import sys, os ,shutil ,string ,codecs 
import urllib,urllib.parse
import requests 
from html.parser  import  HTMLParser
from lxml import etree  


#引用根目录类文件夹
#sys.path.append(r'D:/我的工作/学习/MyProject/日报提交/myFunction')
sys.path.append(r'../myFunction')


#全局项目字典
pDict = dict()

    
#获取所有项目信息       
def __get_prjinfo_all__(clsWeb):
    
    #获取外出项ID，然后删除之
    strUrl = "util/frametree/OpensingleXtreeAction.do?datatype=son&openid=attendance_project&rootname=项目工作&conds=projectname@like&param=508,260&keyname=projectid"
    clsWeb.__set_param__(strUrl)
    r = requests.get(clsWeb.Referer, cookies = clsWeb.cookie)
    

    #lxml操作
    html = etree.HTML(r.text)
    
    #筛选数据，14个td才是数据开始 
    rr = html.xpath("/descendant::script[position()=14]") 
    nLen = len(rr) 
    if(nLen > 1):
        return (False, pDict)


    #初步解析，分解树结构
    strTemp = str(etree.tostring(rr[0]))
    strTemps = strTemp.split('new xyTree.NodeNormal')

    nLen = len(strTemps)
    if(nLen < 2):
        return (False, pDict)

 
    #中文网页编码解析对象	
    htmlparser = HTMLParser()
    
    #循环提取所有并解析
    for i in range(1, nLen):
        strTemp2 = str(strTemps[i])
        strTemps2 = strTemp2.split(' = ')

	#提取有值对象
        if(len(strTemps2)>0):
            #for j in range(0, len(strTemps2)):
                #print(strTemps2[j])
                
            strName = clsWeb.Get_EleStr(strTemps2[0],"(\\'","\\');")
            strKey = clsWeb.Get_EleStr(strTemps2[1],"\\'","\\';")

            #中文转换
            strName = htmlparser.unescape(strName)
            pDict[strName] = strKey
            #print(strName)
            #print(pDict[strName])
            
    #保存项目字典
    path = "./mySetting/Prj_Dict.csv"
    __write_prjinfo_all__(pDict, path)
    return (True, pDict)

#记录项目信息       
def __write_prjinfo_all__(pDict, path):
    #提取配置文件  
    f = codecs.open(path, 'wb+', 'utf-8')    

    #循环输出结果
    for key in pDict.keys():
        f.write('%s,%s\r\n' % (key, pDict[key])) 
         
    #关闭文件      
    f.close()
    return True

#检索项目信息及Key 
def __get_prj__(pKey):
    #完整匹配
    pKey = pKey.strip()
    match_data = {}
    for (key, value) in pDict.items(): 
        if key == pKey:
            match_data[key] = value
            return match_data
            
    match_data = {}
    for (key, value) in pDict.items():
        #if key.startswith(pKey):
        if key.find(pKey) >=0 :
            match_data[key] = value
            #print(key)

    return match_data



