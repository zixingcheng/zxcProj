# -*- coding: utf-8 -*-
"""
Created on  张斌 2020-02-25 14:28:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com

    数据监测类，风险策略分析
"""
import sys, os, mySystem 
import myData_Monitor

#引用根目录类文件夹--必须，否则非本地目录起动时无法找到自定义类
mySystem.Append_Us("../../Quote_Data", False, __file__) 
mySystem.Append_Us("", False) 


# 自定义数据监测类--风险策略
class myData_Monitor_Risk(myData_Monitor.myData_Monitor):
    def __init__(self, name, saveData=True, valueDelta=0.0025, valueMax=0, valueMin=0, valueLast=0, valueBase=0, riskSets = {}):
        super().__init__(name, saveData, valueDelta, valueMax, valueMin, valueLast, valueBase)
        self.init_riskSets(riskSets)
    # 初始风险策略参数
    def init_riskSets(self, riskSets = {}):
        self.stopProfit_Dynamic = riskSets.get("stopProfit_Dynamic", True)          #动态止盈
        self.stopProfit = riskSets.get("stopProfit", 0.06)                          #止盈线，默认为6%
        self.stopProfit_Retreat = riskSets.get("stopLoss_Retreat", 0.01)            #止盈回撤，默认为1%
        self.stopProfit_goon = riskSets.get("stopProfit_goon", False)               #是否止盈中
        self.profitMax_Stage = -999999; self.profitMax_Stage_last = -999999     

        self.stopLoss_Dynamic = riskSets.get("stopLoss_Dynamic", True)              #动态止损
        self.stopLoss = riskSets.get("stopLoss", -0.02)                             #止损线，默认为-2%
        self.stopLoss_Retreat = riskSets.get("stopLoss_Retreat", 0.01)              #止损回撤，默认为1% 
        self.stopLoss_goon = riskSets.get("stopLoss_goon", False)                   #是否止损中
        self.profitMin_Stage = 9999999; self.profitMin_Stage_last = 9999999        
        
    # 自定义处理
    def handle_user(self, msg):
        self.checkState(msg)    # 检查止盈止损状态
        
    # 检查止盈止损状态
    def checkState(self, msg):
        prift = msg['Profit']
        price = msg['Value']
        state = msg['codeState']

        # 上涨为止盈，下跌为止损
        if(prift > 0):
            if(prift >= self.stopProfit):                       # 超过止盈线
                if(self.stopProfit_Dynamic):                    # 开启动态止盈
                    if(self.stopProfit_goon == False):          # 未激活止盈监测
                        self.stopProfit_goon = True             # 激活止盈监测状态
                        self.stopLoss_goon = False              # 关闭止损监测状态
                        self.profitMax_Stage_last = prift       # 赋值阶段最高收益-止盈时  
                        self.setState(True, msg, True)          # 设置止盈状态
                else:
                    self.setState(True, msg)                    # 设置止盈状态
        elif(prift < 0):  
            if(prift <= self.stopLoss):                         # 超过止损线
                if(self.stopLoss_Dynamic):                      # 开启动态止损
                    if(self.stopLoss_goon == False):            # 未激活止损监测
                        self.stopLoss_goon = True               # 激活止损监测状态
                        self.stopProfit_goon = False            # 关闭止盈监测状态
                        self.profitMin_Stage_last = prift       # 赋值阶段最低收益-止损时  
                        self.setState(False, msg, True)         # 设置止损状态
                else:
                    self.setState(False, msg)                   # 设置止损状态

        # 止盈监测激活时，回撤判断 
        if(self.stopProfit_goon):       
            # 回撤超过界限，激活止盈(精度修正+0.00000001,避免计算过程小数点精度导致的临界计算错误)
            if(state == -1):
                if(self.profitMax_Stage_last - prift - self.stopProfit_Retreat + 0.00000001 >= 0.0):
                    self.setState(True, msg)
                    self.profitMax_Stage_last = prift
            else:
                self.updataStatic(prift)    # 新高统计
                pass                        # 其他止盈逻辑-特殊
        elif(self.stopLoss_goon):       
            # 回撤超过界限，激活止损(精度修正+0.00000001,避免计算过程小数点精度导致的临界计算错误)
            if(state == -1):
                if(self.profitMin_Stage_last - prift - self.stopLoss_Retreat + 0.00000001 >= 0.0):
                    self.setState(False, msg)               # 更新最大最小值等统计信息
                    self.profitMin_Stage_last = prift
            else:
                self.updataStatic(prift)    # 新低统计
                pass                        # 其他止盈逻辑-特殊
    #设置止盈止损状态   
    def setState(self, isStopProfit, msgOld = None, isBreak = False): 
        self.isStop_Profit = isStopProfit
        self.isStop_Loss = not isStopProfit
        
        # 组装消息
        if(msgOld != None):
            self.updataStatic(msgOld['Profit'])
            riskType = self.iif(self.isStop_Profit, "stopProfit", "stopLoss")
            isDynamic = self.iif(self.isStop_Profit, self.stopProfit_Dynamic, self.stopLoss_Dynamic)
            lastProfit = self.iif(self.isStop_Profit, self.profitMax_Stage_last, self.profitMin_Stage_last)

            msg = msgOld.copy()
            msg['Type'] = "RISK"
            msg['riskInfo'] = {'riskType': riskType, 'isBreak': isBreak, 'isDynamic': isDynamic, 'lastProfit': lastProfit, 'minProfit': self.profitMin_Stage, 'maxProfit': self.profitMax_Stage} 
            self.msgList.append(msg)
            
            # 调用装饰函数
            self.configured_reply(msg['Type'], False)
            
    # 更新最大最小值等统计信息
    def updataStatic(self, prift):
        if(self.profitMin_Stage_last == 999999):  self.profitMin_Stage_last = prift
        if(self.profitMax_Stage_last == -999999):  self.profitMax_Stage_last = prift

        if(self.profitMax_Stage_last < prift):       # 新高判断
            self.profitMax_Stage_last = prift        # 赋值阶段最高价
        if(self.profitMax_Stage < prift):  self.profitMax_Stage = prift  

        if(self.profitMin_Stage > prift):            # 新低判断
            self.profitMin_Stage = prift             # 赋值阶段最低价



if __name__ == '__main__':
    datas1 = [12, 11.7, 12.7, 13.3, 10.4, 10.6, 10.7, 10.9, 10.8, 10.75, 10.8, 10.7]
    datas2 = [10.6, 10.5, 10.4, 10.3, 10.2, 10.1, 10.0, 9.9, 9.8, 9.6]
    datas3 = [9.8, 9.6]
    pRisk = myData_Monitor_Risk("Test",valueMin=9.5, valueMax=10.8, valueBase=10, valueDelta=0.0025)
    
    # 装饰函数，处理监测到的上升、下降、拐点
    @pRisk.msg_register(["RISK"])
    def Reply_Raise(msg): 
        print(msg)

    # 循环数据进行监测
    for x in datas1:
        pRisk.add_data(x)
    
    print("")
