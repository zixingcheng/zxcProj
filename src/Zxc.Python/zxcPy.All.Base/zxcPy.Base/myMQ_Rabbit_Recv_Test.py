# -*- coding: utf-8 -*-
"""
Created on  张斌 2018-08-13 18:30:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com

    MQ 消息队列操作 
"""
import sys, time, pika, threading
from atexit import register
from myMQ_Rabbit import myMQ_Rabbit
         

if __name__ == '__main__':
    #实例生产者、消费者
    nameMQ = 'Test'
    pMQ_Recv = myMQ_Rabbit(False)
    pMQ_Recv.Init_Queue(nameMQ, False)
    pMQ_Recv.Init_callback_RecvMsg(pMQ_Recv.Recv_Msg)
    
    #接收消息线程--第二消息接收顺序有问题
    thrdMQ = threading.Thread(target = pMQ_Recv.Start)
    thrdMQ.setDaemon(False)
    thrdMQ.start()

    print()
