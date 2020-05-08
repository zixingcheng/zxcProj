# -*- coding: utf-8 -*-
"""
Created on  张斌 2018-08-13 18:30:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com

    MQ 消息队列操作 （需要rabbitmq， 安装教程网上很多）
"""
import sys, time, pika, threading
import myData
from atexit import register


class myMQ_Rabbit:
    #初始构造 
    def __init__(self, isSender = False, nameQueue = 'zxcTest', Host = "106.13.206.223", Port = 5672, usrName = 'admin', usrPwd = 'a123456'):
        self.isSender = isSender    #是否为生产者
        self.Host = Host            #指定远程RabbitMQ的地址
        self.Port = Port            #指定远程RabbitMQ的端口
        self.nameQueue = nameQueue  #队列名
        self.usrName = usrName      #远程RabbitMQ的用户名
        self.usrPwd = usrPwd        #远程RabbitMQ的用户密码
        self.callback_RecvMsg = None#消息接收回调函数
        self.isAutoAck = True       #接收消息不通知
        self.Init()                 #初始MQ
    #初始RabbitMQ认证及连接信息
    def Init(self):
        #认证信息
        self.usrCredentials = pika.PlainCredentials(self.usrName, self.usrPwd)       
        #创建连接
        self.usrConn = pika.BlockingConnection(pika.ConnectionParameters(host=self.Host, port=self.Port, credentials=self.usrCredentials, heartbeat=None))    
    #初始消息接收回调    
    def Init_callback_RecvMsg(self, callback_RecvMsg):
        self.callback_RecvMsg = callback_RecvMsg
    #初始消息队列    
    def Init_Queue(self, nameQueue, isDurable = False, isAuto_ack = True):
        #在连接上创建一个频道
        self.usrChannel = self.usrConn.channel() 

        #声明一个队列，生产者和消费者都要声明一个相同的队列，用来防止万一某一方挂了，另一方能正常运行
        self.isDurable = isDurable
        self.modeDelivery = myData.iif(self.isDurable, 2, 1)
        self.usrChannel.queue_declare(queue=nameQueue, durable=isDurable)    # durable=True 持久化

        #接收到消息后会给rabbitmq发送一个确认
        self.isAutoAck = isAuto_ack
        if(isAuto_ack == False):
            self.usrChannel.basic_qos(prefetch_count=1)       #消费者给rabbitmq发送一个信息：在消费者处理完消息之前不要再给消费者发送消息

        #区分生产者(发送)/消费者(接收)
        if(self.isSender == False):
            #调用回调函数，从队列里取消息
            self.usrChannel.basic_consume(on_message_callback=self.callback_Consumer,     #调用回调函数，从队列里取消息
                            queue=nameQueue,                  #指定取消息的队列名
                            auto_ack=isAuto_ack               #该参数调整 ,设置成 False，在调用callback函数时，未收到确认标识，消息会重回队列。True，无论调用callback成功与否，消息都被消费掉
                            #no_ack=isNo_ack                  #取完一条消息后，不给生产者发送确认消息，默认是False的，即  默认给rabbitmq发送一个收到消息的确认，一般默认即可
                           )
        else: 
            self.nameQueue = nameQueue

    #检查连接         
    def _Check_Connection(self):
        #TCP是否关闭或正在关闭，则重连
        isReConnect = False
        #if(self.usrConn.is_closed or self.usrConn.is_closing):
        if(self.usrConn.is_closed):
            self.Init()
            isReConnect = True

        #重建频道
        if(isReConnect or self.usrChannel.is_closed):
            #在连接上创建一个频道
            self.usrChannel = self.usrConn.channel() 

            #声明一个队列，生产者和消费者都要声明一个相同的队列，用来防止万一某一方挂了，另一方能正常运行
            self.usrChannel.queue_declare(queue=self.nameQueue)

    #发送消息    
    def Send_Msg(self, nameQueue, msg):
        #区分生产者(发送)/消费者(接收)
        if(self.isSender):
            self._Check_Connection()    
            self.usrChannel.basic_publish(exchange='',      #交换机
                            routing_key=nameQueue,          #路由键，写明将消息发往哪个队列，本例是将消息发往队列hello
                            body=msg,                       #生产者要发送的消息  
                            properties=pika.BasicProperties(delivery_mode=self.modeDelivery)  #设置消息持久化，将要发送的消息的属性标记为2，表示该消息要持久化
                            )
        else: pass

    #消息队列开始    
    def Start(self):
        self.usrChannel.start_consuming()           #开始循环取消息    #消息队列开始    
    #消息队列关闭
    def Close(self,):
        self.usrConn.close()    #关闭连接
        
    #定义一个回调函数，用来接收生产者发送的消息
    def callback_Consumer(self, ch, method, properties, body): 
        #print("[消费者] recv %s" % body
        #Recv_Msg(body)      #接收消息处理

        #回调，通知处理消息
        if(self.callback_RecvMsg != None):
            if(self.callback_RecvMsg(body.decode('utf-8'))):
                #回复确认消息已处理
                if(self.isAutoAck == False):
                    ch.basic_ack(delivery_tag = method.delivery_tag)  #接收到消息后会给rabbitmq发送一个确认
                pass

    #定义消息接收方法，外部可重写@register
    def Recv_Msg(self, body):
        print("[消费者] Recv_Msg %s" % body)
        return True
    #register(Recv_Msg, 'body')     #装饰器方法未研究透，有问题，暂时放弃


if __name__ == '__main__':
    #实例生产者、消费者 http://106.13.206.223:15672/#/
    nameMQ = 'zxcTest'
    pMQ_Send = myMQ_Rabbit(True, 'zxcTest', "106.13.206.223")
    pMQ_Send.Init_Queue(nameMQ, True, False)
    pMQ_Send2 = myMQ_Rabbit(True, 'zxcTest', "106.13.206.223")
    pMQ_Send2.Init_Queue(nameMQ, True, False)
    
    pMQ_Recv = myMQ_Rabbit(False, 'zxcTest', "106.13.206.223")
    pMQ_Recv.Init_Queue(nameMQ, True)
    pMQ_Recv.Init_callback_RecvMsg(pMQ_Recv.Recv_Msg)
    
    #接收消息线程
    thrdMQ = threading.Thread(target = pMQ_Recv.Start)
    thrdMQ.setDaemon(False)
    thrdMQ.start() 
    

    #循环测试
    nTimes = 1000
    for x in range(1, nTimes):
        #发送消息
        msg = "hello world " + str(x)
        print("[生产者] send '", msg)
        pMQ_Send.Send_Msg(nameMQ, msg)
        time.sleep(0.00001) 
        
        msgDict = {'FromUserName': '茶叶一主号', 'Text': 'h2i 你好', 'Type': 'TEXT'}
        pMQ_Send2.Send_Msg(nameMQ, msg + "--Sender2" + str(msgDict))
        time.sleep(0.1)

    #注册普通文本消息回复                 
    #@register  #装饰器方法未研究透，有问题，暂时放弃
    #def Recv_Msg(body):
    #    print("[消费者] recv override %s" % body)

    print()
