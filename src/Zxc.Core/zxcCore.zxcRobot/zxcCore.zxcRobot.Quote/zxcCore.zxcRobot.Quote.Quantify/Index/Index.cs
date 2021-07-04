using zxcCore.Enums;
using zxcCore.zxcData.Cache.Memory;
using zxcCore.zxcRobot.Quote.Data;
using System;
using System.Collections.Generic;
using zxcCore.Extensions;
using System.ComponentModel;

namespace zxcCore.zxcRobot.Quote.Quantify
{
    /// <summary>指标类型
    /// </summary>
    public enum typeIndex
    {
        /// <summary>无
        /// </summary>
        none = 0,
        [EnumAttr("CCI指标", typeof(Index_CCI<Data_Quote>)), Description("CCI指标")]
        /// <summary>zxc聚宽API
        /// </summary>
        CCI = 1
    }


    /// <summary>行情指标基类
    /// </summary>
    public class Index
    {
        #region 属性及构造

        public string _Tag = "";
        /// <summary>标识
        /// </summary>
        public string Tag { get { return _Tag; } }

        public int _N = 14;
        /// <summary>N日
        /// </summary>
        public int N { get { return _N; } }


        public typeTimeFrequency _QuoteTimeType;
        /// <summary>数据时间类型
        /// </summary>
        public typeTimeFrequency QuoteTimeType { get { return _QuoteTimeType; } }


        public Index(int n = 14, typeTimeFrequency timeFrequency = typeTimeFrequency.m15)
        {
            _Tag = "指标 基类";
            _N = n;
            _QuoteTimeType = timeFrequency;
        }

        #endregion


        /// <summary>计算所有
        /// </summary>
        /// <returns></returns>
        public virtual bool Calculate_All()
        {
            return true;
        }
        /// <summary>计算当前
        /// </summary>
        /// <returns></returns>
        public virtual double Calculate()
        {
            return double.NaN;
        }
        /// <summary>计算指定时间指标
        /// </summary>
        /// <param name="dtNow"></param>
        /// <param name="data">当前时间数据</param>
        /// <returns></returns>
        public virtual double Calculate(DateTime dtNow, Data_Quote data = null)
        {
            return double.NaN;
        }

        /// <summary>缓存指标值
        /// </summary>
        /// <param name="dIndex"></param>
        /// <param name="dtNow"></param>
        /// <returns></returns>
        public virtual bool CacheIndex(double dIndex, DateTime dtNow)
        {
            return true;
        }
    }


    /// <summary>行情指标基类
    /// </summary>
    public class Index<T> : Index where T : Data_Quote
    {
        #region 属性及构造

        protected internal Dictionary<DateTime, CacheInfo<T>> _DataCacheInfos = null;
        protected internal Dictionary<DateTime, double> _valueIndexs = null;
        public Index(Dictionary<DateTime, CacheInfo<T>> dataCacheInfos, int n = 14, typeTimeFrequency timeFrequency = typeTimeFrequency.m15) :
            base(n, timeFrequency)
        {
            _DataCacheInfos = dataCacheInfos;
            _valueIndexs = new Dictionary<DateTime, double>();
        }
        ~Index()
        {
            // 缓存数据？
        }

        #endregion

    }

}
