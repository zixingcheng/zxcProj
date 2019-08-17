#-*- coding: utf-8 -*-
"""
# 克隆自聚宽文章
#   链接：https://www.joinquant.com/post/3147
#   标题：二八轮动小市值策略改进版07年至16年4000多倍
#   作者：零零发

Created on  墨紫 2019-08-06 17:16:00   
    @version: v1.0.0
    @email:  ********@qq.com
    
市值轮动买卖策略--测试
    配置指定频率的调仓日，在调仓日每日指定时间，计算沪深300指数和中证500指数当前的20日涨
    幅，如果2个指数的20日涨幅有一个为正，则进行选股调仓，之后如此循环往复。

止损策略：
    大盘止损：(可选)
        1. 每分钟取大盘前130日的最低价和最高价，如果最高大于最低的两倍则清仓，停止交易。
        2. 每分钟判断大盘是否呈现三只黑鸦止损，如果是则当天清仓并停止交易，第二天停止交
           易一天。

    个股止损：(可选)
        每分钟判断个股是否从持仓后的最高价回撤幅度，如果超过个股回撤阈值，则平掉该股持仓

    二八止损：(必需)
        每日指定时间，计算沪深300指数和中证500指数当前的20日涨幅，如果2个指数涨幅都为负，
        则清仓，重置调仓计数，待下次调仓条件满足再操作 
"""
import datetime
from kuanke.user_space_api import * 

# 初始化相关参数
class strategy_initialize():
    def __init__(self):
        g.starttime = datetime.datetime.now()
        pass

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
        
        # 配置二八指数
        #g.index2 = '000300.XSHG'  # 沪深300指数，表示二，大盘股
        #g.index8 = '000905.XSHG'  # 中证500指数，表示八，小盘股
        g.index2 = '000016.XSHG'        # 上证50指数
        g.index8 = '399333.XSHE'        # 中小板R指数
        g.index_growth_rate_20 = 0.01   # 判定调仓的二八指数20日增幅
            
    ## 重置参数，仅针对需要当日重置的参数
    def reset_param(self):
        # 部分参数更新
        g.current_data = get_current_data()     # 提取当前的股票信息
        g.is_stock_clean = False                # 是否已经清仓
        
        # 重置当日大盘价格止损状态
        if g.is_market_stop_loss_by_price:
            g.is_day_stop_loss_by_price = False
        
            # 清空当日个股250天内最大的3日涨幅的缓存
        if g.is_stock_stop_loss or g.is_stock_stop_profit:
            g.pct_change.clear()

        # 重置三黑鸦状态
        g.is_last_day_3_black_crows = False
        if g.is_market_stop_loss_by_3_black_crows:
            g.cur_drop_minute_count = 0
        pass

    ## 初始化-股票筛选参数
    def init_check_stocks(self):
        # 按PE、EPS选股
        g.pick_by_pe = False    # 是否根据PE选股
        g.pick_by_eps = True   # 是否根据EPS选股
        #region 按PE、EPS选股
        
        # 如果根据PE选股，则配置最大和最小PE值
        if g.pick_by_pe:
            g.max_pe = 200
            g.min_pe = 0
        
        # 配置选股最小EPS值
        if g.pick_by_eps:
            g.min_eps = 0
            
        # 是否对股票评分
        g.is_rank_stock = True
        if g.is_rank_stock:
            # 参与评分的股票数目
            g.rank_stock_count = 20

        #endregion

        # 过滤配置
        g.filter_gem = True         # 配置是否过滤创业板股票
        g.filter_blacklist = True   # 配置是否过滤黑名单股票，回测建议关闭，模拟运行时开启
        g.filter_paused = True      # 是否过滤停盘
        g.filter_delisted = True    # 是否过滤退市
        g.filter_st = True          # 是否过滤

        # 股票池
        g.current_data = get_current_data()
        g.pick_stock_count = 100    # 备选股票数目
        #g.security_universe_index = ["000300.XSHG"]
        #g.security_universe_user_securities = []

        # 行业列表
        g.industry_list = ["801010","801020","801030","801040","801050","801080","801110","801120","801130","801140","801150","801160","801170","801180","801200","801210","801230","801710","801720","801730","801740","801750","801760","801770","801780","801790","801880","801890"]

        # 概念列表
        g.concept_list = []
    ## 初始化-股票筛选参数
    def init_check_stocks_sort(self):
        # 总排序准则： desc-降序、asc-升序
        #g.check_out_lists_ascending = 'desc'
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
        #g.order_style_str = 'by_cap_mean'
        #g.order_style_value = 100
    
        # 设定是否卖出buy_lists中的股票
        #g.sell_will_buy = True

        # 固定出仓的数量或者百分比
        #g.sell_by_amount = None
        #g.sell_by_percent = None

        # 获取未卖出的股票
        g.open_sell_securities = []
        pass

    ## 初始化-风险控制
    def init_risk_management(self):
        # 策略风控信号
        #g.risk_management_signal = True

        # 策略当日触发风控清仓信号
        #g.daily_risk_management = True

        # 单只最大买入股数或金额
        #g.max_buy_value = None
        #g.max_buy_amount = None

        # 配置是否个股止损/止盈
        g.is_stock_stop_loss = True
        g.is_stock_stop_profit = False
        g.is_stock_clean = False
        g.threshold_stock_stop_loss = 0.02      # 默认亏损时止损阈值
        g.is_stop_loss_threshold_auto = False   # 是否自动计算个股止损阈值
        
        # 配置是否根据大盘历史价格止损
        # 大盘指数前130日内最高价超过最低价2倍，则清仓止损
        # 注：关闭此止损，收益增加，但回撤会增加
        g.is_market_stop_loss_by_price = True
        
        # 如下参数不能更改
        if g.is_market_stop_loss_by_price:
            # 记录当日是否满足大盘价格止损条件，每日盘后重置
            g.is_day_stop_loss_by_price = False 

            # 配置价格止损判定指数，默认为上证指数，可修改为其他指数
            g.index_4_stop_loss_by_price = '000001.XSHG'

        # 配置是否开启大盘三黑鸦止损
        # 个人认为针对大盘判断三黑鸦效果并不好，首先有效三只乌鸦难以判断，准确率实际来看也不好，
        # 其次，分析历史行情看一般大盘出现三只乌鸦的时候，已经严重滞后了，使用其他止损方式可能会更好
        g.is_market_stop_loss_by_3_black_crows = False
        g.index_4_stop_loss_by_3_black_crows = '000001.XSHG'    # 配置三黑鸦判定指数，默认为上证指数，可修改为其他指数
        if g.is_market_stop_loss_by_3_black_crows:
            # 配置三黑鸦止损开启需要当日大盘为跌的分钟计数达到
            g.dst_drop_minute_count = 10            

    ## 初始化-缓存信息
    def init_cache_data(self):
        #股票评分
        if g.is_rank_stock:
            if g.rank_stock_count > g.pick_stock_count:
                g.rank_stock_count = g.pick_stock_count

        #止损、止盈则缓存个股涨幅信息
        if g.is_stock_stop_loss or g.is_stock_stop_profit:
            # 缓存当日个股250天内最大的3日涨幅，避免当日反复获取，每日盘后清空
            g.pct_change = {}

        # 缓存股票持仓价、之后的最高价、平仓价
        g.open_price = {}
        g.close_price = {}
        g.last_high = {}
        pass

