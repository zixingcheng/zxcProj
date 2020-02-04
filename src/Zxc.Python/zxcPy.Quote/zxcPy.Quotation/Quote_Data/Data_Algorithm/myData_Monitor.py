# -*- coding: utf-8 -*-
"""
Created on  张斌 2018-07-13 14:28:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com

    数据监测类，分析拐点与方向等
"""
import sys, os, mySystem 

#引用根目录类文件夹--必须，否则非本地目录起动时无法找到自定义类
mySystem.Append_Us("../../Quote_Data", False, __file__) 
mySystem.Append_Us("", False) 


# 自定义数据监测类
class myData_Monitor():
    def __init__(self, name, saveData=True, valueDelta=0.0025, valueMax=0, valueMin=0, valueLast=0, valueBase=0):
        self.functionDict = {}          # 缓存外部装饰函数，用于回调
        self.saveData = saveData
        self.dataNum = 0
        self.datas = []
        self.datasMonitor = []
        self.msgList = []
        self.state = 0

        self.valueDelta = valueDelta
        self.valueBase = valueBase; self.valueLast = valueLast
        self.valueMax = valueMax; self.valueMax_last = valueMax
        self.valueMin = valueMin; self.valueMin_last = valueMin
        self.valueIndexs = [0] * 5      # 依次：valueLast、valueMax_last、valueMin_last、valueMax、valueMin
        
    # 消息装饰函数，用于传递外部重写方法，便于后续调用      
    def msg_register(self, monitorType = ["RAISE", "FALL", "BREAK"]):
        def _msg_register(fn): 
            # 按消息类型记录
            for _monitorType in monitorType:
                self.functionDict[_monitorType] = fn 
            return fn
        return _msg_register
    # 回调装饰函数，封装触发消息，并回调
    def configured_reply(self, monitorType):
        # 提取触发消息
        msg = self.get_msg()

        # 提取消息类型对应的装饰函数
        replyFn = self.functionDict.get(msg['Type'], None)
        if(replyFn != None):
            try:
                r = replyFn(msg) 
            except:
                pass 
            
    # 提取最新一条返回信息                
    def get_msg(self):
        if(len(self.msgList) > 0):
            msg = self.msgList[0].copy()
            self.msgList.pop(0)
        return msg
    # 添加新数据
    def add_data(self, dataValue, step = 1):
        # 多步长转为单步处理
        if(step > 1 and self.dataNum > 0):
            value = self.datas[self.dataNum -1]
            for x in range(0, step):
                self.add_data(value)

        # 分析处理数据
        if(step == 1):
            if(self.saveData): self.datas.append(dataValue)    # 缓存
            self.dataNum += 1
            self.handle_data(dataValue)
            
            # 更新最大最小值等缓存信息
            self.updata_buffer(dataValue, True)
    # 更新最大最小值等缓存信息
    def updata_buffer(self, dataValue, hasLast_old=False):
            if(hasLast_old):
                self.valueLast_old = dataValue;  self.valueIndexs[0] = self.dataNum - 1
            if(self.valueMax_last < dataValue): 
                self.valueMax_last = dataValue; self.valueIndexs[1] = self.dataNum - 1
                if(self.valueMax < dataValue): 
                    self.valueMax = dataValue; self.valueIndexs[3] = self.dataNum - 1
                    
            if(self.valueMin_last > dataValue): 
                self.valueMin_last = dataValue; self.valueIndexs[2] = self.dataNum - 1
                if(self.valueMax_last < dataValue): 
                    self.valueMax_last = dataValue; self.valueIndexs[4] = self.dataNum - 1

    # 处理新数据，分为增大、减小、拐点
    def handle_data(self, dataValue, recursion = False):
        # 数据初始
        if(self.dataNum == 1):
            if(self.valueMax_last == 0): self.valueMax_last = dataValue
            if(self.valueMin_last == 0): self.valueMin_last = dataValue
            if(self.valueBase == 0): self.valueBase = dataValue
            if(self.valueLast == 0): self.valueLast = self.valueBase
            self.valueLast_old = self.valueLast

        # 数值变动幅度区间超限
        monitorType = ""; hitLimit = False; valueLast = dataValue
        ratio = (dataValue - self.valueLast) / self.valueBase
        if(ratio * self.state >= 0):             # 同方向，超限触发超限点及该值
            if(ratio > 0):      # 上升
                monitorType = "RAISE"; self.state = 1
            elif(ratio< 0):     # 下降
                monitorType = "FALL";  self.state = -1
                
            # 超限跨区间限制处理
            if(abs(ratio) > self.valueDelta):
                valueLast = self.valueLast + self.valueBase * self.valueDelta * self.state
                hitLimit = True; ratio = self.valueDelta; self.valueLast = valueLast            
                self.updata_buffer(valueLast)   # 更新最大最小值等缓存信息
            elif(recursion == False):           # 未超限不触发
                monitorType = ""
        else:
            # 拐点判断(反向超限3/4即为拐点)
            valueLimit = self.iif(self.state > 0, self.valueMax_last, self.valueMin_last)
            ratioLimit = (dataValue - valueLimit) / self.valueBase * (4 / 3)        #放大4/3倍，对应阈值的3/4
            if(abs(ratioLimit) > self.valueDelta):
                monitorType = "BREAK"; hitLimit = True; self.state = - self.state; 
                valueLast = valueLimit; self.valueLast = valueLast
                ratio = (valueLimit - self.valueLast) / self.valueBase

                # 上一个最大最小值同步拐点值，同步后续计算
                if(self.state > 0): 
                    self.valueMax_last = self.valueMin_last; self.valueIndexs[1] = self.dataNum - 1
                else:
                    self.valueMin_last = self.valueMax_last; self.valueIndexs[2] = self.dataNum - 1

        # 组装消息
        if(monitorType != ""):
            index = self.dataNum - 2 + (valueLast - self.valueLast_old)/(dataValue - self.valueLast_old)
            if(monitorType == "BREAK"): 
                index = self.iif(self.state < 0, self.valueIndexs[1], self.valueIndexs[2])
            msg = {"Index": index, "Type": monitorType, "codeState": self.state, "hitLimit": hitLimit, "Value":  valueLast, "Ratio":  ratio}
            self.msgList.append(msg)
            self.datasMonitor.append([index, valueLast, monitorType, self.state, hitLimit])

            # 调用装饰函数
            self.configured_reply(monitorType)

            # 拐点处理
            if(hitLimit): self.handle_data(dataValue, True)
    
    #三元运算
    def iif(self, condition, true_part, false_part):  
        return (condition and [true_part] or [false_part])[0]


