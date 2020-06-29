# -*- coding: utf-8 -*-
"""
Created on  张斌 2020-05-20 09:58:00 
    @author: zhang bin
    @email:  zhangbin@qq.com

    Ftp Server --脚本启动，单例
""" 
import myFTP 
    
    
# FTP配置信息-市生态环境局
Host = "19.104.44.141"      
Port = 9010
User = "qixiang"        
UserPW = "qixtglptxiang"

# 本地上传文件夹路径
localDir = 'D:/ftpDGSQXJ/Data'        #-市气象局-Data文件夹 
dataFloder = 'Data'                 
    

if __name__ == '__main__':     
    # 初始Ftp并运行
    pFTP_Monitor = myFTP.myFTP_Monitor(Host, Port, User, UserPW, localDir, dataFloder)
    pFTP_Monitor.startWatch()
