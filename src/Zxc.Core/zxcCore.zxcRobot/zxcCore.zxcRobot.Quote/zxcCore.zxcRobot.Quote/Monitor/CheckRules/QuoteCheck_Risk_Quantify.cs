//===============================================================================
// Copyright @ 2021 Guangzhou Yijian Life Technology Co.,Ltd. All rights reserved.
// Copyright @ 2021 广州易简生活科技有限公司.  版权所有.
//===============================================================================
// 文件名称： 
// 功能描述：QuoteCheck_Risk_Quantify --行情风险监测-量化
// 创建标识：zxc   2021-07-04
// 修改标识： 
// 修改描述：
//===============================================================================
using System;
using System.Collections.Generic;
using System.Linq;
using zxcCore.zxcData.Cache.Memory;
using zxcCore.Common;
using zxcCore.zxcData.Analysis;
using zxcCore.zxcRobot.Quote;
using zxcCore.zxcRobot.Quote.Data;
using zxcCore.zxcRobot.Quote.Quantify;

namespace zxcCore.zxcRobot.Monitor.DataCheck
{
    /// <summary>数据检查-风险监测量化信息
    /// </summary>
    public class QuoteCheck_Risk_Quantify<T> : DataCheck_Quote<T> where T : Data_Quote
    {
        #region 属性及构造

        //量化分析对象 
        protected internal Quantify_Quote _quoteQuantify = null;
        //protected DataAnalyse_KeyPoints_EventArgs _eventArgs = null;
        //protected internal double _valueDelta = 0.0025;         //涨跌拐点判断范围

        public QuoteCheck_Risk_Quantify(string tagName, IDataCache<T> dataCache, string setting) : base(tagName, dataCache, setting)
        {
            _tagAlias = "风控提醒";
            _quoteQuantify = new Quantify_Quote(tagName, (IDataCache<Data_Quote>)dataCache);
            _quoteQuantify.Init_Index(typeIndex.CCI, 14);

            //_dataAnalyse = new DataAnalyse_KeyPoints(tagName);
            //_dataAnalyse.DataAnalyse_Trigger += new DataAnalyse_KeyPoints_EventHandler(EventHandler_DataAnalyse_Trigger);
        }
        ~QuoteCheck_Risk_Quantify()
        {
            // 缓存数据？
        }

        #endregion


        public override bool CheckData()
        {
            return true;
        }
        public override bool CheckData(DateTime dtTime, T data, IDataCache<T> dataCache = null)
        {
            bool bResult = base.CheckData(dtTime, data, dataCache);

            //量化分析处理
            bResult = _quoteQuantify.Calculate(dtTime, _data);
            return bResult;
        }


        protected internal new string getMsg_Infix()
        {
            string strMsg = "";
            //if (_eventArgs != null)
            //{
            //    if (_eventArgs.MonitorType == typeKeyPoints.BREAK)
            //    {
            //        string tag0 = _eventArgs.MonitorType2 > 0 ? "上涨拐点" : "下降拐点";
            //        strMsg = string.Format("\n{0}：{1}({2}).", _tagAlias, tag0, this.getValue_str(_eventArgs.Value));
            //    }
            //}
            return strMsg;
        }


        //数据分析触发事件
        protected void EventHandler_DataAnalyse_Trigger(object sender, DataAnalyse_KeyPoints_EventArgs e)
        {
            //_eventArgs = e;
            //zxcConsoleHelper.Debug(true, "{0}:: {1}", DateTime.Now, e.MonitorType.ToString());

            ////组装消息
            //string msg = this.getMsg_Infix();
            //if (msg != "")
            //{
            //    msg = this.getMsg_Perfix() + msg;
            //    msg += this.getMsg_Suffix();

            //    //输出、打印信息
            //    string usrTo = this.getUser_str();
            //    this.NotifyMsg(msg, usrTo);
            //    zxcConsoleHelper.Debug(true, "DataCheck_Risk:: {0}   ---{1}.\n{2}", this.getMsg_Perfix(), _data.DateTime, msg);
            //}
        }

    }
}
