# -*- coding: utf-8 -*-
"""
Created on  张斌 2018-04-04 11:00:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com

    myWeb, Api接口操作, 基于flask
"""
import sys, string
from flask import Flask
from flask_restful import reqparse, Api, Resource
import mySystem, Config 


#Web接口类
class myWeb(): 
    def __init__(self, hostIP = "0.0.0.0", nPort = 8080, bDebug = False):
        self.host = hostIP
        self.port = nPort
        #self.debug = bDebug

        #创建app，并使用RestApi方式
        #Flask初始化参数尽量使用你的包名，这个初始化方式是官方推荐的，官方解释：http://flask.pocoo.org/docs/0.12/api/#flask.Flask
        self.app = Flask(__name__)   

        # Get the config from object of DecConfig
        # 使用 onfig.from_object() 而不使用 app.config['DEBUG'] 是因为这样可以加载 class DevConfig 的配置变量集合，而不需要一项一项的添加和修改。
        self.app.config.from_object(Config.DevConfig)

        #初始Api
        self.api = Api(self.app) 

        # 指定主页 URL='/' 的路由规则
        # 当访问 HTTP://server_ip/ GET(Default) 时，call home()
        @self.app.route('/')
        def home():
            return '<h1>Hello! There is GModel_Py_WebApi...</h1>'

    #添加API类
    def add_API(self, pyApi, url): 
        self.api.add_resource(pyApi, url)
 
    #运行
    def run(self): 
        #官方启动方式参见：http://flask.pocoo.org/docs/0.12/quickstart/#a-minimal-application
        self.app.run()  

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
    from flask import Flask


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