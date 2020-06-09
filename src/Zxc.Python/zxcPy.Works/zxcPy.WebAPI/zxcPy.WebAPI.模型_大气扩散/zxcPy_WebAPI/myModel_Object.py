 # -*- coding: utf-8 -*-
"""
Created on  张斌 2020-06-08 10:58:00 
    @author: zhang bin
    @email:  zhangbin@qq.com

    pyModel --模型-对象基类
""" 
import sys, os, math, mySystem

mySystem.Append_Us("", False)  
import myData, myData_Trans



# 参数信息
windLst = ["北","北东北","东北","东东北","东","东东南","东南","南东南","南","南西南","西南","西西南","西","西西北","西北","北西北"]
windLst_en = ["N","NNE","NE","ENE","E","ESE","SE","SSE","S","SSW","SW","WSW","W","WNW","NW","NNW"] 
windRatio_p = [0.15,0.15,0.2,0.25,0.4,0.5,0.07,0.07,0.1,0.15,0.35,0.55]
sunLst_Inclination = [-22,-15,-5,6,17,22,22,17,7,-5,-15,-22,-21,-12,-2,10,19,23,21,14,3,-8,-18,-23,-19,-9,2,13,23,23,19,11,-1,-12,-21,-23]
sunLst_Elevation = [15,35,65,180]
sunLst_Radiation = [-2,-1,-1,1,2,3,0,0,1,1]
cloudLst = ["少云","多云"]
airLst_Stability = ["A","B","C","D","E","F"]
airRatio_Stability = ["A","A","B","D","E","F","A","B","C","D","E","F","B","C","C","D","D","E","C","C","D","D","D","D","C","D","D","D","D","D"]
airRatio_y = [[1000,0.901074,0.425809,-1,0.850934,0.602052],[1000,0.914370,0.281846,-1,0.865014,0.396353],[1000,0.924279,0.177154,-1,0.885157,0.232123],[1000,0.929418,0.110726,-1,0.888723,0.146669],[1000,0.920818,0.0864001,-1,0.896864,0.101947],[1000,0.929418,0.0553634,-1,0.888723,0.0733348]]
airRatio_z = [[300,1.121540,0.0799904,500,1.523600,0.00854771,-1,2.108810,0.000211545],[500,0.964435,0.127190,-1,1.093560,0.0570251],[-1,0.917595,0.106803],[2000,0.826212,0.104634,10000,0.632023,0.400167,-1,0.555360,0.810763],[1000,0.788370,0.0927529,10000,0.565188,0.433384,-1,0.414743,1.73241],[1000,0.784400,0.0620765,10000,0.525969,0.370015,-1,0.322659,2.406910]]



# 对象类-风
class myObj_Wind():
    def __init__(self):
        self.wind_Speed = 0
        self.wind_Direction = 0
        self.wind_Direction2 = 0
        self.wind_Direction_Alias = ""
        self.wind_Height = 0
        self.wind_Tiem_start= myData_Trans.Tran_ToDatetime("")
        self.wind_Tiem_duration = 0

    # 风信息初始
    def initWind(self, direction, speed, higth = 0, startTime = "", duration = -1):
        self.wind_Speed = myData_Trans.To_Float(str(speed))
        self.wind_Direction = self.initWind_Direction(direction)
        self.wind_Direction2 = 90 - self.wind_Direction
        if(self.wind_Direction2 < 0): self.wind_Direction2 += 360
        self.wind_Height = myData_Trans.To_Float(str(higth))
        self.wind_Tiem_start = startTime
        if(type(self.wind_Tiem_start) == str):
            self.wind_Tiem_start = myData_Trans.Tran_ToDatetime(startTime)
        self.wind_Tiem_duration = duration

    # 风信息初始-风向
    def initWind_Direction(self, direction):
        index = -1
        try:
            index = windLst.index(direction)
        except :
            try:
                index = windLst_en.index(direction)
            except :
                pass
        if(index < 0): index = 0
        self.wind_Direction_Alias = windLst[index]
        direction = index * 22.5
        return direction

    # 风信息计算-风速
    def getWind_Speed(self, height, air):
        z1 = myData.iif(self.wind_Height <1 , 1, self.wind_Height)
        p = windRatio_p[air.index]
        u = self.wind_Speed * pow(height / z1, p)
        return u
  
