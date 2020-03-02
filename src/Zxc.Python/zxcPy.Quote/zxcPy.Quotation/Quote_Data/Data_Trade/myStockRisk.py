#-*- coding: utf-8 -*-
"""
Created on  张斌 2020-02-25 22:58:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com
    
    自定义简易库表操作-股票风险设置记录，基于数据监测类
"""
import sys, os, time, copy, datetime, mySystem
from collections import OrderedDict
from operator import itemgetter, attrgetter
from decimal import Decimal

#引用根目录类文件夹--必须，否则非本地目录起动时无法找到自定义类
mySystem.Append_Us("../Prjs", False, __file__)
mySystem.Append_Us("../../../zxcPy.Quotation", False, __file__)
mySystem.Append_Us("../../../zxcPy.Quotation/Quote_Source", False, __file__)
mySystem.Append_Us("../../../zxcPy.Quotation/Quote_Data/Data_Algorithm", False, __file__)
mySystem.Append_Us("", False) 
import myEnum, myIO, myIO_xlsx, myData, myData_DB, myData_Trans, myManager_Msg, myDebug #myQuote_Setting
import myQuote, myData_Monitor_Risk



# 股票风险设置记录 
class mySet_StockRisk():
    def __init__(self, dictSets = None):  
        self.ID = -1
        self.usrID = ""
        self.usrTag = ""
        self.stockID = ""           #标的编号
        self.stockName = ""         #标的名称
        self.stockAvg = 0           #标的均价-所有买入 
        self.stockNum = 0           #标的数量
        self.sumStock_Trade = 0     #更新交易数量-买卖
        self.stockPosition = 1      #标的仓位-当前
        self.stockFee = 0.003       #标的手续费率,卖出时统一计算
        
        self.fixHit = False             #是否启用定量监测
        self.limitHit = True            #是否启用高低边界监测
        self.deltaProfit = 0.0025       #数据监测触发最小间隔
        self.stopProfit = 0.06          #止盈线，默认为6%
        self.stopLoss = -0.02           #止损线，默认为-2%
        self.stopProfit_Dynamic = True  #动态止盈 
        self.stopLoss_Dynamic = True    #动态止损 
        self.stopProfit_Retreat = 0.01  #止盈回撤，默认为1%
        self.stopLoss_Retreat = 0.01    #止损回撤，默认为1%
        self.stopProfit_Trade = 0.2     #止盈交易比例，默认为20%
        self.stopLoss_Trade = 0.2       #止损交易比例，默认为20%
        
        self.priceMax = 0               #最高价格，默认为0，用于统计
        self.priceMin = 0               #最低价格，默认为0，用于统计
        self.priceCost = 0              #成本价格，默认为0，买卖时更新，当前仓位的实际成本均价，累计卖出收益，卖出手续费
        self.priceAvg_sell = 0          #卖出均价，默认为0，用于统计
        self.priceNow = 0               #当前价格，默认为0，用于统计
        self.profitMax_Stage = 0        #阶段止盈，默认为0，触发止盈时更新
        self.profitMin_Stage = 0        #阶段止损，默认为0，触发止损时更新
        self.profitMax = 0              #最大浮盈，默认为0，触发止盈时更新
        self.profitMin = 0              #最小浮盈，默认为0，触发止损时更新
        self.profitNow = 0              #阶段浮盈-当前价格，默认为0，用于统计
        self.pricePrecision = 2         #价格小数点精度
        self.stopProfit_goon = False    #正止盈状态
        self.stopLoss_goon = False      #正止损状态
        self.logOperates = []           #操盘记录
        self.sumOperates = 0            #操盘记录数，用于更新统计判断

        self.datetime = datetime.datetime.now()  
        self.remark = ""                #备注
        self.valid = True               #是否有效
        self.dictSets = {}              #字典型设置信息
        self.Trans_FromDict(dictSets, False)

    # 转换为字典结构
    def Trans_ToDict(self, dictSets = None):  
        if(dictSets == None): dictSets = self.dictSets
        dictSets['ID'] = self.ID
        dictSets['用户名'] = self.usrID
        dictSets['用户标签'] = self.usrTag
        dictSets['标的编号'] = self.stockID
        dictSets['标的名称'] = self.stockName
        dictSets['标的均价'] = round(self.stockAvg, 4)
        dictSets['标的数量'] = self.stockNum
        dictSets['标的仓位'] = round(self.stockPosition, 4)
        dictSets['手续费率'] = round(self.stockFee, 4)
        
        dictSets['定量监测'] = self.fixHit
        dictSets['边界限制'] = self.limitHit
        dictSets['监测间隔'] = self.deltaProfit
        dictSets['止盈线'] = self.stopProfit
        dictSets['止损线'] = self.stopLoss
        dictSets['动态止盈'] = self.stopProfit_Dynamic
        dictSets['动态止损'] = self.stopLoss_Dynamic
        dictSets['止盈回撤'] = self.stopProfit_Retreat
        dictSets['止损回撤'] = self.stopLoss_Retreat
        dictSets['止盈比例'] = self.stopProfit_Trade
        dictSets['止损比例'] = self.stopLoss_Trade
        
        dictSets['最高价格'] = round(self.priceMax, 4)
        dictSets['成本价格'] = round(self.priceCost, 4)
        dictSets['卖出均价'] = round(self.priceAvg_sell, 4)
        dictSets['当前价格'] = round(self.priceNow, 4)
        dictSets['阶段止盈'] = round(self.profitMax_Stage, 4)
        dictSets['阶段止损'] = round(self.profitMin_Stage, 4)        
        dictSets['最高浮盈'] = round(self.profitMax, 4)
        dictSets['当前浮盈'] = round(self.profitNow, 4)
        dictSets['止盈状态'] = self.stopProfit_goon
        dictSets['止损状态'] = self.stopLoss_goon

        dictSets['日期'] = self.datetime
        dictSets['isDel'] = not self.valid 
        dictSets['备注'] = self.remark
        dictSets['操作日志'] = self.logOperates
        dictSets['操作统计数'] = self.sumOperates
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
        

        #交易信息必须存在
        if(dictSets == None): return False
        index = -1
        strTime = dictSets.get('日期', "")
        if(type(strTime) != str): strTime = myData_Trans.Tran_ToDatetime_str(dictSets['日期'], "%Y-%m-%d %H:%M:%S")
        for x in self.logOperates:
            if(x['时间'] == strTime):
                index += 1
                break

        #解析信息
        self.ID = dictSets.get('ID',-1)
        self.usrID = dictSets['用户名']
        self.usrTag = dictSets.get('用户标签',"")
        self.stockID = dictSets.get('标的编号',"")
        self.stockName = dictSets.get('标的名称',"")  

        stockNum_temp = myData_Trans.To_Float(str(dictSets.get("标的数量", 0)))
        stockAvg_temp = myData_Trans.To_Float(str(dictSets.get("标的均价", 0)))
        stockPosition_temp = myData_Trans.To_Float(str(dictSets.get("标的仓位", 1)))
        if(stockNum_temp == 0 or stockNum_temp == 0): return False

        self.datetime = dictSets.get("日期", self.datetime)
        self.remark = dictSets.get("备注", self.remark)
        self.isDel = dictSets.get('isDel', not self.valid)  

        if(canLog):
            #提取时间
            strTime = self.datetime
            if(type(strTime) != str): strTime = myData_Trans.Tran_ToDatetime_str(strTime, "%Y-%m-%d %H:%M:%S")

            #存在则更新
            if(index == -1):
                self.logOperates.append({"股数": stockNum_temp,"股价":stockAvg_temp,"时间": strTime})    #仓位变化记录
            else:
                self.logOperates[index] = {"股数": stockNum_temp,"股价":stockAvg_temp,"时间": strTime}
        else:
            self.logOperates = dictSets.get('操作日志', self.logOperates)
        self.sumOperates = dictSets.get('操作统计数',0)
        
        #计算仓位变化
        if(index == -1):
            stockNum = self.stockNum
            if(stockNum_temp > 0):
                #买入时更新成本 
                stockNum += abs(stockNum_temp) 
                stockMoney = self.stockAvg * self.stockNum + stockNum_temp * stockAvg_temp
                self.stockPosition = (stockNum_temp * stockPosition_temp + self.stockNum * self.stockPosition) / stockNum
                self.stockAvg = stockMoney / stockNum
                self.stockNum = int(stockNum) 
            else:
                #卖出更新仓位
                self.stockPosition = (stockNum_temp * stockPosition_temp + self.stockNum * self.stockPosition) / stockNum
                if(self.stockPosition <= 0):
                    self.stockPosition = 0
                    self.valid = False
            
        self.stockFee = dictSets.get("手续费率", self.stockFee)
        self.limitHit = dictSets.get("边界限制", self.limitHit)
        self.fixHit = dictSets.get("定量监测", self.fixHit)
        self.deltaProfit = dictSets.get("监测间隔", self.deltaProfit)
        
        self.stopProfit = dictSets.get("止盈线", self.stopProfit)
        self.stopLoss = dictSets.get("止损线", self.stopLoss)
        self.stopProfit_Dynamic = dictSets.get("动态止盈", self.stopProfit_Dynamic)
        self.stopLoss_Dynamic = dictSets.get("动态止损", self.stopLoss_Dynamic)
        self.stopProfit_Retreat = dictSets.get("止盈回撤", self.stopProfit_Retreat)
        self.stopLoss_Retreat = dictSets.get("止损回撤", self.stopLoss_Retreat)
        self.stopProfit_Trade = dictSets.get("止盈比例", self.stopProfit_Trade)
        self.stopLoss_Trade = dictSets.get("止损比例", self.stopLoss_Trade)
        
        self.priceMax = dictSets.get("最高价格", self.priceMax)
        self.priceCost = dictSets.get("成本价格", self.stockAvg)
        self.priceAvg_sell = dictSets.get("卖出均价", stockAvg_temp)
        self.priceNow = dictSets.get("当前价格", stockAvg_temp)
        self.profitMax_Stage = dictSets.get("阶段止盈", self.profitMax_Stage)
        self.profitMin_Stage = dictSets.get("阶段止损", self.profitMin_Stage)
        self.profitNow = dictSets.get("当前浮盈", self.profitNow)
        self.stopProfit_goon = dictSets.get("止盈状态", self.stopProfit_goon)
        self.stopLoss_goon = dictSets.get("止损状态", self.stopLoss_goon)
        
        #操盘记录数不一致，更新统计判断
        if(self.sumOperates != len(self.logOperates)):
            self.Static_Profit(self.priceNow)
        return True

    # 统计收益（实际浮盈、已卖出收益）
    def Static_Profit(self, strokPrice, bUpdata = True):  
        #累计买入、卖出
        sumStock_Buy = 0
        sumMoney_Buy = 0
        sumStock_Sell = 0
        sumMoney_Sell_fee = 0
        maxPrice = 0; minPrice =999999
        for x in self.logOperates:
            if(x["股数"] < 0):
                sumStock_Sell += x["股数"]
                sumMoney_Sell_fee += x["股价"] * x["股数"]      #计算含手续费
            else:
                sumStock_Buy += x["股数"]
                sumMoney_Buy += x["股价"] * x["股数"]           #计算含手续费
            if(maxPrice < x["股价"]): maxPrice = x["股价"]
            if(minPrice > x["股价"]): minPrice = x["股价"]

        #统计计算
        sumStock_Trade = sumStock_Buy + abs(sumStock_Sell)
        sumMoney_Sell = sumMoney_Sell_fee * (1 - self.stockFee)                     #卖出总金额（不含手续费）
        sumMoney = (sumStock_Buy + sumStock_Sell) * strokPrice - sumMoney_Sell      #当前市值（含卖出）
        sumStock = sumStock_Buy + sumStock_Sell
        profitNow = sumMoney / sumMoney_Buy - 1                                     #当前浮盈-阶段
        stockAvg_sell = 0
        if(sumStock_Sell != 0):
            stockAvg_sell = sumMoney_Sell_fee / sumStock_Sell                       #卖出均价
        stockCost = (sumMoney_Buy + sumMoney_Sell) / myData.iif(sumStock <= 0, sumStock_Buy, sumStock)

        #更新
        if(bUpdata == True):
            self.sumStock_Trade = sumStock_Trade            #更新交易数量-买卖
            self.priceCost = stockCost                      #更新成本价格
            self.priceNow = strokPrice                      #更新当前价格
            self.priceAvg_sell = stockAvg_sell              #更新卖出均价
            self.profitNow = profitNow                      #更新当前阶段浮盈
            if(self.profitMax < self.profitMax_Stage):
                self.profitMax = self.profitMax_Stage       #更新最大浮盈
            if(self.profitMin > self.profitMin_Stage):
                self.profitMin = self.profitMin_Stage       #更新最小浮盈
            if(self.priceMax < maxPrice): self.priceMax = maxPrice
            if(self.priceMin == 0 or self.priceMin > minPrice): self.priceMin = minPrice
        return profitNow, stockCost

