using Newtonsoft.Json.Linq;
using System;
using System.ComponentModel;
using zxcCore.Extensions;

namespace zxcCore.zxcRobot.Quote.Data
{
    /// <summary>行情数据时间类型
    /// </summary>
    public enum typeQuoteTime
    {
        /// <summary>实时数据
        /// </summary>
        [EnumAttr("无", "none")]
        none = 0,
        /// <summary>实时数据
        /// </summary>
        [EnumAttr("实时", "real")]
        real = 1,
        /// <summary>1分钟数据
        /// </summary>
        [EnumAttr("分钟", "1m")]
        m1 = 2,
        /// <summary>5分钟数据
        /// </summary>
        [EnumAttr("5分钟", "5m")]
        m5 = 3,
        /// <summary>15分钟数据
        /// </summary>
        [EnumAttr("15分钟", "15m")]
        m15 = 4,
        /// <summary>30分钟数据
        /// </summary>
        [EnumAttr("30分钟", "30m")]
        m30 = 5,
        /// <summary>60分钟数据
        /// </summary>
        [EnumAttr("60分钟", "60m")]
        m60 = 6,
        /// <summary>120分钟数据
        /// </summary>
        [EnumAttr("120分钟", "120m")]
        m1200 = 7,
        /// <summary>日数据
        /// </summary>
        [EnumAttr("日", "1d")]
        day = 8,
        /// <summary>周数据
        /// </summary>
        [EnumAttr("周", "1w")]
        week = 9,
        /// <summary>月数据
        /// </summary>
        [EnumAttr("月", "1M")]
        month = 10,
        /// <summary>年数据
        /// </summary>
        [EnumAttr("年", "1Y")]
        year = 11
    }

    /// <summary>行情数据来源类型
    /// </summary>
    public enum typeQuotePlat
    {
        /// <summary>无
        /// </summary>
        none = 0,
        [EnumAttr("zxc聚宽API", true), Description("zxc聚宽API")]
        /// <summary>zxc聚宽API
        /// </summary>
        JQDataAPI_zxc = 1,
        [EnumAttr("聚宽API", true), Description("聚宽API")]
        /// <summary>聚宽API
        /// </summary>
        JQDataAPI = 2,
        [EnumAttr("新浪API", false), Description("新浪API")]
        /// <summary>新浪API
        /// </summary>
        SinaAPI = 3
    }


    /// <summary>行情数据接口-基础数据
    /// </summary>
    public interface IData_Quote
    {
        double Price_Per { get; set; }
        double Price_Open { get; set; }
        double Price_Close { get; set; }

        double Price_Limit_H { get; set; }
        double Price_Limit_L { get; set; }

        double Price_High { get; set; }
        double Price_Low { get; set; }
        double Price_Avg { get; set; }
        double TradeTurnover { get; set; }
        double TradeValume { get; set; }

        DateTime DateTime { get; set; }
        bool IsSuspended { get; set; }

        typeQuotePlat QuotePlat { get; set; }
        typeQuoteTime QuoteTimeType { get; set; }

        double Value { get; }
        double Value_RF { get; }

        bool FromJson(JObject jsonData, typeQuoteTime quoteTime);
    }

}