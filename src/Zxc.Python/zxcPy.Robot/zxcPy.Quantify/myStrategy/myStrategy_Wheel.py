#-*- coding: utf-8 -*-
"""
# 克隆自聚宽文章
#   链接：https://www.joinquant.com/post/3147
#   标题：二八轮动小市值策略改进版07年至16年4000多倍
#   作者：零零发

Created on  墨紫 2019-08-06 17:16:00   
    @version: v1.0.0
    @email:  ********@qq.com
    
市值轮动买卖策略--

    配置指定频率的调仓日，在调仓日每日指定时间，计算沪深300指数和中证500指数当前的20日涨
    幅，如果2个指数的20日涨幅有一个为正，则进行选股调仓，之后如此循环往复。

止损策略：
    个股止损：(可选)
        每分钟判断个股是否从持仓后的最高价回撤幅度，如果超过个股回撤阈值，则平掉该股持仓
"""
from kuanke.user_space_api import *



# 初始化相关参数
class strategy_initialize():
    def __init__(self):
        self.trade_total_count = 0
        self.trade_success_count = 0
        self.statis = {'win': [], 'loss': []}

    ## 初始化-基础参数
    def init_param(self):
        # 设置基准指数：沪深300指数 '000300.XSHG'
        set_benchmark('000300.XSHG')
        # 设定滑点百分比，系统默认的滑点是PriceRelatedSlippage(0.00246)
        #set_slippage(FixedSlippage(0.004))
        # 设定成交量比例
        #set_option('order_volume_ratio', 1)
        # 股票类交易手续费是：买入时佣金万分之三，卖出时佣金万分之三加千分之一印花税, 每笔交易佣金最低扣5块钱
        set_order_cost(OrderCost(open_tax=0, close_tax=0.001, open_commission=0.0003, close_commission=0.0003, min_commission=5), type='stock')
        # True为开启动态复权模式，使用真实价格交易
        set_option('use_real_price', True)
    
    ## 重置参数，仅针对需要当日重置的参数
    def reset_param(self):
        #if g.is_market_stop_loss_by_price:
            # 重置当日大盘价格止损状态
        #    g.is_day_stop_loss_by_price = False
        pass

    ## 初始化-股票筛选参数
    def init_check_stocks(self):
        # 备选股票数目
        g.pick_stock_count = 100

        # 是否根据PE选股
        g.pick_by_pe = False
        # 如果根据PE选股，则配置最大和最小PE值
        if g.pick_by_pe:
            g.max_pe = 200
            g.min_pe = 0
            
        # 是否根据EPS选股
        g.pick_by_eps = True
        # 配置选股最小EPS值
        if g.pick_by_eps:
            g.min_eps = 0

        # 是否过滤停盘
        g.filter_paused = True
        # 是否过滤退市
        g.filter_delisted = True
        # 是否只有ST
        g.only_st = False
        # 是否过滤ST
        g.filter_st = True

        # 股票池
        g.security_universe_index = ["000300.XSHG"]
        g.security_universe_user_securities = []

        # 行业列表
        g.industry_list = ["801010","801020","801030","801040","801050","801080","801110","801120","801130","801140","801150","801160","801170","801180","801200","801210","801230","801710","801720","801730","801740","801750","801760","801770","801780","801790","801880","801890"]

        # 概念列表
        g.concept_list = []

    ## 初始化-股票筛选参数
    def init_check_stocks_sort(self):
        # 总排序准则： desc-降序、asc-升序
        g.check_out_lists_ascending = 'desc'
        pass

    ## 初始化-股票买卖设置
    def init_trading(self):
        # 调仓频率，单位：日
        g.period = 3
        # 调仓日计数器，单位：日
        g.day_count = 0
        # 配置调仓时间（24小时分钟制）
        g.adjust_position_hour = 14
        g.adjust_position_minute = 50
        
        # 买入股票数目
        g.buy_stock_count = 2
        # 是否可重复买入
        g.filter_holded = False

        # 委托类型
        g.order_style_str = 'by_cap_mean'
        g.order_style_value = 100
    
        # 设定是否卖出buy_lists中的股票
        g.sell_will_buy = True

        # 固定出仓的数量或者百分比
        g.sell_by_amount = None
        g.sell_by_percent = None
        pass

    ## 初始化-风险控制
    def init_risk_management(self):
        # 策略风控信号
        g.risk_management_signal = True

        # 策略当日触发风控清仓信号
        g.daily_risk_management = True

        # 单只最大买入股数或金额
        g.max_buy_value = None
        g.max_buy_amount = None

        # 配置是否个股止损/止盈
        g.is_stock_stop_loss =False
        g.is_stock_stop_profit = False

    ## 初始化-缓存信息
    def init_cache_data(self):
        #股票评分
        #if g.is_rank_stock:
        #    if g.rank_stock_count > g.pick_stock_count:
        #        g.rank_stock_count = g.pick_stock_count

        #止损、止盈则缓存个股涨幅信息
        if g.is_stock_stop_loss or g.is_stock_stop_profit:
            # 缓存当日个股250天内最大的3日涨幅，避免当日反复获取，每日盘后清空
            g.pct_change = {}

        # 缓存股票持仓后的最高价
        g.last_high = {}
        pass
    
