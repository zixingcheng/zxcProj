using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Linq;
using zxcCore.Common;
using zxcCore.Extensions;

namespace zxcCore.zxcData.Analysis
{
    /// <summary>数据趋势
    /// </summary>
    public enum typeDataTrend
    {
        /// <summary>下降
        /// </summary>
        [EnumAttr("下降", -1), Description("下降")]
        FALL = -1,
        /// <summary>无
        /// </summary>
        [EnumAttr("平", 0), Description("平")]
        NONE = 0,
        /// <summary>上升
        /// </summary>
        [EnumAttr("上升", 1), Description("上升")]
        RAISE = 1
    }
    /// <summary>数据趋势-详情(配合typeDataTrend使用)
    /// </summary>
    public enum typeDataTrend_Detail
    {
        /// <summary>急减速
        /// </summary>
        /// </summary>
        [EnumAttr("急减速", 2), Description("急减速")]
        SLOWTOP = -2,
        /// <summary>减缓
        /// </summary>
        /// </summary>
        [EnumAttr("减缓", 2), Description("减缓")]
        SLOWDOWN = -1,
        /// <summary>匀速
        /// </summary>
        [EnumAttr("匀速", 1), Description("匀速")]
        NONE = 0,
        /// <summary>加速
        /// </summary>
        [EnumAttr("加速", 3), Description("加速")]
        SPEEDUP = 1,
        /// <summary>急加速
        /// </summary>
        [EnumAttr("急加速", 3), Description("急加速")]
        SPEEDTOP = 2,
    }
    /// <summary>数据趋势-关键点
    /// </summary>
    public enum typeDataTrend_KeyPoint
    {
        /// <summary>非关键点
        /// </summary>
        NONE = 0,
        /// <summary>低点
        /// </summary>
        [EnumAttr("低点", 1), Description("低点")]
        MIN = 1,
        /// <summary>高点
        /// </summary>
        [EnumAttr("高点", 9), Description("高点")]
        MAX = 9,
        /// <summary>拐点
        /// </summary>
        [EnumAttr("拐点", 1), Description("拐点")]
        INFLECTION = 5,
        /// <summary>临界压力点（压力区间下限）
        /// </summary>
        [EnumAttr("临界压力点", 10), Description("临界压力点")]
        PRESSURE_NEAR = 10,
        /// <summary>压力点
        /// </summary>
        [EnumAttr("压力点", 11), Description("压力点")]
        PRESSURE = 11,
        /// <summary>突破点
        /// </summary>
        [EnumAttr("突破点", 12), Description("突破点")]
        PRESSURE_BREACH = 12,
        /// <summary>临界支撑点（支撑区间上限）
        /// </summary>
        [EnumAttr("临界支撑点", -10), Description("临界支撑点")]
        SUPPORT_NEAR = -10,
        /// <summary>支撑点
        /// </summary>
        [EnumAttr("支撑点", -11), Description("支撑点")]
        SUPPORT = -11,
        /// <summary>破位点
        /// </summary>
        [EnumAttr("破位点", -12), Description("破位点")]
        SUPPORT_CRASH = -12,
    }


    /// <summary>数据趋势标签信息
    /// </summary>
    public class DataTrend_LabelInfo
    {
        #region 属性及构造

        /// <summary>当前值标签
        /// </summary>
        public string Tag { get; set; }

        /// <summary>当前对应涨跌幅
        /// </summary>
        public double Value_Profit { get; set; }
        /// <summary>当前对应值
        /// </summary>
        public double Value { get; set; }
        /// <summary>当前对应修正值
        /// </summary>
        public double Value_Amend { get; set; }
        /// <summary>当前关键点位线值
        /// </summary>
        public double Value_KeyLine { get; set; }

        /// <summary>与前一值的差值
        /// </summary>
        public double Difference { get; set; }
        /// <summary>与前一值的差值比例
        /// </summary>
        public double Difference_Ratio { get; set; }

        /// <summary>数据趋势
        /// </summary>
        public typeDataTrend DataTrend { get; set; }
        /// <summary>数据趋势-详情(不准确，需完善)
        /// </summary>
        protected internal typeDataTrend_Detail DataTrend_Detail { get; set; }
        /// <summary>数据趋势-关键点
        /// </summary>
        public typeDataTrend_KeyPoint DataTrend_KeyPoint { get; set; }



        //protected internal Data _DataBase = null;
        //protected internal Data _DataLast = null;
        public DataTrend_LabelInfo()   //Data data, string tag = "")
        {
            //Tag = tag;
            //_DataBase = data;
        }

        #endregion

    }

}
