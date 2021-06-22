using System;
using zxcCore.Extensions;

namespace zxcCore.zxcRobot.Quote
{
    /// <summary>行情数据时间类型
    /// </summary>
    public enum typeQuoteTime
    {
        /// <summary>实时数据
        /// </summary>
        [EnumAttr("实时", "real")]
        real = 0,
        /// <summary>1分钟数据
        /// </summary>
        [EnumAttr("分钟", "m1")]
        m1 = 1,
        /// <summary>5分钟数据
        /// </summary>
        [EnumAttr("5分钟", "m5")]
        m5 = 2,
        /// <summary>15分钟数据
        /// </summary>
        [EnumAttr("15分钟", "m15")]
        m15 = 3,
        /// <summary>30分钟数据
        /// </summary>
        [EnumAttr("30分钟", "m30")]
        m30 = 4,
        /// <summary>60分钟数据
        /// </summary>
        [EnumAttr("60分钟", "m60")]
        m60 = 5,
        /// <summary>日数据
        /// </summary>
        [EnumAttr("日", "day")]
        day = 6,
        /// <summary>周数据
        /// </summary>
        [EnumAttr("周", "week")]
        week = 7,
        /// <summary>月数据
        /// </summary>
        [EnumAttr("月", "month")]
        month = 8,
        /// <summary>年数据
        /// </summary>
        [EnumAttr("年", "year")]
        year = 9
    }


    /// <summary>行情数据接口
    /// </summary>
    public interface IData_Quote
    {
        string StockID { get; set; }
        string StockName { get; set; }
        typeStock StockType { get; set; }
        typeStockExchange StockExchange { get; set; }

        string StockID_Tag { get; }

        double Price_Per { get; set; }
        double Price_Open { get; set; }
        double Price_Close { get; set; }

        double Price_High { get; set; }
        double Price_Low { get; set; }
        double Price_Avg { get; set; }
        double TradeTurnover { get; set; }
        double TradeValume { get; set; }

        DateTime DateTime { get; set; }
        bool IsSuspended { get; set; }

        typeQuoteTime QuoteTimeType { get; set; }
        double Value { get; }
        double Value_RF { get; }

        bool IsIndex();
    }

}