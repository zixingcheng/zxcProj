# -*- coding: utf-8 -*-
"""
Created on  张斌 2018-04-04 11:00:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com

    myWeb, Api接口操作, 基于flask
"""
import sys, string
from flask import Flask
from flask import render_template, flash, redirect    #导入模块，flash函数，redirect函数
from flask_restful import reqparse, Api, Resource
from flask_bootstrap import Bootstrap
from flask_script import Manager

#导入模块
from flask_wtf import FlaskForm         #FlaskForm 为表单基类
from wtforms import BooleanField,IntegerField,StringField,TextAreaField,PasswordField,SubmitField       #导入字符串字段，密码字段，提交字段
from wtforms.validators import DataRequired,ValidationError,Email,Regexp,EqualTo,Required
import mySystem, Config 

#参考：https://blog.csdn.net/bestallen/article/details/52077533
class LoginForm(FlaskForm):
    openid = StringField('openid', [DataRequired()])  #定义LoginForm类，有2个属性，第一个openid，是一个文本输入框
    remember_me = BooleanField('remember_me', default=False)    #第二个remember_me是一个勾选框，告诉系统要不要勾选，默认不勾选



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

        #创建bootstrap
        bootstrap = Bootstrap(self.app)
        manager = Manager(self.app)

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
 
    #添加一个页面(普通页面)
    def add_Web(self): 
        #添加一个页面(普通页面)
        @self.app.route('/login', methods = ['GET', 'POST'])   #这里'/login'表示的是，网页最后后缀是/login的时候，访问login.html页面
        def login():
            form = LoginForm()                  #生成form实例，给render_template渲染使用
            if form.validate_on_submit():       #调用form实例里面的validate_on_submit()功能，验证数据是否安全，如是返回True，默认返回False
                flash('Login requested for OpenID="' + form.openid.data + '", remember_me=' + str(form.remember_me.data))
                return redirect('/index') #如果数据符合要求，重定向到主页
            return render_template('login.html',  #如果数据不符合要求，则再次读取login.html页面
                title = 'Sign In',
                form = form)

        @self.app.route("/mockservice",methods=['GET','POST'])
        def MockController():
            form = MockCreate()
            code = form['code']
            api = form['api']
            return render_template("HTML/test.html",api=api,data=code)
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

class MockCreate(FlaskForm):
    user_email = StringField("email address",[Email()])
    api = StringField("api",[Required()])
    submit = SubmitField("Submit")
    code = IntegerField("code example: 200",[Required()])
    alias = StringField("alias for api")
    data = TextAreaField("json format",[Required()])


def main():
    # 创建新线程
    pWeb = myWeb()
    pWeb.add_API(myAPI, '/test')
    pWeb.add_API(myAPI_p, '/test/<param>')
    pWeb.add_Web()
    pWeb.run()
    #pWeb.start()    #线程方式启动有问题

    print("Exiting Main Web...")

if __name__ == '__main__':   
    main()