# -*- coding: utf-8 -*-
"""
Created on  张斌 2019-03-30 15:58:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com

    pyWeb --股票代码查询
""" 
import sys, os, string, mySystem 

#导入模块
from flask import jsonify, request, flash, render_template, redirect    #导入模块
from flask_wtf import FlaskForm                                         #FlaskForm 为表单基类
from wtforms import BooleanField,IntegerField,DecimalField,StringField,TextAreaField,PasswordField,SubmitField,RadioField,DateField,SelectField,SelectMultipleField       #导入字符串字段，密码字段，提交字段
from wtforms.validators import DataRequired,ValidationError,Email,Regexp,EqualTo,Required,NumberRange,Length

mySystem.Append_Us("", False)  
mySystem.Append_Us("../zxcPy.Robot/Roots", False, __file__)
mySystem.Append_Us("../../zxcPy.Quote/zxcPy.Quotation", False, __file__)
import myIO, myWeb, myDebug, myData_Json, myRoot_Usr, myQuote
from myGlobal import gol


# 股票模糊查询页面
class stockQueryForm(FlaskForm):  
    #商品信息
    stockID = StringField('股票代码', [DataRequired(),Length(min=4, max=8)], render_kw={"placeholder": "请输入股票代码"})  
    stockName = StringField('股票名称', [DataRequired(),Length(min=2, max=6)], render_kw={"placeholder": "请输入股票名称"})
 

#集中添加所有Web
def add_Webs(pWeb):      
    #添加页面--股票模糊查询
    @pWeb.app.route('/stockQuery')
    def stockQuery(): 
        #载入配置
        code_id=request.args.get('code_id', "")
        code_name=request.args.get('code_name', "") 

        pStocks = gol._Get_Value('setsStock', None)
        lstStock = pStocks._Find(code_id, code_name)
        
        lstExtypes = []
        lstCode_id = []
        lstCode_Name = []
        lstCode_NameEN = []
        for x in lstStock:
            lstExtypes.append(x.extype)
            lstCode_id.append(x.code_id)
            lstCode_Name.append(x.code_name)
            lstCode_NameEN.append(x.code_name_En)
            
        jsonStocks = myData_Json.Json_Object()
        jsonStocks["extypes"] = lstExtypes
        jsonStocks["code_ids"] = lstCode_id
        jsonStocks["code_names"] = lstCode_Name
        jsonStocks["code_namesEN"] = lstCode_NameEN
        return jsonStocks.ToString() 