# 自定义简易库表操作-股票风险设置记录 
class myDataDB_StockRisk(myData_DB.myData_Table):
    def __init__(self, nameDB = "zxcDB_StockRisk", dir = ""):  
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
            psetRisk = mySet_StockRisk()
            psetRisk.Trans_FromDict(rowInfo)

            #调用基类更新
            psetRisk.Trans_ToDict(rowInfo)
        return super()._Check(rowInfo, updata)
    # 单条有效修正
    def _Check_oneValid(self, rowInfo): 
        if(rowInfo.get('用户名', '') != ""):
            datas = self.Query("用户名== " + rowInfo['用户名'] + " && 用户标签==" + rowInfo['用户标签'] + " && 标的编号==" + rowInfo['标的编号'])
            for x in datas:
                datas[x]['isDel'] = True
        return True
    # 检查是否相同--继承需重写  
    def _IsSame(self, rowInfo, rowInfo_Base): 
        if(super()._IsSame(rowInfo, rowInfo_Base)): return True

        # 必须ID相同、是否删除相同
        if(rowInfo['ID'] > 0):
            if(rowInfo['ID'] != rowInfo_Base['ID']): return False
        if(rowInfo['isDel'] != rowInfo_Base['isDel']): return False
        if(rowInfo['用户名'] == rowInfo_Base['用户名'] and rowInfo['用户标签'] == rowInfo_Base['用户标签']):
            if(rowInfo['标的编号'] == rowInfo_Base['标的编号']):
                if (rowInfo['日期'] - rowInfo_Base['日期']).days < 1024:
                    return True
        return False
            
    # 更新
    def _Updata(self, x, rowInfo, bSave = False, bCheck = True): 
        #参数设置更新
        if(bCheck == True):
            psetRisk = mySet_StockRisk(self.rows[x])
            psetRisk.Trans_FromDict(rowInfo)
            psetRisk.Trans_ToDict(rowInfo)

        #调用基类更新
        super()._Updata(x, rowInfo, bSave)
    
    # 提取设置集
    def getSets(self, setDB = None): 
        # 查询数据
        if(setDB == None):
            setDB = gol._Get_Value('zxcDB_StockRisk')
        dictSet = setDB.Query("isDel==False" , "", True)
        return dictSet
    # 提取设置，指定用户名、股票编号
    def getSet(self, usrNmae, usrTag, stockID, isDel = False, setDB = None): 
        # 组装查询条件
        strFilter = F"isDel=={str(isDel)} && 用户名=={usrNmae} && 用户标签=={usrTag} && 标的编号=={stockID}" 

        # 查询数据
        if(setDB == None):
            setDB = gol._Get_Value('zxcDB_StockRisk')
        dictSet = setDB.Query(strFilter, "", True)

        # 提取及返回
        lstSet = list(dictSet.values())
        if(len(lstSet) == 1):
            return lstSet[0]
        return None
    # 提取交易风险对象，指定用户名、股票编号
    def getTradeRisk(self, usrNmae, usrTag, stockID, avg5 = False, avg10 = False, avg20 = False, end_date=None): 
        # 提取设置
        setDB = gol._Get_Value('zxcDB_StockRisk')
        dictSet = self.getSet(usrNmae, usrTag, stockID, False, setDB)
        if(dictSet == None): return None
        
        # 获取均值
        nTimes = myData.iif(dictSet['标的名称'].count('50ETF') == 1, 10000, 1)
        stockSource = gol._Get_Value('quoteSource_API', None)
        avgs = [0, 0, -1, -1, -1, -1]
        if(avg5):
            avg5s = stockSource.getPrice_avg_day(stockID, 5, False, end_date)
            avgs[0] = avg5s['low'] * nTimes
            avgs[1] = avg5s['high'] * nTimes
        if(avg10):
            avg10s = stockSource.getPrice_avg_day(stockID, 10, False, end_date)
            avgs[2] = avg10s['low'] * nTimes
            avgs[3] = avg10s['high'] * nTimes
        if(avg20):
            avg20s = stockSource.getPrice_avg_day(stockID, 10, False, end_date)
            avgs[4] = avg20s['low'] * nTimes
            avgs[5] = avg20s['high'] * nTimes

        # 初始风险监测对象
        pSet = mySet_StockRisk(dictSet)
        if(nTimes == 10000):    # 修正期权默认设置
            pSet.stopProfit = 0.06          #止盈线，默认为6%
            pSet.stopLoss = 0.06            #止损线，默认为-2%  
            pSet.stopProfit_Retreat = 0.03  #止盈回撤，默认为1%, 超过止盈线以上则为2倍
            pSet.stopLoss_Retreat = 0.02    #止损回撤，默认为1%
        pRisk = myMonitor_StockRisk(avgs[0], avgs[1], avgs[2], avgs[3], avgs[4], avgs[5])
        pRisk.initSet(pSet, setDB)
        pRisk.saveSet()
        return pRisk


