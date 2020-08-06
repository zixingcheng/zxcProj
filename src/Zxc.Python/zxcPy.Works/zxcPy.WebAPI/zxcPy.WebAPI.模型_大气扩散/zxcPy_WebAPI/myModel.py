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
        self.modelResult = {"success": 1, "data": {}, "msg": "", "err": ""}
        pass

# 模型-大气扩散
class myModel_Atmospheric_Diffusion(myModel_Base):
    def __init__(self):
        super().__init__()
        self.modelName = "Atmospheric_Diffusion"  
        self.modelName_Alias = "大气扩散模型" 
        self.modelType = "webAPI"          
        self.modelResult = ""       
        self.modeRunning = False

        self.wind = myModel_Object.myObj_Wind()
        self.air = myModel_Object.myObj_Air()
        self.sun = myModel_Object.myObj_Sun()
        self.longitude_Leak = 0
        self.latitude_Leak = 0
        self.height_Leak = 0
        self.massrate_Leak = 0
        self.infoTargets = []
        self.dtLeak = myData_Trans.Tran_ToDatetime("")
        self.hasChimney = False
        self.hasLog = True
     
    # 初始参数信息-dict参数串
    def initParam(self, param):
        errLst = []
        self.modeState = -1
        if(True):
            self.tag = param.get('tag', "")
            dictInfo_Leak = param.get("infoLeak")
            self.longitude_Leak = dictInfo_Leak.get('longitude', "")
            self.latitude_Leak = dictInfo_Leak.get('latitude', "")
            self.height_Leak = dictInfo_Leak.get('height_leak', "")
            self.massrate_Leak = dictInfo_Leak.get('massrate_leak', "")
            self.dtLeak = myData_Trans.Tran_ToDatetime(dictInfo_Leak.get('timestart_leak', ""))
            
            dictInfo_Chimney = dictInfo_Leak.get("chimney", '')
            self.hasChimney = dictInfo_Chimney != ""
            if(self.hasChimney):
                self.chimney_diameter = dictInfo_Chimney.get('diameter', "")
                self.chimney_temperature_outlet = dictInfo_Chimney.get('temperature_outlet', "")
                self.chimney_smoke_speed_outlet = dictInfo_Chimney.get('smoke_speed_outlet', "")
                self.chimney_wind_speed_outlet = dictInfo_Chimney.get('wind_speed_outlet', "")

                if(self.chimney_diameter == ""): errLst.append('diameter') 
                if(self.chimney_temperature_outlet == ""): errLst.append('temperature_outlet') 
                if(self.chimney_smoke_speed_outlet == ""): errLst.append('smoke_speed_outlet') 
                
            if(self.longitude_Leak == ""): errLst.append('longitude') 
            if(self.latitude_Leak == ""): errLst.append('latitude') 
            if(self.height_Leak == ""): errLst.append('height_leak') 
            if(self.massrate_Leak == ""): errLst.append('massrate_leak') 
        
            self.infoTargets = []
            dictInfo_Targets = param.get("infoTarget")
            for x in dictInfo_Targets:
                id_Target = x.get('id', "")
                longitude_Target = x.get('longitude', "")
                latitude_Target = x.get('latitude', "")
                height_Target = x.get('height', "")
                self.infoTargets.append([id_Target, longitude_Target, latitude_Target, height_Target])
                
                if(id_Target == ""): errLst.append('id') 
                if(longitude_Target == ""): errLst.append('longitude') 
                if(latitude_Target == ""): errLst.append('latitude') 
                if(height_Target == ""): errLst.append('height') 

            dictInfo_Evn = param.get("infoEnvironment")
            wind_speed = dictInfo_Evn.get('wind_speed', "")
            wind_direction = dictInfo_Evn.get('wind_direction', "")
            wind_height = dictInfo_Evn.get('wind_height', "")
            air_Stability = dictInfo_Evn.get('air_stability', "")
            temperature = dictInfo_Evn.get('temperature', "")
            cloudy_is = dictInfo_Evn.get('cloudy_is', "")

            if(wind_speed == ""): errLst.append('wind_speed') 
            if(wind_direction == ""): errLst.append('wind_direction') 
            if(wind_height == ""): errLst.append('wind_height') 
            if(temperature == ""): errLst.append('temperature') 
            if(cloudy_is == ""): errLst.append('cloudy_is') 
        
        #参数检查
        if(len(errLst) > 0):
            return False
        
        #初始环境对象
        self.wind.initWind(wind_direction, wind_speed, wind_height, self.dtLeak, -1)
        self.sun.initSun_Infos(self.longitude_Leak, self.latitude_Leak, self.dtLeak, myData.iif(cloudy_is, "多云", ""))
        self.air.initAir_Stability(air_Stability, self.wind.wind_Speed, self.sun.level_Radiation, temperature)
        
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
        if(self.modeRunning): return False
        self.modeRunning = True
        try:
            self.modeState = 1
            self._Create_Result()
            self.modelResult['data']['tag'] = self.tag
            self.modelResult['data']['concentration_unit'] = "mg/m3"
            self.modelResult['data']['results'] = []

            # 参数提取
            Q = self.massrate_Leak
            u = self.wind.getWind_Speed(self.height_Leak, self.air)
            H = self.height_Leak
            H_delta = self._getH_delta()
            H += H_delta
            
            # 循环计算所有目标点
            for x in self.infoTargets:
                id = x[0]
                longitude_Target = myData_Trans.To_Float(str(x[1]))
                latitude_Target = myData_Trans.To_Float(str(x[2]))
                z = myData_Trans.To_Float(str(x[3]))
                
                # 坐标系调整
                deltaX = (longitude_Target - self.longitude_Leak) * 111000 * math.cos(math.radians(self.latitude_Leak))
                deltaY = (latitude_Target - self.latitude_Leak) * 111000

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
                
                # 组装返回结果
                res = {"id": id, "concentration": Cxyz}
                self.modelResult['data']['results'].append(res)
                self._log(id, longitude_Target, latitude_Target, z, Cxyz, deltaXY, deltaX, deltaY)
            self.modeState = 2
        except Exception as err:
            self.modeState = -2
            self.modelResult['err'] = str(err)
            self._log(id, longitude_Target, latitude_Target, z, u, -1, deltaXY, deltaX, deltaY)
        finally:
            self.modeRunning = False
            self.modelResult['success'] = myData.iif(self.modeState == 2, 1, 0)
            return self.modeState == 2

    # 模型运行--测试用
    def _getCxyz(self):
        try: 
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
            self.modelResult['data']['concentration'] = Cxyz
            self.modelResult['data']['concentration_unit'] = "mg/m3"
            print(self.modeState, str(Cxyz))
        except Exception as err:
            self.modeState = -2
            self.modelResult['err'] = str(err)
        finally:
            self.modeRunning = False
            self.modelResult['success'] = myData.iif(self.modeState == 2, 1, 0)
            self.modelResult['data']['tag'] = self.tag
            return self.modeState == 2
    # 计算烟气抬升高度
    def _getH_delta(self):
        if(self.hasChimney == False): return 0
        
        # 参数提取
        T0 = self.air.temperature
        T1 = myData_Trans.To_Float(str(self.chimney_temperature_outlet))
        Vs = myData_Trans.To_Float(str(self.chimney_smoke_speed_outlet))
        D = myData_Trans.To_Float(str(self.chimney_diameter))
        U = myData_Trans.To_Float(str(self.chimney_wind_speed_outlet))
        if(self.chimney_wind_speed_outlet == ""):
            U = self.wind.getWind_Speed(self.height_Leak, self.air)
        
        # 计算烟气热释放率，KJ/s
        Pa = 1010
        h = Vs * 1
        r = D / 2
        Qv = math.pi * r * r * h
        T_delta = T1 - T0
        Qh = 0.35 * Pa * Qv * T_delta / (T1 + 273.15)
        
        # 计算烟气抬升高度
        if(Qh >2100 or T_delta > 35):
            Hs = myData.iif(self.height_Leak > 240, 240, self.height_Leak)
            if(Qh >21000):
                H_delta = 1.303 * math.pow(Qh, 1/3) * math.pow(Hs, 2/3) / U
            else:
                H_delta = 0.292 * math.pow(Qh, 3/5) * math.pow(Hs, 2/5) / U
        elif(Qh <2100 and Qh > 1700):
            Hs = myData.iif(self.height_Leak > 240, 240, self.height_Leak)
            H1_delta = 2 * (1.5 * Vs * D + 0.01 * Qh) / U - 0.048 * (Qh - 1700) / U
            H2_delta = 0.292 * math.pow(Qh, 3/5) * math.pow(Hs, 2/5) / U
            H_delta = H1_delta + (H2_delta - H1_delta) * (Qh - 1700) / 400
        elif(Qh < 1700 or T_delta < 35):
            H_delta = 2 * (1.5 * Vs * D + 0.01 * Qh) / U
        return H_delta
    # 记录日志
    def _log(self, id_Target, lon, lat, height, Q, deltaXY, deltaX, deltaY):
        if(self.hasLog == False): return

        #保存数据
        strDir, strName = myIO.getPath_ByFile(__file__)
        strPath =  strDir + "/static/Log"

        headStr = ""
        if(os.path.exists(strPath) == False):
            myIO.mkdir(strPath) 
        strPath =  strPath + "/" + myData_Trans.Tran_ToDatetime_str(None, "%Y-%m-%d") + ".csv"
        if(os.path.exists(strPath) == False):
            headStr = "id_Target, concentration, height, tag, longitude_Leak, latitude_Leak, height_Leak, massrate_Leak, speed, direction, windH, temperature, cloudy_is, chimney_diameter, chimney_temperature_outlet, chimney_temperature_outlet, chimney_wind_speed_outlet, dtTimestr, lon, lat, deltaXY, deltaX, deltaY"
            
        #文件追加数据内容
        with open(strPath, 'a+') as f:
            if(headStr != ""):
                f.write(headStr) 
               
            dtTimestr = myData_Trans.Tran_ToDatetime_str(self.dtLeak)
            if(self.hasChimney):
                infoChimney = F'{self.chimney_diameter},{self.chimney_temperature_outlet},{self.chimney_temperature_outlet},{self.chimney_wind_speed_outlet}'
            else:
                infoChimney = F',,,'
            strLine = F'{id_Target},{Q},{height},{self.tag},{self.longitude_Leak},{self.latitude_Leak},{self.height_Leak},{self.massrate_Leak},{self.wind.wind_Speed},{self.wind.wind_Direction_Alias},{self.wind.wind_Height},{self.air.temperature},{self.sun.numCloud},{infoChimney},{dtTimestr},{lon},{lat},{deltaXY},{deltaX},{deltaY}'
            f.write("\n" + strLine) 
        return True 

    # 模型结果提取
    def getResult(self):
        return myData_Json.Trans_ToJson_str(self.modelResult)
    


