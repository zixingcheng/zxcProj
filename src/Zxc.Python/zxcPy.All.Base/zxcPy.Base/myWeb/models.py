# -*- coding: utf-8 -*-
"""
Created on  张斌 2018-04-04 11:00:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com

    myWeb, Api接口操作, 基于flask
"""

class Admin(db.Model):
    __tablename= 'admin'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)   # unique代表不能重复，唯一的
    pwd = db.Column(db.String(100), nullable=False)
    is_super = db.Column(db.SmallInteger)                           #是否为超级管理员
    role_id = db.Column(db.Integer,db.ForeignKey('role.id'))
    addtime = db.Column(db.DateTime, index=True, default=datetime.datetime.now)

    adminlogs = db.relationship('Adminlog',backref='admin')
    adminoption = db.relationship('Oplogs', backref='admin')

    def __repr__(self):
        return '<Admin %r>' % self.name

    #定义密码验证函数
    def check_pwd(self,pwd):
        from werkzeug.security import check_password_hash           #由于密码是加密的，所以要引入相应的加密函数
        return  check_password_hash(self.pwd,pwd)