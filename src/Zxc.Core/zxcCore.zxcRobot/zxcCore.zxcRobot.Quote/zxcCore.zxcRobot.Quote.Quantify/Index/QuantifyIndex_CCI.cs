using System;
using System.Collections.Generic;
using System.Linq;
using zxcCore.Common;
using zxcCore.Enums;
using zxcCore.zxcData.Analysis;
using zxcCore.zxcData.Analysis.Quote;
using zxcCore.zxcData.Cache.Memory;
using zxcCore.zxcRobot.Quote.Data;

namespace zxcCore.zxcRobot.Quote.Quantify
{
    /// <summary>量化指标CCI
    /// </summary>
    public class QuantifyIndex_CCI<T> : QuantifyIndex<T> where T : Data_Quote
    {
        #region 属性及构造

        public QuantifyIndex_CCI(Dictionary<DateTime, CacheInfo<T>> dataCacheInfos, int n = 14, typeTimeFrequency timeFrequency = typeTimeFrequency.m15) :
            base(dataCacheInfos, n, timeFrequency)
        {
            //设置关键线
            this.InitTrend_KeyLine("CCI_100", 100, true, 0.191);
            this.InitTrend_KeyLine("CCI_-100", -100, true, 0.191);
        }
        ~QuantifyIndex_CCI()
        {
            // 缓存数据？
        }

        #endregion


        //数据处理--自定义
        protected override bool dataHandle_User(DataTrend_Index data, DataTrend_Index dataLast_Recursion = null)
        {
            return true;
        }
        //数据处理事件返回对象
        protected override DataAnalyse_Trend_EventArgs dataHandle_EventArgs(DataTrend_Index data)
        {
            //组装消息
            DataAnalyse_Trend_EventArgs pArgs = new DataAnalyse_Trend_EventArgs(data);

            //输出信息
            //if (data.LabelInfo.DataTrend_KeyPoint != typeDataTrend_KeyPoint.NONE)
            //{
            //    double profit = data.LabelInfo.Value_Profit;
            //    var msg = new { DataTrend = data.LabelInfo.DataTrend, DataTrend_KeyPoint = data.LabelInfo.DataTrend_KeyPoint, hitLimit = data.IsHitPoint, Value = data.Value, Ratio = data.LabelInfo.Difference_Ratio, Profit = profit };
            //    zxcConsoleHelper.Debug(true, "{0}", msg.ToString());
            //}
            return pArgs;
        }

        //创建指标计算对象
        public override QuoteIndex<T> Create_QuoteIndex()
        {
            return new zxcData.Analysis.Quote.QuoteIndex_CCI<T>(null, _N);
        }

    }

}
