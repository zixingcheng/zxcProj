#-*- coding: utf-8 -*-
"""
Created on  张斌 2019-09-24 22:58:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com
    
    自定义简易库表操作-股票风险设置记录
"""
import sys, os, time, copy, datetime, mySystem
from collections import OrderedDict
from operator import itemgetter, attrgetter
from decimal import Decimal

#引用根目录类文件夹--必须，否则非本地目录起动时无法找到自定义类
mySystem.Append_Us("../Prjs", False, __file__)
mySystem.Append_Us("../../../zxcPy.Quotation", False, __file__)
mySystem.Append_Us("", False) 
import myEnum, myIO, myIO_xlsx, myData, myData_DB, myData_Trans, myDebug #myQuote_Setting



# 股票风险设置记录 
class mySet_StockTradeRisk():
    def __init__(self, dictSets = None, nameDB = "zxcDB_StockTradeRisk", dir = ""):  
        self.usrID = ""
        self.stockID = ""           #标的编号
        self.stockName = ""         #标的名称
        self.stockAvg = 0           #标的均价
        self.stockNum = 0           #标的数量
        self.stockPosition = 1      #标的仓位
        
        self.stopProfit = 0.06          #止盈线，默认为6%
        self.stopLoss = -0.02           #止损线，默认为-2%
        self.stopProfit_Dynamic = True  #动态止盈 
        self.stopLoss_Dynamic = True    #动态止损 
        self.stopProfit_Retreat = 0.01  #止盈回撤，默认为1%, 超过止盈线以上则为2倍
        self.stopLoss_Retreat = 0.01    #止损回撤，默认为1%
        self.stopProfit_Trade = 0.2     #止盈交易比例，默认为20%
        self.stopLoss_Trade = 0.2       #止损交易比例，默认为20%
        
        self.maxPrice = 0               #最高价格，默认为0，用于统计
        self.maxProfit = 0              #阶段浮盈，默认为0，触发止盈时更新
        self.stopProfit_goon = False    #正止盈状态
        self.logOperates = []           #操盘记录

        self.datetime = datetime.datetime.now()  
        self.remark = ""                #备注
        self.valid = True               #是否有效
        self.dictSets = {}              #字典型设置信息
        self.Trans_FromDict(dictSets, False)

    # 转换为字典结构
    def Trans_ToDict(self, dictSets = None):  
        if(dictSets == None): dictSets = self.dictSets
        dictSets['用户名'] = self.usrID
        dictSets['标的编号'] = self.stockID
        dictSets['标的名称'] = self.stockName
        dictSets['标的均价'] = self.stockAvg
        dictSets['标的数量'] = self.stockNum
        dictSets['标的仓位'] = self.stockPosition
        
        dictSets['止盈线'] = self.stopProfit
        dictSets['止损线'] = self.stopLoss
        dictSets['动态止盈'] = self.stopProfit_Dynamic
        dictSets['动态止损'] = self.stopLoss_Dynamic
        dictSets['止盈回撤'] = self.stopProfit_Retreat
        dictSets['止损回撤'] = self.stopLoss_Retreat
        dictSets['止盈比例'] = self.stopProfit_Trade
        dictSets['止损比例'] = self.stopLoss_Trade
        
        dictSets['最高价格'] = self.maxPrice
        dictSets['阶段浮盈'] = self.maxProfit
        dictSets['止盈状态'] = self.stopProfit_goon

        dictSets['日期'] = self.datetime
        if(self.valid == False):
            dictSets['isDel'] = True 
        dictSets['备注'] = self.remark
        dictSets['操作日志'] = self.logOperates
        return self.dictSets
    # 转换为对象，由字典结构
    def Trans_FromDict(self, dictSets, canLog = True):  
        #验证股票信息
        #pStocks = gol._Get_Value('setsStock', None)
        #lstStock = pStocks._Find(dictSets.get('标的编号',""), dictSets.get('标的名称',""), exType="")
        #if(len(lstStock) != 1): return{}
        #pStock = lstStock[0]
        #self.stockID = pStock.code_id
        #self.stockName = pStock.code_name

        #解析信息
        if(dictSets == None): return False
        self.usrID = dictSets['用户名']
        self.stockID = dictSets.get('标的编号',"")
        self.stockName = dictSets.get('标的名称',"")  

        stockNum_temp = myData_Trans.To_Float(str(dictSets.get("标的数量", 0)))
        stockAvg_temp = myData_Trans.To_Float(str(dictSets.get("标的均价", 0)))
        stockPosition_temp = myData_Trans.To_Float(str(dictSets.get("标的仓位", 1)))
        if(stockNum_temp == 0 or stockNum_temp == 0): return False
        if(canLog):
            self.logOperates.append({"股数": stockNum_temp,"股价":stockAvg_temp})    #仓位变化记录
        else:
            self.logOperates = dictSets.get('操作日志', self.logOperates)
        
        #计算仓位变化
        stockNum = self.stockNum + abs(stockNum_temp)
        stockMoney = self.stockAvg * self.stockNum + stockNum_temp * stockAvg_temp
        self.stockPosition = (stockNum_temp * stockPosition_temp + self.stockNum * self.stockPosition) / stockNum
        self.stockAvg = stockMoney / stockNum
        self.stockNum = int(stockNum)
        
        self.stopProfit = dictSets.get("止盈线", self.stopProfit)
        self.stopLoss = dictSets.get("止损线", self.stopLoss)
        self.stopProfit_Dynamic = dictSets.get("动态止盈", self.stopProfit_Dynamic)
        self.stopLoss_Dynamic = dictSets.get("动态止损", self.stopLoss_Dynamic)
        self.stopProfit_Retreat = dictSets.get("止盈回撤", self.stopProfit_Retreat)
        self.stopLoss_Retreat = dictSets.get("止损回撤", self.stopLoss_Retreat)
        self.stopProfit_Trade = dictSets.get("止盈比例", self.stopProfit_Trade)
        self.stopLoss_Trade = dictSets.get("止损比例", self.stopLoss_Trade)
        
        self.maxPrice = dictSets.get("最高价格", self.maxPrice)
        self.maxProfit = dictSets.get("阶段浮盈", self.maxProfit)
        self.stopProfit_goon = dictSets.get("止盈状态", self.stopProfit_goon)

        self.datetime = dictSets.get("日期", self.datetime)
        self.remark = dictSets.get("备注", self.remark)
        self.valid = not dictSets.get('isDel',False)  
        if(self.stockNum == 0): 
            self.valid = False
        return True

    # 统计收益（实际浮盈、已卖出收益）
    def Static_Profit(self, price):  
        #统计已经卖出的收益
        sumProfit = 0
        sumStock = 0
        for x in self.logOperates:
            if(x["股数"] < 0):
                sumStock += x["股数"]
                sumProfit += x["股价"] * x["股数"]
            pass

        #计算浮盈
        profit = (price * (self.stockNum - sumStock) + sumProfit) / self.stockNum * self.stockAvg - 1
        return profit, sumProfit
    
