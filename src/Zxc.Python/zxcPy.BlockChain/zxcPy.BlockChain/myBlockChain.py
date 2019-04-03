# -*- coding: utf-8 -*-
"""
Created on  张斌 2018-09-29 11:56:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com

    区块链--区块类
    参考：zhaoyu1995 https://blog.csdn.net/baidu_26118459/article/details/79776648?utm_source=copy 
"""
import hashlib, json
import mySystem 
from time import time
from uuid import uuid4 
    
#引用根目录类文件夹--必须，否则非本地目录起动时无法找到自定义类
mySystem.Append_Us("", False)    
import myDebug
from myGlobal import gol  


#区块
class myBlock(object):
    def __init__(self, index, timestamp):
        self.index = index              #区块索引
        self.timestamp = timestamp      #时间戳 
        self.transactions = []          #交易信息
        self.proof = None               #工作量证明
        self.previous_hash = None       #哈希验证值
        self.data = None                #数据

    #Json个数数据
    def toStr(self):
        block = {
            'index': self.index,
            'timestamp': self.timestamp,
            'transactions': self.transactions,
            'proof': proof,
            'previous_hash': self.previous_hash or self.hash(self.chain[-1]),
            'data': self.data
        }
        block_string = json.dumps(block, sort_keys=True).encode()
        return block_string

#区块链
class myBlockChain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []

        # 创建起源区块
        self.new_block(proof=0, previous_hash=1)
        
    #创建区块并添加进行链 
    def new_block(self, proof, previous_hash=None, bAdd=True):
        """
        Create a new Block in the Blockchain
        :param proof: <int> The proof given by the Proof of Work algorithm
        :param previous_hash: (Optional) <str> Hash of previous Block
        :return: <dict> New Block
        """

        #创建新区块
        block = myBlock(len(self.chain), time())
        block.current_transactions = []
        block.proof = proof
        block.previous_hash = previous_hash or self.hash(self.chain[-1])

        # 添加进区块
        if(bAdd):
            self.chain.append(block)
        return block 
    #添加交易信息，并添加进交易链  
    def new_transaction(self, sender, recipient, amount, bAdd = True):
        """
        Creates a new transaction to go into the next mined Block
        :param sender: <str> Address of the Sender
        :param recipient: <str> Address of the Recipient
        :param amount: <int> Amount
        :return: <int> The index of the Block that will hold this transaction
        """

        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })
        return self.last_block.index + 1

    #工作量证明计算
    def proof_of_work(self, last_proof):
        """
        Simple Proof of Work Algorithm:
         - Find a number p' such that hash(pp') contains leading 4 zeroes, where p is the previous p'
         - p is the previous proof, and p' is the new proof
        :param last_proof: <int>
        :return: <int>
        """

        #工作量计算，调用工作量证明算法
        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1
        return proof
    

    #工作量证明算法
    @staticmethod
    def valid_proof(proof, last_proof):
        #简易算法，包含4个前置0
        #guess = f'{last_proof}{proof}'.encode()
        guess = str(proof) + str(last_proof)
        guess_hash = hashlib.sha256(guess.encode()).hexdigest()
        return guess_hash[:3] == "000"
    
    #区块哈希值算法
    @staticmethod
    def hash(block): 
        # 必须固定数据结构，否则哈希计算不同
        return hashlib.sha256(block.toStr()).hexdigest()
    
    #返回链里最后一个区块
    @property
    def last_block(self):
        return self.chain[-1]
        pass
    
    
#初始全局区块链 
gol._Init()             #先必须在主模块初始化（只在Main模块需要一次即可）
gol._Set_Setting("zxcBlockChain", myBlockChain())


#主启动程序
if __name__ == "__main__":    
    # We run the proof of work algorithm to get the next proof...
    blockchain = gol._Get_Setting("zxcBlockChain", None)
    last_block = blockchain.last_block
    last_proof = last_block.proof
    proof = blockchain.proof_of_work(last_proof)

    # We must receive a reward for finding the proof.
    # The sender is "0" to signify that this node has mined a new coin.
    node_identifier = ""
    blockchain.new_transaction(
        sender="0",
        recipient=node_identifier,
        amount=1,
    )

    # Forge the new Block by adding it to the chain
    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof, previous_hash)
    print(block.proof)