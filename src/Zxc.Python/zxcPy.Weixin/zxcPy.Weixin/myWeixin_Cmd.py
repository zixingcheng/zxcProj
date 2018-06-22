# -*- coding: utf-8 -*-
"""
Created on  张斌 2017-11-19 14:58:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com

    Rest API --Weixin API操作 
"""
import os, time  
import mySystem 
    
#引用根目录类文件夹--必须，否则非本地目录起动时无法找到自定义类
mySystem.Append_Us("", False)    
import myWeb, myMMap
from myGlobal import gol   


#API-命令--共享内存
class myAPI_Weixin_Cmd(myWeb.myAPI): 
    def get(self, user, text, type = "Text"):
        pMMap_Manager = gol._Get_Value('manageMMap')
        if(pMMap_Manager == None):
            return False
        print(user, text, type)

        #生成并写入命令
        dict0 = {'FromUserName': user, 'Text': text, 'Type': type}        
        pMMdata = myMMap.myMMap_Data(dict0, 0)      #生成命令--共享内存数据对象
        ind = pMMap_Manager.Write(pMMdata)          #写入命令--共享内存
        
        #读取测试
        pMMdata_M2, ind2 = pMMap_Manager.Read(ind)  
        print(pMMdata_M2.value)
        return ind


#主程序启动
if __name__ == '__main__': 
    # 创建内存映射
    try:
        pMMap_Manager = myMMap.myMMap_Manager("D:\myGit\zxcProj\src\Zxc.Python\zxcPy.Weixin\Data/zxcMMap.dat")
        
        ind = 0
        while(True):
            dict0 = {'FromUserName': '茶叶一主号', 'Text': 'text--登陆', 'Type': 'Text'}        
            pMMdata = myMMap.myMMap_Data(dict0, 0)
            #ind = pMMap_Manager.Write(pMMdata)
            
            pMMdata_M2, ind = pMMap_Manager.Read(ind, True)
            if(pMMdata_M2 != None):
                print(pMMdata_M2.value)
            time.sleep(1)
    except:
        bWrite = False
    exit()