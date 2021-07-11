using System;
using System.Collections.Generic;
using zxcCore.zxcData.Analysis;

namespace zxcCore.zxcRobot.Quote.Quantify
{
    /// <summary>行情量化分析过程触发事件
    /// </summary>
    /// <param name="sender"></param>
    /// <param name="e"></param>
    public delegate void Quantify_Quote_EventHandler(object sender, Quantify_Quote_EventArgs e);


    /// <summary>行情量化分析过程触发事件Args
    /// </summary>
    public class Quantify_Quote_EventArgs : DataAnalyse_Trend_EventArgs
    {
        #region 属性及构造



        public Quantify_Quote_EventArgs(DataTrend_Index data = null) : base(data)
        {
            _data = data;
        }
        ~Quantify_Quote_EventArgs()
        {
            // 缓存数据？
        }

        #endregion
    }

}