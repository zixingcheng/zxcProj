using System;
using System.Collections.Generic;

namespace zxcCore.zxcData.DataAnalysis
{
    /// <summary>分析标识类型
    /// </summary>
    public enum typeKeyPoints
    {
        /// <summary>无操作
        /// </summary>
        NONE = -99,
        /// <summary>下降
        /// </summary>
        FALL = -1,
        /// <summary>拐点
        /// </summary>
        BREAK = 0,
        /// <summary>上升
        /// </summary>
        RAISE = 1
    }
    /// <summary>分析标识类型-细分
    /// </summary>
    public enum typeKeyPoints_detail
    {
        /// <summary>无操作
        /// </summary>
        NONE = -99,
        /// <summary>下降波动
        /// </summary>
        FALL_WAVE = -11,
        /// <summary>下降拐点
        /// </summary>
        FALL_BREAK = -10,
        /// <summary>下降
        /// </summary>
        FALL = -1,
        /// <summary>拐点
        /// </summary>
        BREAK = 0,
        /// <summary>上升
        /// </summary>
        RAISE = 1,
        /// <summary>上升拐点
        /// </summary>
        RAISE_BREAK = 10,
        /// <summary>上升波动
        /// </summary>
        RAISE_WAVE = 11
    }

    /// <summary>数据分析过程触发事件
    /// </summary>
    /// <param name="sender"></param>
    /// <param name="e"></param>
    public delegate void DataAnalyse_KeyPoints_EventHandler(object sender, DataAnalyse_KeyPoints_EventArgs e);


    /// <summary>数据分析过程触发事件Args
    /// </summary>
    public class DataAnalyse_KeyPoints_EventArgs : EventArgs
    {
        #region 属性及构造

        public typeKeyPoints MonitorType = typeKeyPoints.NONE;
        public typeKeyPoints_detail MonitorType2 = typeKeyPoints_detail.NONE;
        public double Value = 0;

        public DataAnalyse_KeyPoints_EventArgs()
        {
        }
        ~DataAnalyse_KeyPoints_EventArgs()
        {
            // 缓存数据？
        }

        #endregion
    }

}