# 筛选股票
class strategy_check_stocks():
    def __init__(self):
        pass
    
    # 选股操作，选取指定数目的小市值股票，再进行过滤，最终挑选指定可买数目的股票
    def pick_stocks(self, context, data):
        q = None
        # PE、EPS选股
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
    
        # 提取查询股票代码
        df = get_fundamentals(q)
        stock_list = list(df['code'])
        
        # 股票筛选过滤
        stock_list = self.filter_gem_stock(context, stock_list)         # 过滤创业版股票
        stock_list = self.filter_blacklist_stock(context, stock_list)   # 过滤黑名单股票
        
        stock_list = self.filter_paused_stock(stock_list)               # 过滤停牌股票
        stock_list = self.filter_st_stock(stock_list)                   # 过滤ST股票
        stock_list = self.filter_delisted_stock(stock_list)             # 过滤具有退市标签的股票
        stock_list = self.filter_limitup_stock(context, stock_list)     # 过滤涨停的股票
        stock_list = self.filter_limitdown_stock(context, stock_list)   # 过滤跌停的股票         
        stock_list = self.rank_stocks(data, stock_list)                 # 股票评分
        
        # 根据20日股票涨幅过滤效果不好，故注释
        # stock_list = filter_by_growth_rate(stock_list, 15)
        g.buy_stocks = stock_list
        return stock_list

    # 过滤创业版股票
    def filter_gem_stock(self, context, stock_list):
        if g.filter_gem == False: return stock_list
        return [stock for stock in stock_list if stock[0:3] != '300']
    
    # 过滤20日增长率为负的股票
    def filter_by_growth_rate(stock_list, n):
        return [stock for stock in stock_list if get_growth_rate(stock, n) > 0]
    '''
    # 过滤新股
    def filter_new_stock(stock_list):
        stocks = get_all_securities(['stock'])
        stocks = stocks[(context.current_dt.date() - stocks.start_date) > datetime.timedelta(60)].index
    '''

    # 过滤黑名单股票
    def filter_blacklist_stock(self, context, stock_list):
        if g.filter_blacklist == False: return stock_list
        blacklist = g.blacklist.get_blacklist()
        return [stock for stock in stock_list if stock not in blacklist]

    # 过滤停牌股票
    def filter_paused_stock(self, stock_list):
        if g.filter_paused == False: return stock_list
        current_data = g.current_data
        return [stock for stock in stock_list if not current_data[stock].paused]

    # 过滤ST股票
    def filter_st_stock(self, stock_list):
        if g.filter_st == False: return stock_list
        current_data = g.current_data
        return [stock for stock in stock_list 
            if not current_data[stock].is_st 
            and 'ST' not in current_data[stock].name]

    # 过滤具有退市标签的股票
    def filter_delisted_stock(self, stock_list):
        if g.filter_delisted == False: return stock_list
        current_data = g.current_data
        return [stock for stock in stock_list 
            if not current_data[stock].is_st 
            and '*' not in current_data[stock].name 
            and '退' not in current_data[stock].name]
        
    # 过滤涨停的股票
    def filter_limitup_stock(self, context, stock_list):
        last_prices = history(1, unit='1m', field='close', security_list=stock_list)
        current_data = get_current_data()
    
        # 已存在于持仓的股票即使涨停也不过滤，避免此股票再次可买，但因被过滤而导致选择别的股票
        # return [stock for stock in stock_list if stock in context.portfolio.positions.keys() 
        #    or last_prices[stock][-1] < current_data[stock].high_limit * 0.995]
        return [stock for stock in stock_list if stock in list(context.portfolio.positions.keys()) 
            or last_prices[stock][-1] < current_data[stock].high_limit]

    # 过滤跌停的股票
    def filter_limitdown_stock(self, context, stock_list):
        last_prices = history(1, unit='1m', field='close', security_list=stock_list)
        current_data = get_current_data()
    
        #return [stock for stock in stock_list if last_prices[stock][-1] > current_data[stock].low_limit]
        #return [stock for stock in stock_list if stock in context.portfolio.positions.keys() 
        #    or last_prices[stock][-1] > current_data[stock].low_limit * 1.005]
        return [stock for stock in stock_list if stock in list(context.portfolio.positions.keys()) 
            or last_prices[stock][-1] > current_data[stock].low_limit]
    
    # 股票评分
    def rank_stocks(self, data, stock_list):
        #log.debug("评分前备选股票: %s" %(stock_list))

        # 设置评分，且数据足够
        if g.is_rank_stock == False: return stock_list
        if len(stock_list) > g.rank_stock_count:
             stock_list = stock_list[:g.rank_stock_count]
        if len(stock_list) == 0: return stock_list

        # 初始结果集缓存
        dst_stocks = {}
        for stock in stock_list:
            h = attribute_history(stock, 130, unit='1d', fields=('close', 'high', 'low'), skip_paused=True)
            low_price_130 = h.low.min()
            high_price_130 = h.high.max()

            avg_15 = data[stock].mavg(15, field='close')
            cur_price = data[stock].close

            #avg_15 = h['close'][-15:].mean()
            #cur_price = get_close_price(stock, 1, '1m')

            score = (cur_price-low_price_130) + (cur_price-high_price_130) + (cur_price-avg_15)
            #score = ((cur_price-low_price_130) + (cur_price-high_price_130) + (cur_price-avg_15)) / cur_price
            dst_stocks[stock] = score
        
        # 提取评分结果数据 
        df = pd.DataFrame(list(dst_stocks.values()), index=list(dst_stocks.keys()))
        df.columns = ['score']
        #df = df.sort(columns='score', ascending=True)
        df = df.sort_values(by="score")
        
        # 选取指定可买数目的股票
        stock_list = df.index
        if len(stock_list) > g.buy_stock_count:
            stock_list = stock_list[:g.buy_stock_count]
        #log.debug("评分后备选股票: %s" %(stock_list))
        return stock_list
