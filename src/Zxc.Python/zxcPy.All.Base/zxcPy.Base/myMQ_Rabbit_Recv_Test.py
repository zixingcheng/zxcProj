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
         
class myMQ_Rabbit_Recv:
    #定义消息接收方法，外部可重写@register
    def Recv_Msg(self, body):
        print("[消费者] Recv_Msg %s" % body)
        return True

if __name__ == '__main__':
    #实例生产者、消费者
    nameMQ = 'zxcTest'
    pMQ_Recv = myMQ_Rabbit(False)
    pMQ_Recv.Init_Queue(nameMQ, True)

    p = myMQ_Rabbit_Recv()
    pMQ_Recv.Init_callback_RecvMsg(p.Recv_Msg)
    
    #接收消息线程--第二消息接收顺序有问题
    thrdMQ = threading.Thread(target = pMQ_Recv.Start)
    thrdMQ.setDaemon(False)
    thrdMQ.start()

    print()
