using System;
using System.Collections.Generic;
using zxcCore.Extensions;

namespace zxcCore.Enums
{
    /// <summary>时间间隔枚举
    /// </summary>
    public enum typeTimeFrequency
    {
        /// <summary>实时数据
        /// </summary>
        [EnumAttr("无", "none"), EnumValue(0)]
        none = 0,
        /// <summary>实时数据
        /// </summary>
        [EnumAttr("实时", "real"), EnumValue(1)]
        real = 1,
        /// <summary>实时数据
        /// </summary>
        [EnumAttr("半分钟", ""), EnumValue(30)]
        s30 = 2,
        /// <summary>1分钟数据
        /// </summary>
        [EnumAttr("分钟", "1m"), EnumValue(60)]
        m1 = 3,
        /// <summary>5分钟数据
        /// </summary>
        [EnumAttr("5分钟", "5m"), EnumValue(300)]
        m5 = 4,
        /// <summary>10分钟数据
        /// </summary>
        [EnumAttr("10分钟", ""), EnumValue(600)]
        m10 = 5,
        /// <summary>15分钟数据
        /// </summary>
        [EnumAttr("15分钟", "15m"), EnumValue(900)]
        m15 = 6,
        /// <summary>30分钟数据
        /// </summary>
        [EnumAttr("30分钟", "30m"), EnumValue(1800)]
        m30 = 7,
        /// <summary>60分钟数据
        /// </summary>
        [EnumAttr("60分钟", "60m"), EnumValue(3600)]
        m60 = 8,
        /// <summary>120分钟数据
        /// </summary>
        [EnumAttr("120分钟", "120m"), EnumValue(7200)]
        m120 = 9,
        /// <summary>日数据
        /// </summary>
        [EnumAttr("日", "1d"), EnumValue(86400)]
        day = 10,
        /// <summary>周数据
        /// </summary>
        [EnumAttr("周", "1w"), EnumValue(604800)]
        week = 11,
        /// <summary>月数据
        /// </summary>
        [EnumAttr("月", "1M"), EnumValue(2464000)]
        month = 12,
        /// <summary>年数据
        /// </summary>
        [EnumAttr("年", "1Y"), EnumValue(31536000)]
        year = 13
    }

}
