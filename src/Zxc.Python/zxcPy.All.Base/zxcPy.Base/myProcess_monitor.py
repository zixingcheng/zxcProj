# -*- coding: utf-8 -*-
"""
Created on  张斌 2020-07-22 20:30:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com

    进程监测守护（注册表）
"""
import os, sys, codecs, psutil, time, datetime, threading
import myRegistry


# PROCESS_RE = re.compile("pid=\d{1,4},\sname='\S{1,20}'") # 采用正则，获取数据 pid=x/xx/xxx/xxxx, name=[1~20个字符，
# 监控windows系统所有进程服务任务。定时任务执行，发现run.pid进程号系统中不存在，执行命令python Demo.py启动程序
class myProcess_monitor:
    def __init__(self, interval = 5, isMonitor = False, isCopy = False):
        self.reg = myRegistry.myRegistry("Monitor")
        self.dictMonitors = {}
        self.funChange = None
        self.interval = interval
        self.isMonitor = isMonitor
        self.isCopy = isCopy
        self.nTimes = 0

        #初始默认监测内容
        if(self.isMonitor):
            if(self.isCopy):
                self.initMonitor("myProcess_monitor", -1)
            else:
                self.initReg(__file__)
                self.initMonitor("myProcess_monitor_copy", -1)
                self.initMonitors()
        else:
            self.initMonitor("myProcess_monitor", -1)
        time.sleep(2)

    #注册脚本信息    
    def initReg(self, filePath, timeRule = "", vaild = True):
        fileName = os.path.basename(filePath)
        name = fileName.split('.')[0]

        self.reg.setValue(name + "_PID", str(os.getpid()), self.reg.key)
        self.reg.setValue(name + "_PATH", filePath, self.reg.key)
        self.reg.setValue(name + "_TIMES", timeRule, self.reg.key)
        self.reg.setValue(name + "_STATE", "0", self.reg.key)

        #记录监测集
        if(name.count('myProcess_monitor') < 1):
            strMonitor = self.getMONITORS()
            lstMonitor = strMonitor.split(',')
            if(not name in lstMonitor):
                if(vaild):
                    strMonitor += "," + name
                    print(self.getTimeTag() + F"INFO:: 新增进程守护设置({name})")
            else:
                if(vaild == False):
                    strMonitor.replace(name, "")
                    strMonitor.replace(",,", ",")
                    print(self.getTimeTag() + F"INFO:: 移除进程守护设置({name})")
            self.reg.setValue("myProcess_monitor_MINOTORS", strMonitor, self.reg.key)

            #监测启动守护进程
            self.getPIDs()
            self.checkPID("myProcess_monitor")

    #初始监测进程信息集(注册表设置)   
    def initMonitors(self):
        if(self.isCopy): return 
        strMonitor = self.getMONITORS()
        lstMonitor = strMonitor.split(',')
        for x in lstMonitor:
            if(x == ""): continue;
            pid = self.getPID(x) 
            self.initMonitor(x, pid, 1)

        #移除tag1无设置项
        keys = self.dictMonitors.keys()
        for x in keys:
            pSet = self.dictMonitors[x]
            if(pSet['tag'] != 1): continue
            if(x not in lstMonitor):
                self.dictMonitors.pop(x)
                print(self.getTimeTag() + F"INFO::移除守护进程({name})")
    #初始监测进程信息    
    def initMonitor(self, name, pid, tag = 0):
        if(pid == -1):
            pid = self.getPID(name)

        if(self.dictMonitors.get(name, None) == None):
            self.dictMonitors[name] = {'pid': pid, 'path': "", 'times': []}
            print(self.getTimeTag() + F"INFO:: 新增守护进程({pid}：{name})")
        else:
            print(self.getTimeTag() + F"INFO:: 同步守护进程({pid}：{name})")
        self.dictMonitors[name]['pid'] = pid
        self.dictMonitors[name]['tag'] = pid
        self.dictMonitors[name]['state'] = self.getSTATE(name)
        self.dictMonitors[name]['path'] = self.getPATH(name)
        self.dictMonitors[name]['times'] = self.getTIEMS(name)

    #获取进程号PID
    def getPID(self, name):   
        data = self.reg.getValue(name + "_PID", self.reg.key)
        pid = data[0]
        if(pid == ""): pid = -1
        if(self.dictMonitors.get(name, None) != None):
            self.dictMonitors[name]['pid'] = pid
        return pid
    #获取进程号PID
    def getSTATE(self, name):   
        data = self.reg.getValue(name + "_STATE", self.reg.key)
        state = data[0]
        if(state == ""): 
            state = 0; self.reg.setValue(name + "_STATE", "0", self.reg.key);
        if(self.dictMonitors.get(name, None) != None):
            self.dictMonitors[name]['state'] = state
        return state
    #获取进程PATH
    def getPATH(self, name):   
        data = self.reg.getValue(name + "_PATH", self.reg.key)
        return data[0]
    #获取进程timerange
    def getTIEMS(self, name):   
        data = self.reg.getValue(name + "_TIMES", self.reg.key)
        return data[0]
    #获取进程集
    def getMONITORS(self):   
        data = self.reg.getValue("myProcess_monitor_MINOTORS", self.reg.key)
        return data[0]
    #获取进程号PIDs
    def getPIDs(self):   
        self.pids = psutil.pids() 
        for x in self.dictMonitors:
            pid = self.getPID(x)
            if(pid != ""):
                self.dictMonitors[x]['pid'] = pid
    #获取进程号PID
    def getPID_byName(self, name = 'cmd.exe'):   
        self.pids = psutil.pids() 
        pids = []
        for x in self.pids:
            try:
                p = psutil.Process(x)
                if(p.name() == name):
                    pids.append(x)
            except :
                pass
        return pids
    # 时间前缀
    def getTimeTag(self):
        strTime = datetime.datetime.strftime(datetime.datetime.now(), "%m-%d %H:%M:%S")   
        return strTime + ">> "

    #检查PIDs       
    def checkPIDs(self):  
        self.getPIDs()
        for x in self.dictMonitors:
            self.checkPID(x)
    #检查PID
    def checkPID(self, name):  
        if(True):
            pid = int(self.dictMonitors[name]['pid'])
            if(pid in self.pids):
                p = psutil.Process(pid)
                try:
                    return
                except :
                    pass

            #处理不存在
            if(self.checkTIMES(name)):
                #增加状态锁，避免同时操作
                if(self.getSTATE(name) != "0"): return
                self.reg.setValue(name + "_STATE", "1", self.reg.key); self.getSTATE(name);

                print("\r\n" + self.getTimeTag() + F"INFO:: 监测进程({name})已退出，重启中...")
                thrdRestart = threading.Thread(target = self.restartPID, args=[name, pid])
                thrdRestart.setDaemon(False)
                thrdRestart.start()
                if(self.funChange != None):
                    self.funChange()
                time.sleep(5)
    #检查PIDs       
    def checkTIMES(self, name):  
        #使用crontab规则：M H D m d command
	    #   M: 分（0-59） H：时（0-23） D：天（1-31） m: 月（1-12） d: 周（0-6） 0为星期日(或用Sun或Mon简写来表示) 
        #每天 的8-13,14-20点 的每2分钟 时执行命令:  "*/2 8-13,14-20 * * * ")    
        timeRule = self.dictMonitors[name].get('times', "")
        if(len(timeRule) < 1): return True

        #解析时间规则
        times = timeRule.split(' ')
        if(len(times) < 5): return True

        #解析
        isVaild = True
        isVaild += self.checkRule(times[0], 'M')
        isVaild += self.checkRule(times[1], 'H')
        isVaild += self.checkRule(times[2], 'D')
        isVaild += self.checkRule(times[3], 'm')
        isVaild += self.checkRule(times[4], 'd')
        return isVaild == 6
    #解析月\周\天\时\分
    def checkRule(self, timeRule, type = 'M'):  
        isVaild = False
        if(timeRule == "*"): return True    # 全时

        #区间校检
        timeRanges = {"M": [0, 59], "H": [0, 23], "D": [1, 31], "m": [1, 12], "d": [0, 6]}
        timeRange = timeRanges.get(type, None)
        if(timeRange == None): return False
        
        #取当前时间信息
        dtNow = datetime.datetime.now()
        times = {"M": dtNow.minute, "H": dtNow.hour, "D": dtNow.day, "m": dtNow.month, "d": dtNow.weekday}
        if(times[type] >= timeRanges[type][0] and times[type] <= timeRanges[type][1]):
            pass
        else:
            return False

        #设置校检(*、*/2、8-13,14-20)
        timeRules = timeRule.split(',')
        for x in timeRules:
            if(x.count('-') == 0):          #单一值
                if(x.count('/') == 0 ):
                    if(str(times[type]) == x):
                        isVaild = True; break;
                else:
                    timeT = int(x.split('/')[1])
                    if(times[type] % timeT == 0):
                        isVaild = True; break;
            else:
                timeSets = x.split('-')
                if(x.count('/') == 0 ):
                    if(times[type] >= int(timeSets[0]) and times[type] <= int(timeSets[1])):
                        isVaild = True; break;
                else:
                    pass  #有些复杂，暂留
            pass
        return isVaild
    #恢复PID      
    def restartPID(self, name, pid):  
        path = self.dictMonitors[name]['path'] 
        if(path != ""):
            cmd = "start cmd.exe @cmd /k python " + path
            os.system(cmd)            #os.startfile("python " + path)   #os.popen(cmd)

            #同步信息
            nTimes = 0; bSucess = True
            pid = str(pid)
            pidNew = self.getPID(name)
            while(pidNew == pid):
                pidNew = self.getPID(name)
                time.sleep(3); nTimes += 1;
                print(self.getTimeTag() + F"INFO:: 重启进程({pid}：{name})......")
                if(nTimes > self.interval):
                    print(self.getTimeTag() + F"INFO:: 重启进程({pidNew}：{name})失败！\r\n")
                    bSucess = False 
            if(bSucess):
                time.sleep(2)
                self.cleanProcess()         #删除空cmd进程
                print(self.getTimeTag() + F"INFO:: 已重启进程({pidNew}：{name})\r\n")
            self.reg.setValue(name + "_STATE", "0", self.reg.key); self.getSTATE(name);
     

    # 开始监测
    def start(self):
        if(self.isMonitor == False): return 
        self.isRuning = True
        self.thrd_Handle = threading.Thread(target = self.thrdMonitor)
        self.thrd_Handle.setDaemon(False)
        self.thrd_Handle.start()
    # 停止监测    
    def close(self):
        if(self.isMonitor == False): return 
        self.isRuning = False
        self.thrd_Handle.stop()
    # 监测-线程实现
    def thrdMonitor(self):
        while(True):
            try:
                self.checkPIDs()
            except Exception as err:
                print(self.getTimeTag() + "Error:: " + str(err))
            time.sleep(self.interval)

            self.nTimes += 1
            if(self.nTimes > 10):
                self.nTimes = 0
                self.initMonitors()

    # 变动信息装饰函数
    def change(self):
        # 定义一个嵌套函数
        def _change(fn):
            self.funChange = fn
        return _change
    
    #删除进程P
    def cleanProcess(self, name = 'cmd.exe'):  
        pids = self.getPID_byName(name)
        for x in pids:
            os.system('taskkill.exe /pid:' + str(x) + ' -f')
        pass


if __name__ == '__main__':
    #单例运行检测
    from myGlobal import gol  
    gol._Init()             #先必须在主模块初始化（只在Main模块需要一次即可）
    #单例运行检测
    if(gol._Run_Lock(__file__) == False):
       #sys.exit()pid = 711
       print(str(os.getpid()))
       #os.popen('taskkill.exe /pid:' + str(os.getpid()) + " /F")
       os._exit(0)
       #os.kill(signal.SIGKILL)
       
    print(F"Start:: myProcess_monitor({str(os.getpid())})")
    pMonitor = myProcess_monitor(5, True, False)
    pMonitor.start()
 