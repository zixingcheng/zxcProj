 # -*- coding: utf-8 -*-
"""
Created on  张斌 2020-06-08 10:58:00 
    @author: zhang bin
    @email:  zhangbin@qq.com

    pyWeb_API --大气扩散模型-WebAPI
""" 
import sys, os, mySystem

#导入模块
from flask import Flask, Response, jsonify, request                     #导入模块
from flask_restful import reqparse, Api, Resource

mySystem.Append_Us("../zxcPy_WebAPI", False, __file__)
mySystem.Append_Us("", False)  
import myIO, myData, myData_Json, myData_Trans, myWeb
from zxcPy_WebAPI import *
import zxcPy_WebAPI.myModel

 
#模型-大气扩散WebAPI
class myAPI_Model_Atmospheric_Diffusion(myWeb.myAPI):
    def get(self, param):
        # 模型调用
        pModel = zxcPy_WebAPI.myModel.myModel_Atmospheric_Diffusion()

        # 模型参数初始 
        pModel.initParam_str(param)
        
        # 模型运行 
        pModel.runModel()
        
        # 模型结果返回 
        strReturn = pModel.getResult()
        return strReturn

