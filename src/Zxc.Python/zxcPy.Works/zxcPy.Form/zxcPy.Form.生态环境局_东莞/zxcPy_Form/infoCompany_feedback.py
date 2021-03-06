﻿ # -*- coding: utf-8 -*-
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
class myCompanyForm(FlaskForm):  
    # 企业信息
    txtStyle = "font-size: 16px;width: 360px;height: 30px;"
    companyID = StringField('统一社会信用代码', [DataRequired(),Length(min=18, max=18)], render_kw={"placeholder": "请输入统一社会信用代码", "style": txtStyle})  
    companyName = StringField('企业全称', [DataRequired(),Length(min=2, max=50)], render_kw={"placeholder": "请输入企业全称", "style": txtStyle})
    companyInStreet = StringField('所在镇街', [DataRequired(),Length(min=2, max=50)], render_kw={"placeholder": "请输入企业所在镇街", "style": txtStyle})
    companyInVillage = StringField('所属村（社区）', [DataRequired(),Length(min=2, max=50)], render_kw={"placeholder": "请输入企业所属村（社区）", "style": txtStyle})
    companyAdrr = StringField('详细地址', [DataRequired(),Length(min=6, max=100)], render_kw={"placeholder": "请输入企业详细地址", "style": txtStyle})    
    companyScale = StringField('企业规模', [DataRequired()], render_kw={"placeholder": "请选择企业规模", "style": txtStyle})
    companySpecialcase = StringField('特殊情形', [DataRequired()], render_kw={"placeholder": "请选择企业特殊情形", "style": txtStyle})
    companyManangeclass = StringField('管理类别', [DataRequired()], render_kw={"placeholder": "请选择企业管理类别", "style": txtStyle})
    companyContacts = StringField('图片上传人', [DataRequired(),Length(min=2, max=8)], render_kw={"placeholder": "请输入图片上传人姓名", "style": txtStyle})
    companyPhone = StringField('电话号码', validators=[DataRequired(),Regexp("1[3578]\d{9}", message="手机格式不正确")], render_kw={"placeholder": "请输入联系电话", "style": txtStyle})
    
    save = SubmitField('保存信息', render_kw={"class": "btn-submit-upload","style": "margin-left:10px"})                    # 保存按钮

    # 图片信息 
    imgName_1 = StringField('图片_相关部门证明', [], render_kw={"style": "display:none;"}) 
    imgName_2 = StringField('图片_正门照片', [], render_kw={"style": "display:none;"}) 
    imgName_3 = StringField('图片_生产车间照片', [], render_kw={"style": "display:none;"}) 
    imgName_4 = StringField('图片_营业执照注销', [], render_kw={"style": "display:none;"}) 
    imgName_5 = StringField('图片_断水断电证明', [], render_kw={"style": "display:none;"}) 
    imgName_6 = StringField('图片_执法笔录', [], render_kw={"style": "display:none;"}) 
    