# 配置股票黑名单
class strategy_check_stocks_blacklist():
    def __init__(self):
        pass

    # 配置股票黑名单
    # 列出当且极不适宜购买的股票
    # 注：1. 黑名单有时效性，回测的时候最好不使用，模拟交易建议使用
    #     2. 用一模块或者大数据分析收集这类股票，定时更新
    def get_blacklist(self):
        # 黑名单一览表，更新时间 2016.7.10 by 沙米
        # 科恒股份、太空板业，一旦2016年继续亏损，直接面临暂停上市风险
        blacklist = ["600656.XSHG","300372.XSHE","600403.XSHG","600421.XSHG","600733.XSHG","300399.XSHE",
                     "600145.XSHG","002679.XSHE","000020.XSHE","002330.XSHE","300117.XSHE","300135.XSHE",
                     "002566.XSHE","002119.XSHE","300208.XSHE","002237.XSHE","002608.XSHE","000691.XSHE",
                     "002694.XSHE","002715.XSHE","002211.XSHE","000788.XSHE","300380.XSHE","300028.XSHE",
                     "000668.XSHE","300033.XSHE","300126.XSHE","300340.XSHE","300344.XSHE","002473.XSHE"]
        return blacklist
# 缓存信息
class strategy_cache_data():
    def __init__(self):
        pass

    # 获取个股前n天的m日增幅值序列
    # 增加缓存避免当日多次获取数据
    def get_pct_change(self, security, n, m):
        pct_change = None
        if security in list(g.pct_change.keys()):
            pct_change = g.pct_change[security]
        else:
            h = attribute_history(security, n, unit='1d', fields=('close'), skip_paused=True)
            pct_change = h['close'].pct_change(m)   # 3日的百分比变比（即3日涨跌幅）
            g.pct_change[security] = pct_change
        return pct_change

