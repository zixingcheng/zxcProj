# -*- coding: utf-8 -*-
"""
Created on  张斌 2018-08-13 18:30:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com

    MQ 消息队列操作 
"""
import sys, time, pika
from atexit import register


class myMQ_Rabbit:
    #初始构造 
    def __init__(self, isSender = False, Host = "http://127.0.0.1", usrName = 'guest', usrPwd = 'guest'):
        self.isSender = isSender    #是否为生产者
        self.Host = Host            #指定远程RabbitMQ的地址
        self.usrName = usrName      #远程RabbitMQ的用户名
        self.usrPwd = usrPwd        #远程RabbitMQ的用户密码
        self.Init()                 #初始MQ
    #初始RabbitMQ认证及连接信息
    def Init(self):
        #认证信息
        self.usrCredentials = pika.PlainCredentials(self.usrName, self.usrPwd)       
        #创建连接
        self.usrConn = pika.BlockingConnection(pika.ConnectionParameters('127.0.0.1', credentials=self.usrCredentials))    
    #初始消息队列    
    def Init_Queue(self, nameQueue, isNo_ack = True):
        #在连接上创建一个频道
        self.usrChannel = self.usrConn.channel() 

        #声明一个队列，生产者和消费者都要声明一个相同的队列，用来防止万一某一方挂了，另一方能正常运行
        self.usrChannel.queue_declare(queue = nameQueue)

        #接收到消息后会给rabbitmq发送一个确认
        if(isNo_ack == False):
            self.usrChannel.basic_qos(prefetch_count=1)     #消费者给rabbitmq发送一个信息：在消费者处理完消息之前不要再给消费者发送消息

        #区分生产者(发送)/消费者(接收)
        if(self.isSender == False):
            #调用回调函数，从队列里取消息
            self.usrChannel.basic_consume(self.callback_RecvMsg,    #调用回调函数，从队列里取消息
                            queue=nameQueue,                #指定取消息的队列名
                            no_ack=isNo_ack                 #取完一条消息后，不给生产者发送确认消息，默认是False的，即  默认给rabbitmq发送一个收到消息的确认，一般默认即可
                            #,properties=pika.BasicProperties(delivery_mode=2,)#设置消息持久化，将要发送的消息的属性标记为2，表示该消息要持久化
                            )
        else: pass
    #发送消息    
    def Send_Msg(self, nameQueue, msg):
        #区分生产者(发送)/消费者(接收)
        if(self.isSender):
            self.usrChannel.basic_publish(exchange='',      #交换机
                            routing_key=nameQueue,          #路由键，写明将消息发往哪个队列，本例是将消息发往队列hello
                            body=msg)                       #生产者要发送的消息
        else: pass

    #消息队列开始    
    def Start(self):
        self.usrChannel.start_consuming()#开始循环取消息    #消息队列开始    
    #消息队列关闭
    def Close(self,):
        self.usrConn.close()    #关闭连接

    #定义一个回调函数，用来接收生产者发送的消息
    def callback_RecvMsg(self, ch, method, properties, body): 
        #print("[消费者] recv %s" % body
        ch.basic_ack(delivery_tag=method.delivery_tag)  #接收到消息后会给rabbitmq发送一个确认
        Recv_Msg(body)      #接收消息处理

    #定义消息接收方法，外部可重写@register
    def Recv_Msg(self, body):
        print("[消费者] recv %s" % body)
    register(Recv_Msg, 'body')

         

if __name__ == '__main__':
    #实例生产者、消费者
    nameMQ = 'Test'
    pMQ_Send = myMQ_Rabbit(True)
    pMQ_Send.Init_Queue(nameMQ)
    pMQ_Send2 = myMQ_Rabbit(True)
    pMQ_Send2.Init_Queue(nameMQ)
    
    pMQ_Recv = myMQ_Rabbit(False)
    pMQ_Recv.Init_Queue(nameMQ, False)

    #循环测试
    nTimes = 10
    for x in range(1, nTimes):
        #发送消息
        msg = "hello world " + str(x)
        print("[生产者] send '", msg)
        pMQ_Send.Send_Msg(nameMQ, msg)
        pMQ_Send2.Send_Msg(nameMQ, msg + "--Sender2")
        time.sleep(0.1)
        
    #注册普通文本消息回复                 
    @register
    def Recv_Msg(body):
        print("[消费者] recv override %s" % body)

    #接收消息
    print('[消费者] waiting for msg .')
    pMQ_Recv.Start()


    print()