# 股票风险监测类 
class myMonitor_TradeRisk():
    def __init__(self, minPrice5, maxPrice5, minPrice10=-1, maxPrice10=-1, minPrice20=-1, maxPrice20=-1):  
        self.setRisk = mySet_StockTradeRisk()   #交易风险设置
        self.maxPrice5 = maxPrice5              #5日最高价
        self.maxPrice10 = maxPrice10            #10日最高价
        self.maxPrice20 = maxPrice20            #20日最高价
        self.minPrice5 = minPrice5              #5日最低价
        self.minPrice10 = minPrice10            #10日最低价
        self.minPrice20 = minPrice20            #20日最低价
        self.maxPrice = max(self.maxPrice5, self.maxPrice10, self.maxPrice20)
        self.minPrice = min(self.minPrice5, self.minPrice10, self.minPrice20)

        self.isStop_Profit = False              #是否激活止盈，与止损互斥
        self.isStop_Loss = False                #是否激活止损，与止盈互斥
        self.stopProfit_Retreat = 0             #当前止盈回撤，超过止盈线以上则为2倍

    #初始风险设置
    def initSet(self, setRisk):
        self.setRisk = setRisk
        
    #通知接收新行情
    def notifyQuotation(self, price):
        #检查止盈止损状态
        self.checkState(price)

        #执行动态止盈止损
        if(self.isStop_Profit):
            myDebug.Debug(self.stopProfit(price))
        elif(self.isStop_Loss):
            self.isStop_Loss = False
        else:
            prift = price / self.setRisk.stockAvg - 1
            strProfit = str(Decimal((prift * 100)).quantize(Decimal('0.00'))) + "%"
            myDebug.Debug("收益：" + strProfit)

            
    #止盈操作
    def stopProfit(self, price):
        #组装止盈提示
        prift = price / self.setRisk.stockAvg - 1                           #涨幅
        priftMax = self.setRisk.maxPrice / self.setRisk.stockAvg - 1        #最大涨幅
        numSell = self.setRisk.stopProfit_Trade * self.setRisk.stockNum     #卖出数量
        if(self.setRisk.stopProfit_Trade > self.setRisk.stockPosition):     #低仓位修正
            numSell = self.setRisk.stockPosition * self.setRisk.stockNum    
        strPrice = str(Decimal(price).quantize(Decimal('0.00'))) + " 元"    #价格
        strSell = str(int(numSell)) + "股"                                  #股数
        strRetreat = str(Decimal((self.stopProfit_Retreat * 100)).quantize(Decimal('0.0'))) + "%"       #回撤
        strTrade = str(Decimal((self.setRisk.stopProfit_Trade * 10)).quantize(Decimal('0.0'))) + "成"   #仓位
        strMax_now = str(Decimal((self.setRisk.maxProfit * 100)).quantize(Decimal('0.00'))) + "%"       #阶段浮盈
        strMax = str(Decimal((priftMax * 100)).quantize(Decimal('0.00'))) + "%"                         #最大浮盈
        strProfit = str(Decimal((prift * 100)).quantize(Decimal('0.0'))) + "%"                          #当前收益
        strReutrn = self.setRisk.stockName + ": 回撤逾 " + strRetreat + ",建议止盈. 卖出 " + strSell + "(总仓 " + strTrade +  "),收益: " + strProfit + ",阶段高点: " + strMax_now + ",最高点: " + strMax + "."
        #strReutrn = F"测试股票: {strPrice}, 回撤逾 {strRetreat}.\r\n操作策略: 建议止盈, 操作 {strTrade}仓, 卖出 {strSell}.\r\n策略收益: {strProfit}, 总收益 {strProfit}, 涨幅前高 {strMax_now}, 最高 {strMax}."
        
        #设置同步
        self.setRisk.maxProfit = prift  #修正阶段高值
        self.setRisk.stockPosition = Decimal(self.setRisk.stockPosition) - Decimal(self.setRisk.stopProfit_Trade)
        self.isStop_Profit = False      #恢复状态
        return strReutrn

    #设置止盈止损状态   
    def setState(self, isStopProfit):
        if(self.setRisk.stockPosition >= 0):
            self.isStop_Profit = isStopProfit
            self.isStop_Loss = not isStopProfit

    #检查止盈止损状态
    def checkState(self, price):
        #仓位检查
        if(self.setRisk.stockPosition <=0): return

        #计算盈亏比例,更新统计值
        prift = price / self.setRisk.stockAvg - 1
        if(self.setRisk.maxPrice < price):
            self.setRisk.maxPrice = price

        #区分止盈、止损，互斥
        if(prift > 0):
            #过止盈线触发止盈
            if(self.setRisk.stopProfit_Dynamic):    #开启动态止盈
                #区分是否正止盈中
                if(self.setRisk.stopProfit_goon):
                    #回撤率修正，止盈线以上则为2倍，扩大回撤容忍范围，可以减少总回撤率
                    self.stopProfit_Retreat = self.setRisk.stopProfit_Retreat
                    if(prift > self.setRisk.stopProfit + self.setRisk.stopProfit_Retreat):
                        self.stopProfit_Retreat = self.setRisk.stopProfit_Retreat * 2

                    #回撤超过界限，激活止盈
                    if(self.setRisk.maxProfit - prift > self.stopProfit_Retreat):
                        self.setState(True)
                    else:
                        #更新阶段最高价
                        if(self.setRisk.maxProfit < prift):
                            self.setRisk.maxProfit = prift      #赋值阶段最高价
                else:   
                    #非止盈状态，超过止盈线时激活止盈
                    if(prift >= self.setRisk.stopProfit):
                        self.setRisk.stopProfit_goon = True     #激活止盈状态
                        self.setRisk.maxProfit = prift          #赋值阶段最高价
            else:
                #超过止盈线时激活止盈
                if(prift >= self.setRisk.stopProfit):
                    self.isStop_Profit = True
                    self.isStop_Loss = False
        else:
            if(self.setRisk.stopLoss_Dynamic):      #开启动态止损
                if(prift >= self.setRisk.stopLoss):
                    self.isStop_Loss = True
                    self.isStop_Profit = False
        
        


