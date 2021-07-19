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
using zxcCore.Common;
using zxcCore.Extensions;
using zxcCore.zxcData.Analysis;
using zxcCore.zxcData.Cache.Memory;
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
        protected Quantify_Quote_EventArgs _eventArgs = null;
        //protected internal double _valueDelta = 0.0025;         //涨跌拐点判断范围

        public QuoteCheck_Risk_Quantify(string tagName, IDataCache<T> dataCache, string setting) : base(tagName, dataCache, setting)
        {
            _tagAlias = "风控提醒";
            _quoteQuantify = new Quantify_Quote(tagName, (IDataCache<Data_Quote>)dataCache);
            _quoteQuantify.Init_Index(typeIndex.CCI, 14);
            _quoteQuantify.Quantify_Quote_Trigger += new Quantify_Quote_EventHandler(EventHandler_QuantifyQuote_Trigger);
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
            if (_eventArgs != null)
            {
                DataTrend_LabelInfo pLabelInfo = _eventArgs.Data.LabelInfo;
                int nEnum = (int)pLabelInfo.DataTrend_KeyPoint;
                if (Math.Abs(nEnum) >= 5)
                {
                    string tag0 = "";
                    if (pLabelInfo.DataTrend_KeyPoint == typeDataTrend_KeyPoint.INFLECTION)
                    {
                        tag0 = pLabelInfo.DataTrend.Get_AttrName() + " " + pLabelInfo.DataTrend_KeyPoint.Get_AttrName();
                    }
                    else
                    {
                        tag0 = pLabelInfo.DataTrend.Get_Description() + " " + pLabelInfo.DataTrend_KeyPoint.Get_Description();
                    }
                    strMsg = string.Format("\n{0}：{3}({4})\n{1}({2}).", _tagAlias, tag0, this.getValue_str(pLabelInfo.Value_KeyLine).Replace("元", ""), pLabelInfo.Tag, pLabelInfo.Value_TimeType.Get_AttrName());
                }
            }
            return strMsg;
        }


        //数据分析触发事件
        protected void EventHandler_QuantifyQuote_Trigger(object sender, Quantify_Quote_EventArgs e)
        {
            //组装消息
            _eventArgs = e;
            string msg = this.getMsg_Infix();
            if (msg != "")
            {
                msg = this.getMsg_Perfix() + msg;
                msg += this.getMsg_Suffix();

                //输出、打印信息
                string usrTo = this.getUser_str(true);
                this.NotifyMsg(msg, usrTo);
                zxcConsoleHelper.Debug(true, "QuoteCheck_Risk_Quantify:: {0}   ---{1}.\n{2}", this.getMsg_Perfix(), _data.DateTime, msg);

                double profit = e.Data.LabelInfo.Value_Profit;
                var msg2 = new { DataTrend = e.Data.LabelInfo.DataTrend, DataTrend_KeyPoint = e.Data.LabelInfo.DataTrend_KeyPoint, hitLimit = e.Data.IsHitPoint, Value = e.Data.Value, Ratio = e.Data.LabelInfo.Difference_Ratio, Profit = profit };
                zxcConsoleHelper.Debug(true, "{0}", msg2.ToString());
            }
        }

    }
}
