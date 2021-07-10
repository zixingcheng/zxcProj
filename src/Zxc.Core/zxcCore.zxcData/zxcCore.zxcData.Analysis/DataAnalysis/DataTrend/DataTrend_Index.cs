using System;
using System.Collections.Generic;
using System.Linq;

namespace zxcCore.zxcData.Analysis
{
    /// <summary>数据趋势对象-指标
    /// </summary>
    /// 
    public class DataTrend_Index : Data
    {
        #region 属性及构造

        protected internal string _Tag = "";
        /// <summary>当前标签（对应指标名称）
        /// </summary>
        public string Tag { get { return _Tag; } }

        protected internal bool _IsVirtual = false;
        /// <summary>是否虚拟值
        /// </summary>
        public virtual bool IsVirtual { get { return _IsVirtual; } }
        protected internal bool _IsHitPoint = false;
        /// <summary>是否固定分隔点
        /// </summary>
        public virtual bool IsHitPoint { get { return _IsHitPoint; } }



        protected internal DataTrend_LabelInfo _LabelInfo = null;
        /// <summary>标签信息
        /// </summary>
        public virtual DataTrend_LabelInfo LabelInfo { get { return _LabelInfo; } }


        protected internal DataAnalyse_Trend _DataAnalyse_Trend = null;                 //数据分析对象(注入)
        protected internal DataTrend_Index _DataTrend_Index_Last = null;                //前值
        protected internal DataTrend_Index _DataTrend_Index_VirtualBase = null;         //绑定对象（虚拟对象是存在）
        public DataTrend_Index(double value, DateTime time, DataAnalyse_Trend dataAnalyse_Index, DataTrend_Index dataVBase = null) : base(value, time)
        {
            _Tag = "DataIndex";
            _IsVirtual = dataVBase != null;
            _DataAnalyse_Trend = dataAnalyse_Index;
            _DataTrend_Index_VirtualBase = dataVBase;
            _LabelInfo = new DataTrend_LabelInfo();
        }

        #endregion


        /// <summary>初始前值信息 
        /// </summary>
        /// <param name="dataLast">前一个值</param>
        /// <returns></returns>
        public virtual bool InitLastValue(DataTrend_Index dataLast)
        {
            _DataTrend_Index_Last = dataLast;
            return true;
        }


    }

}