# 交易操作
class strategy_trade():
    def __init__(self):
        pass
    
    # 调仓时段判断
    def is_can_trade_data(self, context):
        # 获得当前时间
        hour = context.current_dt.hour
        minute = context.current_dt.minute
    
        # 每天下午14:50调仓
        if hour == g.adjust_position_hour and minute == g.adjust_position_minute:
            return True
        return False
    
    # 调仓操作
    def do_trade_data(self, context, data):
        if(self.is_can_trade_data(context) == False): return
        log.info("调仓日计数 [%d]" %(g.day_count))

        # 回看指数前20天的涨幅
        gr_index2 = g.functions.get_growth_rate(g.index2)
        gr_index8 = g.functions.get_growth_rate(g.index8)
        log.info("当前%s指数的20日涨幅 [%.2f%%]" %(get_security_info(g.index2).display_name, gr_index2*100))
        log.info("当前%s指数的20日涨幅 [%.2f%%]" %(get_security_info(g.index8).display_name, gr_index8*100))
        
        # 指数低于20日前值则清仓
        if gr_index2 <= g.index_growth_rate_20 and gr_index8 <= g.index_growth_rate_20:
            if(len(context.portfolio.positions.keys()) > 0):
                log.info("==> 清仓，指数低于20日前值")
            g.trade.clear_position(context)
            g.day_count = 0
        else: #if  gr_index2 > g.index_growth_rate_20 or ret_index8 > g.index_growth_rate_20:
            if(g.day_count % g.period == 0):                    # 调仓间隔日
                log.info("==> 满足条件进行调仓")
                g.check_stocks.pick_stocks(context, data)       # 选股

                log.info("选股后可买股票: %s" %(g.buy_stocks)) 
                self.adjust_position(context, g.buy_stocks)     # 调仓操作
            g.day_count += 1

    # 获取前n个单位时间当时的收盘价
    def get_close_price(self, security, n, unit='1d'):
        return attribute_history(security, n, unit, ('close'), True)['close'][0]
    
    # 根据待买股票创建或调整仓位
    # 对于因停牌等原因没有卖出的股票则继续持有
    # 始终保持持仓数目为g.buy_stock_count
    def adjust_position(self, context, stocks_buy):
        # 循环当前开仓标的，清仓非调仓标的
        stocks_now = list(context.portfolio.positions.keys())
        for stock in stocks_now:
            if stock not in stocks_buy:
                # 非调仓标的，清仓
                log.info("stock [%s] in position is not buyable" %(stock))
                position = context.portfolio.positions[stock]
                self.close_position(context, position)
            else:
                log.info("stock [%s] is already in position" %(stock))
    
        # 根据股票数量分仓
        #position_count = len(stocks_now)
        position_count = len(context.portfolio.positions)
        if g.buy_stock_count > position_count:
            # 此处只根据可用金额平均分配购买，不能保证每个仓位平均分配
            value = context.portfolio.cash / (g.buy_stock_count - position_count)  # @# 可以考虑非均分开仓

            # 循环标的执行开仓
            for stock in stocks_buy:
                # @# 已存在标的，处理有些简单
                #if stock not in stocks_now or context.portfolio.positions[stock].total_amount == 0:
                if context.portfolio.positions[stock].total_amount == 0:
                    if self.open_position(context, stock, value):
                        if len(context.portfolio.positions) == g.buy_stock_count:
                            break

    # 开仓，买入指定价值的证券
    # 报单成功并成交（包括全部成交或部分成交，此时成交量大于0），返回True
    # 报单失败或者报单成功但被取消（此时成交量等于0），返回False
    def open_position(self, context, security, value):
        order = self.order_target_value_(security, value)
        if order != None and order.filled > 0:
            # 报单成功并有成交则初始化最高价
            cur_price = self.get_close_price(security, 1, '1m')
            g.open_price[security] = cur_price
            g.last_high[security] = cur_price
            if(security in g.close_price):
                g.close_price.pop(security)

            # 只要有成交，无论全部成交还是部分成交，则统计
            position = context.portfolio.positions[security]
            g.trade_stat.watch(security, order.filled, position.avg_cost, position.price)
            return True
        g.is_stock_clean = (len(context.portfolio.positions) ==0)   # 是否已经清仓
        return False

    # 平仓，卖出指定持仓
    # 平仓成功并全部成交，返回True
    # 报单失败或者报单成功但被取消（此时成交量等于0），或者报单非全部成交，返回False
    def close_position(self, context, position):
        security = position.security
        order = self.order_target_value_(security, 0) # 可能会因停牌失败
        if order != None:
            if order.filled > 0:
                # 只要有成交，无论全部成交还是部分成交，则统计盈亏
                g.trade_stat.watch(security, order.filled, position.avg_cost, position.price, True)

            # 全部成交则删除相关证券的最高价缓存
            if order.status == OrderStatus.held and order.filled == order.amount:
                if security in g.last_high:
                    g.close_price[security] = position.price
                    g.last_high.pop(security)
                    g.open_price.pop(security)
                else:
                    log.warn("last high price of %s not found" %(security))
                return True

        g.is_stock_clean = (len(context.portfolio.positions) ==0)   # 是否已经清仓
        return False

    # 清空卖出所有持仓
    def clear_position(self, context):
        if context.portfolio.positions:
            log.info("==> 清仓，卖出所有股票")
            for stock in list(context.portfolio.positions.keys()):
                position = context.portfolio.positions[stock]
                self.close_position(context, position)
        g.is_stock_clean = (len(context.portfolio.positions) ==0)   # 是否已经清仓
    
    # 卖出未卖出成功的股票
    def sell_default_open_sell(self, context):
        g.open_sell_securities = list(set(g.open_sell_securities))
        open_sell_securities = [s for s in context.portfolio.positions.keys() if s in g.open_sell_securities]
        if len(open_sell_securities)>0:
            for stock in open_sell_securities:
                self.order_target_value_(stock, 0)
        g.open_sell_securities = [s for s in g.open_sell_securities if s in context.portfolio.positions.keys()]
        return

    # 自定义下单
    # 根据Joinquant文档，当前报单函数都是阻塞执行，报单函数（如order_target_value）返回即表示报单完成
    # 报单成功返回报单（不代表一定会成交），否则返回None
    def order_target_value_(self, security, value):
        if value == 0:
            log.debug("Selling out %s" % (security))
        else:
            log.debug("Order %s to value %f" % (security, value))
        
        # 如果股票停牌，创建报单会失败，order_target_value 返回None
        # 如果股票涨跌停，创建报单会成功，order_target_value 返回Order，但是报单会取消
        # 部成部撤的报单，聚宽状态是已撤，此时成交量>0，可通过成交量判断是否有成交
        return order_target_value(security, value)
# 交易信息
class strategy_trade_info():
    def __init__(self):
        self.stock = ""
        self.open_count = 0
        self.open_price = 0
        self.open_date = datetime.datetime.now()
        self.profit = 0
        self.close_price = 0
        self.close_date = datetime.datetime.now() 
