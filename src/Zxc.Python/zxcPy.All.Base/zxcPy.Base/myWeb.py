# -*- coding: utf-8 -*-
"""
Created on  张斌 2018-04-04 11:00:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com

    myWeb, Api接口操作, 基于flask
    @依赖库： flask
"""
import sys, string
from flask import Flask
from flask import jsonify
from flask_restful import reqparse, Api, Resource
import mySystem, myThread 
import logging

log = logging.getLogger('zxc')
log.setLevel(logging.ERROR)

#Web接口类
class myWeb(myThread.myThread): 
    def __init__(self, hostIP = "0.0.0.0", nPort = 8080, bDebug = True):
        super().__init__("", 0) # 必须调用
        self.host = hostIP
        self.port = nPort
        self.debug = bDebug

        #创建app，并使用RestApi方式
        #Flask初始化参数尽量使用你的包名，这个初始化方式是官方推荐的，官方解释：http://flask.pocoo.org/docs/0.12/api/#flask.Flask
        self.app = Flask(__name__)   
        self.api = Api(self.app)  
        
        #添加一个页面(普通页面)
        @self.app.route('/HelloWorld')
        def hello_world():
            return "Hello World......!" 
        
        #添加一个页面(错误页面)
        @self.app.errorhandler(404)  
        def not_found(error):  
            return jsonify({'error':'Not found'}), 404  

    #添加API类
    def add_API(self, pyApi, url): 
        self.api.add_resource(pyApi, url)
    
        #添加一个页面(普通页面)
        #@self.app.route('/HelloWorld')
        #def hello_world():
        #    return "Hello World......!" 
 
    #运行
    def run(self, use_reloader=False): 
        #官方启动方式参见：http://flask.pocoo.org/docs/0.12/quickstart/#a-minimal-application
        self.app.run(host = self.host, port = self.port, debug = self.debug, use_reloader = use_reloader)  

#API接口类(Restful)
class myAPI(Resource):
    def get(self): 
        return "Get: This is myWeixin_API's Test web page..."
    def put(self): 
        return "Put: This is myWeixin_API's Test web page..."
    def delete(self): 
        return "Delete: This is myWeixin_API's Test web page..."

class myAPI_p(myAPI):
    def get(self, param):
        strReturn = "参数：" + param
        return strReturn


def main():
    # 创建新线程
    pWeb = myWeb()
    pWeb.add_API(myAPI, '/test')
    pWeb.add_API(myAPI_p, '/test/<param>')
    pWeb.run()
    #pWeb.start()    #线程方式启动有问题

    print("Exiting Main Web...")

if __name__ == '__main__':   
    main()