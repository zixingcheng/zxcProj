# -*- coding: utf-8 -*-
"""
Created on  张斌 2020-10-26 09:58:00 
    @author: zhang bin
    @email:  zhangbin@qq.com

    Ftp Server --拉取脚本启动，单例
""" 
import os, time, requests, mySystem 
from os.path import join as pjoin
import json, shutil

#引用根目录类文件夹--必须，否则非本地目录起动时无法找到自定义类
mySystem.Append_Us("", False)  
import myFTP, myIO, mySecurity

    
# FTP配置信息-市生态环境局_DMZ
VaildDays = 30              #有效天数，超出忽略，以避免远期数据持续同步
VaildDays_LastFile = 45     #有效天数(本地保存时间)，超出删除 
Host = "120.197.146.81"      
Port = 9001
User = "downloadZP"        
UserPW = "Down$#.,]ZP"
User2 = "uploadZP"        
UserPW2 = "Z.,Mi^*P"
User3 = "ZPmicrodownload"        
UserPW3 = "Z.!@#]micro.P#$,Dow<>?load"
User4 = "taskup"        
UserPW4 = "Css!@.#$cowrk.cdMO"

# 本地上传文件夹路径
localBase = '/root/App/ftpData/ftpDocking'
localBase = 'D:/ftpData/ftpDocking' 
localDir = localBase + "/task"   
dataFloder = ''     
localDir2 = localBase + "/taskfeed"   
dataFloder2 = '' 
localDir3 = localBase + "/alarm"   
dataFloder3 = ''  
localDir4 = localBase + "/taskcompany"   
dataFloder4 = ''  

jobDir = 'D:/myCode/zxcProj/src/Zxc.Core/zpCore.MicroStation/ftpData'
#jobDir = '/root/App/api-WZ/ftpData'

if __name__ == '__main__':    
    from myGlobal import gol  
    gol._Init()             #先必须在主模块初始化（只在Main模块需要一次即可）
    #单例运行检测
    if(gol._Run_Lock(__file__) == False):
       exit(0)
       
    # 初始Ftp并运行 
    print(F"Start:: runFTP({str(os.getpid())})")
    pFTP_downLoad = myFTP.myFTP_Monitor(Host, Port, User, UserPW, localDir, dataFloder, 12, VaildDays, VaildDays_LastFile)
    pFTP_upLoad = myFTP.myFTP_Monitor(Host, Port, User2, UserPW2, localDir2, dataFloder2, 12, VaildDays, VaildDays_LastFile)
    pFTP_downLoad2 = myFTP.myFTP_Monitor(Host, Port, User3, UserPW3, localDir3, dataFloder3, 12, VaildDays, VaildDays_LastFile) 
    pFTP_downLoad3 = myFTP.myFTP_Monitor(Host, Port, User4, UserPW4, localDir4, dataFloder4, 12, VaildDays, VaildDays_LastFile) 
    

    # 处理任务下载信息
    @pFTP_downLoad.my_ftp.downloaded_file()
    def Reply1(file_name, local_path): 
        path = jobDir + "/task/" + file_name
        path_old = jobDir + "/task_old/" + file_name
        if(os.path.exists(path) == False and os.path.exists(path_old) == False):
            file_nameN = file_name.replace(".json", "_key.json")
            myIO.copyFile(local_path, jobDir + "/task/", file_nameN, False)
            mySecurity.DecryptFiles(jobDir + "/task/")
    # 拷贝任务上传信息
    def copyFiles_upload(): 
        files = myIO.getFiles(jobDir + "/taskfeed/")
        for x in files:
            if(os.path.isdir(x)): 
                if(len(myIO.getFiles(x)) == 0):
                    myIO.deldir(x)
                continue;
            fileName = myIO.getFileName(x)
            picDir = ""
            if("pic_" in fileName):
                picDir = "/" + fileName[0:17]
            infos = fileName.split('_')
            targetDir = localDir2 + "/" + infos[1][0:6] + "/" + infos[1] + picDir 
            myIO.copyFile(x, targetDir, '', False)
        #加密文件处理-暂留
        #mySecurity.EncryptFiles(jobDir + "/alarm/")
        
    # 处理告警下载信息
    @pFTP_downLoad2.my_ftp.downloaded_file()
    def Reply2(file_name, local_path): 
        path = jobDir + "/alarm/" + file_name
        path_old = jobDir + "/alarm_old/" + file_name
        if(os.path.exists(path) == False and os.path.exists(path_old) == False):
            file_nameN = file_name.replace(".json", "_key.json")
            myIO.copyFile(local_path, jobDir + "/alarm/", file_nameN, False)
            mySecurity.DecryptFiles(jobDir + "/alarm/")
             
    # 处理企业任务下载信息
    @pFTP_downLoad3.my_ftp.downloaded_file()
    def Reply3(file_name, local_path): 
        path = jobDir + "/taskcompany/" + file_name
        path_old = jobDir + "/taskcompany_old/" + file_name
        if(os.path.exists(path) == False and os.path.exists(path_old) == False):
            file_nameN = file_name.replace(".json", "_key.json")
            myIO.copyFile(local_path, jobDir + "/taskcompany/", file_nameN, False)
            mySecurity.DecryptFiles(jobDir + "/taskcompany/")

    # 下载        
    pFTP_downLoad.my_ftp.noVaildwords = ["step"]
    #pFTP_downLoad.downLoad_files();
    #pFTP_downLoad2.downLoad_files();
    #pFTP_downLoad3.downLoad_files();

    # 上传
    copyFiles_upload()
    pFTP_upLoad.upLoad_files();

    exit(0)
     