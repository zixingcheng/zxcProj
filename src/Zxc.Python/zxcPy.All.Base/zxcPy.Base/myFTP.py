# -*- coding: utf-8 -*-
"""
Created on  张斌 2020-05-21 16:30:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com

    FTP操作 
       --参考 博客地址：http://blog.csdn.net/ouyang_peng/article/details/79271113 作者：欧阳鹏
"""
import os, sys, time, datetime, socket, threading
from ftplib import FTP
from myIO_monitor import myMonitor_File
import myProcess_monitor


# FTP自动下载、自动上传脚本，可以递归目录操作
class myFTP:
    def __init__(self, host, port, localFolder):
        # 初始化 FTP 客户端
        self.localFolder = localFolder
        self.host = host
        self.port = port
        self.closed = True
        self.ftp = FTP()
        self.ftp.encoding = 'gbk'               # 重新设置下编码方式

        self.logDir = os.path.abspath(os.path.join(localFolder, ".."))  
        self.logFile = self.logDir + '/Logs/log_{}.txt'.format(datetime.datetime.strftime(datetime.datetime.now(), "%Y_%m_%d"))
        self.log_file = open(self.logFile, "a")
        self.file_list = []
        self.delete_files()                   # 保留三天内的文件
    # FTP 登录
    def login(self, username, password):
        try:
            timeout = 60
            socket.setdefaulttimeout(timeout)

            # 0主动模式 1 #被动模式
            self.ftp.set_pasv(True)

            # 打开调试级别2，显示详细信息
            # self.ftp.set_debuglevel(2)
            self.debug_print('开始尝试连接到 %s' % self.host)
            self.ftp.connect(self.host, self.port)
            self.debug_print('成功连接到 %s' % self.host)

            self.debug_print('开始尝试登录到 %s' % self.host)
            self.ftp.login(username, password)
            self.debug_print('成功登录到 %s' % self.host)

            self.debug_print(self.ftp.welcome)
            self.closed = False
        except Exception as err:
            self.deal_error("FTP 连接或登录失败 ，错误描述为：%s" % err)
            pass

    # 下载文件
    def download_file(self, local_file, remote_file):
        self.debug_print("download_file()---> local_path = %s ,remote_path = %s" % (local_file, remote_file))
        if self.is_same_size(local_file, remote_file):
            self.debug_print('%s 文件大小相同，无需下载' % local_file)
            return
        else:
            try:
                self.debug_print('>>>>>>>>>>>>下载文件 %s ... ...' % local_file)
                buf_size = 1024
                file_handler = open(local_file, 'wb')
                self.ftp.retrbinary('RETR %s' % remote_file, file_handler.write, buf_size)
                file_handler.close()
            except Exception as err:
                self.debug_print('下载文件出错，出现异常：%s ' % err)
                return
    # 从远程目录下载多个文件到本地目录
    def download_file_tree(self, local_path, remote_path):
        print("download_file_tree()--->  local_path = %s ,remote_path = %s" % (local_path, remote_path))
        try:
            self.ftp.cwd(remote_path)
        except Exception as err:
            self.debug_print('远程目录%s不存在，继续...' % remote_path + " ,具体错误描述为：%s" % err)
            return

        if not os.path.isdir(local_path):
            self.debug_print('本地目录%s不存在，先创建本地目录' % local_path)
            os.makedirs(local_path)

        self.debug_print('切换至目录: %s' % self.ftp.pwd())
        self.file_list = []
        self.ftp.dir(self.get_file_list)     # 方法回调

        remote_names = self.file_list
        self.debug_print('远程目录 列表: %s' % remote_names)
        for item in remote_names:
            file_type = item[0]
            file_name = item[1]
            local = os.path.join(local_path, file_name)
            if file_type == 'd':
                print("download_file_tree()---> 下载目录： %s" % file_name)
                self.download_file_tree(local, file_name)
            elif file_type == '-':
                print("download_file()---> 下载文件： %s" % file_name)
                self.download_file(local, file_name)
            self.ftp.cwd("..")
            self.debug_print('返回上层目录 %s' % self.ftp.pwd())
        return True
    # 从本地上传文件到
    def upload_file(self, local_file, remote_file):
        if not os.path.isfile(local_file):
            self.debug_print('%s 不存在' % local_file)
            return
        
        if self.is_same_size(local_file, remote_file):
            self.debug_print('跳过同名、且大小相等的文件: %s' % local_file)
            return

        buf_size = 1024
        try:
            with open(local_file,'rb')as f:
                self.ftp.storbinary('STOR %s' % remote_file, f, buf_size)
        except Exception as err:
            self.deal_error("FTP 上传失败 ，错误描述为：%s" % err)
            pass
        self.debug_print('上传: %s' % local_file + "成功!")
    # 从本地上传目录下多个文件到
    def upload_file_tree(self, local_path, remote_path, updatLog = False):
        if not os.path.isdir(local_path):
            self.debug_print('本地目录 %s 不存在' % local_path)
            return

        self.ftp.cwd(remote_path)
        self.debug_print('切换至远程目录: %s' % self.ftp.pwd())

        local_name_list = os.listdir(local_path)
        for local_name in local_name_list:
            src = os.path.join(local_path, local_name)
            if os.path.isdir(src):
                try:
                    self.ftp.mkd(local_name)
                except Exception as err:
                    self.debug_print("目录已存在 %s ,具体错误描述为：%s" % (local_name, err))
                self.debug_print("upload_file_tree()---> 上传目录： %s" % local_name)
                self.upload_file_tree(src, local_name)
            else:
                if(updatLog == False and len(local_name) > 4):  #屏蔽日志文件
                    if(local_name[0:4] == "log_"): continue
                self.debug_print("upload_file_tree()---> 上传文件： %s" % local_name)
                self.upload_file(src, local_name)
        self.ftp.cwd("..")
    
    # 获取文件列表
    def get_file_list(self, line):
        file_arr = self.get_file_name(line)
        # 去除  . 和  ..
        if file_arr[1] not in ['.', '..']:
            self.file_list.append(file_arr)
    # 获取文件名
    def get_file_name(self, line):
        pos = line.rfind(':')
        while (line[pos] != ' '):
            pos += 1
        while (line[pos] == ' '):
            pos += 1
        file_arr = [line[0], line[pos:]]
        return file_arr
    # 退出
    def close(self):
        self.debug_print("close()---> FTP退出\n")
        self.ftp.quit()
        self.closed = True
        self.log_file.close()
        
    # 打印日志
    def debug_print(self, s):
        self.write_log(s)
    # 处理错误异常
    def deal_error(self, e):
        log_str = '发生错误: %s' % e
        self.write_log(log_str)
        sys.exit()
    # 记录日志
    def write_log(self, log_str):
        time_now = time.localtime()
        date_now = time.strftime('%Y-%m-%d %H:%M:%S', time_now)
        format_log_str = "%s ---> %s \n " % (date_now, log_str)
        print(format_log_str)
        if(self.log_file.closed):
            self.log_file = open(self.logFile, "a")
        self.log_file.write(format_log_str)
        
    # 判断远程文件和本地文件大小是否一致
    def is_same_size(self, local_file, remote_file):
        try:
            local_file_size = os.path.getsize(local_file)
        except Exception as err:
            self.debug_print("is_same_size() 错误描述为：%s" % err)
            return 0
        
        try:
            remote_file_size = self.ftp.size(remote_file)
        except Exception as err:
            remote_file_size = -1

        # 大文件延时
        if(remote_file_size != local_file_size):
            if(local_file_size > 1024 * 30):
                time.sleep(10)
        self.debug_print('local_file_size:%d  , remote_file_size:%d' % (local_file_size, remote_file_size))
        return remote_file_size == local_file_size
    # 删除文件
    def delete_files(self, days = -5):
        file_list = [self.localFolder, self.logDir]     # 文件夹列表
        today = datetime.datetime.now()                 # 获取当前时间
        offset = datetime.timedelta(days=days)          # 计算偏移量,前n天
        re_date = (today + offset)                      # 获取想要的日期的时间,即前n天时间
        re_date_unix = time.mktime(re_date.timetuple()) # 前n天时间转换为时间戳
        reF_date = (today + offset * 6)                  # 获取想要的日期的时间,即前n*5天时间
        reF_date_unix = time.mktime(re_date.timetuple()) # 前n*5天时间转换为时间戳

        try:
            while file_list:                            # 判断列表是否为空
                path = file_list.pop()                  # 删除列表最后一个元素，并返回给 
                for item in os.listdir(path):           # 遍历列表 
                    pathFile = os.path.join(path, item) # 组合绝对路径 
                    if os.path.isfile(pathFile):        # 判断绝对路径是否为文件
                        # 比较时间戳,文件修改时间小于等于3天前
                        if os.path.getmtime(pathFile) <= re_date_unix:
                            fileName = os.path.basename(pathFile).lower()
                            if(fileName.count("readme.") == 1):
                                continue                   # 屏蔽readme文件
                            os.remove(pathFile)
                            self.debug_print('删除文件{}'.format(pathFile))
                            time.sleep(2)
                    else:
                        if not os.listdir(pathFile):  # 判断目录是否为空
                            # 若目录为空，则删除，并递归到上一级目录，如若也为空，则删除，依此类推
                            if os.path.getmtime(pathFile) <= reF_date_unix:
                                os.removedirs(pathFile)
                                self.debug_print('删除空目录{}'.format(pathFile))
                        else:
                            # 为文件夹时,添加到列表中。再次循环。
                            file_list.append(pathFile)
            return True
        except Exception as err:
            self.deal_error("FTP 连接或登录失败 ，错误描述为：%s" % err)
            return False
    
