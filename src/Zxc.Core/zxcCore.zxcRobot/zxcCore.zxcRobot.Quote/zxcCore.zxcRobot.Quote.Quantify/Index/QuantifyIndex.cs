using zxcCore.Enums;
using zxcCore.zxcData.Cache.Memory;
using zxcCore.zxcRobot.Quote.Data;
using System;
using System.Collections.Generic;
using zxcCore.Extensions;
using System.ComponentModel;
using zxcCore.zxcData.Analysis;
using zxcCore.zxcData.Analysis.Quote;
using System.Linq;

namespace zxcCore.zxcRobot.Quote.Quantify
{
    /// <summary>指标类型
    /// </summary>
    public enum typeIndex
    {
        /// <summary>无
        /// </summary>
        none = 0,
        [EnumAttr("CCI指标", typeof(QuantifyIndex_CCI<Data_Quote>)), Description("CCI指标")]
        /// <summary>zxc聚宽API
        /// </summary>
        CCI = 1
    }


    /// <summary>量化指标基类
    /// </summary>
    public class QuantifyIndex : DataAnalyse_Trend
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


        public QuantifyIndex(int n = 14, typeTimeFrequency timeFrequency = typeTimeFrequency.m15) : base("QuantifyIndex", timeFrequency)
        {
            _Tag = "指标 基类";
            _N = n;
        }

        #endregion


        /// <summary>计算所有
        /// </summary>
        /// <returns></returns>
        public virtual bool Calculate_All(bool isLastData = false)
        {
            return true;
        }
        /// <summary>计算指定时间指标
        /// </summary>
        /// <param name="dtNow"></param>
        /// <param name="data">当前时间数据</param>
        /// <returns></returns>
        public virtual double Calculate(DateTime dtNow, Data_Quote data = null, bool isLastData = false)
        {
            return double.NaN;
        }
        /// <summary>计算检查
        /// </summary>
        /// <returns></returns>
        public virtual bool Calculate_Check(DateTime dtNow)
        {
            return true;
        }

        /// <summary>缓存指标值
        /// </summary>
        /// <param name="dIndex"></param>
        /// <param name="dtNow"></param>
        /// <returns></returns>
        public virtual bool CacheIndex(double dIndex, DateTime dtNow, bool isLastData = false)
        {
            return true;
        }
    }


    /// <summary>量化指标基类
    /// </summary>
    public class QuantifyIndex<T> : QuantifyIndex where T : Data_Quote
    {
        #region 属性及构造

        protected internal Dictionary<DateTime, CacheInfo<T>> _DataCacheInfos = null;
        protected internal Dictionary<DateTime, double> _valueIndexs = null;
        public QuantifyIndex(Dictionary<DateTime, CacheInfo<T>> dataCacheInfos, int n = 14, typeTimeFrequency timeFrequency = typeTimeFrequency.m15) :
            base(n, timeFrequency)
        {
            _DataCacheInfos = dataCacheInfos;
            _valueIndexs = new Dictionary<DateTime, double>();
        }
        ~QuantifyIndex()
        {
            // 缓存数据？
        }

        #endregion


        /// <summary>计算所有
        /// </summary>
        /// <returns></returns>
        public override bool Calculate_All(bool isLastData = false)
        {
            //提取可用计算时间，并循环计算
            List<DateTime> lstTime = _DataCacheInfos.Keys.OrderByDescending(e => e).Take(_DataCacheInfos.Count - _N).ToList();
            lstTime.Reverse();      //调整为升序

            bool bResult = true;
            foreach (var item in lstTime)
            {
                bResult = bResult && this.Calculate(item, null, isLastData) != double.NaN;
            }
            return bResult;
        }
        /// <summary>计算指定时间指标
        /// </summary>
        /// <param name="dtNow"></param>
        /// <param name="data">当前时间数据</param>
        /// <returns></returns>
        public override double Calculate(DateTime dtNow, Data_Quote data = null, bool isLastData = false)
        {
            //忽略已经计算
            if (!this.Calculate_Check(dtNow))
                return _valueIndexs[dtNow];

            //筛选指定时间指标计算数据
            List<CacheInfo<T>> lstQuote = _DataCacheInfos.Values.Where(e => e.DateTime <= dtNow).OrderByDescending(e => e.DateTime).Take(_N).ToList();

            //初始指标计算对象
            QuoteIndex<T> pIndex_CCI = this.Create_QuoteIndex();
            if (pIndex_CCI.Init(lstQuote))
            {
                //指标计算
                double dIndex = pIndex_CCI.Calculate();

                this.CacheIndex(dIndex, dtNow, isLastData);
                return Math.Round(dIndex, 4);
            }
            return double.NaN;
        }
        /// <summary>计算检查
        /// </summary>
        /// <returns></returns>
        public override bool Calculate_Check(DateTime dtNow)
        {
            if (_valueIndexs.ContainsKey(dtNow))
                return false;
            return true;
        }

        /// <summary>创建指标计算对象
        /// </summary>
        /// <returns></returns>
        public virtual QuoteIndex<T> Create_QuoteIndex()
        {
            return null;
        }


        //数据处理--自定义
        protected override bool dataHandle_User(DataTrend_Index data, DataTrend_Index dataLast_Recursion = null)
        {
            return true;
        }
        //数据处理事件返回对象
        protected override DataAnalyse_Trend_EventArgs dataHandle_EventArgs(DataTrend_Index data)
        {
            return base.dataHandle_EventArgs(data);
        }


        /// <summary>缓存指标值
        /// </summary>
        /// <param name="dIndex"></param>
        /// <param name="dtNow"></param>
        /// <returns></returns>
        public override bool CacheIndex(double dIndex, DateTime dtNow, bool isLastData = false)
        {
            _valueIndexs[dtNow] = dIndex;

            //初始信息
            if (!_IsInited)
            {
                double dValue = (int)(dIndex / 10) * 10;

                this.setConsoleState(false);
                this.Init(dValue, dtNow, 0.191, dValue, dValue, 19.1, 0.02, 38.2);
            }
            return this.Analysis(dIndex, dtNow, !isLastData);
        }

    }

}