if __name__ == '__main__':
    # 模型测试
    pModel = myModel_Atmospheric_Diffusion()

    # 模型参数初始
    param = { "tag": "ADDFSDGDG", 
              "infoLeak": { 
                                "longitude": 113.8, 
                                "latitude": 22.8, 
                                "height_leak": 45,
                                "massrate_leak": 720,
                                "timestart_leak": "2020-06-09 12:00:00",
                                "chimney":{
                                            "diameter": 1,
                                            "temperature_outlet": 100,
                                            "smoke_speed_outlet": 5,
                                            "wind_speed_outlet": ""
                                    }
                           },
              "infoTarget": [{ 
                                "id": "1", 
                                "longitude": 113.83, 
                                "latitude": 22.83, 
                                "height": 0
                           },
                             { 
                                "id": "2", 
                                "longitude": 113.835, 
                                "latitude": 22.835, 
                                "height": 0
                           }],
             "infoEnvironment": {
                                "wind_speed": 2, 
                                "wind_direction": "SW",
                                "wind_height": 10,
                                "air_stability": "C",
                                "temperature": 26,
                                "cloudy_is": True
                                }
            }
    jsonParam = myData_Json.Trans_ToJson_str(param)
    pModel.initParam_str(jsonParam)

    pModel.runModel()
    print(pModel.getResult())