# 交易信息统计
class strategy_trade_stat():
    def __init__(self):
        self.trade_total_count = 0
        self.trade_success_count = 0
        self.statis = {'win': [], 'loss': []}
        self.trade_infos = {}
    def reset(self):
        self.trade_total_count = 0
        self.trade_success_count = 0
        self.statis = {'win': [], 'loss': []}
    
    # 卖出成功后针对卖出的量进行盈亏统计
    def watch(self, stock, sold_amount, avg_cost, cur_price, bSell = False):
        # 生成交易信息
        if(bSell == False):
            trade_info = strategy_trade_info()
            trade_info.stock = stock
            trade_info.open_count = sold_amount
            trade_info.open_price = cur_price
            trade_info.open_date = datetime.datetime.now()

            # 缓存交易信息
            stock_infos = self.trade_infos.get(stock, None)
            if stock_infos == None:
                stock_infos = []
                self.trade_infos[stock] = stock_infos
            stock_infos.insert(0, trade_info)
        else:
            trade_info = self.trade_infos[stock][0]
            trade_info.profit = cur_price / trade_info.open_price - 1
            trade_info.close_price = cur_price
            trade_info.close_date = datetime.datetime.now() 
            
            # 记录交易次数便于统计胜率
            self.trade_total_count += 1
            current_value = sold_amount * cur_price
            cost = sold_amount * avg_cost
            
            # 卖出成功后针对卖出的量进行盈亏统计
            percent = round((current_value - cost) / cost * 100, 2)
            if current_value > cost:
                self.trade_success_count += 1
                win = [stock, percent]
                self.statis['win'].append(win)
            else:
                loss = [stock, percent]
                self.statis['loss'].append(loss)
 
    # 报告统计信息
    def report(self, context):
        cash = context.portfolio.cash
        totol_value = context.portfolio.portfolio_value
        position = 1 - cash / totol_value
        log.info("收盘后持仓概况:%s" % str(list(context.portfolio.positions)))
        log.info("仓位概况:%.2f" % position)
        self.print_win_rate(context.current_dt.strftime("%Y-%m-%d"), context.current_dt.strftime("%Y-%m-%d"), context)
    # 打印胜率
    def print_win_rate(self, current_date, print_date, context):
        if str(current_date) == str(print_date):
            win_rate = 0
            if 0 < self.trade_total_count and 0 < self.trade_success_count:
                win_rate = round(self.trade_success_count / float(self.trade_total_count), 3)
            most_win = self.statis_most_win_percent()
            most_loss = self.statis_most_loss_percent()
            starting_cash = context.portfolio.starting_cash
            total_profit = self.statis_total_profit(context)

            print("-")
            print('------------绩效报表------------')
            print('交易次数: {0}, 盈利次数: {1}, 胜率: {2}'.format(self.trade_total_count, self.trade_success_count, str(win_rate * 100) + str('%')))
            if len(most_win) > 0:
                print('单次盈利最高: {0}, 盈利比例: {1}%'.format(most_win['stock'], most_win['value']))
            if len(most_loss) > 0:
                print('单次亏损最高: {0}, 亏损比例: {1}%'.format(most_loss['stock'], most_loss['value']))
            print('总资产: {0}, 本金: {1}, 盈利: {2}, 盈亏比率：{3}%'.format(starting_cash + total_profit, starting_cash, total_profit, total_profit / starting_cash * 100))
            print('--------------------------------')
            print("-")

    # 统计单次盈利最高的股票
    def statis_most_win_percent(self):
        result = {}
        for statis in self.statis['win']:
            if {} == result:
                result['stock'] = statis[0]
                result['value'] = statis[1]
            else:
                if statis[1] > result['value']:
                    result['stock'] = statis[0]
                    result['value'] = statis[1]
        return result

    # 统计单次亏损最高的股票
    def statis_most_loss_percent(self):
        result = {}
        for statis in self.statis['loss']:
            if {} == result:
                result['stock'] = statis[0]
                result['value'] = statis[1]
            else:
                if statis[1] < result['value']:
                    result['stock'] = statis[0]
                    result['value'] = statis[1]
        return result

    # 统计总盈利金额    
    def statis_total_profit(self, context):
        return context.portfolio.portfolio_value - context.portfolio.starting_cash
    
