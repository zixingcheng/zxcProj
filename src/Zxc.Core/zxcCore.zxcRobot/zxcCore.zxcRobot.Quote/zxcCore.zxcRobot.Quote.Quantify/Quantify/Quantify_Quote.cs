//===============================================================================
// Copyright @ 2021 Guangzhou Yijian Life Technology Co.,Ltd. All rights reserved.
// Copyright @ 2021 广州易简生活科技有限公司.  版权所有.
//===============================================================================
// 文件名称： 
// 功能描述：Quantify_Quote --行情量化分析
// 创建标识：zxc   2021-07-04
// 修改标识： 
// 修改描述：
//===============================================================================
using System;
using System.Collections.Generic;
using zxcCore.Common;
using zxcCore.Extensions;
using zxcCore.zxcData.Analysis;
using zxcCore.zxcData.Cache.Memory;
using zxcCore.zxcRobot.Quote.Data;

namespace zxcCore.zxcRobot.Quote.Quantify
{
    /// <summary>行情量化分析
    /// </summary>
    public class Quantify_Quote
    {
        #region 属性及构造

        /// <summary行情量化分析事件
        /// </summary>
        public event Quantify_Quote_EventHandler Quantify_Quote_Trigger;


        protected internal IDataCache<Data_Quote> _DataCache = null;           //缓存数据对象
        protected internal Dictionary<typeIndex, QuantifyIndex> _QuantifyIndexs = null;
        public Quantify_Quote(string tagName, IDataCache<Data_Quote> dataCache)
        {
            _QuantifyIndexs = new Dictionary<typeIndex, QuantifyIndex>();
            _DataCache = dataCache;
        }

        #endregion



        /// <summary>初始指标对象
        /// </summary>
        /// <param name="typeIndex"></param>
        /// <param name="n">指标时间步长</param>
        /// <returns></returns>
        public virtual bool Init_Index(typeIndex typeIndex, int n = 14)
        {
            if (_DataCache == null) return false;
            QuantifyIndex pIndex = this.Get_Index(typeIndex);

            //初始指标对象
            if (pIndex == null)
            {
                pIndex = (QuantifyIndex)zxcReflectionHelper.CreateObj<Data_Quote>((Type)typeIndex.Get_AttrValue(), new object[] { _DataCache.DataCaches, n, _DataCache.DataCache_Set.Time_Frequency });
                pIndex.DataAnalyse_Trend_Trigger += new DataAnalyse_Trend_EventHandler(DataAnalyse_QuantifyIndex_EventHandler);

                //分析全部
                pIndex.Calculate_All(true);
                _QuantifyIndexs[typeIndex] = pIndex;
            }
            return true;
        }
        //提取量化因子对象
        public virtual QuantifyIndex Get_Index(typeIndex typeIndex)
        {
            QuantifyIndex pIndex = null;
            if (!_QuantifyIndexs.TryGetValue(typeIndex, out pIndex))
            {
                return null;
            }
            return pIndex;
        }


        //数据监测实现（具化数据对象及缓存）-观察者模式
        public virtual bool Calculate(DateTime dtTime, Data_Quote data)
        {
            bool bResult = true;
            foreach (KeyValuePair<typeIndex, QuantifyIndex> quoteIndex in _QuantifyIndexs)
            {
                bResult = bResult && (quoteIndex.Value.Calculate(dtTime, data) != double.NaN);
            }
            return bResult;
        }


        //量化因子触发事件
        protected internal void DataAnalyse_QuantifyIndex_EventHandler(object sender, DataAnalyse_Trend_EventArgs e)
        {
            //Console.WriteLine(DateTime.Now + "::");
            if (e.Data.LabelInfo.DataTrend_KeyPoint != typeDataTrend_KeyPoint.NONE)
            {
                //触发处理事件
                this.dataHandle_Event(e.Data);
            }
        }

        //量化因子处理事件
        protected virtual bool dataHandle_Event(DataTrend_Index data)
        {
            //组装消息
            if (data.IsValid && this.Quantify_Quote_Trigger != null)
            {
                Quantify_Quote_EventArgs pArgs = this.dataHandle_EventArgs(data);
                this.Quantify_Quote_Trigger(this, pArgs);
                return true;
            }
            return true;
        }
        //数量化因子事件返回对象
        protected virtual Quantify_Quote_EventArgs dataHandle_EventArgs(DataTrend_Index data)
        {
            //组装消息
            Quantify_Quote_EventArgs pArgs = new Quantify_Quote_EventArgs(data);

            //输出信息
            //if (true)
            //{
            //    double profit = data.LabelInfo.Value_Profit;
            //    var msg = new { DataTrend = data.LabelInfo.DataTrend, DataTrend_KeyPoint = data.LabelInfo.DataTrend_KeyPoint, hitLimit = data.IsHitPoint, Value = data.Value, Ratio = data.LabelInfo.Difference_Ratio, Profit = profit };
            //    zxcConsoleHelper.Debug(true, "{0}", msg.ToString());
            //}
            return pArgs;
        }

    }
}
