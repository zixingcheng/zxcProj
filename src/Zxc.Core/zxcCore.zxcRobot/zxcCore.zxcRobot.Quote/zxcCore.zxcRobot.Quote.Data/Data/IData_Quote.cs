using Newtonsoft.Json.Linq;
using System;
using System.ComponentModel;
using zxcCore.Enums;
using zxcCore.Extensions;

namespace zxcCore.zxcRobot.Quote.Data
{
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
        typeTimeFrequency QuoteTimeType { get; set; }

        double Value { get; }
        double Value_RF { get; }

        bool FromJsonObj(JObject jsonData, typeTimeFrequency quoteTime);
    }

}