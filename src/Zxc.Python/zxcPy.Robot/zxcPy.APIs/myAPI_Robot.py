# -*- coding: utf-8 -*-
"""
Created on  张斌 2018-07-04 15:58:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com

    Rest API --平台注册
"""
import os, copy  
import mySystem 
    
#引用根目录类文件夹--必须，否则非本地目录起动时无法找到自定义类
mySystem.Append_Us("", False)    
import myWeb
from myGlobal import gol   



#API-平台注册
class myAPI_Robot_RegistPlant(myWeb.myAPI): 
    def get(self, usrName, usrID, plantName):
        pMsg = copy.deepcopy(gol._Get_Setting('Return_strFormat', {}))
        if(plantName == ""): return pMsg
        
        #提取平台集 
        pRoot = gol._Get_Value('rootRobot')
        pPlants = pRoot.usrPlants
        pPlant = pPlants.Find(plantName)
        if(pPlant == None):
            pPlant = pPlants.Regist(usrName, usrID, plantName)
        
        pMsg['result'] = True
        pMsg['toke'] = pPlant.usrToken
        return pMsg


#集中添加所有API
def add_APIs(pWeb):     
    # 创建Web 
    pWeb.add_API(myAPI_Robot_RegistPlant, '/regist/plant/<usrName>/<usrID>/<plantName>')
    


#主程序启动
if __name__ == '__main__': 
    mySystem.Append_Us("../zxcPy.Robot/Roots", True, __file__)
    import myRoot

    #测试
    namePlant = "wx"
    token = ""

    #注册平台, 取token
    pReg = myAPI_Robot_RegistPlant()
    token = pReg.get("myTest", "@zxcv", "wx")
    print(token)