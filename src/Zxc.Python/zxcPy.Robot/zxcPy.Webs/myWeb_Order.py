# -*- coding: utf-8 -*-
"""
Created on  张斌 2019-03-26 15:58:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com

    pyWeb --订单新增
""" 
import sys, os, string, mySystem 

#导入模块
from flask import jsonify, request, flash, render_template, redirect    #导入模块
from flask_wtf import FlaskForm                                         #FlaskForm 为表单基类
from wtforms import BooleanField,IntegerField,DecimalField,StringField,TextAreaField,PasswordField,SubmitField,RadioField,DateField,SelectField,SelectMultipleField       #导入字符串字段，密码字段，提交字段
from wtforms.validators import DataRequired,ValidationError,Email,Regexp,EqualTo,Required,NumberRange,Length

mySystem.Append_Us("", False)  
import myIO, myWeb, myDebug, myData_Json
from myGlobal import gol


# 订单添加页面
class orderAddForm(FlaskForm):  
    usrID = StringField('usrID', default="")                    #用户名

    #商品信息
    orderType = StringField('商品大类', default="")  
    orderTargetType = StringField('商品分类', [DataRequired(),Length(min=2, max=8)], render_kw={"placeholder": "请选择商品分类"})
    orderTarget = StringField('商品名称', [DataRequired(),Length(min=2, max=8)], render_kw={"placeholder": "请选择商品名称"})
    orderPrice = StringField('价格', [DataRequired()])    
    orderNum = StringField('购买数量', [DataRequired()])     
    orderMoney = StringField('总金额', [DataRequired()])   
    orderRebate = StringField('折扣金额',  [DataRequired()])    
    
    orderUsrName = StringField('收货人', [DataRequired(),Length(min=2, max=6)], render_kw={"placeholder": "请输入收货人姓名"})
    orderUsrPhone = StringField('联系电话', validators=[DataRequired(),Regexp("1[3578]\d{9}", message="手机格式不正确")], render_kw={"placeholder": "请输入联系电话"})
    orderAddress = StringField('收货地址', validators=[DataRequired()], render_kw={"class": "form-control","placeholder": "请输入收货地址"}) 
 

#集中添加所有API
def add_Webs(pWeb):     
    #添加默认主页
    pWeb.add_Web()  
    
    #添加页面--订单商品查询
    @pWeb.app.route('/orderSets')
    def orderSets(): 
        #载入配置
        nameType=request.args.get('type')
        text = myIO.getContent(pWeb.baseDir + "/Setting/OrderSets-"+ nameType +".json", True, False)
        #jsonSets = myData_Json.Json_Object()
        #jsonSets.Trans_FromStr(text) 
        #return jsonSets.ToString()
        return text

    #添加页面--订单新增
    @pWeb.app.route('/orderAdd/<orderType>', methods = ['GET', 'POST'])    
    def orderAdd(orderType):
        form = orderAddForm()                       #生成form实例，给render_template渲染使用 
        form.orderType = orderType
        if form.validate_on_submit():               #调用form实例里面的validate_on_submit()功能，验证数据是否安全，如是返回True，默认返回False
            return redirect('/orderBase')           #如果数据符合要求，重定向到主页
        return render_template('orderAdd.html', title = 'Order Add', form = form, orderType = orderType)     #如果数据不符合要求，则再次读取orderAdd.html页面

