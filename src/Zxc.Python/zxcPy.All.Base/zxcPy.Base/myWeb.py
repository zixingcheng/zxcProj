# -*- coding: utf-8 -*-
"""
Created on  张斌 2018-04-04 11:00:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com

    myWeb, Api接口操作, 基于flask
    @依赖库： flask
"""
import sys, os, string, mySystem
from flask import Flask, Response, make_response, send_from_directory
from flask import jsonify, request, render_template, redirect   #导入模块
from flask_restful import reqparse, Api, Resource
from flask_wtf import FlaskForm                                 #FlaskForm 为表单基类 
from werkzeug.utils import secure_filename

import logging
log = logging.getLogger('zxc')
log.setLevel(logging.ERROR) 

mySystem.Append_Us("", False)  
import myIO, myData_Json, myThread 



#限制上传文件类型，设置允许的文件格式
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'JPG', 'PNG', 'gif', 'GIF', 'pdf', 'PDF'])
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

#提取web服务设置信息
def get_InfoServer(fileObj, evnSERVER_HOST = 'SERVER_HOST', evnSERVER_PORT = 'SERVER_PORT', defPort = 5555): 
    #提取端口号(环境变量)
    strDir, strName = myIO.getPath_ByFile(fileObj)
    dirBase = os.path.abspath(os.path.join(strDir, "")) 
    try:
        from os import environ
        HOST = environ.get(evnSERVER_HOST, 'localhost')
        PORT = environ.get(evnSERVER_PORT, 88)
        PORT = int(environ.get(evnSERVER_PORT, str(defPort)))
    except Exception:
        HOST = "127.0.0.1"
        PORT = 5555
    return HOST, PORT, dirBase


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
        JSON_AS_ASCII = False
        CSRF_ENABLED = True
        SECRET_KEY = 'you-will-never-guess'

#Web接口类
class myWeb(myThread.myThread): 
    def __init__(self, hostIP = "0.0.0.0", nPort = 5000, bDebug = True, webFolder = './', threaded = False, processes = 1):
        super().__init__("", 0) # 必须调用
        self.host = hostIP
        self.port = nPort
        self.debug = bDebug 
        self.threaded = threaded 
        self.processes = processes 
        self.baseDir = webFolder
        self.imgDir = self.baseDir + "/static/images/"

        #创建app，并使用RestApi方式
        #Flask初始化参数尽量使用你的包名，这个初始化方式是官方推荐的，官方解释：http://flask.pocoo.org/docs/0.12/api/#flask.Flask
        self.app = Flask(__name__, template_folder=webFolder + "templates", static_folder=webFolder + "static")   

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
             
        # API-上传图片
        @self.app.route('/img_upload/<string:fileTag>', methods=['POST', 'GET'], strict_slashes=False)
        def api_img_upload(fileTag):
            #提取图片路径
            f = request.files[fileTag]
            fi = request.args.get('company_id', "")
            prefixName = request.args.get('prefixName', "")

            #剔除非支持图片格式
            if not (f and allowed_file(f.filename)):
                return jsonify({"status": 0, "error": 1001, "msg": "请检查上传的图片类型，仅限于png、PNG、jpg、JPG、bmp、pdf"})

            #调整文件命名，避免重复
            fname_new = save_img(f, prefixName)
            return jsonify({"status": 1, "msg": "上传成功", "fileName": fname_new, "filePath": "/static/images/upload"})
        # 图片保存，唯一名称
        def save_img(f, namePreffix = ""):
            #调整文件命名，避免重复
            #fname = secure_filename(f.filename)     #?
            fname = f.filename
            suffix = fname.rsplit('.', 1)[1]

            if(namePreffix + "" != ""): namePreffix = namePreffix + "_"
            fname_new = namePreffix + myIO.create_UUID() + '.' + suffix
            f.save(os.path.join(self.imgDir + "upload", fname_new))
            return fname_new

        # API-显示图片
        @self.app.route('/img/<string:typename>/<string:filename>', methods=['GET'])
        def api_img_show(typename, filename):
            if(typename == "base"): 
                path = self.imgDir + filename
            else:
                path = self.imgDir + typename + "/" + filename
            if(os.path.exists(path)):
                image_data = open(path, "rb").read()
                response = make_response(image_data)
                response.headers['Content-Type'] = 'image/png'
                return response
        # API-下载图片
        @self.app.route('/img_download/<string:typename>/<string:filename>', methods=['GET'])
        def api_img_download(typename, filename):
            if request.method == "GET":
                if(typename == "base"): 
                    path = self.imgDir
                else:
                    path = self.imgDir + typename + "/"
                return send_from_directory(path, filename, as_attachment=True)

        # API-下载文件
        @self.app.route('/download/<string:filename>', methods=['GET'])
        @self.app.route('/download/<string:typename>/<string:filename>', methods=['GET'])
        def api_download(filename, typename = 'base'):
            if request.method == "GET":
                if(typename == "base"): 
                    path = self.baseDir + "/static/data/"
                else:
                    path = self.baseDir + "/static/data/" + typename + "/"
                return send_from_directory(path, filename, as_attachment=True)
            
        ''' 静态文件访问的路由规则-自实现--已取消
        # 静态文件访问的路由规则
        @self.app.route('/', defaults={'path': ''})
        @self.app.route('/<path:path>')
        def get_resource(path):     
            mimetypes = {
                ".css": "text/css",
                ".html": "text/html",
                ".js": "application/javascript",
            }
            complete_path = os.path.join(self.baseDir, path)
            ext = os.path.splitext(path)[1]
            mimetype = mimetypes.get(ext, "text/html")
            content = get_file(complete_path)
            return Response(content, mimetype=mimetype)
        # 提取文件信息
        def get_file(filename):  # pragma: no cover
            try:
                src = os.path.join(dirPath, filename)
                # Figure out how flask returns static files
                # Tried:
                # - render_template
                # - send_file
                # This should not be so non-obvious
                return open(src,'r', encoding='UTF-8').read()
            except IOError as exc:
                return str(exc)
        '''

    #运行
    def run(self, use_reloader=False): 
        #官方启动方式参见：http://flask.pocoo.org/docs/0.12/quickstart/#a-minimal-application
        self.app.run(host = self.host, port = self.port, debug = self.debug, threaded = self.threaded, processes = self.processes, use_reloader = use_reloader)  
        
         

# RESTfulAPI的参数解析 -- put / post参数解析
parser = reqparse.RequestParser()
parser.add_argument("params", type=str, required=True, help="need user params")


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
    pWeb = myWeb("127.0.0.1", 5000, True)
    pWeb.add_API(myAPI, '/test')
    pWeb.add_API(myAPI_p, '/test/<param>')

    # 添加新网页
    pWeb.add_Web()
    @pWeb.app.route("/hello")
    def hello():
        return "Hello...."
    
    #使用jsonify模块来让网页直接显示json数据
    @pWeb.app.route('/json')
    def re_json():
        #定义数据格式
        json_dict={'id':10,'title':'flask的应用','content':'flask的json'}
        #使用jsonify来讲定义好的数据转换成json格式，并且返回给前端
        return jsonify(json_dict)

    pWeb.run()

    #pWeb.start()    #线程方式启动有问题
    print("Exiting Main Web...")

if __name__ == '__main__':   
    main()