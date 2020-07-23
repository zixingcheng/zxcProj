# -*- coding: utf-8 -*-
"""
Created on  张斌 2020-05-20 09:58:00 
    @author: zhang bin
    @email:  zhangbin@qq.com

    Ftp Server --脚本启动，单例
""" 
import os, mySystem 

#引用根目录类文件夹--必须，否则非本地目录起动时无法找到自定义类
mySystem.Append_Us("", False)  
import myFTP, myProcess_monitor
    
    
# FTP配置信息-市生态环境局
Host = "19.104.44.141"      
Port = 9010
User = "qixiang"        
UserPW = "qixtglptxiang"

# 本地上传文件夹路径
localDir = 'D:/ftpDGSQXJ/Data'        #-市气象局-Data文件夹 
dataFloder = 'Data'                 
    

if __name__ == '__main__':    
    from myGlobal import gol  
    gol._Init()             #先必须在主模块初始化（只在Main模块需要一次即可）
    #单例运行检测
    if(gol._Run_Lock(__file__) == False):
       exit(0)
       
    # 初始Ftp并运行 
    print(F"Start:: runFTP({str(os.getpid())})")
    pFTP_Monitor = myFTP.myFTP_Monitor(Host, Port, User, UserPW, localDir, dataFloder)
    pFTP_Monitor.startWatch()

    monitor = myProcess_monitor.myProcess_monitor(5)
    monitor.initReg(__file__, "* * * * * ")                    #每天任一分钟 时执行命令