# -*- coding: utf-8 -*-
"""
Created on  张斌 2016-10-16 09:00:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com

    Main函数测试(带参数)，参数格式化提取(参数转参数类)，及错误调试等
"""

import sys
import getopt

import myData_Trans, myData_Json



#自定义错误
class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg



#自定义参数(获取cmd等shell到的参数，并以该类返回便于直接参数调用) 
class Usargv():
    def __init__(self, options = "", long_options = [], argv = None, printDict = False):
        self.basePath = ""
        self.baseArgv = argv
        self.baseOptions = options
        self.basePrintDict = printDict
        self.baseLong_Options = []
        self.baseLong_Options_N = []
        
        #解析长参数
        for opt in long_options:
            strOpt = opt.strip()
            strOptName = strOpt
            if strOpt.count("=") == 1:
                if strOpt[-1:] == "=":
                    strOptName = strOpt[0:-1:]    #有=参数 
                else:
                    continue
            else:
                #无=参数为设置，全部默认为False，参数有设置则更新为True
                self.__dict__[strOptName]  = False

            #记录长参数信息
            self.baseLong_Options.append(strOpt)
            self.baseLong_Options_N.append(strOptName)            
 
        
        #提取参数信息
        self._GetParam(argv)        
    

        
    #提取参数信息
    def _GetParam(self, argv = None):
        if argv is None:
            self.baseArgv = sys.argv
        #print("Usparam Test:")
        #Usage("Err")
        
        try:
            try:                
                #处理命令行参数
                self.basePath = self.baseArgv[0]
                opts, args = getopt.getopt(self.baseArgv[1:], self.baseOptions, self.baseLong_Options)

                #循环提取命令行参数
                for opt, arg in opts:
                    #提取参数名
                    nCount = opt.count("-")
                    bLong = False
                    strName = opt[1:]
                    if(nCount == 2):
                        strName = opt[2:]
                        bLong = True
                         

                    #转换为类属性
                    if(bLong):
                        #判断是否有=好，无的为布尔类型
                        nIndex = self.baseLong_Options_N.index(strName)
                        if(self.baseLong_Options[nIndex] == strName):
                            #名称相同为无=参数
                            self.__dict__[strName]  = True 
                        else:
                            self.__dict__[strName]  = arg 
                    else:
                        self.__dict__[strName]  = arg 

                    if(self.basePrintDict):
                        print (strName) 
                        print (self.__dict__[strName])
                        
                if(self.basePrintDict):
                    print ("Done: Param Loaded.") 
                        
            except (getopt.error):
                strLong = ""
                for opt in self.baseLong_Options:
                    strLong += "--" + opt + " " 
                print ("Err: Param Error \n  you can use param like:") 
                print ("    ***.py " + self.baseOptions + " or " + strLong)
                print ("  for help you can use --help") 
                raise Usage("Err")

        except (Usage):
            print("Err:")
            print(sys.stderr, Usage.msg)
            #print(sys.stderr, "for help use --help")
            return 2


    #提取指定项值
    def _GetParamValue(self, strParam):        
        #判断是否有=好，无的为布尔类型  
        if(strParam in self.__dict__): 
            return self.__dict__[strParam]
        else:
            return ""

    #提取指定项值集,提取多值,单项设置多值方式返回
    def _GetParamValues(self, strParams, default, strSplit = ","):
        #循环提取项
        pValues = []
        nIndex = 0
        for strParam in strParams:
            default_Value = 0
            if(len(default) > nIndex):
                default_Value = default[nIndex] 
            nIndex += 1
            
            #判断是否有=好，无的为布尔类型
            value = ""
            if(strParam in self.__dict__): 
                value = self.__dict__[strParam]

            #解析值集 
            pValues.append(myData_Trans.To_Floats(value, strSplit, default_Value))
            
        return pValues


    #提取指定项值集,提取多值,单项设置多值方式返回
    def _GetParamValues_ByJson(self, strParams, default):
        #循环提取项
        pValues = []
        nIndex = 0
        for strParam in strParams:
            default_Value = 0
            if(len(default) > nIndex):
                default_Value = default[nIndex] 
            nIndex += 1  
            
            #判断是否有=好，无的为布尔类型
            value = ""
            if(strParam in self.__dict__): 
                value = self.__dict__[strParam]                

            #未设置则修正为默认
            if(value == ""):
                value = default_Value
   
            #value解析为Json,直接转换为List
            if(type(value) == str): 
                pJson = myData_Json.Trans_ToJson(value)
                #print(pJson)   
                if(type(pJson)== list):
                    pValues.append(pJson) 
                else:                
                    pValues.append(default_Value)
            else:
                pValues.append(default_Value)
                
        return pValues  



if __name__ == '__main__':
    #main()
    #pArgv = Usargv("",["help","output="])
    pArgv = Usargv("",["prj="])
    print(pArgv._GetParamValue("prj"))
    print(pArgv.basePath)
    

    #直接编译会发生错误，但通过cmd可以正确执行
    #d = int(pArgv.b) * 10
    #print(d)
 
    
    #sys.exit(pArgv)

