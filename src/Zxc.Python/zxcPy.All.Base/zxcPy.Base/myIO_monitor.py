# -*- coding: utf-8 -*-
"""
Created on  张斌 2020-07-22 20:30:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com

    文件变动信息监测
"""
import os, sys, time, threading
import win32file
import win32con


ACTIONS = {
  1: "Created",
  2: "Deleted",
  3: "Updated",
  4: "Renamed from something",
  5: "Renamed to something"
}
FILE_LIST_DIRECTORY = 0x0001


# 文件变动信息监测
class myMonitor_File:
    def __init__(self, localFolder):
        self.functionDict = {}
        self.funChange = None
        self.watchFolder = localFolder
        print("Watching changes in", self.watchFolder , "\n")
        self.hDir = win32file.CreateFile(
                                      self.watchFolder,
                                      FILE_LIST_DIRECTORY,
                                      win32con.FILE_SHARE_READ | win32con.FILE_SHARE_WRITE,
                                      None,
                                      win32con.OPEN_EXISTING,
                                      win32con.FILE_FLAG_BACKUP_SEMANTICS,
                                      None
                                     )
    # 开始监测    
    def startWatch(self):
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
        while(True):
            results = win32file.ReadDirectoryChangesW(
                self.hDir,
                1024,
                True,
                win32con.FILE_NOTIFY_CHANGE_FILE_NAME |
                win32con.FILE_NOTIFY_CHANGE_DIR_NAME |
                win32con.FILE_NOTIFY_CHANGE_ATTRIBUTES |
                win32con.FILE_NOTIFY_CHANGE_SIZE |
                win32con.FILE_NOTIFY_CHANGE_LAST_WRITE |
                win32con.FILE_NOTIFY_CHANGE_SECURITY,
                None,
                None)
            
            # 变化监测
            nChanges = 0
            for action, filename in results:
                full_filename = os.path.join(self.watchFolder, filename)

                # 具体监测内容
                actioType = ACTIONS.get(action, "Unknown")
                replyFn = self.functionDict.get(actioType, None)
                if(replyFn != None):
                    nChanges += 1
                    r = replyFn(actioType) 
                print (full_filename, ACTIONS.get(action, "Unknown"))

            # 触发变化事件
            if(nChanges > 0):
                self.funChange()
            time.sleep(0)

    # 变动信息装饰函数
    def change(self):
        # 定义一个嵌套函数
        def _change(fn):
            self.funChange = fn
        return _change
    # 变动信息装饰函数，用于传递外部重写方法，便于后续调用    
    def changes_register(self, monitorType = ["Created", "Deleted", "Updated", "Renamed from something", "Renamed to something"]):
        def _changes_register(fn): 
            # 按类型记录
            for _monitorType in monitorType:
                self.functionDict[_monitorType] = fn 
            return fn
        return _changes_register

     
if __name__ == "__main__":
    path_to_watch = 'C:/Users/16475/Desktop/FTp/ftpFiles'
    fileMonitor = myMonitor_File(path_to_watch)

    # 装饰函数，文件变动触发
    @fileMonitor.changes_register()
    def Reply(params): 
        print(params)
    # 装饰函数，文件变动触发
    @fileMonitor.change()
    def Change(): 
        print("sdfsdf")


    fileMonitor.startWatch()