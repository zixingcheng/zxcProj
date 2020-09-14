# -*- coding: utf-8 -*-
"""
Created on  张斌 2020-05-19 19:58:00 
    @author: zhang bin
    @email:  zhangbin@qq.com

    pyWeb --生态环境局上传代码
""" 
import sys, os, string, mySystem  

#导入模块
from flask import jsonify, request, flash, render_template, redirect    #导入模块
from flask_wtf import FlaskForm                                         #FlaskForm 为表单基类
from wtforms import BooleanField,IntegerField,DecimalField,StringField,TextAreaField,PasswordField,SubmitField,RadioField,DateField,SelectField,SelectMultipleField       #导入字符串字段，密码字段，提交字段
from wtforms.validators import DataRequired,ValidationError,Email,Regexp,EqualTo,Required,NumberRange,Length

from flask import Flask, render_template, request, redirect, url_for, make_response,jsonify
from werkzeug.utils import secure_filename
import os
import time
from datetime import timedelta
 
#设置允许的文件格式
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'JPG', 'PNG', 'bmp'])
 
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
 

mySystem.Append_Us("", False)  
mySystem.Append_Us("../zxcPy.Robot/Roots", False, __file__)
mySystem.Append_Us("../../zxcPy.Quote/zxcPy.Quotation", False, __file__)
import myIO, myWeb, myWeb_urlLib, myDebug, myData_Json, myRoot_Usr
from myGlobal import gol


 
# 测试设置页面
class myTestForm(FlaskForm):  
    #商品信息
    stockID = StringField('股票代码', [DataRequired(),Length(min=4, max=10)], render_kw={"placeholder": "请输入股票代码"})  
    stockName = StringField('股票名称', [DataRequired(),Length(min=2, max=12)], render_kw={"placeholder": "请输入股票名称/首字母"})
     
   
#集中添加所有Web
def add_Webs(pWeb):          
    #添加页面--股票选择页面-测试
    # @app.route('/upload', methods=['POST', 'GET'])
    #添加页面--股票选择页面-测试
    @pWeb.app.route('/zxcWebs/stock/myTest', methods=['POST', 'GET'])  # 添加路由
    def upload():
        if request.method == 'POST':
            f = request.files['file']
 
            if not (f and allowed_file(f.filename)):
                return jsonify({"error": 1001, "msg": "请检查上传的图片类型，仅限于png、PNG、jpg、JPG、bmp"})
 
            user_input = request.form.get("name")
            basepath = os.path.dirname(__file__)  # 当前文件所在路径
 
            upload_path = os.path.join(basepath, 'static/images', secure_filename(f.filename))  # 注意：没有的文件夹一定要先创建，不然会提示没有该路径
            # upload_path = os.path.join(basepath, 'static/images','test.jpg')  #注意：没有的文件夹一定要先创建，不然会提示没有该路径
            f.save(upload_path)
 
            # 使用Opencv转换一下图片格式和名称
            #img = cv2.imread(upload_path)
            #cv2.imwrite(os.path.join(basepath, 'static/images', 'test.jpg'), img)
            return render_template('upload_ok.html',userinput=user_input, val1=time.time())
        return render_template('upload.html')

    # show photo
    @pWeb.app.route('/zxcWebs/stock/show/<string:filename>', methods=['GET'])
    def show_photo(filename):
        basedir = os.path.dirname(__file__)  # 当前文件所在路径
        if request.method == 'GET':
            if filename is None:
                pass
            else:
                image_data = open(os.path.join(basedir, 'static/images/%s' % filename), "rb").read()
                response = make_response(image_data)
                response.headers['Content-Type'] = 'image/png'
                return response
        else:
            pass