# 股票风险监测类 
class myMonitor_StockRisk():
    """
    交易策略：
    1.前20/10/5日高点取最高，日内高点，回撤起始1%建议平仓 20%，回撤2%建议平仓 20%，回撤3%建议平仓 20%，回撤4%建议平仓 20%，回撤5%建议平仓 20%
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
    def __init__(self, minPrice5, maxPrice5, minPrice10=9999999, maxPrice10=-9999999, minPrice20=9999999, maxPrice20=-9999999):  
        self.setRisk = mySet_StockRisk()   #交易风险设置
        self.maxPrice5 = maxPrice5              #5日最高价
        self.maxPrice10 = maxPrice10            #10日最高价
        self.maxPrice20 = maxPrice20            #20日最高价
        self.minPrice5 = minPrice5              #5日最低价
        self.minPrice10 = minPrice10            #10日最低价
        self.minPrice20 = minPrice20            #20日最低价
        self.maxPrice = max(self.maxPrice5, self.maxPrice10, self.maxPrice20)
        self.minPrice = min(self.minPrice5, self.minPrice10, self.minPrice20)

        self.priceNow = 0                       #当前价格
        self.profitNow = 0                      #当前浮盈
        self.stopProfit_Trade = 1               #当前止盈交易比例
        self.stopLoss_Trade = 1                 #当前止损交易比例
        self.stopProfit_Retreat = 0             #当前止盈回撤，超过止盈线以上则为2倍
        self.markStop_Profit = 0                #标记止盈提醒次数
        self.sumStock_Trade = 0                 #更新交易数量-买卖
    # 初始风险设置
    def initSet(self, setRisk, setDB):
        self.setRisk = setRisk
        self.setDB = setDB

        # 初始风险数据监测类及配置
        #if(setRisk.priceMin == 0): setRisk.priceMin = setRisk.priceNow
        #if(setRisk.priceMax == 0): setRisk.priceMax = setRisk.priceNow
        name = setRisk.stockID + "_" + setRisk.usrID + "_" + setRisk.usrTag
        self.riskMonitor = myData_Monitor_Risk.myData_Monitor_Risk(name, True, valueMin=setRisk.priceMin, valueMax=setRisk.priceMax, valueLast=setRisk.priceNow, valueBase=setRisk.priceCost, valueDelta=setRisk.deltaProfit)
        
        self.riskMonitor.fixedHit = setRisk.fixHit                          #定量监测
        self.riskMonitor.limitHit = setRisk.limitHit                        #高低边界监测
        self.riskMonitor.stopProfit_Dynamic = setRisk.stopProfit_Dynamic    #动态止盈
        self.riskMonitor.stopProfit = setRisk.stopProfit                    #止盈线，默认为6%
        self.riskMonitor.stopProfit_Retreat = setRisk.stopProfit_Retreat    #止盈回撤，默认为1%
        self.riskMonitor.stopProfit_goon = setRisk.stopProfit_goon          #是否止盈中
        
        self.riskMonitor.stopLoss_Dynamic = setRisk.stopLoss_Dynamic        #动态止损
        self.riskMonitor.stopLoss = setRisk.stopLoss                        #止损线，默认为-2%
        self.riskMonitor.stopLoss_Retreat = setRisk.stopLoss_Retreat        #止损回撤，默认为1% 
        self.riskMonitor.stopLoss_goon = setRisk.stopLoss_goon              #是否止损中
        
        self.riskMonitor.profitMax_Stage = self.setRisk.profitMax               #最大浮盈
        self.riskMonitor.profitMin_Stage = self.setRisk.profitMin               #最小浮盈 
        self.riskMonitor.profitMax_Stage_last = self.setRisk.profitMax_Stage    #阶段止盈位
        self.riskMonitor.profitMin_Stage_last = self.setRisk.profitMin_Stage    #阶段止损位 
        #self.riskMonitor.init_riskSets()

        # 装饰函数，处理监测到的上升、下降、拐点
        @self.riskMonitor.msg_register(["RAISE", "FALL", "BREAK"])
        def Reply_Raise(msg): 
            #print(msg)
            pass

        # 装饰函数，处理监测到的上升、下降、拐点
        @self.riskMonitor.msg_register(["RISK"])
        def Reply_Risk(msg): 
            self.handleRisk(msg, self.riskMonitor.saveData)
            #print(msg)
            pass

    # 保存修改
    def saveSet(self):
        self.updataRiskSet()            #同步风险交易数据
        
        # 保存
        dictRisk = self.setRisk.Trans_ToDict()
        self.setDB._Updata(self.setRisk.ID, dictRisk, True, False)
    # 同步风险交易数据
    def updataRiskSet(self):
        self.setRisk.stopProfit_goon = self.riskMonitor.stopProfit_goon         #是否止盈中
        self.setRisk.stopLoss_goon = self.riskMonitor.stopLoss_goon             #是否止损中  
        self.setRisk.profitMax = self.riskMonitor.profitMax_Stage               #最大浮盈，默认为0，触发止盈时更新
        self.setRisk.profitMin = self.riskMonitor.profitMin_Stage               #最小浮盈，默认为0，触发止损时更新
        self.setRisk.profitMax_Stage = self.riskMonitor.profitMax_Stage_last    #阶段止盈，默认为0，触发止盈时更新
        self.setRisk.profitMin_Stage = self.riskMonitor.profitMin_Stage_last    #阶段止损，默认为0，触发止损时更新
        self.setRisk.priceMax = self.riskMonitor.valueMax      
        self.setRisk.priceMin = self.riskMonitor.valueMin     
        self.setRisk.priceNow = self.riskMonitor.valueLast  
    # 更新交易操作
    def updataTrade(self, strokPrice, stockNum):
        #复制当前设置
        rowInfo = {'ID': self.setRisk.ID,'用户名': self.setRisk.usrID,'用户标签': self.setRisk.usrTag, '标的编号': self.setRisk.stockID, '标的名称': self.setRisk.stockName, '标的均价': strokPrice, '标的数量': stockNum}
        self.setRisk.Trans_FromDict(rowInfo) 
        self.setRisk.Static_Profit(strokPrice)  #收益统计
        self.saveSet()                          #保存修改

    # 通知接收新行情
    def notifyQuotation(self, price, bSave_Auto = True):
        self.riskMonitor.saveData = bSave_Auto
        self.riskMonitor.add_data(price)
        return 
        
    # 风险处置
    def handleRisk(self, msg, bSave_Auto = True):
        strTitle = ""
        if(msg['Type'] == "RISK"):
            riskInfo = msg['riskInfo']
            self.updataRiskSet()                        #同步风险交易数据
            self.priceNow = msg['Value']
            self.profitNow = msg['Profit']
            
            typeBorder = riskInfo['typeBorder']
            if(riskInfo['riskType'] == 'stopProfit'):
                if(typeBorder == 'newHighest'):         #新高
                    strTitle = self.getTitleMark(self.priceNow, True, not riskInfo['hitPoint'], True, True)
                elif(typeBorder == 'newHigher'):        #新高-阶段
                    strTitle = self.getTitleMark(self.priceNow, True, not riskInfo['hitPoint'], False, True)
                else:
                    strTitle = self.getTitleMark(self.priceNow, False, False, False, True)
            elif(riskInfo['riskType'] == 'stopLoss'):
                if(typeBorder == 'newLowest'):          #新低
                    strTitle = self.getTitleMark(self.priceNow, True, not riskInfo['hitPoint'], True, False)
                elif(typeBorder == 'newLower'):         #新低-阶段
                    strTitle = self.getTitleMark(self.priceNow, True, not riskInfo['hitPoint'], False, False)
                else:
                    strTitle = self.getTitleMark(self.priceNow, False, False, False, False)
        return strTitle

    

        #检查止盈止损状态
        self.checkState(price)

        #执行动态止盈止损
        strTitle = ""
        if(self.isStop_Profit):
            strTitle = self.stopProfit(price, bSave_Auto)
        elif(self.isStop_Loss):
            self.isStop_Loss = False            
        else:
            prift = price / self.setRisk.stockAvg - 1
            strProfit = str(Decimal((prift * 100)).quantize(Decimal('0.00'))) + "%"
            myDebug.Debug("收益：" + strProfit)
            
            #触发止盈-每次启动提醒一次
            if(self.setRisk.stopProfit_goon and self.markStop_Profit == 0):
                strTitle = self.getTitleMark(price, True) 
        return strTitle

            
    #交易策略-止盈(1.非动态，到达位置立即卖出，1.动态，到达位置触发止盈) 
    def handleTrade_stopProfit(self, price, bSave_Auto = False):
        """
        交易策略：
        1.止盈后，分段每回撤1%建议平仓 n%，直到清仓；
        2.建议需要记录，便于分阶段处理。
        """
        #提取股票交易建议信息
        tradeInfo = self.getTradeInfo(price)
        numSell = tradeInfo['numSell'] 

        #自动更新交易记录
        if(bSave_Auto):
            self.updataTrade(price, -numSell)
        else:
            self.setRisk.Static_Profit(price)  #收益统计

        #返回提示信息
        return self.getTitleMark(price, True, numSell)

    # 提取股票交易建议信息
    def getTradeInfo(self, price, stopProfit = True, numSell = 0):
        #股票信息
        self.setRisk.Static_Profit(price)                                   #更新股票操作统计信息
        prift = price / self.setRisk.stockAvg - 1                           #涨幅
        priftMax = self.setRisk.priceMax / self.setRisk.stockAvg - 1        #最大涨幅
        
        self.stopProfit_Retreat = myData.iif(self.setRisk.stopProfit_Dynamic, self.setRisk.stopProfit_Retreat, 1)
        self.stopLoss_Retreat = myData.iif(self.setRisk.stopLoss_Dynamic, self.setRisk.stopLoss_Retreat, 1)
        self.stopProfit_Trade = myData.iif(self.setRisk.stopProfit_Dynamic, self.setRisk.stopProfit_Trade, 1)
        self.stopLoss_Trade = myData.iif(self.setRisk.stopLoss_Dynamic, self.setRisk.stopLoss_Trade, 1)
        numTrade = myData.iif(stopProfit, self.stopProfit_Trade, self.setRisk.stopLoss_Trade)
        
        if(numSell == 0):
            numSell = numTrade * self.setRisk.stockNum                      #卖出数量
            if(numTrade > self.setRisk.stockPosition):                      #低仓位修正
                numSell = self.setRisk.stockPosition * self.setRisk.stockNum    
            numSell = int(Decimal(numSell) + Decimal(0.5))
        return {"prift": prift, "priftMax": priftMax, "numTrade": numTrade, "numSell": numSell}
    # 提取返回信息
    def getTitleMark(self, price, isHit, isNewLimit, isBreakLimit = True, isStopProfit = True, numSell = 0):
        #提取股票交易建议信息
        tradeInfo = self.getTradeInfo(price) 
        numTrade = tradeInfo['numTrade'] 
        numSell = tradeInfo['numSell'] 
        
        #组装提示要素
        strPrice = str(Decimal(price).quantize(Decimal('0.00'))) + " 元"    #价格
        strSell = str(numSell) + "股"                                       #股数
        strRetreat = str(Decimal((self.stopProfit_Retreat * 100)).quantize(Decimal('0.0'))) + "%"       #回撤
        strTrade = str(Decimal((numTrade * 10)).quantize(Decimal('0.0'))) + "成"                        #仓位
        strProfit = str(Decimal((self.setRisk.profitNow * 100)).quantize(Decimal('0.00'))) + "%"        #当前收益
        strProfitNow = str(Decimal((self.profitNow * 100)).quantize(Decimal('0.0'))) + "%"              #当前浮盈
        strMax = str(Decimal((self.setRisk.profitMax * 100)).quantize(Decimal('0.00'))) + "%"           #最高浮盈
        strMaxStage = str(Decimal((self.setRisk.profitMax_Stage * 100)).quantize(Decimal('0.00'))) + "%"#阶段浮盈-前高
        
        #触发止盈止损
        strReutrn = F"{self.setRisk.stockName}: {strPrice}"
        if(isHit):
            if(isNewLimit == False):    #第一次触发
                if(isStopProfit):   
                    strReutrn += F", 浮盈超 {strProfitNow}, 触发止盈.\r\n操作策略: 启动动态止盈.\r\n策略收益: {strProfit}."
                else:
                    strReutrn += F", 浮亏超 {strProfitNow}, 触发止损.\r\n操作策略: 启动动态止损.\r\n策略收益: {strProfit}."
            else:                       #再一次触发                
                if(isStopProfit):  
                    strTag = myData.iif(isBreakLimit, "突破新高", "阶段新高")
                    strReutrn += F", 浮盈超 {strProfitNow}, {strTag}.\r\n操作策略: 动态止盈线上移.\r\n策略收益: {strProfit}, 涨幅前高 {strMaxStage}, 最高 {strMax}."
                else:
                    strTag = myData.iif(isBreakLimit, "突破新低", "阶段新低")
                    strReutrn += F", 浮亏超 {strProfitNow}, {strTag}.\r\n操作策略: 动态止损线上移.\r\n策略收益: {strProfit}, 涨幅前高 {strMaxStage}, 最高 {strMax}."
        else:
            if(isStopProfit):   
                if(self.setRisk.stopProfit_Dynamic == False):
                    strReutrn += F", 浮盈超 {strProfitNow}.\r\n操作策略: 建议止盈, 操作 全仓, 卖出 {strSell}.\r\n策略收益: {strProfit}, 涨幅前高 {strMaxStage}, 最高 {strMax}."
                else:
                    strReutrn += F", 回撤逾 {strRetreat}.\r\n操作策略: 建议止盈, 操作 {strTrade}仓, 卖出 {strSell}.\r\n策略收益: {strProfit}, 当前浮盈: {strProfitNow}, 涨幅前高 {strMaxStage}, 最高 {strMax}."
            else:
                if(self.setRisk.stopLoss_Dynamic == False):
                    strReutrn += F", 浮亏超 {strProfitNow}.\r\n操作策略: 建议止损, 操作 全仓, 卖出 {strSell}.\r\n策略收益: {strProfit}, 涨幅前高 {strMaxStage}, 最高 {strMax}."
                else:
                    strReutrn += F", 亏损逾 {strRetreat}.\r\n操作策略: 建议止损, 操作 {strTrade}仓, 卖出 {strSell}.\r\n策略收益: {strProfit}, 当前浮盈: {strProfitNow}, 涨幅前高 {strMaxStage}, 最高 {strMax}."
        myDebug.Debug(strReutrn.replace("\r\n", ""))
        return strReutrn

    #校正回撤动态幅度 
    def checkPiofitRetreat(self):
        #默认回撤为设置值 
        self.stopProfit_Retreat = self.setRisk.stopProfit_Retreat
            
        #特殊修正
        if(1 == 1):
            #计算当前与前期高点差价
            profitStage = self.setRisk.profitMax_Stage - self.setRisk.profitMax
            
            #回撤率修正，阶段盈利为前高2倍以上，扩大回撤容忍范围为2倍，可以减少总回撤率
            if(profitStage >= (self.setRisk.stopProfit) * 3):
                self.stopProfit_Retreat = self.setRisk.stopProfit_Retreat * 3
            elif(profitStage >= (self.setRisk.stopProfit) * 2):
                self.stopProfit_Retreat = self.setRisk.stopProfit_Retreat * 2
            pass
      
        #最大回撤限制
        self.stopProfit_Retreat = myData.iif(self.stopProfit_Retreat > 0.06, 0.06, self.stopProfit_Retreat)
        return self.stopProfit_Retreat


# 风险控制操作类 
class myStockRisk_Control():
    def __init__(self):   
        self.riskDB = gol._Get_Value('zxcDB_StockRisk')
        self.stockSet = gol._Get_Value('setsStock')
        self.msgManger = gol._Get_Setting('manageMsgs')
        self.initRiskSets()
    # 初始风控设置集
    def initRiskSets(self):  
        pSets = self.riskDB.getSets(self.riskDB )
        self.dictRisk = {}
        for x in pSets:
            pSet = pSets[x]
            pRisk = self.initRiskSet(pSet['用户名'], pSet['用户标签'], pSet['标的编号'], pSet['标的名称'], False)

            #缓存
            dictRisk = self.dictRisk.get(pSet['标的编号'], {})
            dictRisk[pSet['用户名'] + "_" + pSet['用户标签']] = pRisk
            if(len(dictRisk) == 1):
                self.dictRisk[pSet['标的编号']] = dictRisk
        
    # 初始风控设置
    def initRiskSet(self, usrID, usrTag, stockID, stockName, bCheck = True):  
        #解析正确股票信息
        if(bCheck == True):
            stocks = self.stockSet._Find(stockID, stockName, "****")
            if(len(stocks) == 1):
                pStock = stocks[0]
                stockID = pStock.code_id + "." + pStock.extype2
                stockName = pStock.code_name 

        #提取风险对象
        pRisk = self.riskDB.getTradeRisk(usrID, usrTag, stockID, True)
        return pRisk
        
    # 提取风控对象
    def getRiskSet(self, usrID, usrTag, stockID, stockName, bCheck = True):  
        #解析正确股票信息
        if(bCheck):
            stocks = self.stockSet._Find(stockID, stockName, "****")
            if(len(stocks) == 1):
                pStock = stocks[0]
                stockID = pStock.code_id + "." + pStock.extype2
                stockName = pStock.code_name

        #提取
        dictRisk = self.dictRisk.get(stockID, None)
        if(dictRisk == None): return None
        return dictRisk.get(usrID, None)

    # 添加设置
    def addRiskSet(self, usrID, usrTag, stockID, stockName, stockPrice, stockNum, time = "", dictSet = {}):  
        dictSet['用户名'] = usrID  
        dictSet['用户标签'] = usrTag
        
        #解析正确股票信息
        if(True):
            stocks = self.stockSet._Find(stockID, stockName, "****")
            if(len(stocks) == 1):
                pStock = stocks[0]
                stockID = pStock.code_id + "." + pStock.extype2
                stockName = pStock.code_name

        dictSet['标的编号'] = stockID
        dictSet['标的名称'] = stockName
        dictSet['标的均价'] = stockPrice
        dictSet['标的数量'] = stockNum
        dictSet['日期'] = myData.iif(time != "", time, myData_Trans.Tran_ToDatetime_str(None, "%Y-%m-%d %H:%M:%S"))

        #添加
        strR = self.riskDB.Add_Row(dictSet, True)
        myDebug.Debug(strR)
        
    #通知接收新行情
    def notifyRisk(self, price, stockID, stockName, bSave_Auto = True):
        #提取设置字典
        dictRisk = self.dictRisk.get(stockID, None)
        if(dictRisk != None):
            for x in dictRisk:
                pRisk = dictRisk[x]
                strR = pRisk.notifyQuotation(price, bSave_Auto)

                #发送消息
                if(strR != ""):
                    msg = self.msgManger.OnCreatMsg()
                    msg["usrName"] = "@*股票风控监测群"
                    msg["msgType"] = "TEXT"
                    msg["usrPlat"] = "wx"
                    msg["msg"] = strR
                    self.msgManger.OnHandleMsg(msg, '', True)   #必须check



# 初始全局消息管理器
from myGlobal import gol 
gol._Init()                 # 先必须在主模块初始化（只在Main模块需要一次即可）
gol._Set_Value('zxcDB_StockRisk', myDataDB_StockRisk())     #实例 股票收益库对象 
gol._Get_Value('zxcDB_StockRisk').Add_Fields(['用户名', '用户标签', '标的编号', '标的名称', '标的均价', '标的数量', "标的仓位", "手续费率", '边界限制','监测定量','监测间隔','止盈线', '动态止盈', '止盈回撤', '止盈比例', '止损线', '动态止损', '止损回撤', '止盈比例', '最高价格', '成本价格', '当前价格', '卖出均价','阶段止盈','阶段止损','当前浮盈','止盈状态','止损状态', '日期', '备注', '操作统计数', '操作日志'], ['string','string','string','string','float','int','float','float','bool','bool','float','float','bool','float','float','float','bool','float','float','float','float','float','float','float','float','float','bool','bool','datetime','string','int','list'], [])
gol._Set_Value('zxcRisk_Control', myStockRisk_Control())    #实例 风险控制操作类 



#主启动程序
if __name__ == "__main__":
    #测试库表操作
    pDB = gol._Get_Value('zxcDB_StockRisk')
    pRisks = gol._Get_Value('zxcRisk_Control')
    
    # 添加买入及测试信息 sz,002547,春兴精工,CXJG,stock,CN,深圳证券交易所,XSHE
    pRisks.addRiskSet('茶叶一主号','','002547',"", 8, 10000, '2019-08-27 11:11:00', {}) 
    pRisks.addRiskSet('茶叶一主号','','300033',"", 96.943, 700, '2019-08-27 11:11:00', {}) 
    pRisks.addRiskSet('茶叶一主号','','10001832.XSHG',"50ETF购12月3000", 210.0, 20, '2019-10-23 09:31:00', {}) 
    pRisks.addRiskSet('茶叶一主号','','10002033.XSHG',"50ETF购12月2900", 300, 10, '2019-10-23 09:31:00', {}) 


    # 添加行数据
    if(1==1):
        print(pDB.Add_Row({'用户名': '茶叶一主号', '标的编号': '600001', '标的名称': "测试股票", '标的均价': '10.3', '标的数量': 5000, '止盈线': 0.08, '日期': '2019-08-27 11:11:00'}, True))
        print(pDB.Add_Row({'用户名': '茶叶一主号', '标的编号': '600001', '标的名称': "测试股票", '标的均价': '9.7', '标的数量': 5000, '日期': '2019-08-27 11:12:00'}, True))
    
        # 查询数据
        dictSet = pDB.Query("isDel==False && 用户名==茶叶一主号 && 标的编号==600001", "", True)
        pSet = mySet_StockRisk(list(dictSet.values())[0])


        # 风险监测测试
        pRisk = myMonitor_StockRisk(9.5, 10.8)
        pRisk.initSet(pSet, pDB)
        pRisk.notifyQuotation(12)     
        pRisk.notifyQuotation(11.7)     #回撤 
        pRisk.notifyQuotation(12.7)      
        pRisk.notifyQuotation(13.3)      
        pRisk.notifyQuotation(10.4)     #回撤
        pRisk.notifyQuotation(10.6)
        pRisk.notifyQuotation(10.7)     
        pRisk.notifyQuotation(10.9)     
        pRisk.notifyQuotation(10.8)     #回撤
        pRisk.notifyQuotation(10.75)     
        pRisk.notifyQuotation(10.8)     
        pRisk.notifyQuotation(10.7)     #回撤
        pRisk.notifyQuotation(10.6, False)
        pRisk.notifyQuotation(10.55, False)
        pRisk.notifyQuotation(10.5, False)
        pRisk.notifyQuotation(10.8)     
        pRisk.notifyQuotation(10.7)     #回撤
        pRisk.notifyQuotation(10.6)      
        pRisk.notifyQuotation(10.4)     
        pRisk.notifyQuotation(10.3)     

    # 期权交易测试
    pSource = gol._Get_Value('quoteSource_API', None)
    if(1 == 2):
        print("当天3000的期权信息：")
        pSource = gol._Get_Value('quoteSource_API', None)
        sources = pSource.getPrice(security='10001832.XSHG',frequency='1m',start_date='2019-11-29 09:30:00',end_date='2019-11-29 15:00:00')
    
        # 添加买入及测试信息
        print(pDB.Add_Row({'用户名': '茶叶一主号', '标的编号': '10001832.XSHG', '标的名称': "50ETF购12月3000", '标的均价': '210', '标的数量': 10, '日期': '2019-10-14 09:31:00'}, True))
    
        pRisk = pDB.getTradeRisk('茶叶一主号', '', '10001832.XSHG', True)
        for x in range(0, len(sources)):
             pRisk.notifyQuotation(sources['high'][x] * 10000)    

        print()
        
    # 期权交易测试-实时模拟
    if(1 == 2):
        #初始风险对象
        pRisk_300033 = pRisks.getRiskSet('茶叶一主号', '','300033', "", True)
        pRisk_3000 = pRisks.getRiskSet('茶叶一主号', '','10001832.XSHG', "", True)
        pRisk_3100 = pRisks.getRiskSet('茶叶一主号', '','10002033.XSHG', "", True)

        #消息初始 
        pMMsg = gol._Get_Setting('manageMsgs')
        msg = pMMsg.OnCreatMsg()
        msg["usrName"] = "@*股票风控监测群"
        msg["msgType"] = "TEXT"
        msg["usrPlat"] = "wx"

        #循环
        #dtTime = myData_Trans.Tran_ToDatetime("2019-10-23 09:30:00", "%Y-%m-%d %H:%M:%S")
        num = 1
        while(True):
            #时间参数
            #dtTime += datetime.timedelta(minutes=1)
            dtNow = myData_Trans.Tran_ToDatetime_str(None, "%Y-%m-%d %H:%M")
            dtStart = myData_Trans.Tran_ToDatetime(dtNow + ":00", "%Y-%m-%d %H:%M:%S")
            dtNext = myData_Trans.Tran_ToDatetime(dtNow + ":59", "%Y-%m-%d %H:%M:%S")
        
            #提取当前期权价格
            sources_300033 = pSource.getPrice(security='300033.XSHE',frequency='1m',start_date=dtStart,end_date=dtNext)
            sources_3000 = pSource.getPrice(security='10001832.XSHG',frequency='1m',start_date=dtStart,end_date=dtNext)
            sources_3100 = pSource.getPrice(security='10002033.XSHG',frequency='1m',start_date=dtStart,end_date=dtNext)
            if(len(sources_3100) < 1): continue
            
            priceAvg_300033 = sources_300033['money'][0] / sources_300033['volume'][0]
            priceAvg_3000 = sources_3000['money'][0] / sources_3000['volume'][0]
            priceAvg_3100 = sources_3100['money'][0] / sources_3100['volume'][0]
            print(priceAvg_300033, priceAvg_3000, priceAvg_3100, "---", dtStart)

            #风险调用
            bSave = myData.iif(num % 5 == 0, True, False)
            pRisk.notifyRisk(priceAvg_300033, '300033.XSHE', "", bSave)
            pRisk.notifyRisk(priceAvg_3000, '10001832.XSHG', "", bSave)
            pRisk.notifyRisk(priceAvg_3100, '10002033.XSHG', "", bSave)

            #延时5秒     
            time.sleep(10)
        

    #需要调整盈利对比，实际利润变动，不可靠
    print()



#开发内容：
#   1.增加风险控制交易，可以简化为按标识识别，非真实交易，真实交易需同步（非必需）。
