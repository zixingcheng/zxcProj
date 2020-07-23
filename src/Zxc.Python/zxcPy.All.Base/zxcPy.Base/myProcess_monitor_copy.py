# -*- coding: utf-8 -*-
"""
Created on  张斌 2020-07-22 20:30:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com

    进程监测守护（副本守护）
"""
import os
import myProcess_monitor


#进程守护副本
class myProcess_monitor_copy:
    def __init__(self):
        self.monitor = myProcess_monitor.myProcess_monitor(5, True, True)
        self.monitor.initReg(__file__, "* * * * * ")   #每天 的8-13,14-20点 的每2分钟 时执行命令

    # 开始监测
    def start(self):
        self.monitor.start()
        pass
    # 停止监测    
    def close(self):
        self.monitor.close()


if __name__ == '__main__':
    #单例运行检测
    from myGlobal import gol  
    gol._Init()             #先必须在主模块初始化（只在Main模块需要一次即可）
    #单例运行检测
    if(gol._Run_Lock(__file__) == False):
       exit(0)
       
    print(F"Start:: myProcess_monitor_copy({str(os.getpid())})")
    pMonitor_copy = myProcess_monitor_copy()
    pMonitor_copy.start()