# FTP自动下载、自动上传脚本，自动监测文件夹变动执行上传         
class myFTP_Monitor:
    def __init__(self, host, port, username, password, localDir, dataFolder, limitH = 12):
        self.my_ftp = myFTP(host, port, localDir)
        self.username = username
        self.password = password
        self.localDir = localDir
        self.logDir = os.path.abspath(os.path.join(localDir, "..")) + "/Logs/"
        self.dataFolder = dataFolder
        self.updatLog = False           #上传日志
        self.timesChange = 0            #文件夹变动次数计数器
        self.timesDT = 0                #时间变化
        self.timesDT_total = 0          #时间变化-总，控制退出 
        self.timeSleep = 6              #时间-休眠
        self.timesLimit_total_S = limitH * 3600     
        
        # 监测本地文件变化，然后执行上传
        self.fileMonitor = myMonitor_File(self.localDir)
        # 装饰函数，文件变动触发
        @self.fileMonitor.changes_register()
        def Reply(params): 
            pass
        # 装饰函数，文件变动触发
        @self.fileMonitor.change()
        def Change(): 
            self.timesChange += 1

    # 文件夹上传FTP
    def upLoad_files(self):
        try:
            # FTP已登录时退出
            if(not self.my_ftp.closed): 
                return

            # 删除历史时间数据
            self.my_ftp.delete_files()

            # FTP登录
            self.my_ftp.login(self.username, self.password)

            # 下载单个文件 --测试
            # my_ftp.download_file("G:/ftp_test/XTCLauncher.apk", "/App/AutoUpload/ouyangpeng/I12/Release/XTCLauncher.apk")

            # 下载目录 --测试
            # my_ftp.download_file_tree("G:/ftp_test/", "App/AutoUpload/ouyangpeng/I12/")

            # 上传单个文件--测试
            # my_ftp.upload_file(my_ftp.localFolder + "Test2.txt", "/Test/Test2.txt")

            # 上传目录
            self.my_ftp.upload_file_tree(self.localDir, self.dataFolder, self.updatLog)
            
            # 上传日志目录
            if(self.updatLog):
                self.my_ftp.upload_file_tree(self.logDir, "Logs", self.updatLog)

            # 退出FTP
            self.my_ftp.close()
            self.timesChange -= 1
        except Exception as err:
            self.my_ftp.deal_error("FTP 上传失败 ，错误描述为：%s" % err)
            self.my_ftp.close()
            pass
        self.updatLog = False           #屏蔽日志文件，避免频繁上传
    
    # 开始监测    
    def startWatch(self):
        self.fileMonitor.startWatch()    #上传文件，并开始监测

        # 本地文件夹变动计数器监测
        self.isRuning = True
        self.thrd_Handle = threading.Thread(target = self.thrdWatch)
        self.thrd_Handle.setDaemon(False)
        self.thrd_Handle.start()
    # 停止监测    
    def closeWatch(self):
        self.isRuning = False
        self.thrd_Handle.stop()
    # 监测-线程实现
    def thrdWatch(self):
        running = True
        while(running):
            try:
                # 监测到有变动时执行上传-线程方式
                if(self.timesChange > 0):
                    self.thrd_Upload = threading.Thread(target = self.upLoad_files)
                    self.thrd_Upload.setDaemon(False)
                    self.thrd_Upload.start()
            except Exception as err:
                self.my_ftp.deal_error("FTP 上传失败 ，错误描述为：%s" % err)
                pass

            # 时间变化监测，超过5分钟默认文件夹变更，避免文件夹变动监测失败
            self.timesDT += self.timeSleep              #时间变化
            self.timesDT_total += self.timeSleep        #时间变化-总
            if(self.timesDT > 300):
                self.timesDT = 0
                self.timesChange += 1
                self.updatLog = True                    #上传日志文件

                # 超过总时间时退出
                if(self.timesDT_total > self.timesLimit_total_S):
                    running = False
                self.my_ftp.debug_print("脚本已运行" + str(self.timesDT_total / 60) + "分钟")
            time.sleep(self.timeSleep)