#集中添加所有Web
def add_Webs(appWeb, dirBase):
    #添加接口--查询公司信息
    @appWeb.app.route('/zxcAPI/company_fb/query')
    def companyQuery_fb(): 
        #载入配置
        company_id = request.args.get('company_id', "")
        company_name = request.args.get('company_name', "") 
        print(company_id,company_name)

        dbCompany = gol._Get_Value('dbCompany_fb')
        pCompany = dbCompany.getCompany(company_id, company_name)
        if(pCompany == None):
            pCompany = dbCompany.OnCreat_RowInfo();
            pCompany['companyID'] = company_id
            pCompany['companyName'] = company_name
        else:
            pCompany = pCompany.copy()

        #修正部分信息
        jsonCompany = myData_Json.Json_Object(pCompany)
        if(jsonCompany['editTime'] != ""):
            jsonCompany['editTime'] = '' 
        return jsonCompany.ToString() 

    # 添加页面--公司活性炭信息登记页面
    @appWeb.app.route('/zxcWebs/companyinfo_fb', methods = ['GET', 'POST'])  
    @appWeb.app.route('/zxcWebs/companyinfo_fb/<string:companyID>', methods = ['GET', 'POST'])    
    def upload_company_fb(companyID = ""):
        form = myCompanyForm()              #生成form实例，给render_template渲染使用  
        needRefresh = True
        editSucess = False
        if form.validate_on_submit():       #调用form实例里面的validate_on_submit()功能，验证数据是否安全，如是返回True，默认返回False
            if form.save.data:              # 保存按钮被单击 
                # 组装row信息
                rowInfo = {}
                if(True):
                    rowInfo["ID"] = "-1"
                    if(form.companyID.data == "000000000000000000"):
                        companyID = "_" + myIO.create_UUID()
                        rowInfo["companyID"] = companyID
                    else:
                        rowInfo["companyID"] = form.companyID.data
                    rowInfo["companyName"] = form.companyName.data
                    rowInfo["companyInStreet"] = form.companyInStreet.data
                    rowInfo["companyInVillage"] = form.companyInVillage.data
                    rowInfo["companyAdrr"] = form.companyAdrr.data
                    rowInfo["companyScale"] = form.companyScale.data
                    rowInfo["companySpecialcase"] = form.companySpecialcase.data
                    rowInfo["companyManangeclass"] = form.companyManangeclass.data
                    rowInfo["companyContacts"] = form.companyContacts.data
                    rowInfo["companyPhone"] = form.companyPhone.data
                    
                    rowInfo["imgName_1"] = form.imgName_1.data.replace("/static/images/upload/", "")
                    rowInfo["imgName_2"] = form.imgName_2.data.replace("/static/images/upload/", "")
                    rowInfo["imgName_3"] = form.imgName_3.data.replace("/static/images/upload/", "")
                    rowInfo["imgName_4"] = form.imgName_4.data.replace("/static/images/upload/", "")
                    rowInfo["imgName_5"] = form.imgName_5.data.replace("/static/images/upload/", "")
                    rowInfo["imgName_6"] = form.imgName_6.data.replace("/static/images/upload/", "")

                # 添加并保存信息
                # rowInfo = myData_Trans.Tran_ToStr(pValues, ',')
                dbCompany = gol._Get_Value('dbCompany_fb')
                if(dbCompany.Add_Row(rowInfo, True, True, "companyInfo") != ""):
                    editSucess = True
        else:
            # 保存时，验证失败，不需要刷新
            if form.save.data:
                needRefresh = False
        return render_template('company_feedback.html', title = 'company upload', form = form, companyID = companyID, needRefresh = needRefresh, editSucess = editSucess)
    
    #添加接口--删除筛选公司
    @appWeb.app.route('/zxcAPI/companys_fb/query/del')
    def companysQuery_del_fb(): 
        #载入配置
        companyID = request.args.get('companyID', "")
        companyName = request.args.get('companyName', "") 
             
        #删除
        res = {"success": 1, "data": "", "msg": ""}
        try:
            dbCompany = gol._Get_Value('dbCompany_fb')
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
    @appWeb.app.route('/zxcAPI/companys_fb/query')
    def companysQuery_fb(): 
        #载入配置
        pageIndex = myData_Trans.To_Int(request.args.get('pageIndex', 1))
        pageSize = myData_Trans.To_Int(request.args.get('pageSize', 15))

        companyID = request.args.get('companyID', "")
        companyName = request.args.get('companyName', "") 
        companyInStreet = request.args.get('companyInStreet', "") 
        companyInVillage = request.args.get('companyInVillage', "") 
        companyAdrr = request.args.get('companyAdrr', "") 
        companyScale = request.args.get('companyScale', "") 
        companySpecialcase = request.args.get('companySpecialcase', "") 
        companyManangeclass = request.args.get('companyManangeclass', "") 
        companyContacts = request.args.get('companyContacts', "") 
        
        #组装筛选条件
        fliter = ""
        if(companyID != ""): fliter += " && companyID == " + companyID
        if(companyName != ""): fliter += " && companyName %like% " + companyName
        if(companyInStreet != ""): fliter += " && companyInStreet == " + companyInStreet
        if(companyInVillage != ""): fliter += " && companyInVillage == " + companyInVillage
        if(companyAdrr != ""): fliter += " && companyAdrr == " + companyAdrr
        if(companyScale != ""): fliter += " && companyScale == " + companyScale
        if(companySpecialcase != ""): fliter += " && companySpecialcase == " + companySpecialcase
        if(companyManangeclass != ""): fliter += " && companyManangeclass == " + companyManangeclass
        if(companyContacts != ""): fliter += " && companyContacts == " + companyContacts
        if(fliter != ""): fliter = fliter[4:]
        
        #筛选
        res = {"success": 1, "data": "", "msg": ""}
        try:
            dbCompany = gol._Get_Value('dbCompany_fb')
            totalCount, pCompanys = dbCompany.getCompanys(param = fliter, isDel = False, page = pageIndex, per_page = pageSize)
            res['data'] = pCompanys
            res['totalCount'] = totalCount
        except Exception as err:
            res['success'] = 0
            res['msg'] = str(err)
        return myData_Json.Trans_ToJson_str(res)

    # 添加页面--筛选公司列表页面
    @appWeb.app.route("/zxcWebs/companyinfos_fb",methods=['GET','POST'])
    @appWeb.app.route("/zxcWebs/companyinfos_fb/<int:page>",methods=['GET','POST'])
    def query_companys_fb(page=1):
        return render_template('company_feedback_list.html')
    
    #添加接口--保存筛选公司列表
    @appWeb.app.route('/zxcAPI/companys_fb/query/save')
    def companysQuery_save_fb(): 
        #载入配置
        companyID = request.args.get('companyID', "")
        companyName = request.args.get('companyName', "") 
        companyInStreet = request.args.get('companyInStreet', "") 
        companyInVillage = request.args.get('companyInVillage', "") 
        companyAdrr = request.args.get('companyAdrr', "") 
        companyScale = request.args.get('companyScale', "") 
        companySpecialcase = request.args.get('companySpecialcase', "") 
        companyManangeclass = request.args.get('companyManangeclass', "") 
        companyContacts = request.args.get('companyContacts', "") 
        companyContacts = request.args.get('companyContacts', "") 
        
        #组装筛选条件
        fliter = ""
        if(companyID != ""): fliter += " && companyID == " + companyID
        if(companyName != ""): fliter += " && companyName %like% " + companyName
        if(companyInStreet != ""): fliter += " && companyInStreet == " + companyInStreet
        if(companyInVillage != ""): fliter += " && companyInVillage == " + companyInVillage
        if(companyAdrr != ""): fliter += " && companyAdrr == " + companyAdrr
        if(companyScale != ""): fliter += " && companyScale == " + companyScale
        if(companySpecialcase != ""): fliter += " && companySpecialcase == " + companySpecialcase
        if(companyManangeclass != ""): fliter += " && companyManangeclass == " + companyManangeclass
        if(companyContacts != ""): fliter += " && companyContacts == " + companyContacts
        if(fliter != ""): fliter = fliter[4:]
        
        #筛选
        res = {"success": 1, "data": "", "msg": ""}
        try:
            dbCompany = gol._Get_Value('dbCompany_fb')
            totalCount, pCompanys = dbCompany.getCompanys(param = fliter, isDel = False, page = 1, per_page = 99999999)
            if(totalCount == 0): 
                res['success'] = 0
                res['msg'] = str(err)
                return myData_Json.Trans_ToJson_str(res)

            #保存属性信息
            nameUUID = myIO.create_UUID()
            dirTemp =  myIO.checkPath(appWeb.baseDir + "static/data/temp/temp_" + nameUUID + "/")
            myIO.mkdir(dirTemp, True, True)
            nameFile = "企业信息数据表"
            if(totalCount == 1): nameFile = pCompanys[0]['companyName']
            nameFile = nameFile + "_" + nameUUID
            dbCompany.Save_as_csv(dirTemp + nameFile + ".csv", pCompanys, True)

            #保存相关图片
            files = []; newfiles = [];
            imgSrcdir =  appWeb.baseDir
            dictImgs = { "imgName_1" : "图片_相关部门证明",
                        "imgName_2" : "图片_正门照片",
                        "imgName_3" : "图片_生产车间照片",
                        "imgName_4" : "图片_营业执照注销",
                        "imgName_5" : "图片_断水断电证明",
                        "imgName_6" : "图片_执法笔录",
                }
            for x in pCompanys:
                #文件夹保存图片
                dirCompany = dirTemp + x['companyName'] + "/"
                for name in dictImgs:
                    nameImg = dictImgs[name].replace("图片_", "")
                    filesImg = x[name].split(';')
                    targetDir = dirCompany + nameImg

                    # 拷贝文件到文件夹
                    ind = 0
                    for xx in filesImg:
                        ind += 1
                        if(xx == ''): continue;
                        pathDest = myIO.copyFile(imgSrcdir + xx, targetDir, nameImg + "_" + str(ind))
                        files.append(pathDest)
                        newfiles.append(pathDest.replace(dirTemp, ""))
            files.append(dirTemp + nameFile+ ".csv")
            newfiles.append(nameFile + ".csv")
            
            #压缩文件
            zip_name = nameFile 
            zip_path = appWeb.baseDir + "static/data/Companys/"
            
            #if(myIO.Save_Files_zip(files, newfiles, zip_path, zip_name)):
            if(myIO.Save_Floders_zip(dirTemp, zip_path, zip_name)):
                res['filename'] = zip_name + '.zip'
                res['filefloder'] = "Companys"
                res['totalCount'] = totalCount
            else:
                res['success'] = 0
                res['msg'] = str(err)
            myIO.deldir(dirTemp)
        except Exception as err:
            res['success'] = 0
            res['msg'] = str(err)
        return myData_Json.Trans_ToJson_str(res)


add_Webs(appWeb, dirBase)