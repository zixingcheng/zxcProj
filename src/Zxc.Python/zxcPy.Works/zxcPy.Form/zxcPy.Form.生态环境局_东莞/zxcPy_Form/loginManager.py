 # -*- coding: utf-8 -*-
"""
Created on  张斌 2020-11-30 20:20:00 
    @author: zhang bin
    @email:  zhangbin@qq.com

    pyWeb --用户登录管理类
""" 
import sys, os, time, datetime, string, mySystem  
from datetime import timedelta

#导入模块
from flask_login import UserMixin                               #引入用户基类
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

mySystem.Append_Us("", False)  
import myIO, myWeb
from zxcPy_Form import * 
 

#User接口类 
class myWeb_LoginUser(myWeb.myWeb_LoginUser):
    # 用户类 
    def __init__(self, user):
        super().__init__(user)
    
    # 根据用户ID获取用户实体，为 login_user 方法提供支持
    @staticmethod
    def queryUser(user_name):
        if not user_name:
            return None

        # 组装查询条件
        strFilter = F"Isitavailable==1 && ( Username='{user_name}' || Userid='{user_name}')"
            
        # 查询数据
        dataDB = gol._Get_Value('dbCompany_fb')
        values = dataDB.Query(strFilter, "", True, "UserInfoCompany")
        if(len(values) == 1):
            return myWeb_LoginUser({
                    "Userid": values[0]["Userid"],
                    "Username": values[0]["Username"],
                    "Userpwd": values[0]["Userpwd"]
                })
        return None

    def is_authenticated(self):
        return True
    def is_active(self):
        return True
    def is_anonymous(self):
        return False
    def get_id(self):
        return self.userid