"""
交易策略：
1.10/5日高点取最高，日内高点，回撤起始1%建议平仓 20%，回撤2%建议平仓 20%，回撤3%建议平仓 20%，回撤4%建议平仓 20%，回撤5%建议平仓 20%
2.建议需要记录，便于分阶段处理。
3.止盈规则：
	达到指定涨幅时（默认6%），触发交易止盈/动态止盈。
	动态止盈：
		按回撤比例分阶段分步卖出，从当前最高点回撤1%时第一次触发，之后每回撤1%触发一次，连续回撤5%时全部卖出。
		当涨幅回升，突破新高时，初始回撤触发状态，即从高点再次回撤1%时触发，直到卖出完毕。
			突破新高规则：涨幅突破前一阶段止盈点，涨幅突破止盈涨幅线，涨幅突破10/5日高点。突破后实时比对更新新高。
			
	关键点：止盈线、10/5日高点、回撤后实时新高
"""

# 自定义简易库表操作-股票风险设置记录 
class myDataDB_StockTradeRisk(myData_DB.myData_Table):
    def __init__(self, nameDB = "zxcDB_StockTradeRisk", dir = ""):  
        #初始根目录信息
        if(dir == ""):
            strDir, strName = myIO.getPath_ByFile(__file__)
            self.Dir_Base = os.path.abspath(os.path.join(strDir, "../../.."))  
            self.Dir_DataDB = self.Dir_Base + "/Data/DB_Trade/Stock_Risks/"
            myIO.mkdir(self.Dir_DataDB, False) 
        super().__init__(nameDB, self.Dir_DataDB, True) 
    
        
    # 检查是否已经存在   
    def _Check(self, rowInfo, updata = False): 
        #修正数据类型 
        if(rowInfo.get('操作日志', "") == ""):
            psetRisk = mySet_StockTradeRisk()
            psetRisk.Trans_FromDict(rowInfo)

            #调用基类更新
            psetRisk.Trans_ToDict(rowInfo)
        return super()._Check(rowInfo, updata)
    #单条有效修正
    def _Check_oneValid(self, rowInfo): 
        if(rowInfo.get('用户名', '') != ""):
            datas = self.Query("用户名== " + rowInfo['用户名'] + " && 标的编号==" + rowInfo['标的编号'])
            for x in datas:
                datas[x]['isDel'] = True
        return True
    # 检查是否相同--继承需重写  
    def _IsSame(self, rowInfo, rowInfo_Base): 
        if(super()._IsSame(rowInfo, rowInfo_Base)): return True

        if(rowInfo['用户名'] == rowInfo_Base['用户名']):
            if(rowInfo['标的编号'] == rowInfo_Base['标的编号']):
                if (rowInfo['日期'] - rowInfo_Base['日期']).days < 1024:
                    return True
        return False
            
    # 更新
    def _Updata(self, x, rowInfo): 
        #参数设置更新
        psetRisk = mySet_StockTradeRisk(self.rows[x])
        psetRisk.Trans_FromDict(rowInfo)

        #调用基类更新
        psetRisk.Trans_ToDict(rowInfo)
        super()._Updata(x, rowInfo )
    