# 公用函数
class strategy_functions():
    def __init__(self):
        pass
    
    # 获取股票n日以来涨幅，根据当前价计算--需要进一步完善
    def get_growth_rate(self, security, n=20):
        price_20 = self.get_close_price(security, n)         #前20日收盘价
        price_now = self.get_close_price(security, 1, '1m')  #前一分钟价
    
        # 存在时计算相对n日前的价格涨幅
        if not isnan(price_20) and not isnan(price_now) and price_20 != 0:
            return (price_now - price_20) / price_20
        else:
            log.error("数据非法, security: %s, %d日收盘价: %f, 当前价: %f" %(security, n, price_20, price_now))
            return 0
    
    # 获取前n个单位时间当时的收盘价
    def get_close_price(self, security, n, unit='1d'):
        return attribute_history(security, n, unit, ('close'), True)['close'][0]
    
    # 个股止损
    def is_need_stop_loss(self, context, data, stock, n = 3):
        if g.is_stock_clean: return False

        # 未亏损时，忽略止损
        open_price = g.open_price[stock]    # 开仓价格
        cur_price = data[stock].close       # 最新收盘价格
        if(open_price <= cur_price): return False   
        
        # 亏损比例小于默认设定值，忽略止损
        rate_loss = 1 - cur_price /open_price 
        if(rate_loss <= g.threshold_stock_stop_loss): return False   
        
        # 计算个股回撤止损阈值
        threshold = g.functions.get_stop_loss_threshold(stock, n)
        if(threshold > g.threshold_stock_stop_loss): 
            if(rate_loss <= threshold): return False   
            
        log.info("==> 个股止损, stock: %s, cur_price: %f, last_high: %f, rate_loss: %f,threshold: %f" 
            %(stock, cur_price, g.last_high[stock], rate_loss, threshold))
        return True

    # 个股止盈
    def is_need_stop_profit(self, context, data, stock, n = 3):
        if g.is_stock_clean: return False

        # 未亏损时，忽略止损
        open_price = g.open_price[stock]    # 开仓价格
        cur_price = data[stock].close       # 最新收盘价格
        if(open_price <= cur_price): return False   
        
        # 统计开仓后高值
        if g.last_high[stock] < cur_price: 
            g.last_high[stock] = cur_price
           
        


            xi = attribute_history(stock, g.period, '1d', 'high', skip_paused=True)
            ma = xi.max()
            
            threshold = g.functions.get_stop_loss_threshold(stock, g.period)
            #log.debug("个股止损阈值, stock: %s, threshold: %f" %(stock, threshold))
            if cur_price < g.last_high[stock] * (1 - threshold):
                log.info("==> 个股止损, stock: %s, cur_price: %f, last_high: %f, threshold: %f" 
                    %(stock, cur_price, g.last_high[stock], threshold))

                position = context.portfolio.positions[stock]
                if g.trade.close_position(context, position):
                    g.day_count = 0
                    g.riskLevel += 1

    # 计算个股回撤止损阈值，即个股在持仓n天内能承受的最大跌幅，返回正值
    def get_stop_loss_threshold(self, security, n = 3):
        if(g.is_stop_loss_threshold_auto): return g.threshold_stock_stop_loss

        # 算法：(个股250天内最大的n日跌幅 + 个股250天内平均的n日跌幅)/2
        pct_change = g.cache_data.get_pct_change(security, 250, n)
        #log.debug("pct of security [%s]: %s", pct)
        maxd = pct_change.min()
        #maxd = pct[pct<0].min()
        avgd = pct_change.mean()
        #avgd = pct[pct<0].mean()
        # maxd和avgd可能为正，表示这段时间内一直在增长，比如新股
        bstd = (maxd + avgd) / 2

        # 数据不足时，计算的bstd为nan
        if not isnan(bstd):
            if bstd != 0:
                return abs(bstd)
            else:
                # bstd = 0，则 maxd <= 0
                if maxd < 0:
                    # 此时取最大跌幅
                    return abs(maxd)
        return 0.03     # 默认配置回测止损阈值最大跌幅为-3.0%，阈值高貌似回撤降低
    
    # 计算个股止盈阈值
    # 算法：个股250天内最大的n日涨幅
    # 返回正值
    def get_stop_profit_threshold(self, security, n = 3):
        pct_change = g.cache_data.get_pct_change(security, 250, n)
        maxr = pct_change.max()
    
        # 数据不足时，计算的maxr为nan
        # 理论上maxr可能为负
        if (not isnan(maxr)) and maxr != 0:
            return abs(maxr)
        return 0.30 # 默认配置止盈阈值最大涨幅为20%
# 公用函数-技术指标
class strategy_functions_indexes():
    def __init__(self):
        pass
    
    # 三只乌鸦
    def is_3_black_crows(self, stock):
        # talib.CDL3BLACKCROWS

        # 三只乌鸦说明来自百度百科
        # 1. 连续出现三根阴线，每天的收盘价均低于上一日的收盘
        # 2. 三根阴线前一天的市场趋势应该为上涨
        # 3. 三根阴线必须为长的黑色实体，且长度应该大致相等
        # 4. 收盘价接近每日的最低价位
        # 5. 每日的开盘价都在上根K线的实体部分之内；
        # 6. 第一根阴线的实体部分，最好低于上日的最高价位
        #
        # 算法
        # 有效三只乌鸦描述众说纷纭，这里放宽条件，只考虑1和2
        # 根据前4日数据判断
        # 3根阴线跌幅超过4.5%

        h = attribute_history(stock, 4, '1d', ('close','open'), skip_paused=True, df=False)
        h_close = list(h['close'])
        h_open = list(h['open'])

        if len(h_close) < 4 or len(h_open) < 4:
            return False
 
        # 三根阴线
        if h_close[-4] > h_open[-4] \
            and (h_close[-1] < h_close[-2] and h_close[-2] < h_close[-3]) \
            and (h_close[-1] < h_open[-1] and h_close[-2]< h_open[-2] and h_close[-3] < h_open[-3]) \
            and h_close[-1] / h_close[-3] - 1 < -0.045 and get_current_data(stock)< h_close[-1]*0.995:
            return True
        return False
    '''
     # 一阳三阴
        if h_close[-4] > h_open[-4] \
            and (h_close[-1] < h_open[-1] and h_close[-2]< h_open[-2] and h_close[-3] < h_open[-3]):
            #and (h_close[-1] < h_close[-2] and h_close[-2] < h_close[-3]) \
            #and h_close[-1] / h_close[-3] - 1 < -0.045:
            return True
        return False
    '''  
    '''
    def is_3_black_crows(stock, data):
        # talib.CDL3BLACKCROWS
        his =  attribute_history(stock, 2, '1d', ('close','open'), skip_paused=True, df=False)
        closeArray = list(his['close'])
        closeArray.append(data[stock].close)
        openArray = list(his['open'])
        openArray.append(get_current_data()[stock].day_open)

        if closeArray[0]<openArray[0] and closeArray[1]<openArray[1] and closeArray[2]<openArray[2]:
            if closeArray[-1]/closeArray[0]-1>-0.045:
                his2 =  attribute_history(stock, 4, '1d', ('close','open'), skip_paused=True, df=False)
                closeArray1 = his2['close']
                if closeArray[0]/closeArray1[0]-1>0:
                    return True
        return False
    '''
    
