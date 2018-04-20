# -*- coding: utf-8 -*-
"""
Created on  张斌 2018-04-03 18:00:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com

    线程操作接口操作

"""
import sys, string, threading

#线程
class myThread (threading.Thread):  #继承父类threading.Thread
    def __init__(self, name, threadID = 0, queue = None):
        super().__init__()      #必须调用
        self.thrdID = threadID
        self.thrdQueue = queue
        self.name = name
        self.exitFlag = False

    #把要执行的代码写到run函数里面 线程在创建后会直接运行run函数 
    def run(self):                   #把要执行的代码写到run函数里面 线程在创建后会直接运行run函数 
        print("Starting " + self.name)
        i = 0
        while not self.exitFlag:
            if(i % 10000 == 0):
                print(str(i))
            i += 1
            if i > 10000*10 : break
        print("Exiting " + self.name)

    #退出接口
    def _stop(self):   
        threading.Thread._stop(self)     
        self.exitFlag = True      


def main():
    # 创建新线程
    thread = myThread("Thread-1", 1)
    thread.start()  
    
    print("Exiting Main Thread")

if __name__ == '__main__':   
    main()