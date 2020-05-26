 # -*- coding: utf-8 -*-
"""
Created on  张斌 2020-05-20 10:20:00 
    @author: zhang bin
    @email:  zhangbin@qq.com

    pyWeb --生态环境局表单代码
""" 
import sys, os, string, mySystem  

#导入模块
from flask import jsonify, request, flash, render_template, redirect    #导入模块
from flask_wtf import FlaskForm                                         #FlaskForm 为表单基类
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import BooleanField,IntegerField,DecimalField,StringField,TextAreaField,PasswordField,SubmitField,RadioField,DateField,SelectField,SelectMultipleField       #导入字符串字段，密码字段，提交字段
from wtforms.validators import DataRequired,ValidationError,Email,Regexp,EqualTo,Required,NumberRange,Length
from werkzeug.utils import secure_filename

import os
import time
from datetime import timedelta



mySystem.Append_Us("", False)  
import myIO
from zxcPy_Form import * 


# 测试设置页面
class myTestForm(FlaskForm):  
    #商品信息
    stockID = StringField('股票代码', [DataRequired(),Length(min=4, max=10)], render_kw={"placeholder": "请输入股票代码"})  
    stockName = StringField('股票名称', [DataRequired(),Length(min=2, max=12)], render_kw={"placeholder": "请输入股票名称/首字母"})


def save_image(files):
    images = []
    for img in files:
        # 处理文件名
        filename = hashlib.md5(current_user.username + str(time.time())).hexdigest()[:10]
        image = photos.save(img, name=filename + '.')
        file_url = photos.url(image)
        url_s = create_show(image)  # 创建展示图
        url_t = create_thumbnail(image)  # 创建缩略图
        images.append((file_url, url_s, url_t))
    return images

#集中添加所有Web
def add_Webs(appWeb, dirBase):       
    imgPath = dirBase + "/static/images/"
    dirPath = dirBase
    
    #添加页面--股票选择页面-测试
    @appWeb.app.route('/zxcWebs/stock/myTest', methods=['POST', 'GET'])  # 添加路由
    def upload():
        if request.method == 'POST':
            f = request.files['file']
 
            if not (f and allowed_file(f.filename)):
                return jsonify({"error": 1001, "msg": "请检查上传的图片类型，仅限于png、PNG、jpg、JPG、bmp"})
 
            user_input = request.form.get("name")
            basepath = os.path.dirname(__file__)  # 当前文件所在路径
 
            upload_path = os.path.join(dirBase, imgPath + "upload", secure_filename(f.filename))  # 注意：没有的文件夹一定要先创建，不然会提示没有该路径
            # upload_path = os.path.join(basepath, 'static/images','test.jpg')  #注意：没有的文件夹一定要先创建，不然会提示没有该路径
            f.save(upload_path)
 
            # 使用Opencv转换一下图片格式和名称
            #img = cv2.imread(upload_path)
            #cv2.imwrite(os.path.join(basepath, 'static/images', 'test.jpg'), img)
            return render_template('upload_ok.html',userinput=user_input, val1=time.time())
        return render_template('upload.html')
    
    @appWeb.app.route('/upload')
    def upload_test():
        return render_template('up.html')

    

add_Webs(appWeb, dirBase)