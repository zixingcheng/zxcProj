 # -*- coding: utf-8 -*-
"""
Created on  张斌 2020-05-20 10:20:00 
    @author: zhang bin
    @email:  zhangbin@qq.com

    pyWeb --生态环境局表单代码
""" 
import sys, os, time, datetime, string, mySystem  
from datetime import timedelta

#导入模块
from flask import jsonify, request, flash, render_template, redirect    #导入模块
from flask_wtf import FlaskForm                                         #FlaskForm 为表单基类
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import BooleanField,IntegerField,DecimalField,StringField,TextAreaField,PasswordField,SubmitField,RadioField,SelectField,SelectMultipleField       #导入字符串字段，密码字段，提交字段
from wtforms.validators import InputRequired,DataRequired,ValidationError,Email,Regexp,EqualTo,Required,NumberRange,Length
from werkzeug.utils import secure_filename
from wtforms.fields.html5 import DateField
#from flask_pagination import Pagination

mySystem.Append_Us("", False)  
import myIO, myData, myData_Json, myData_Trans
from zxcPy_Form import * 


# 企业信息设置页面
class myCompanyForm_active_carbon(FlaskForm):  
    # 企业信息
    txtStyle = "font-size: 16px;width: 360px;height: 30px;"
    companyID = StringField('统一社会信用代码', [DataRequired(),Length(min=18, max=18)], render_kw={"placeholder": "请输入统一社会信用代码", "style": txtStyle})  
    companyName = StringField('企业全称', [DataRequired(),Length(min=2, max=50)], render_kw={"placeholder": "请输入企业全称", "style": txtStyle})
    companyInStreet = StringField('所在镇街', [DataRequired(),Length(min=2, max=50)], render_kw={"placeholder": "请输入企业所在镇街", "style": txtStyle})
    companyInVillage = StringField('所属村（社区）', [DataRequired(),Length(min=2, max=50)], render_kw={"placeholder": "请输入企业所属村（社区）", "style": txtStyle})
    companyAdrr = StringField('详细地址', [DataRequired(),Length(min=6, max=100)], render_kw={"placeholder": "请输入企业详细地址", "style": txtStyle})    
    companyScale = StringField('企业规模', [DataRequired()], render_kw={"placeholder": "请选择企业规模", "style": txtStyle})
    companyContacts = StringField('企业联系人', [DataRequired(),Length(min=2, max=8)], render_kw={"placeholder": "请输入企业联系人", "style": txtStyle})
    companyPhone = StringField('电话号码', validators=[DataRequired(),Regexp("1[3578]\d{9}", message="手机格式不正确")], render_kw={"placeholder": "请输入联系电话", "style": txtStyle})
    
    companyHasProcess  = StringField('是否采用活性炭吸附工艺', [DataRequired()], render_kw={"placeholder": "请选择是否采用活性炭吸附工艺", "style": txtStyle})
    companyNumProcess = IntegerField('活性炭吸附工艺设施套数', [InputRequired(),NumberRange(min=-1, max=100)], render_kw={"placeholder": "请输入采用活性炭吸附工艺设施套数", "style": txtStyle})
    companyRecycle = IntegerField('正常更换周期（日/次）', [InputRequired(),NumberRange(min=0, max=365)], render_kw={"placeholder": "请输入更换周期（日/次）", "style": txtStyle})
    companyVolumeTotal = DecimalField('设计总填装量（千克）', [InputRequired(),NumberRange(min=0, max=99999)], render_kw={"placeholder": "请输入设计总填装量（千克）", "style": txtStyle})
    
    companyRedate = DateField('新活性炭更换日期', default='', format='%Y-%m-%d', render_kw={"placeholder": "请选择新活性炭更换日期", "style": txtStyle}) 
    companyRevolume = DecimalField('新活性炭更换量（千克）', [InputRequired(),NumberRange(min=0, max=99999)], render_kw={"placeholder": "请输入新活性炭更换量（千克）", "style": txtStyle})
    companyTransferredvolume = DecimalField('已转移废活性炭量（千克）', [InputRequired(),NumberRange(min=0, max=99999)], render_kw={"placeholder": "请输入已转移废活性炭量（千克）", "style": txtStyle})
    companyNoTransferredvolume = DecimalField('暂未转移废活性炭量（千克）', [InputRequired(),NumberRange(min=0, max=99999)], render_kw={"placeholder": "请输入暂未转移废活性炭量（千克）", "style": txtStyle})
    
    save = SubmitField('保存信息', render_kw={"class": "btn-submit-upload","style": "margin-left:10px"})                    # 保存按钮
    
    # 图片信息 
    imgName_1 = StringField('图片_1', [], render_kw={"style": "display:none;"}) 
    imgName_2 = StringField('图片_2', [], render_kw={"style": "display:none;"}) 
    imgName_3 = StringField('图片_3', [], render_kw={"style": "display:none;"}) 
    imgName_4 = StringField('图片_4', [], render_kw={"style": "display:none;"}) 
    imgName_5 = StringField('图片_5', [], render_kw={"style": "display:none;"}) 
    imgName_6 = StringField('图片_6', [], render_kw={"style": "display:none;"}) 
    
