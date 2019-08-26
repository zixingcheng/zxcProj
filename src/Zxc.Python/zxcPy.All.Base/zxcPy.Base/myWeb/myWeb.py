# -*- coding: utf-8 -*-
"""
Created on  张斌 2018-04-04 11:00:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com

    myWeb, Api接口操作, 基于flask
"""
import sys, os, string
from flask import Flask
from flask import render_template, flash, redirect, request, jsonify    #导入模块，flash函数，redirect函数
from flask_restful import reqparse, Api, Resource


#导入模块
from flask_wtf import FlaskForm         #FlaskForm 为表单基类
from wtforms import BooleanField,IntegerField,DecimalField,StringField,TextAreaField,PasswordField,SubmitField,RadioField,DateField,SelectField,SelectMultipleField       #导入字符串字段，密码字段，提交字段
from wtforms.validators import DataRequired,ValidationError,Email,Regexp,EqualTo,Required,NumberRange,Length
import mySystem, Config 
 
mySystem.Append_Us("", False) 
billTypes = [('None', '无')]

import myIO, myData_Json, myManager_Bill

class LoginForm(FlaskForm):
    openid = StringField('openid', [DataRequired()])            #定义LoginForm类，有2个属性，第一个openid，是一个文本输入框
    remember_me = BooleanField('remember_me', default=False)    #第二个remember_me是一个勾选框，告诉系统要不要勾选，默认不勾选
    
class MockCreate(FlaskForm):
    user_email = StringField("email address",[Email()])
    api = StringField("api",[Required()])
    submit = SubmitField("Submit")
    code = IntegerField("code example: 200",[Required()])
    alias = StringField("alias for api")
    data = TextAreaField("json format",[Required()])

class billAddForm(FlaskForm):
    openid = StringField('openid', [DataRequired()])            #定义LoginForm类，有2个属性，第一个openid，是一个文本输入框
    remember_me = BooleanField('remember_me', default=False)    #第二个remember_me是一个勾选框，告诉系统要不要勾选，默认不勾选
    usrID = StringField('usrID', default="")                    #用户名


    #账单类型
    #billType = RadioField('账单类型', choices=[(True, '收入'), (False, '支出')]) 
    lstChoices = []
    for x in myManager_Bill.myBileType:
        lstChoices.append((x, x))        
    billType = SelectField('账单类型', choices=lstChoices)      #交易分类(细分小类)
    
    #账单记录时间，文本输入框，必须输入是"年-月-日"格式的日期
    billTime = DateField('账单时间', format='%Y-%m-%d')                    
   

    #交易方
    tradeParty = StringField('交易方', [DataRequired(), Length(min=1, max=20)])          
    #交易内容
    tradeTarget = StringField('交易内容', [DataRequired('请输入交易内容'), Length(min=4, max=20)]) 

    #交易分类，下拉单选框，choices里的内容会在Option里，里面每个项是(值，显示名)对
    tradeType = SelectField('交易分类', choices=[('None', '无')])          
    tradeType2 = SelectField('交易小类', choices=[('None', '无')])          #交易分类(细分小类)
    tradeType3 = SelectField('交易子类', choices=[('None', '无')])          #交易分类(细分子类)
    
    #交易金额，显示时保留两位小数
    tradeMoney = DecimalField('交易金额', places=2, default=0.00)         
    tradePrice = DecimalField('交易单价', places=2, default=0.00)         
    tradeNum = DecimalField('交易数量', places=2, default=0.00)             
    tradePoundage = DecimalField('手续费', places=2, default=0.00)   

    #交易时间，文本输入框，必须输入是"年-月-日"格式的日期
    tradeTime = DateField('交易时间', format='%Y-%m-%d')         


