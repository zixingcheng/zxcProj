# -*- coding: utf-8 -*-
"""
Created on  张斌 2019-03-26 15:58:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com

    pyWeb --订单新增
""" 
import sys, os, string, datetime, mySystem 

#导入模块
from flask import jsonify, request, flash, render_template, redirect    #导入模块
from flask_wtf import FlaskForm                                         #FlaskForm 为表单基类
from wtforms import BooleanField,IntegerField,DecimalField,StringField,TextAreaField,PasswordField,SubmitField,RadioField,DateField,SelectField,SelectMultipleField       #导入字符串字段，密码字段，提交字段
from wtforms.validators import DataRequired,ValidationError,Email,Regexp,EqualTo,Required,NumberRange,Length

mySystem.Append_Us("", False)  
mySystem.Append_Us("../zxcPy.Robot/Roots", False, __file__)
import myIO, myWeb, myDebug, myData_Json, myData_Trans, myRoot_Usr
import myManager_Bill
from myGlobal import gol


# 订单添加页面
class orderAddForm(FlaskForm):  
    usrID = StringField('usrID', default="")                    #用户名
    recorderName = StringField('recorderName', default="")      #记录人姓名

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
    orderRemark = StringField('备注信息', render_kw={"placeholder": "请输入备注信息，可为空"})   

#集中添加所有API
def add_Webs(pWeb):     
    #添加默认主页
    pWeb.add_Web()  
    
    #添加页面--订单商品查询
    @pWeb.app.route('/zxcWebs/order/Sets')
    def orderSets(): 
        #载入配置
        nameType=request.args.get('type')
        text = myIO.getContent(pWeb.baseDir + "/Setting/OrderSets-"+ nameType +".json", True, False)
        #jsonSets = myData_Json.Json_Object()
        #jsonSets.Trans_FromStr(text) 
        #return jsonSets.ToString()
        return text
    

    #添加页面--订单新增
    @pWeb.app.route('/zxcWebs/order/Add/<orderType>', methods = ['GET', 'POST'])    
    def orderAdd(orderType):
        form = orderAddForm()                       #生成form实例，给render_template渲染使用 
        form.orderType.data = orderType
        form.recorderName.data = request.args.get('usrID', "")
        if(form.recorderName.data == ""): return "无效链接！"

        if form.validate_on_submit():               #调用form实例里面的validate_on_submit()功能，验证数据是否安全，如是返回True，默认返回False
            #添加订单 
            recorder = usrAdd(form)                 #添加用户
            pRes = orderAdd_Updata(form, orderType) #订单信息更新
            return pRes.replace('\n', '<br/>')
        return render_template('orderAdd.html', title = 'Order Add', form = form, orderType = orderType)     #如果数据不符合要求，则再次读取orderAdd.html页面

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


    #用户信息更新
    def usrAdd(form):
        usrInfos = {}
        usrInfos["usrName_Full"] = form.orderUsrName.data
        usrInfos["usrName"] = form.orderUsrName.data
        usrInfos["usrID"] = form.usrID.data
        usrInfos["usrPhone"] = form.orderUsrPhone.data
        usrInfos["usrAddress"] = form.orderAddress.data
        
        #添加新用户
        pUsers = gol._Get_Setting('sysUsers', None)     #实例 用户对象集
        if(pUsers.Add(usrInfos, True)):
            pUsers._Save() 

        #查询订单记录人 
        recorder = form.recorderName.data
        pUser = pUsers._Find("", recorder, recorder, recorder)
        if(pUser != None): 
            if(pUser.usrName_Full == ""):
                recorder = pUser.usrName_Nick
            else:
                recorder = pUser.usrName_Full
        form.recorderName.data = recorder
        return recorder 

    #订单信息更新  
    def orderAdd_Updata(form, orderType):
        #记录账单
        pManager = gol._Get_Setting('manageBills', None)
        pBills = pManager[orderType]

        billInfo = pBills.OnCreat_BillInfo() 
        billInfo['usrID'] = form.orderUsrName.data
        billInfo['usrBillType'] = "卖出"
        billInfo['recordTime'] = datetime.datetime.now()
        billInfo['recorder'] = form.recorderName.data
        billInfo['tradeID'] = ""
        billInfo['tradeID_Relation'] = ""
        billInfo['tradeParty'] = form.orderUsrName.data
        billInfo['tradeType'] = orderType
        billInfo['tradeTypeTarget'] = form.orderTargetType.data
        billInfo['tradeTarget'] = form.orderTarget.data
        billInfo['tradePrice'] = myData_Trans.To_Float(form.orderPrice.data.split(' ')[0].replace('￥',''))
        billInfo['tradeNum'] = myData_Trans.To_Float(form.orderNum.data.split(' ')[0])
        billInfo['tradeMoney'] = myData_Trans.To_Float(form.orderMoney.data.replace('￥',''))
        billInfo['tradePoundage'] = 0
        billInfo['tradeProfit'] = billInfo['tradeMoney']
        billInfo['tradeTime'] = datetime.datetime.now()
        billInfo['isDel'] = False
        billInfo['remark'] = form.orderRemark.data
        return pBills.Add_ByDict(billInfo)