# 对象类-大气
class myObj_Air():
    def __init__(self):
        self.air_Stability = ""
        self.index = 0
        self.ratio_y_a = 0; self.ratio_y_r = 0
        self.ratio_z_a = 0; self.ratio_z_r = 0

    # 大气信息初始-稳定度
    def initAir_Stability(self, stability, speed = 0, levelRadiation = 0):
        if(stability == "" and speed != 0):
            indSpeed = int(speed - 1.9)
            if(indSpeed < 0): indSpeed = 0
            indRadiation = 3 - levelRadiation
            self.air_Stability = airRatio_Stability[indSpeed * 6 + indRadiation]
            self.index = airLst_Stability.index(self.air_Stability)
        else:
            self.air_Stability = ""
            try:
                self.index = airLst_Stability.index(stability)
                self.air_Stability = airLst_Stability[self.index]
            except :
                pass
        
    # 大气信息初始-稳定度
    def initAir_Ratio(self, distance):
        self.ratio_y_a = 0; self.ratio_y_r = 0
        self.ratio_z_a = 0; self.ratio_z_r = 0
        if(self.air_Stability == ""): return False

        ratioYs = airRatio_y[self.index]
        ind = 0
        while(True):
            if(ratioYs[ind] >= distance or ratioYs[ind] < 0):
                self.ratio_y_a = ratioYs[1 + ind]; 
                self.ratio_y_r = ratioYs[2 + ind]
                break;
            ind += 3
        self.ratio_y = self.ratio_y_r * math.pow(distance, self.ratio_y_a)
            
        ratioZs = airRatio_z[self.index]
        ind = 0
        while(True):
            if(ratioZs[ind] >= distance or ratioZs[ind] < 0):
                self.ratio_z_a = ratioZs[1 + ind]; 
                self.ratio_z_r = ratioZs[2 + ind]
                break;
            ind += 3
        self.ratio_z = self.ratio_z_r * math.pow(distance, self.ratio_z_a)
        
# 对象类-太阳
class myObj_Sun():
    def __init__(self):
        self.angle_Inclination = 0
        self.angle_elevation = 0
        self.level_Radiation = 0

    # 太阳信息初始
    def initSun_Infos(self, longitude, latitude, dtTime, numCloud):
        month = dtTime.month
        day = int(dtTime.day / 10)
        theta = sunLst_Inclination[day * 12 + month - 1]
        self.angle_Inclination = theta
        self.angle_elevation = math.asin(math.sin(math.radians(longitude)) 
                                         * math.sin(math.radians(theta)) 
                                         + math.cos(math.radians(longitude)) 
                                         * math.cos(math.radians(theta)) 
                                         * math.cos(math.radians(15 * dtTime.hour + latitude - 300)))
        #radiation level
        isNight = dtTime.hour <= 6 or dtTime.hour >= 18
        indCloud = myData.iif(numCloud == "多云", 1, 0)
        indElevation = 0
        while(True):
            if(self.angle_elevation <= sunLst_Elevation[indElevation]):
                indElevation += 1; break;
        self.level_Radiation = myData.iif(isNight, sunLst_Radiation[indCloud], sunLst_Radiation[indCloud * 4 + indElevation + 2])



if __name__ == '__main__':
    # 测试
    pWind = myObj_Wind()
    pWind.initWind("SE", 1.5)
    print(pWind.wind_Direction)

    pSun = myObj_Sun()
    pSun.initSun_Infos(113.8, 22.8, myData_Trans.Tran_ToDatetime(""), "多云")
    print(pSun.level_Radiation)

    pAir = myObj_Air()
    pAir.initAir_Stability("", pWind.wind_Speed, pSun.level_Radiation)
    pAir.initAir_Ratio(1000)
    print(pAir.air_Stability, pAir.ratio_y_a, pAir.ratio_y_r, pAir.ratio_z_a, pAir.ratio_z_r)
    
    pWind.initWind("SE", 2, 10)
    print(pWind.getWind_Speed(1, pAir))
    print(pWind.getWind_Speed(10, pAir))
    print(pWind.getWind_Speed(45, pAir))