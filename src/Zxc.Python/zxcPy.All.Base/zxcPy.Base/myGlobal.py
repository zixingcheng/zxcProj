# -*- coding: utf-8 -*-
"""
Created on  张斌 2018-04-22 20:05:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com

    全局变量
""" 

#全局变量
class gol():    
    _gs_Inited = False              #加载标识
    def _Init(bPrint = False):      #初始化
        if(gol._gs_Inited == False):
            if(bPrint):
                print("->>", "初始：全局变量")  
            global _global_dict
            gol._gs_Inited = True
            _global_dict = {}
        
            #全局消息
            _global_dict["golMsgs"] = {}

            #全局设置
            _ms_Setting = {}
            _ms_Setting["CanPrint"] = True
            _ms_Setting["CanPrint_Debug"] = True
            _ms_Setting["CanPrint_Warnning"] = True
            _ms_Setting["CanPrint_Error"] = True
            _ms_Setting["Debug_Depth"] = 0
            _ms_Setting["Return_strFormat"] = {'result': False, 'code': 0,'err': "", 'text': ""}
            _global_dict["golSetting"] = _ms_Setting
            
            if(bPrint):
                print("->>", "\t--已初始全局变量\r\n")  

    def _Set_Value(key, value, cover = False):
        """ 定义一个全局变量 """
        if(cover == False):
            if(_global_dict.get(key, None) == None):
                _global_dict[key] = value
        else:
            _global_dict[key] = value
    def _Get_Value(key, defValue = None):
        """ 获得一个全局变量,不存在则返回默认值 """
        return _global_dict.get(key, defValue)

    #全局设置
    def _Set_Setting(key, value, cover = True):
        dictSet = _global_dict["golSetting"]
        if(cover == False):
            if(dictSet.get(key, None) == None):
                dictSet[key] = value
        else:
            dictSet[key] = value
    def _Get_Setting(key, defValue = None):
        return _global_dict["golSetting"].get(key, defValue)


from myGlobal import gol   
if __name__ == '__main__':   
    gol._Init()#先必须在主模块初始化（只在Main模块需要一次即可）

    #定义跨模块全局变量
    gol._Set_Value('CODE','UTF-8')
    gol._Set_Value('PORT',80)
    gol._Set_Value('HOST','127.0.0.1') 

    print(gol._Get_Value('PORT'))