#初始全局消息管理器
from myGlobal import gol 
gol._Init()     #先必须在主模块初始化（只在Main模块需要一次即可）
gol._Set_Setting('zxcDB_StockTradeRisk', myDataDB_StockTradeRisk())      #实例 股票收益库对象 
gol._Get_Setting('zxcDB_StockTradeRisk').Add_Fields(['用户名', '标的编号', '标的名称', '标的均价', '标的数量', "标的仓位", '止盈线', '动态止盈', '止盈回撤', '止盈比例', '止损线', '动态止损', '止损回撤', '止盈比例', '最高价格', '阶段浮盈', '止盈状态', '日期', '备注', '操作日志'], ['string','string','string','float','int','float','float','bool','float','float','float','bool','float','float','float','float','bool','datetime','string','list'], [])


"""
交易策略：
1.10/5日高点取最高，日内高点，回撤起始1%建议平仓 20%，回撤2%建议平仓 20%，回撤3%建议平仓 20%，回撤4%建议平仓 20%，回撤5%建议平仓 20%
2.建议需要记录，便于分阶段处理。
3.止盈规则：
	达到指定涨幅时（默认6%），触发交易止盈/动态止盈。
	动态止盈：
		按回撤比例分阶段分步卖出，从当前最高点回撤1%时第一次触发，之后每回撤1%触发一次，连续回撤5%时全部卖出。
		当涨幅回升，突破新高时，初始回撤触发状态，即从高点再次回撤1%时触发，直到卖出完毕。
			突破新高规则：涨幅突破前一阶段止盈点，涨幅突破止盈涨幅线，涨幅突破10/5日高点。突破后实时比对更新新高。
			
	关键点：止盈线、10/5日高点、回撤后实时新高

3.止损规则：
	达到指定跌幅时（默认-2%），触发交易止损/动态止损。
	动态止损：
		按跌幅比例分阶段分步卖出，从当前止损线跌1%时第一次触发，之后每跌1%触发一次，连续跌5%时全部卖出。
		当涨幅回升，突破新高时，初始止损触发状态，即从高点再次回撤1%时触发，直到卖出完毕。
			突破新高规则：涨幅突破前一阶段止损点，涨幅突破止损线。突破后实时比对更新新高。
"""