if __name__ == '__main__':
    #pMonitor = myData_Monitor("Test",valueLast=10, valueBase=10, valueDelta=0.01)
    pMonitor = myData_Monitor("Test",valueLast=37.31, valueBase=37.31, valueDelta=0.0025)

    @pMonitor.msg_register(["RAISE", "FALL", "BREAK"])
    def Reply_Raise(msg): 
        print(msg)

    datas1 =[36.01, 35.72, 36.55, 36.06, 36.04, 36.12, 36.12, 36.01, 35.8, 35.76, 36.0, 36.19, 36.13, 36.07, 35.98, 35.9, 36.01, 36.08, 36.16, 36.3, 36.41, 36.35, 36.28, 36.2, 36.12, 36.09, 36.05, 36.07, 36.1, 36.15, 36.27, 36.2, 36.15, 36.14, 36.13, 36.18, 36.22, 36.19, 36.16, 36.08, 36.06, 36.03, 36.07, 36.08, 36.11, 36.08, 36.08, 36.06, 36.0, 35.95, 35.91, 35.92, 36.01, 36.03, 36.04, 36.04, 36.03, 36.02, 36.01, 35.95, 35.95, 35.97, 36.02, 36.02, 36.01, 36.02, 36.02, 36.02, 36.06, 36.07, 36.15, 36.25, 36.32, 36.27, 36.23, 36.21, 36.2, 36.1, 36.03, 36.06, 36.09, 36.17, 36.28, 36.33, 36.31, 36.28, 36.23, 36.29, 36.27, 36.24, 36.2, 36.12, 36.14, 36.13, 36.16, 36.22, 36.28, 36.3, 36.4, 36.37, 36.47, 36.57, 36.68, 36.82, 36.76, 36.61, 36.6, 36.71, 36.84, 36.84, 36.79, 36.73, 36.73, 36.79, 36.83, 36.81, 36.83, 36.81, 36.77, 36.8, 36.86, 36.87, 36.98, 37.06, 37.2, 37.14, 37.03, 36.95, 36.94, 37.0, 37.03, 37.0, 36.98, 37.0, 37.01, 37.02, 37.09, 37.12, 37.21, 37.3, 37.33, 37.4, 37.48, 37.54, 37.32, 37.29, 37.21, 37.13, 37.12, 37.14, 37.14, 37.15, 37.18, 37.17, 37.11, 37.05, 37.01, 36.95, 37.02, 37.05, 37.1, 37.18, 37.17, 37.1, 37.1, 37.08, 37.01, 36.97, 36.96, 36.93, 36.8, 36.82, 36.84, 36.9, 36.91, 36.92, 36.92, 36.91, 36.88, 36.83, 36.83, 36.85, 36.92, 36.97, 37.06, 37.1, 37.13, 37.11, 37.06, 36.97, 37.0, 37.03, 37.04, 37.0, 36.94, 36.88, 36.88, 36.9, 36.94, 36.94, 36.9, 36.87, 36.86, 36.81, 36.76, 36.7, 36.68, 36.7, 36.75, 36.81, 36.83, 36.79, 36.75, 36.73, 36.76, 36.79, 36.8, 36.84, 36.85, 36.85, 36.84, 36.81, 36.72, 36.7, 36.7, 36.69, 36.69, 36.65, 36.57, 36.56, 36.59, 36.7, 36.78, 36.78, 36.63, 36.67, 36.71, 36.71, 36.71]
    datas2 = [10.09, 10.1, 10.13, 10.35, 10.46, 10.20, 9.8, 9.99, 9.86, 10.3, 10.6, 10.99]
    for x in datas1:
        pMonitor.add_data(x)
        
    import myChat
    #plt= myChat.draw_Curve(datas2, xlabel="Time(s)", ylabel="Price($)", title="Test Datas", x_major = 1, y_major = 1)
    plt= myChat.draw_Curve(datas1, xlabel="Time(s)", ylabel="Price($)", title="Test Datas", x_major = 30, y_major = 0.2)
    for x in pMonitor.datasMonitor:
        if(x[4]):
            plt.plot(x[0], x[1], 'om')                                  # 绘制紫红色的圆形的点
            pass
        else:
            plt.plot(x[0], x[1], 'bo')                                  # 绘制紫蓝色的圆形的点
            pass

        if x[2] == "RAISE":
            #plt.quiver(x[0], x[1] - 0.5, 0, 0.2, color='r', width=0.004)  # 绘制箭头
            pass
        elif x[2] == "FALL":
            #plt.quiver(x[0], x[1] + 0.5, 0, -1, color='g', width=0.004) # 绘制箭头
            pass
        elif x[2] == "BREAK":
            if x[3] > 0:
                plt.plot(x[0], x[1], c='r', marker='^' ,markersize=12.)  # 绘制上拐点
                pass
            else:
                plt.plot(x[0], x[1], c='g', marker='v', markersize=12.)  # 绘制下拐点
                pass

    plt.show()
    print("")
