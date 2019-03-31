# -*- coding: utf-8 -*-
"""
Created on  张斌 2019-03-26 15:58:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com

    pyWeb --用户
""" 
import sys, os, string, mySystem 

#导入模块
from flask import jsonify, request, flash, render_template, redirect    #导入模块
from flask_wtf import FlaskForm                                         #FlaskForm 为表单基类
from wtforms import BooleanField,IntegerField,DecimalField,StringField,TextAreaField,PasswordField,SubmitField,RadioField,DateField,SelectField,SelectMultipleField       #导入字符串字段，密码字段，提交字段
from wtforms.validators import DataRequired,ValidationError,Email,Regexp,EqualTo,Required,NumberRange,Length

mySystem.Append_Us("", False)  
mySystem.Append_Us("../zxcPy.Robot/Roots", False, __file__)
import myIO, myWeb, myDebug, myData_Json, myRoot_Usr
from myGlobal import gol



#集中添加所有API
def add_Webs(pWeb):   
    #添加页面--用户信息查询
    @pWeb.app.route('/zxcAPI/robot/user/query')
    def usrInfoQuery(): 
        name=request.args.get('name', "")
        phone=request.args.get('phone', "") 
        pUsers = gol._Get_Setting('sysUsers', None)     #实例 用户对象集
        users = pUsers._Find_ByRealInfo(name, phone)

        jsonUsers = myData_Json.Json_Object()
        lstUsers = []
        lstPhones = []
        lstAddress = []
        for x in users:
            lstUsers.append(x.usrName_Full)
            lstPhones = lstPhones + x.usrPhones
            lstAddress = lstAddress + x.usrAddresss
        jsonUsers["usrName_Fulls"] = lstUsers
        jsonUsers["usrPhones"] = lstPhones
        jsonUsers["usrAddresss"] = lstAddress
        return jsonUsers.ToString() 