#主启动程序
if __name__ == "__main__":
    #测试库表操作
    pDB = gol._Get_Setting('zxcDB_StockTradeRisk')

    # 添加行数据
    print(pDB.Add_Row({'用户名': '茶叶一主号', '标的编号': '600001', '标的名称': "测试股票", '标的均价': '10.3', '标的数量': 5000, '止盈线': 0.06, '日期': '2019-08-27 11:11:00'}, True))
    print(pDB.Add_Row({'用户名': '茶叶一主号', '标的编号': '600001', '标的名称': "测试股票", '标的均价': '9.7', '标的数量': 5000, '日期': '2019-08-27 11:11:00'}, True))
    
    # 查询数据
    dictSet = pDB.Query("isDel==False && 用户名==茶叶一主号 && 标的编号==600001", "", True)
    pSet = mySet_StockTradeRisk(list(dictSet.values())[0])


    # 风险监测测试
    pRisk = myMonitor_TradeRisk(9.5, 10.5)
    pRisk.initSet(pSet)
    pRisk.notifyQuotation(10.61)
    pRisk.notifyQuotation(10.5)     #回撤
    pRisk.notifyQuotation(10.4)     #回撤
    pRisk.notifyQuotation(10.6)
    pRisk.notifyQuotation(10.7)     
    pRisk.notifyQuotation(10.9)
    pRisk.notifyQuotation(10.7)     #回撤
    pRisk.notifyQuotation(10.7)     
    pRisk.notifyQuotation(10.8)     
    pRisk.notifyQuotation(10.7)     
    pRisk.notifyQuotation(10.6)     #回撤
    pRisk.notifyQuotation(10.7)     
    pRisk.notifyQuotation(10.7)     
    pRisk.notifyQuotation(10.6)     #回撤
    pRisk.notifyQuotation(10.4)     
    pRisk.notifyQuotation(10.3)     


    print()

