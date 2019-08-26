# -*- coding: utf-8 -*-
"""
Created on  张斌 2018-04-04 11:00:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com

    myWeb, Api接口操作, 基于flask
"""
from . import adminbapp                 ##导入app
from flask import  render_template,redirect,url_for,flash,session,request
from admin.forms import LoginForm       #引入forms.py文件
from models import Admin                #导入数据库模型
from functools import wraps             #导入装饰器模块
from movie_project import db            #引入sqlalchemy实例化对象

#登录验证装饰器
def login_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if session.get('admin'):        #验证session
            return func(*args, **kwargs)
        else:
            return redirect(url_for('admin.login'))
    return decorated_function


#登录页面
@adminbapp.route('/login/',methods=['GET','POST'])
def login():
    forms = LoginForm()                     #实例化forms
    if forms.validate_on_submit():          #提交的时候进行验证,如果数据能被所有验证函数接受，则返回true，否则返回false
        data = forms.data                   #获取form数据信息（包含输入的用户名（account）和密码（pwd）等信息）,这里的account和pwd是在forms.py里定义的
        admin = Admin.query.filter_by(name=data["account"]).first()         #查询表信息admin表里的用户名信息
        if admin == None:
            flash("账号不存在")              #操作提示信息，会在前端显示
            return redirect(url_for('admin.login'))
        elif admin != None and not admin.check_pwd(data["pwd"]):            #这里的check_pwd函数在models 下Admin模型下定义
            flash("密码错误")
            return  redirect(url_for('admin.login'))
        session['admin'] = data['account']                                  #匹配成功，添加session
        return redirect(request.args.get('next') or url_for('admin.index')) #重定向到首页
    return render_template('admin/login.html',form=forms)