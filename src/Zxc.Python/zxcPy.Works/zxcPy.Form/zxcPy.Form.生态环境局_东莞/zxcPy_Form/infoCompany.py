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
from wtforms.validators import DataRequired,ValidationError,Email,Regexp,EqualTo,Required,NumberRange,Length
from werkzeug.utils import secure_filename
from wtforms.fields.html5 import DateField

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
    companyContacts = StringField('企业联系人', [DataRequired(),Length(min=2, max=8)], render_kw={"placeholder": "请输入企业联系人", "style": txtStyle})
    companyPhone = StringField('电话号码', validators=[DataRequired(),Regexp("1[3578]\d{9}", message="手机格式不正确")], render_kw={"placeholder": "请输入联系电话", "style": txtStyle})
    
    companyHasProcess  = StringField('是否采用活性炭吸附工艺', [DataRequired()], render_kw={"placeholder": "请选择是否采用活性炭吸附工艺", "style": txtStyle})
    companyNumProcess = IntegerField('活性炭吸附工艺设施套数', [DataRequired(),NumberRange(min=0, max=100)], render_kw={"placeholder": "请输入采用活性炭吸附工艺设施套数", "style": txtStyle})
    companyRecycle = IntegerField('正常更换周期（日/次）', [DataRequired(),NumberRange(min=0, max=365)], render_kw={"placeholder": "请输入更换周期（日/次）", "style": txtStyle})
    companyVolumeTotal = DecimalField('设计总填装量（千克）', [DataRequired(),NumberRange(min=0, max=99999)], render_kw={"placeholder": "请输入设计总填装量（千克）", "style": txtStyle})
    
    companyRedate = DateField('新活性炭更换日期', default='', format='%Y-%m-%d', render_kw={"placeholder": "请选择新活性炭更换日期", "style": txtStyle}) 
    companyRevolume = DecimalField('新活性炭更换量（千克）', [DataRequired(),NumberRange(min=0, max=99999)], render_kw={"placeholder": "请输入新活性炭更换量（千克）", "style": txtStyle})
    companyTransferredvolume = DecimalField('已转移废活性炭量（千克）', [DataRequired(),NumberRange(min=0, max=99999)], render_kw={"placeholder": "请输入已转移废活性炭量（千克）", "style": txtStyle})
    companyNoTransferredvolume = DecimalField('暂未转移废活性炭量（千克）', [DataRequired(),NumberRange(min=0, max=99999)], render_kw={"placeholder": "请输入暂未转移废活性炭量（千克）", "style": txtStyle})
    
    save = SubmitField('保存信息', render_kw={"class": "btn-submit-upload","style": "margin-left:10px"})                    # 保存按钮
    query = SubmitField('查询信息', render_kw={"class": "btn-submit-upload","style": "margin-left:10px display:block;"})    # 查询按钮--隐藏
    
    # 图片信息 
    imgName_1 = StringField('图片_1', [], render_kw={"style": "display:none;"}) 
    imgName_2 = StringField('图片_2', [], render_kw={"style": "display:none;"}) 
    imgName_3 = StringField('图片_3', [], render_kw={"style": "display:none;"}) 
    imgName_4 = StringField('图片_4', [], render_kw={"style": "display:none;"}) 
    imgName_5 = StringField('图片_5', [], render_kw={"style": "display:none;"}) 
    imgName_6 = StringField('图片_6', [], render_kw={"style": "display:none;"}) 

#集中添加所有Web
def add_Webs(appWeb, dirBase):
    #添加接口--查询
    @appWeb.app.route('/zxcAPI/company/query')
    def companyQuery(): 
        #载入配置
        company_id = request.args.get('company_id', "")
        company_name = request.args.get('company_name', "") 
        print(company_id,company_name)

        dbCompany = gol._Get_Value('dbCompany')
        pCompany = dbCompany.getCompany(company_id, company_name).copy()
        if(pCompany == None):
            pCompany = dbCompany.OnCreat_RowInfo();
            pCompany['companyID'] = company_id
            pCompany['companyName'] = company_name

        #修正部分信息
        pCompany['companyHasProcess'] = myData.iif(pCompany['companyHasProcess'], "是", "否")
        if(type(pCompany['companyRedate']) == datetime.datetime):
            pCompany['companyRedate'] = myData_Trans.Tran_ToDatetime_str(pCompany['companyRedate'], "%Y-%m-%d")
        jsonCompany = myData_Json.Json_Object(pCompany)
        return jsonCompany.ToString() 

    # 添加页面--公司活性炭信息登记页面
    @appWeb.app.route('/zxcWebs/companyinfo', methods = ['GET', 'POST'])  
    @appWeb.app.route('/zxcWebs/companyinfo/<string:companyID>', methods = ['GET', 'POST'])    
    def upload_company(companyID = ""):
        form = myCompanyForm()                      #生成form实例，给render_template渲染使用  
        needRefresh = True
        editSucess = False
        if form.validate_on_submit():               #调用form实例里面的validate_on_submit()功能，验证数据是否安全，如是返回True，默认返回False
            if form.save.data:  # 保存按钮被单击 
                # 组装row信息
                pValues = []
                if(True):
                    pValues.append("")
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
                dbCompany = gol._Get_Value('dbCompany')
                if(dbCompany.Add_Row_BySimply(rowInfo, True, True) != ""):
                    editSucess = True
        else:
            # 保存时，验证失败，不需要刷新
            if form.save.data:
                needRefresh = False
        return render_template('company_active carbon.html', title = 'company upload', form = form, companyID = companyID, needRefresh = needRefresh, editSucess = editSucess)



    @appWeb.app.route('/zxcWebs/stock/myTest', methods=['POST', 'GET'])  # 添加路由
    def upload():
        if request.method == 'POST':
            f = request.files['file']
 
            if not (f and allowed_file(f.filename)):
                return jsonify({"error": 1001, "msg": "请检查上传的图片类型，仅限于png、PNG、jpg、JPG、bmp"})
 
            user_input = request.form.get("name")
            basepath = os.path.dirname(__file__)  # 当前文件所在路径
 
            imgPath = dirBase + "/static/images/"
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