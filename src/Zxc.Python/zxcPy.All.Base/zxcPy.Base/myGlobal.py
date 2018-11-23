# -*- coding: utf-8 -*-
"""
Created on  张斌 2018-04-22 20:05:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com

    全局变量
""" 
import sys, os, codecs, mySystem 
import myIO 


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
    def _Close(bPrint = False):     #关闭，清空部分特殊对象
       pMMsg = gol._Get_Setting('manageMsgs', None)
       if(pMMsg != None):
           pMMsg._Close()

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
    
    
    #检查脚本是否已经运行（运行生成lock文件）
    def _Run_Lock(_path_): 
        # 提取脚本路径
        strName = myIO.getFileName(_path_)
        strPath = os.path.split(os.path.realpath(_path_))[0] + "/" + strName + ".lock"

        isDone = True
        if(os.path.exists(strPath)):
            # 尝试删除，如果删除失败则运行中
            try:
                os.remove(strPath)
            except :
                isDone = False  
        isDone = not os.path.exists(strPath)

        #创建锁定
        if(isDone):
            lockfile = codecs.open(strPath, 'w+', 'utf-8')
            gol._Set_Setting(strPath, lockfile)
            #pFile.close()      #不关闭保持独占
        else:
            print("脚本已启动! --" + strPath)
            gol._Close()
        return isDone
    def _Run_UnLock(_path_): 
        # 提取脚本路径
        strName = myIO.getFileName(_path_)
        strPath = os.path.split(os.path.realpath(_path_))[0] + "/" + strName + ".lock"

        #文件删除
        isDone = True 
        lockfile = gol._Get_Setting(strPath, None)
        if(lockfile != None):
            try:
                lockfile.close()      #关闭独占
                os.remove(strPath)
            except :
                isLock = False
        isLock = not os.path.exists(strPath) 
        return isLock


from myGlobal import gol   
if __name__ == '__main__':   
    gol._Init()#先必须在主模块初始化（只在Main模块需要一次即可）

    #定义跨模块全局变量
    gol._Set_Value('CODE','UTF-8')
    gol._Set_Value('PORT',80)
    gol._Set_Value('HOST','127.0.0.1') 

    print(gol._Get_Value('PORT'))