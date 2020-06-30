# -*- coding: utf-8 -*-
"""
Created on  张斌 2018-07-04 15:58:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com

    Rest API --接口实现
"""
import os, copy, ast 
import mySystem 
    
#引用根目录类文件夹--必须，否则非本地目录起动时无法找到自定义类
mySystem.Append_Us("../zxcPy.BlockChain", False, __file__)
mySystem.Append_Us("", False)    
import myWeb, myDebug, myBlockChain
from myGlobal import gol   



#API-新矿区
class myAPI_BlockChain_Mine(myWeb.myAPI): 
    def get(self): 
        # We run the proof of work algorithm to get the next proof...
        blockchain = gol._Get_Setting("zxcBlockChain", None)
        last_block = blockchain.last_block
        last_proof = last_block.proof
        proof = blockchain.proof_of_work(last_proof)

        # We must receive a reward for finding the proof.
        # The sender is "0" to signify that this node has mined a new coin.
        blockchain.new_transaction(
            sender="0",
            recipient=node_identifier,
            amount=1,
        )

        # Forge the new Block by adding it to the chain
        previous_hash = blockchain.hash(last_block)
        block = blockchain.new_block(proof, previous_hash)

        response = {
            'message': "New Block Forged",
            'index': block['index'],
            'transactions': block['transactions'],
            'proof': block['proof'],
            'previous_hash': block['previous_hash'],
        }
        return jsonify(response), 200


#API-新交易
class myAPI_newTransaction(myWeb.myAPI): 
    def get(self, transaction_info): 
        return "We'll add a new transaction"
    
#API-新交易
class myAPI_ChainInfo(myWeb.myAPI): 
    def get(self): 
        response = {
            'chain': blockchain.chain,
            'length': len(blockchain.chain),
        }
        return jsonify(response), 200


#集中添加所有API
def add_APIs(pWeb):      
    # 创建Web API
    pWeb.add_API(myAPI_BlockChain_Mine, '/zxcAPI/BlockChain/mine')
    pWeb.add_API(myAPI_newTransaction, '/zxcAPI/BlockChain/new_transaction/<transaction_info>')
    pWeb.add_API(myAPI_ChainInfo, '/zxcAPI/BlockChain/chainInfo')
 
     