#集中添加所有Web
def add_Webs(appWeb, dirBase):
    #添加接口--查询公司信息
    @appWeb.app.route('/zxcAPI/company_ac/query')
    def companyQuery_ac(): 
        #载入配置
        company_id = request.args.get('company_id', "")
        company_name = request.args.get('company_name', "") 
        print(company_id,company_name)

        dbCompany = gol._Get_Value('dbCompany_ac')
        pCompany = dbCompany.getCompany(company_id, company_name)
        if(pCompany == None):
            pCompany = dbCompany.OnCreat_RowInfo();
            pCompany['companyID'] = company_id
            pCompany['companyName'] = company_name
        else:
            pCompany = pCompany.copy()

        #修正部分信息
        pCompany['companyHasProcess'] = myData.iif(pCompany['companyHasProcess'], "是", "否")
        if(type(pCompany['companyRedate']) == datetime.datetime):
            pCompany['companyRedate'] = myData_Trans.Tran_ToDatetime_str(pCompany['companyRedate'], "%Y-%m-%d")
        jsonCompany = myData_Json.Json_Object(pCompany)
        return jsonCompany.ToString() 

    # 添加页面--公司活性炭信息登记页面
    @appWeb.app.route('/zxcWebs/companyinfo_ac', methods = ['GET', 'POST'])  
    @appWeb.app.route('/zxcWebs/companyinfo_ac/<string:companyID>', methods = ['GET', 'POST'])    
    def upload_company_ac(companyID = ""):
        form = myCompanyForm_active_carbon()              #生成form实例，给render_template渲染使用  
        needRefresh = True
        editSucess = False
        if form.validate_on_submit():       #调用form实例里面的validate_on_submit()功能，验证数据是否安全，如是返回True，默认返回False
            if form.save.data:              # 保存按钮被单击 
                # 组装row信息
                pValues = []
                if(True):
                    pValues.append("-1")
                    pValues.append(form.companyID.data)
                    pValues.append(form.companyName.data)
                    pValues.append(form.companyInStreet.data)
                    pValues.append(form.companyInVillage.data)
                    pValues.append(form.companyAdrr.data)
                    pValues.append(form.companyScale.data)
                    pValues.append(form.companyContacts.data)
                    pValues.append(form.companyPhone.data)
    
                    companyHasProcess = myData.iif(form.companyHasProcess.data == "是", True, False)
                    pValues.append(companyHasProcess)
                    pValues.append(form.companyNumProcess.data)
                    pValues.append(form.companyRecycle.data)
                    pValues.append(form.companyVolumeTotal.data)
                
                    pValues.append(myData_Trans.Tran_ToDatetime_str(form.companyRedate.data))
                    pValues.append(form.companyRevolume.data)
                    pValues.append(form.companyTransferredvolume.data)
                    pValues.append(form.companyNoTransferredvolume.data)
            
                    pValues.append(form.imgName_1.data)
                    pValues.append(form.imgName_2.data)
                    pValues.append(form.imgName_3.data)
                    pValues.append(form.imgName_4.data)
                    pValues.append(form.imgName_5.data)
                    pValues.append(form.imgName_6.data)

                # 添加并保存信息
                rowInfo = myData_Trans.Tran_ToStr(pValues, ',')
                dbCompany = gol._Get_Value('dbCompany_ac')
                if(dbCompany.Add_Row_BySimply(rowInfo, True, True) != ""):
                    editSucess = True
        else:
            # 保存时，验证失败，不需要刷新
            if form.save.data:
                needRefresh = False
        return render_template('company_active_carbon.html', title = 'company upload', form = form, companyID = companyID, needRefresh = needRefresh, editSucess = editSucess)
    
    #添加接口--删除筛选公司
    @appWeb.app.route('/zxcAPI/companys_ac/query/del')
    def companysQuery_del_ac(): 
        #载入配置
        companyID = request.args.get('companyID', "")
        companyName = request.args.get('companyName', "") 
             
        #删除
        res = {"success": 1, "data": "", "msg": ""}
        try:
            dbCompany = gol._Get_Value('dbCompany_ac')
            pCompany = dbCompany.getCompany(companyID, companyName)
            if(pCompany != None):
                pCompany["isDel"] = True
                dbCompany.Save_DB()
                res['data'] = "删除成功。"
            else:
                res['data'] = "公司信息不存在。"
        except Exception as err:
            res['success'] = 0
            res['data'] = "删除失败。"
            res['msg'] = str(err)
        return myData_Json.Trans_ToJson_str(res)

    
    #添加接口--查询筛选公司列表
    @appWeb.app.route('/zxcAPI/companys_ac/query')
    def companysQuery_ac(): 
        #载入配置
        pageIndex = myData_Trans.To_Int(request.args.get('pageIndex', 1))
        pageSize = myData_Trans.To_Int(request.args.get('pageSize', 15))

        companyID = request.args.get('companyID', "")
        companyName = request.args.get('companyName', "") 
        companyInStreet = request.args.get('companyInStreet', "") 
        companyInVillage = request.args.get('companyInVillage', "") 
        companyScale = request.args.get('companyScale', "") 
        companyHasProcess = request.args.get('companyHasProcess', "") 
        
        #组装筛选条件
        fliter = ""
        if(companyID != ""): fliter += " && companyID == " + companyID
        if(companyName != ""): fliter += " && companyName == " + companyName
        if(companyInStreet != ""): fliter += " && companyInStreet == " + companyInStreet
        if(companyInVillage != ""): fliter += " && companyInVillage == " + companyInVillage
        if(companyScale != ""): fliter += " && companyScale == " + companyScale
        if(companyHasProcess != ""): 
            fliter += " && companyHasProcess == " + str(myData.iif(companyHasProcess == "是", True, False))
        if(fliter != ""): fliter = fliter[4:]
        
        #筛选
        res = {"success": 1, "data": "", "msg": ""}
        try:
            dbCompany = gol._Get_Value('dbCompany_ac')
            totalCount, pCompanys = dbCompany.getCompanys(param = fliter, isDel = False, page = pageIndex, per_page = pageSize)
            res['data'] = pCompanys
            res['totalCount'] = totalCount
        except Exception as err:
            res['success'] = 0
            res['msg'] = str(err)
        return myData_Json.Trans_ToJson_str(res)

    # 添加页面--筛选公司列表页面
    @appWeb.app.route("/zxcWebs/companyinfos_ac",methods=['GET','POST'])
    @appWeb.app.route("/zxcWebs/companyinfos_ac/<int:page>",methods=['GET','POST'])
    def query_companys_ac(page=1):
        return render_template('company_active_carbon_list.html')
    
    #添加接口--保存筛选公司列表
    @appWeb.app.route('/zxcAPI/companys_ac/query/save')
    def companysQuery_save_ac(): 
        #载入配置
        companyID = request.args.get('companyID', "")
        companyName = request.args.get('companyName', "") 
        companyInStreet = request.args.get('companyInStreet', "") 
        companyInVillage = request.args.get('companyInVillage', "") 
        companyScale = request.args.get('companyScale', "") 
        companyHasProcess = request.args.get('companyHasProcess', "") 
        
        #组装筛选条件
        fliter = ""
        if(companyID != ""): fliter += " && companyID == " + companyID
        if(companyName != ""): fliter += " && companyName == " + companyName
        if(companyInStreet != ""): fliter += " && companyInStreet == " + companyInStreet
        if(companyInVillage != ""): fliter += " && companyInVillage == " + companyInVillage
        if(companyScale != ""): fliter += " && companyScale == " + companyScale
        if(companyHasProcess != ""): 
            fliter += " && companyHasProcess == " + str(myData.iif(companyHasProcess == "是", True, False))
        if(fliter != ""): fliter = fliter[4:]
        
        #筛选
        res = {"success": 1, "data": "", "msg": ""}
        try:
            dbCompany = gol._Get_Value('dbCompany_ac')
            totalCount, pCompanys = dbCompany.getCompanys(param = fliter, isDel = False, page = 1, per_page = 99999999)

            #保存
            path = appWeb.baseDir + "/static/data/Companys/企业信息数据表-活性炭.csv"
            dbCompany.Save_as_csv(path, pCompanys, True)

            res['filename'] = "企业信息数据表-活性炭.csv"
            res['filefloder'] = "Companys"
            res['totalCount'] = totalCount
        except Exception as err:
            res['success'] = 0
            res['msg'] = str(err)
        return myData_Json.Trans_ToJson_str(res)
    

add_Webs(appWeb, dirBase)