#Web接口类
class myWeb(): 
    def __init__(self, hostIP = "0.0.0.0", nPort = 8080, bDebug = False):
        self.host = hostIP
        self.port = nPort
        self.debug = bDebug
        self.billTypes = []
        self.loadSets()         #提取配置信息

        #创建app，并使用RestApi方式
        #Flask初始化参数尽量使用你的包名，这个初始化方式是官方推荐的，官方解释：http://flask.pocoo.org/docs/0.12/api/#flask.Flask
        self.app = Flask(__name__)   

        # Get the config from object of DecConfig
        # 使用 onfig.from_object() 而不使用 app.config['DEBUG'] 是因为这样可以加载 class DevConfig 的配置变量集合，而不需要一项一项的添加和修改。
        self.app.config.from_object(Config.DevConfig)

        #创建bootstrap
        #bootstrap = Bootstrap(self.app)
        #manager = Manager(self.app)

        #初始Api
        self.api = Api(self.app) 

        # 指定主页 URL='/' 的路由规则
        # 当访问 HTTP://server_ip/ GET(Default) 时，call home()
        @self.app.route('/')
        def home():
            return '<h1>Hello! There is GModel_Py_WebApi...</h1>'
        
    def loadSets(self):  
        #初始根目录信息
        strDir, strName = myIO.getPath_ByFile(__file__)
        self.Dir_Base = os.path.abspath(os.path.join(strDir, ".."))  
        self.Dir_Setting = self.Dir_Base + "/myWeb/Setting" 

        #载入配置
        text = myIO.getContent(self.Dir_Setting + "/BillTypes.json", True, False)
        self.jsonSets = myData_Json.Json_Object()
        self.jsonSets.Trans_FromStr(text)
    def saveSets(self): 
        pass


    #添加API类
    def add_API(self, pyApi, url): 
        self.api.add_resource(pyApi, url)
 
    #装饰器类--添加路由页面
    def routeWeb(routeUrl, routeMethods=['POST','GET']):
        def route(func):                            #装饰器加参数需要多加一层嵌套
            def add_routeWeb(*args, **kwargs):      #为了兼容各类函数参数，添加 *args,**kwargs 不固定参数
                
                @self.app.route(routeUrl, methods = routeMethods)
                def newWeb(): 
                    print("aaaaa") 
                return func(*args,**kwargs)
            return add_routeWeb
        return route


    #添加一个页面(普通页面)
    def add_Web(self): 
        #添加一个页面(普通页面)
        @self.app.route('/login', methods = ['GET', 'POST'])   #这里'/login'表示的是，网页最后后缀是/login的时候，访问login.html页面
        def login():
            form = LoginForm()                      #生成form实例，给render_template渲染使用
            if form.validate_on_submit():           #调用form实例里面的validate_on_submit()功能，验证数据是否安全，如是返回True，默认返回False
                flash('Login requested for OpenID="' + form.openid.data + '", remember_me=' + str(form.remember_me.data))
                return redirect('/index')           #如果数据符合要求，重定向到主页
            return render_template('login.html',    #如果数据不符合要求，则再次读取login.html页面
                title = 'Sign In',
                form = form)
        
        #添加一个页面(普通页面)
        @self.app.route('/index', methods = ['GET', 'POST'])   #这里'/index'表示的是，网页最后后缀是/login的时候，访问login.html页面
        def index():
            return render_template('index.html',    #如果数据不符合要求，则再次读取login.html页面
                title = 'index..' )

        
        @self.app.route('/billTypes')
        def billTypes(): 
            return self.jsonSets.ToString()

        
        #添加一个页面(普通页面)
        @self.app.route('/billAdd', methods = ['GET', 'POST'])   #这里'/login'表示的是，网页最后后缀是/login的时候，访问login.html页面
        def billAdd():
            form = billAddForm()                        #生成form实例，给render_template渲染使用
            if form.validate_on_submit():               #调用form实例里面的validate_on_submit()功能，验证数据是否安全，如是返回True，默认返回False
                flash('Login requested for OpenID="' + form.openid.data + '", remember_me=' + str(form.remember_me.data))
                billTypes.append(("Test" + str(len(billTypes)), "Test" + str(len(billTypes)) ))
                return redirect('/billBase')            #如果数据符合要求，重定向到主页
            return render_template('billAdd.html',      #如果数据不符合要求，则再次读取login.html页面
                title = 'Bill Add',
                form = form)
        
        #添加一个页面(普通页面)
        @self.app.route('/billBase', methods = ['GET', 'POST'])   #这里'/index'表示的是，网页最后后缀是/login的时候，访问login.html页面
        def billBase():
            return render_template('billBase.html', title = 'billBase..' )
        
        
        
        # 特别注意的是request.args['**']获取get请求的参数
        # request.form['**']获取post请求的参数,request.values['**']可以获得两种方式的参数
 
        @self.app.route('/ajax')
        def ajax():
            return 'get获取到'+request.args['name']
 
        # 当两种方式分开写时函数注意不要重名
        @self.app.route('/ajax', methods=['POST'])
        def ajax_post():
            return 'post获取到'+request.values['name']
 
        @self.app.route('/<name>')
        def other(name):
            return render_template(name)
          
        @self.app.route('/add')
        def add_numbers():
            print("XCCCCCCCCCCCC")
            a = request.args.get('a', 0, type=int)
            b = request.args.get('b', 0, type=int)
            print(a, b)
            return jsonify(result = a + b)
 

        @self.app.route('/test_get/',methods=['POST','GET'])
        def test_get():
            #获取Get数据
            name=request.args.get('name')
            age=int(request.args.get('age'))

            #返回
            if name=='kikay' and age==18:
                return jsonify({'result':'ok'})
            else:
                return jsonify({'result':'error'})


        @self.app.route("/mockservice",methods=['GET','POST'])
        def MockController():
            form = MockCreate()
            code = form['code']
            api = form['api']
            return render_template("HTML/test.html",api=api,data=code)
    #运行
    def run(self): 
        #官方启动方式参见：http://flask.pocoo.org/docs/0.12/quickstart/#a-minimal-application
        self.app.run(host = self.host, port = self.port, debug = self.debug, use_reloader = False)  

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
    pWeb = myWeb("192.168.24.108", 5000, True)
    pWeb.add_API(myAPI, '/test')
    pWeb.add_API(myAPI_p, '/test/<param>')
    pWeb.add_Web()

    # 添加新网页
    @pWeb.app.route("/hello")
    def hello():
        return "Hello...."
 
    pWeb.run()

    
    #pWeb.start()    #线程方式启动有问题

    print("Exiting Main Web...")

if __name__ == '__main__':   
    main()