# 交易风险控制
class strategy_risk_management():
    def __init__(self):
        pass
    # 风险控制(0:正常，-1:清仓)
    def risk_control(self, context, data):
        # data = get_current_data()
        g.riskLevel = 0
        
        # 交易止损
        self.do_stops_loss(context, data)

        # 交易止盈
        self.do_stops_profit(context, data) 
        pass
            
    # 交易止损
    def do_stops_loss(self, context, data): 
        # 特殊止损
        self.do_stop_loss_by_market_index(context)          # 大盘历史指数止损
        self.do_stop_loss_by_market_3_black_crows(context)  # 大盘三黑鸦止损

        # 全部个股止损
        self.do_stop_loss(context, data)    
        pass

    # 交易止盈
    def do_stops_profit(self, context, data):
        if g.is_stock_stop_profit == False: return
        
        # 全部个股止盈
        self.do_stop_profit(context, data) 
        
        # 特殊止盈
        pass

    # 个股止损
    def do_stop_loss(self, context, data):
        if g.is_stock_clean: return 

        # 循环所有持仓个股，止损
        for stock in list(context.portfolio.positions.keys()):
            # 判断个股是否需要止损
            if (g.functions.is_need_stop_loss(context, data, stock, g.period) == False):
                continue
            
            # 个股止损
            position = context.portfolio.positions[stock]
            if g.trade.close_position(context, position):
                g.day_count = 0
                g.riskLevel += 1 
    
    # 个股止盈
    def do_stop_profit(self, context, data):
        for stock in list(context.portfolio.positions.keys()):
            position = context.portfolio.positions[stock]
            cur_price = data[stock].close
            threshold = g.functions.get_stop_profit_threshold(stock, g.period)
            #log.debug("个股止盈阈值, stock: %s, threshold: %f" %(stock, threshold))
            if cur_price > position.avg_cost * (1 + threshold):
                log.info("==> 个股止盈, stock: %s, cur_price: %f, avg_cost: %f, threshold: %f" 
                    %(stock, cur_price, g.last_high[stock], threshold))

                position = context.portfolio.positions[stock]
                if g.trade.close_position(context, position):
                    g.day_count = 0
    
    # 大盘历史指数止损
    def do_stop_loss_by_market_index(self, context, index=""):
        if g.is_stock_clean: return 
        if g.is_market_stop_loss_by_price == False: return
        if index == "": index = g.index_4_stop_loss_by_price

        # 大盘指数前130日内最高价超过最低价2倍，则清仓止损
        # 基于历史数据判定，因此若状态满足，则当天都不会变化
        # 增加此止损，回撤降低，收益降低
        if not g.is_day_stop_loss_by_price:
            h = attribute_history(index, 160, unit='1d', fields=('close', 'high', 'low'), skip_paused=True)
            low_price_130 = h.low.min()
            high_price_130 = h.high.max()
            if high_price_130 > 2.2 * low_price_130 and h['close'][-1]<h['close'][-4]*1 and  h['close'][-1]> h['close'][-100]:
                # 当日第一次输出日志
                log.info("==> 大盘止损，%s指数前130日内最高价超过最低价2倍, 最高价: %f, 最低价: %f" %(get_security_info(index).display_name, high_price_130, low_price_130))
                g.is_day_stop_loss_by_price = True 

        # 清仓止损
        if g.is_day_stop_loss_by_price:
            g.trade.clear_position(context)
            g.day_count = 0
        return g.is_day_stop_loss_by_price

    # 大盘三黑鸦止损
    def do_stop_loss_by_market_3_black_crows(self, context, index="", n=0):
        if g.is_stock_clean: return 
        if g.is_market_stop_loss_by_3_black_crows == False: return
        
        # 前日三黑鸦，累计当日每分钟涨幅<0的分钟计数
        # 如果分钟计数超过一定值，则开始进行三黑鸦止损
        # 避免无效三黑鸦乱止损
        if g.is_last_day_3_black_crows:
            # 默认参数初始
            if index == "": index = g.index_4_stop_loss_by_3_black_crows
            if n == 0: n = g.dst_drop_minute_count

            # 获取指数涨幅
            if get_growth_rate(index, 1) < 0:
                g.cur_drop_minute_count += 1
            if g.cur_drop_minute_count >= n:
                if g.cur_drop_minute_count == n:
                    log.info("==> 超过三黑鸦止损开始")

                # 清仓止损
                g.trade.clear_position(context)
                g.day_count = 0
                return True
        return False