# 筛选股票
class strategy_check_stocks():
    def __init__(self):
        pass
    
    # 选股操作，选取指定数目的小市值股票，再进行过滤，最终挑选指定可买数目的股票
    def pick_stocks(self, context, data):
        q = None
        if g.pick_by_pe:
            if g.pick_by_eps:
                q = query(valuation.code).filter(
                    indicator.eps > g.min_eps,
                    valuation.pe_ratio > g.min_pe,
                    valuation.pe_ratio < g.max_pe
                ).order_by(
                    valuation.market_cap.asc()
                ).limit(
                    g.pick_stock_count
                )
            else:
                q = query(valuation.code).filter(
                    valuation.pe_ratio > g.min_pe,
                    valuation.pe_ratio < g.max_pe
                ).order_by(
                    valuation.market_cap.asc()
                ).limit(
                    g.pick_stock_count
                )
        else:
            if g.pick_by_eps:
                q = query(valuation.code).filter(
                    indicator.eps > g.min_eps
                ).order_by(
                    valuation.market_cap.asc()
                ).limit(
                    g.pick_stock_count
                )
            else:
                q = query(valuation.code).order_by(
                    valuation.market_cap.asc()
                ).limit(
                    g.pick_stock_count
                )
    
        df = get_fundamentals(q)
        g.buy_stocks = list(df['code'])
        return g.buy_stocks

    ## 股票筛选
    def check_stocks(self, context, data):
        if g.check_stocks_days%g.check_stocks_refresh_rate != 0:
            # 计数器加一
            g.check_stocks_days += 1
            return

        # 计数器归一
        g.check_stocks_days = 1
        return

