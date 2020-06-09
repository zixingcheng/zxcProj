 # -*- coding: utf-8 -*-
"""
Created on  张斌 2020-06-08 10:58:00 
    @author: zhang bin
    @email:  zhangbin@qq.com

    pyModel --大气扩散模型
""" 
import sys, os, math, mySystem

mySystem.Append_Us("", False)  
import myIO, myData, myData_Json, myData_Trans
import myModel_Object

 
# 模型-基类
class myModel_Base():
    def __init__(self):
        self.modelCode = ""         #模型编码
        self.modelName = ""         #模型名称
        self.modelName_Alias = ""   #模型名称-别名
        self.modelType = ""         #模型分类
        self.modelDesc = ""         #模型描述
        self.modelParam = ""        #模型参数信息
        self.modelResult = ""       #模型结果信息
        self.modeState = -1         #当前模型状态
    
    # 创建模型结果格式信息
    def _Create_Result(self):
        self.modelCode = ""         #模型编码
        self.modelName = ""         #模型名称
        self.modelType = ""         #模型分类
        self.modelDesc = ""         #模型描述
        self.modelParam = ""        #模型参数信息
        self.modelResult = ""       #模型结果信息
        pass

# 模型-大气扩散
class myModel_Atmospheric_Diffusion(myModel_Base):
    def __init__(self):
        super().__init__()
        self.modelName = "Atmospheric_Diffusion"  
        self.modelName_Alias = "大气扩散模型" 
        self.modelType = "webAPI"          
        self.modelResult = ""       

        self.wind = myModel_Object.myObj_Wind()
        self.air = myModel_Object.myObj_Air()
        self.sun = myModel_Object.myObj_Sun()
        self.longitude_Leak = 0
        self.latitude_Leak = 0
        self.height_Leak = 0
        self.longitude_Target = 0
        self.latitude_Target = 0
        self.height_Target = 0
        self.massrate_Leak = 0
        self.dtLeak = myData_Trans.Tran_ToDatetime("")
     
    # 初始参数信息-dict参数串
    def initParam(self, param):
        errLst = []
        self.modeState = -1
        if(True):
            dictInfo_Leak = param.get("infoLeak")
            self.longitude_Leak = dictInfo_Leak.get('longitude', "")
            self.latitude_Leak = dictInfo_Leak.get('latitude', "")
            self.height_Leak = dictInfo_Leak.get('height_leak', "")
            self.massrate_Leak = dictInfo_Leak.get('massrate_leak', "")
            self.dtLeak = myData_Trans.Tran_ToDatetime(dictInfo_Leak.get('timestart_leak', ""))
            
            if(self.longitude_Leak == ""): errLst.append('longitude') 
            if(self.latitude_Leak == ""): errLst.append('latitude') 
            if(self.height_Leak == ""): errLst.append('height_leak') 
            if(self.massrate_Leak == ""): errLst.append('massrate_leak') 
        
            dictInfo_Target = param.get("infoTarget")
            self.longitude_Target = dictInfo_Target.get('longitude', "")
            self.latitude_Target = dictInfo_Target.get('latitude', "")
            self.height_Target = dictInfo_Target.get('height', "")

            if(self.longitude_Target == ""): errLst.append('longitude') 
            if(self.latitude_Target == ""): errLst.append('latitude') 
            if(self.height_Target == ""): errLst.append('height_leak') 

            dictInfo_Evn = param.get("infoEnvironment")
            wind_speed = dictInfo_Evn.get('wind_speed', "")
            wind_direction = dictInfo_Evn.get('wind_direction', "")
            wind_height = dictInfo_Evn.get('wind_height', "")
            air_Stability = dictInfo_Evn.get('air_stability', "")
            cloudy_is = dictInfo_Evn.get('cloudy_is', "")

            if(wind_speed == ""): errLst.append('wind_speed') 
            if(wind_direction == ""): errLst.append('wind_direction') 
            if(wind_height == ""): errLst.append('wind_height') 
            if(cloudy_is == ""): errLst.append('cloudy_is') 
        
        #参数检查
        if(len(errLst) > 0):
            return False
        
        #初始环境对象
        self.wind.initWind(wind_direction, wind_speed, wind_height, self.dtLeak, -1)
        self.sun.initSun_Infos(self.longitude_Leak, self.latitude_Leak, self.dtLeak, myData.iif(cloudy_is, "多云", ""))
        self.air.initAir_Stability(air_Stability, self.wind.wind_Speed, self.sun.level_Radiation)

        #记录参数及标识状态
        self.modelParam = param
        self.modeState = 0
        return True
    # 初始参数信息-json参数串
    def initParam_str(self, param):
        #json参数转换为列表
        dictParam = myData_Json.Trans_ToJson(param)
        return self.initParam(dictParam)
    
    # 模型运行
    def runModel(self):
        self.modeState = 1
        self._Create_Result()

        # 参数提取
        Q = self.massrate_Leak
        u = self.wind.getWind_Speed(self.height_Leak, self.air)
        z = self.height_Target
        H = self.height_Leak
        H_delta = self._getH_delta()
        H += H_delta

        # 坐标系调整
        deltaX = (self.longitude_Target - self.longitude_Leak) * 111000 * math.cos(math.radians(self.latitude_Leak))
        deltaY = (self.latitude_Target - self.latitude_Leak) * 111000

        angle_Target = math.atan2(deltaY, deltaX) / (2 * math.acos(-1)) * 360
        angle_wind = self.wind.wind_Direction2 + 180
        if(angle_wind > 360): angle_wind -= 360
        
        angle = angle_Target - angle_wind
        deltaXY = math.sqrt(deltaX * deltaX + deltaY * deltaY)
        deltaY = math.sin(math.radians(angle)) * deltaXY
        deltaX = math.cos(math.radians(angle)) * deltaXY

        if(deltaX < 0): 
            Cxyz = 0
        else:
            # 高斯方程扩散公式实现
            self.air.initAir_Ratio(deltaX)
            theta_y = self.air.ratio_y; theta_z = self.air.ratio_z
            if(z > 50):
                Cxyz = Q / (2 * math.pi * u * theta_y * theta_z) * math.exp( -deltaY * deltaY / (2 * theta_y * theta_y) + math.pow(z - H, 2) / (2 * theta_z * theta_z))
            else:
                #Cxyz = Q / (math.pi * u * theta_y * theta_z) * math.exp(- math.pow(z - H, 2) / (2 * theta_z * theta_z))
                Cxyz = Q / (2 * math.pi * u * theta_y * theta_z) * math.exp( -deltaY * deltaY / (2 * theta_y * theta_y)) * (math.exp(- math.pow(z - H, 2) / (2 * theta_z * theta_z)) + math.exp(- math.pow(z + H, 2) / (2 * theta_z * theta_z)))
        self.modeState = 2
        print(self.modeState, str(Cxyz))
    # 计算烟气抬升高度
    def _getH_delta(self):
        Pa = 1010
        T0 = 20
        T1 = 100
        Vs = 5
        D = 1
        U = 1.46

        h = Vs * 1
        r = D / 2
        Qv = math.pi * r * r * h

        T_delta = T1 - T0
        Qh = 0.35 * Pa * Qv * T_delta / (T1 + 273.15)

        if(Qh < 1700):
            H_delta = 2 * (1.5 * Vs * D + 0.01 * Qh) / U
        return H_delta

    # 模型结果提取
    def getResult(self):
        pass
    


if __name__ == '__main__':
    # 模型测试
    pModel = myModel_Atmospheric_Diffusion()

    # 模型参数初始
    param = { "infoLeak": { 
                                "longitude": 113.8, 
                                "latitude": 22.8, 
                                "height_leak": 45,
                                "massrate_leak": 720,
                                "timestart_leak": "2020-06-09 12:00:00"
                           },
              "infoTarget": { 
                                "longitude": 113.83, 
                                "latitude": 22.83, 
                                "height": 0
                           },
             "infoEnvironment": {
                                "wind_speed": 2, 
                                "wind_direction": "SW",
                                "wind_height": 10,
                                "air_stability": "C",
                                "cloudy_is": True
                                }
            }
    jsonParam = myData_Json.Trans_ToJson_str(param)
    pModel.initParam_str(jsonParam)

    pModel.runModel()
    print(pModel.getResult())