# 交易信息日志
class strategy_log():
    def __init__(self):
        pass
    
    # 当前惨数信息日志
    def log_param(self):
        log.info("调仓日频率: %d日" %(g.period))
        log.info("调仓时间: %s:%s" %(g.adjust_position_hour, g.adjust_position_minute))

        log.info("备选股票数目: %d" %(g.pick_stock_count))

        log.info("是否根据PE选股: %s" %(g.pick_by_pe))
        if g.pick_by_pe:
            log.info("选股最大PE: %s" %(g.max_pe))
            log.info("选股最小PE: %s" %(g.min_pe))

        log.info("是否根据EPS选股: %s" %(g.pick_by_eps))
        if g.pick_by_eps:
            log.info("选股最小EPS: %s" %(g.min_eps))
    
        log.info("是否过滤创业板股票: %s" %(g.filter_gem))
        log.info("是否过滤黑名单股票: %s" %(g.filter_blacklist))
        if g.filter_blacklist:
            log.info("当前股票黑名单：%s" %str(g.blacklist.get_blacklist()))

        log.info("是否对股票评分选股: %s" %(g.is_rank_stock))
        if g.is_rank_stock:
            log.info("评分备选股票数目: %d" %(g.rank_stock_count))

        log.info("买入股票数目: %d" %(g.buy_stock_count))

        log.info("二八指数之二: %s - %s" %(g.index2, get_security_info(g.index2).display_name))
        log.info("二八指数之八: %s - %s" %(g.index8, get_security_info(g.index8).display_name))
        log.info("判定调仓的二八指数20日增幅: %.1f%%" %(g.index_growth_rate_20*100))

        log.info("是否开启大盘历史高低价格止损: %s" %(g.is_market_stop_loss_by_price))
        if g.is_market_stop_loss_by_price:
            log.info("大盘价格止损判定指数: %s - %s" %(g.index_4_stop_loss_by_price, get_security_info(g.index_4_stop_loss_by_price).display_name))

        log.info("大盘三黑鸦止损判定指数: %s - %s" %(g.index_4_stop_loss_by_3_black_crows, get_security_info(g.index_4_stop_loss_by_3_black_crows).display_name))
        log.info("是否开启大盘三黑鸦止损: %s" %(g.is_market_stop_loss_by_3_black_crows))
        if g.is_market_stop_loss_by_3_black_crows:
            log.info("三黑鸦止损开启需要当日大盘为跌的分钟计数达到: %d" %(g.dst_drop_minute_count))

        log.info("是否开启个股止损: %s" %(g.is_stock_stop_loss))
        log.info("是否开启个股止盈: %s" %(g.is_stock_stop_profit))
        

# 初始化函数，相关参数初始等等
def initialize(context):    
    # 初始日志
    log.info("==> initializing @ %s", str(context.current_dt))

    # 初始化相关参数
    g.init = strategy_initialize()
    g.init.init_param()                # 初始化-基础参数
    g.init.init_check_stocks()         # 初始化-股票筛选参数
    g.init.init_check_stocks_sort()    # 初始化-股票筛选参数
    g.init.init_trading()              # 初始化-股票买卖设置
    g.init.init_risk_management()      # 初始化-风险控制
    g.init.init_cache_data()           # 初始化-缓存信息

    # 加载公有函数（）
    g.functions = strategy_functions()
    g.func_indexes = strategy_functions_indexes()   # 指标计算类
    g.cache_data = strategy_cache_data()            # 缓存信息
    
    # 配置股票黑名单
    g.blacklist = strategy_check_stocks_blacklist()
    g.check_stocks = strategy_check_stocks()
    
    # 加载交易、交易统计模块
    g.trade = strategy_trade()
    g.trade_stat = strategy_trade_stat()

    # 加载交易风控模块
    g.risk_management = strategy_risk_management()
    
    # 加载日志模块
    g.log = strategy_log()
    
    # 运行函数
    #run_daily(sell_every_day,'open')           #卖出未卖出成功的股票
    #run_daily(risk_management, 'every_bar')    #风险控制
    #run_daily(check_stocks, 'open')            #选股
    #run_daily(trade, 'open')                   #交易
    #run_daily(selled_security_list_count, 'after_close') #卖出股票日期计数
    #run_daily(do_trading_data, 'every_bar')     #盘中交易（分钟级别）
    
    # 初始日志
    g.log.log_param()                           # 打印策略参数
    log.info("==> initialized @ %s", str(context.current_dt))

# 开盘前运行策略(可选)
def before_trading_start(context):
    log.info("---------------------------------------------")
    log.info("==> before trading start @ %s", str(context.current_dt))

    # 盘前就判断三黑鸦状态，因为判断的数据为前4日
    g.is_last_day_3_black_crows = g.func_indexes.is_3_black_crows(g.index_4_stop_loss_by_3_black_crows)
    if g.is_last_day_3_black_crows:
        log.info("==> 前4日已经构成三黑鸦形态")
        
    # 卖出未卖出成功的股票
    g.trade.sell_default_open_sell(context)
    g.is_stock_clean = (len(context.portfolio.positions) ==0)   # 是否已经清仓
    pass

# 盘中运行-按分钟回测
def handle_data(context, data):
    # 风控监测
    g.risk_management.risk_control(context, data)
    
    # 每天调仓操作  
    g.trade.do_trade_data(context, data)

# 收盘后运行策略(可选)  
def after_trading_end(context):
    g.trade_stat.report(context)

    # 重置当日参数
    g.init.reset_param()
    
    # 得到当前未完成订单
    orders = get_open_orders()
    for _order in list(orders.values()):
        log.info("canceled uncompleted order: %s" %(_order.order_id))
    log.info("==> after trading end @ %s, 耗时 %s 秒", str(context.current_dt), str((datetime.datetime.now() - g.starttime).seconds))
    pass