# 交易操作
class strategy_trade():
    def __init__(self):
        pass
    
    # 调仓时段判断
    def is_do_handle_data(self, context, data):
        # 获得当前时间
        hour = context.current_dt.hour
        minute = context.current_dt.minute
    
        # 每天下午14:50调仓
        if hour == g.adjust_position_hour and minute == g.adjust_position_minute:
            return True
        return False
    
    # 调仓操作
    def do_handle_data(self, context, data):
        if(self.is_do_handle_data(context, data) == False):
            return False

        # 回看指数前20天的涨幅
        log.info("调仓日计数 [%d]" %(g.day_count))
        #gr_index2 = get_growth_rate(g.index2)
        #gr_index8 = get_growth_rate(g.index8)
        #log.info("当前%s指数的20日涨幅 [%.2f%%]" %(get_security_info(g.index2).display_name, gr_index2*100))
        #log.info("当前%s指数的20日涨幅 [%.2f%%]" %(get_security_info(g.index8).display_name, gr_index8*100))

        #if gr_index2 <= g.index_growth_rate_20 and gr_index8 <= g.index_growth_rate_20:
        #    clear_position(context)
        #    g.day_count = 0
        #else: #if  gr_index2 > g.index_growth_rate_20 or ret_index8 > g.index_growth_rate_20:
        if(True):
            if g.day_count % g.period == 0:
                #self.clear_position(context) #清仓

                log.info("==> 满足条件进行调仓")
                #buy_stocks = self.pick_stocks(context, data)
                log.info("选股后可买股票: %s" %(g.buy_stocks))
                self.adjust_position(context, g.buy_stocks)
            g.day_count += 1
    

    # 获取前n个单位时间当时的收盘价
    def get_close_price(self, security, n, unit='1d'):
        return attribute_history(security, n, unit, ('close'), True)['close'][0]
    
    # 根据待买股票创建或调整仓位
    # 对于因停牌等原因没有卖出的股票则继续持有
    # 始终保持持仓数目为g.buy_stock_count
    def adjust_position(self, context, buy_stocks):
        for stock in list(context.portfolio.positions.keys()):
            if stock not in buy_stocks:
                log.info("stock [%s] in position is not buyable" %(stock))
                position = context.portfolio.positions[stock]
                self.close_position(position)
            else:
                log.info("stock [%s] is already in position" %(stock))
    
        # 根据股票数量分仓
        # 此处只根据可用金额平均分配购买，不能保证每个仓位平均分配
        position_count = len(context.portfolio.positions)
        if g.buy_stock_count > position_count:
            value = context.portfolio.cash / (g.buy_stock_count - position_count)

            for stock in buy_stocks:
                if context.portfolio.positions[stock].total_amount == 0:
                    if self.open_position(stock, value):
                        if len(context.portfolio.positions) == g.buy_stock_count:
                            break

    # 开仓，买入指定价值的证券
    # 报单成功并成交（包括全部成交或部分成交，此时成交量大于0），返回True
    # 报单失败或者报单成功但被取消（此时成交量等于0），返回False
    def open_position(self, security, value):
        order = order_target_value(security, value)
        if order != None and order.filled > 0:
            # 报单成功并有成交则初始化最高价
            cur_price = self.get_close_price(security, 1, '1m')
            g.last_high[security] = cur_price
            return True
        return False

    # 平仓，卖出指定持仓
    # 平仓成功并全部成交，返回True
    # 报单失败或者报单成功但被取消（此时成交量等于0），或者报单非全部成交，返回False
    def close_position(self, position):
        security = position.security
        order = order_target_value(security, 0) # 可能会因停牌失败
        if order != None:
            #if order.filled > 0:
                # 只要有成交，无论全部成交还是部分成交，则统计盈亏
                #g.trade_stat.watch(security, order.filled, position.avg_cost, position.price)

            if order.status == OrderStatus.held and order.filled == order.amount:
                # 全部成交则删除相关证券的最高价缓存
                if security in g.last_high:
                    g.last_high.pop(security)
                else:
                    log.warn("last high price of %s not found" %(security))
                return True
        return False

    # 清空卖出所有持仓
    def clear_position(self, context):
        if context.portfolio.positions:
            log.info("==> 清仓，卖出所有股票")
            for stock in list(context.portfolio.positions.keys()):
                position = context.portfolio.positions[stock]
                self.close_position(position)


# 交易信息统计
class strategy_trade_stat():
    def __init__(self):
        pass

# 交易风险控制
class strategy_risk_management():
    def __init__(self):
        pass
    # 风险控制(0:正常，-1:清仓)
    def risk_control(self):
        g.riskLevel = 0
        pass
    
    # 交易操作(调仓)
    def do_trades_control(self, context, data):
        log.info("调仓日计数 [%d]" %(g.day_count))
    
        # 回看指数前20天的涨幅
        gr_index2 = get_growth_rate(g.index2)
        gr_index8 = get_growth_rate(g.index8)
        log.info("当前%s指数的20日涨幅 [%.2f%%]" %(get_security_info(g.index2).display_name, gr_index2*100))
        log.info("当前%s指数的20日涨幅 [%.2f%%]" %(get_security_info(g.index8).display_name, gr_index8*100))

        if gr_index2 <= g.index_growth_rate_20 and gr_index8 <= g.index_growth_rate_20:
            clear_position(context)
            g.day_count = 0
        else: #if  gr_index2 > g.index_growth_rate_20 or ret_index8 > g.index_growth_rate_20:
            if g.day_count % g.period == 0:
                log.info("==> 满足条件进行调仓")
                #buy_stocks = pick_stocks(context, data)
                log.info("选股后可买股票: %s" %(g.buy_stocks))
                adjust_position(context, g.buy_stocks)
            g.day_count += 1

    # 交易风险控制
    def do_stops_riskcontrol(self, context, data):
        # 交易止损
        do_stop_loss(context, data)

        # 交易止盈
        do_stop_profit(context, data)
        pass

    # 交易止损
    def do_stops_loss(self, context, data):
        # 交易止损实现...
        pass

    # 交易止盈
    def do_stops_profit(self, context, data):
        # 交易止盈实现...
        pass

    # 个股止损
    def stock_stop_loss(self, context, data):
        for stock in list(context.portfolio.positions.keys()):
            cur_price = data[stock].close
            xi = attribute_history(stock, 2, '1d', 'high', skip_paused=True)
            ma = xi.max()
            if g.last_high[stock] < cur_price:
                g.last_high[stock] = cur_price
            
            threshold = get_stop_loss_threshold(stock, g.period)
            #log.debug("个股止损阈值, stock: %s, threshold: %f" %(stock, threshold))
            if cur_price < g.last_high[stock] * (1 - threshold):
                log.info("==> 个股止损, stock: %s, cur_price: %f, last_high: %f, threshold: %f" 
                    %(stock, cur_price, g.last_high[stock], threshold))

                position = context.portfolio.positions[stock]
                if close_position(position):
                    g.day_count = 0

    # 个股止盈
    def stock_stop_profit(context, data):
        for stock in list(context.portfolio.positions.keys()):
            position = context.portfolio.positions[stock]
            cur_price = data[stock].close
            threshold = get_stop_profit_threshold(stock, g.period)
            #log.debug("个股止盈阈值, stock: %s, threshold: %f" %(stock, threshold))
            if cur_price > position.avg_cost * (1 + threshold):
                log.info("==> 个股止盈, stock: %s, cur_price: %f, avg_cost: %f, threshold: %f" 
                    %(stock, cur_price, g.last_high[stock], threshold))

                position = context.portfolio.positions[stock]
                if close_position(position):
                    g.day_count = 0


