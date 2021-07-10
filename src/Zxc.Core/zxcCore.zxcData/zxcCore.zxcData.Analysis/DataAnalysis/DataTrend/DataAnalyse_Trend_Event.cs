using System;
using System.Collections.Generic;

namespace zxcCore.zxcData.Analysis
{
    /// <summary>数据分析过程触发事件
    /// </summary>
    /// <param name="sender"></param>
    /// <param name="e"></param>
    public delegate void DataAnalyse_Trend_EventHandler(object sender, DataAnalyse_Trend_EventArgs e);


    /// <summary>数据分析过程触发事件Args
    /// </summary>
    public class DataAnalyse_Trend_EventArgs : EventArgs
    {
        #region 属性及构造

        /// <summary>有效差值范围
        /// </summary>
        protected internal DataTrend_Index _data = null;
        public DataTrend_Index Data { get { return _data; } }


        public DataAnalyse_Trend_EventArgs()
        {
        }
        ~DataAnalyse_Trend_EventArgs()
        {
            // 缓存数据？
        }

        #endregion
    }

}