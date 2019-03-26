# -*- coding: utf-8 -*-
"""
Created on  张斌 2018-04-04 11:00:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com

    myWeb, Api接口操作, 基于flask
    @依赖库： flask
"""
import sys, os, string, mySystem
from flask import Flask
from flask import jsonify, request, render_template, redirect    #导入模块
from flask_restful import reqparse, Api, Resource
from flask_wtf import FlaskForm         #FlaskForm 为表单基类 
import logging
log = logging.getLogger('zxc')
log.setLevel(logging.ERROR) 

mySystem.Append_Us("", False)  
import myIO, myThread 



#Web配置接口类
class myWeb_Config(): 
    class Config(object):
        """Base config class."""
        pass

    class ProdConfig(Config):
        """Production config class."""
        pass

    class DevConfig(Config):
        """Development config class."""
        # Open the DEBUG
        DEBUG = True
        CSRF_ENABLED = True
        SECRET_KEY = 'you-will-never-guess'

#Web接口类
class myWeb(myThread.myThread): 
    def __init__(self, hostIP = "0.0.0.0", nPort = 5000, bDebug = True, webFolder = './'):
        super().__init__("", 0) # 必须调用
        self.host = hostIP
        self.port = nPort
        self.debug = bDebug 
        self.baseDir = webFolder

        #创建app，并使用RestApi方式
        #Flask初始化参数尽量使用你的包名，这个初始化方式是官方推荐的，官方解释：http://flask.pocoo.org/docs/0.12/api/#flask.Flask
        self.app = Flask(__name__, template_folder=webFolder + "templates", static_folder=webFolder + "statics")   

        #初始Api
        self.api = Api(self.app)  
        
        # Get the config from object of DecConfig
        # 使用 onfig.from_object() 而不使用 app.config['DEBUG'] 是因为这样可以加载 class DevConfig 的配置变量集合，而不需要一项一项的添加和修改。
        self.app.config.from_object(myWeb_Config.DevConfig)

        # 创建bootstrap
        # from flask_bootstrap import Bootstrap
        # from flask_script import Manager
        # bootstrap = Bootstrap(self.app)
        # manager = Manager(self.app)

        #添加一个页面(错误页面)
        @self.app.errorhandler(404)  
        def not_found(error):  
            return jsonify({'error':'Not found'}), 404  

    #添加API类
    def add_API(self, pyApi, url): 
        self.api.add_resource(pyApi, url)
    
    #添加页面(普通页面)
    def add_Web(self): 
        # 指定主页 URL='/' 的路由规则
        # 当访问 HTTP://server_ip/ GET(Default) 时，call home()
        @self.app.route('/')
        def home():
            return '<h1>Hello! There is zxcWeb...</h1>'  
 
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
    pWeb = myWeb("192.168.24.108", 5000, True)
    pWeb.add_API(myAPI, '/test')
    pWeb.add_API(myAPI_p, '/test/<param>')

    # 添加新网页
    pWeb.add_Web()
    @pWeb.app.route("/hello")
    def hello():
        return "Hello...."
 
    pWeb.run()

    #pWeb.start()    #线程方式启动有问题
    print("Exiting Main Web...")

if __name__ == '__main__':   
    main()