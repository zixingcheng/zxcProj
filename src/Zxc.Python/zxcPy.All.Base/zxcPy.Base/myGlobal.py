# -*- coding: utf-8 -*-
"""
Created on  张斌 2018-04-22 20:05:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com

    全局变量
"""


#全局变量
class gol():    
    _gs_Inited = False  #加载标识
    def _Init():        #初始化
        if(gol._gs_Inited == False):
            global _global_dict
            _global_dict = {}
            gol._gs_Inited = True
        
            _global_dict["ms_Msgs"] = {}
            print("初始：全局变量")

    def _Set_Value(key, value):
        """ 定义一个全局变量 """
        _global_dict[key] = value
    def _Get_Value(key, defValue = None):
        """ 获得一个全局变量,不存在则返回默认值 """
        try:
            return _global_dict[key]
        except KeyError:
            return defValue


from myGlobal import gol   
if __name__ == '__main__':   
    gol._Init()#先必须在主模块初始化（只在Main模块需要一次即可）

    #定义跨模块全局变量
    gol._Set_Value('CODE','UTF-8')
    gol._Set_Value('PORT',80)
    gol._Set_Value('HOST','127.0.0.1') 

    print(gol._Get_Value('PORT'))