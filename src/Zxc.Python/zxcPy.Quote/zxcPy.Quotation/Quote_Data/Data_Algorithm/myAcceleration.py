# -*- coding: utf-8 -*-
"""
Created on  张斌 2018-07-13 14:28:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com

    算法实现，加速度计算 
"""
import sys, os, mySystem 

#引用根目录类文件夹--必须，否则非本地目录起动时无法找到自定义类
mySystem.Append_Us("../../Quote_Data", False, __file__) 
mySystem.Append_Us("", False) 
import myData_Trans, myData_Json


#加速算法类
class myAcceleration():
    def __init__(self, values = [], originData = 0, interval = 60):
        self.values = [0]
        self.datas = values
        self.originData = originData 
        self.originStep = originData / 10;
        self.interval = interval 
        self.Compute();
      
    def Add_Value(self, value):
        self.datas.append()
        self.Compute();
    def Compute(self):
        nInd_S = len(self.values)
        nNum = len(self.datas)
        for x in range(nInd_S, nNum):
            self.values.append(self.Compute_Acceleration(self.datas[x - 1], self.datas[x]))

    #加速度计算        
    def Compute_Acceleration(self, value1, value2):
        #两两计算
        dAcc1 = (value2 - value1) / self.originStep;
        return dAcc1

if __name__ == '__main__':
    pData = myAcceleration([10,10.01,10.05,10.1,10.2,10.4,10.6,10.59,10.58,10.5,10.4,10.5,10.55,10.56,10.6], 10, 1)
    pData.Compute()
    
    dvalue = 0
    for x in pData.values:
        dvalue += x

    print("")