if __name__ == "__main__":
    #单例运行检测
    from myGlobal import gol  
    gol._Init()             #先必须在主模块初始化（只在Main模块需要一次即可）
    #单例运行检测
    if(gol._Run_Lock(__file__) == False):
       exit(0)

    # FTP配置信息-市气象局
    # Host = "10.152.35.111"      
    # Port = 8021
    # User = "ftpUser"             
    # UserPW = "dgsqxjFTP!@#456"   

    # FTP配置信息-市生态环境局
    # Host = "172.21.95.150"      
    # Port = 8021
    # User = "111111zxc@qq.com"        
    # UserPW = "qaz!@#456"  
    
    # FTP配置信息-市政数局
    Host = "19.104.44.141"      
    Port = 9010
    User = "qixiang"        
    UserPW = "qixtglptxiang"  

    # FTP配置信息-互联网
    # Host = "39.104.57.179"      
    # Port = 21
    # User = "ftp_qxzx"        
    # UserPW = "qx_0522"  

    # 本地上传文件夹路径
    localDir = 'D:/ftpDGSQXJ/Data/'        #-市气象局-Data文件夹
    dataFloder = 'Data'
    
    # 初始Ftp
    print(F"Start:: myFTP({str(os.getpid())})")
    pFTP_Monitor = myFTP_Monitor(Host, Port, User, UserPW, localDir, dataFloder)
    pFTP_Monitor.startWatch()

    monitor = myProcess_monitor.myProcess_monitor(5)
    monitor.initReg(__file__, "* * * * * ")                    #每天任一分钟 时执行命令