# 交易信息日志
class strategy_log():
    def __init__(self):
        pass



# 初始化函数，相关参数初始等等
def initialize(context):    
    # 初始日志
    log.info("==> initialize @ %s", str(context.current_dt))

    # 初始化相关参数
    g.init = strategy_initialize()
    g.init.init_param()                # 初始化-基础参数
    g.init.init_check_stocks()         # 初始化-股票筛选参数
    g.init.init_check_stocks_sort()    # 初始化-股票筛选参数
    g.init.init_trading()              # 初始化-股票买卖设置
    g.init.init_risk_management()      # 初始化-风险控制
    g.init.init_cache_data()           # 初始化-缓存信息
    
    # 配置股票黑名单
    # g.blacklist = strategy_check_stocks_blacklist()
    g.check_stocks = strategy_check_stocks()
    
    # 加载交易、交易统计模块
    g.trade = strategy_trade()
    g.trade_stat = strategy_trade_stat()

    # 加载交易风控模块
    g.risk_management = strategy_risk_management()
    
    # 加载日志模块
    g.log = strategy_log()
    
    # 运行函数
    #run_daily(sell_every_day,'open')        #卖出未卖出成功的股票
    #run_daily(risk_management, 'every_bar') #风险控制
    #run_daily(check_stocks, 'open')         #选股
    #run_daily(trade, 'open')                #交易
    #run_daily(selled_security_list_count, 'after_close') #卖出股票日期计数
    run_daily(do_trade_data, 'every_bar')   #盘中交易（分钟级别）
    
    # 初始日志
    log.info("==> initialized @ %s", str(context.current_dt))

# 开盘前运行策略(可选)
def before_trading_start(context):
    log.info("---------------------------------------------")
    #log.info("==> before trading start @ %s", str(context.current_dt))

    # 盘前就判断三黑鸦状态，因为判断的数据为前4日
    #g.is_last_day_3_black_crows = is_3_black_crows(g.index_4_stop_loss_by_3_black_crows)
    #if g.is_last_day_3_black_crows:
    #    log.info("==> 前4日已经构成三黑鸦形态")
    pass

# 盘中运行-按分钟回测
def do_trade_data(context, data):
    # 风控监测
    g.risk_management.risk_control()
    
    # 每天调仓操作 
    if(g.riskLevel == 0):
        g.check_stocks.pick_stocks(context, data)
        g.trade.do_handle_data(context, data)

# 收盘后运行策略(可选)  
def after_trading_end(context):
    #log.info("==> after trading end @ %s", str(context.current_dt))
    #g.trade_stat.report(context)

    # 重置当日参数
    g.init.reset_param()
    
    # 得到当前未完成订单
    #orders = get_open_orders()
    #for _order in list(orders.values()):
    #    log.info("canceled uncompleted order: %s" %(_order.order_id))
    pass
