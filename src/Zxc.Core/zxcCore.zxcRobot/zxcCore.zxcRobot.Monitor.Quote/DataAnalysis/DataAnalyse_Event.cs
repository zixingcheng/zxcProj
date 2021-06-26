using System;
using System.Collections.Generic;

namespace zxcCore.zxcRobot.DataAnalysis
{
    /// <summary>分析标识类型
    /// </summary>
    public enum typeMonitor
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
    public enum typeMonitor2
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
    public delegate void DataAnalyse_EventHandler(object sender, DataAnalyse_EventArgs e);


    /// <summary>数据分析过程触发事件Args
    /// </summary>
    public class DataAnalyse_EventArgs : EventArgs
    {
        #region 属性及构造

        protected internal typeMonitor MonitorType = typeMonitor.NONE;
        protected internal typeMonitor2 MonitorType2 = typeMonitor2.NONE;
        protected internal double Value = 0;

        public DataAnalyse_EventArgs()
        {
        }
        ~DataAnalyse_EventArgs()
        {
            // 缓存数据？
        }

        #endregion
    }

}