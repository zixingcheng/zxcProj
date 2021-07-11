using System;
using System.Collections.Generic;
using System.Linq;
using zxcCore.Common;
using zxcCore.Extensions;
using zxcCore.zxcData.Analysis;
using zxcCore.zxcData.Cache.Memory;
using zxcCore.zxcRobot.Quote;
using zxcCore.zxcRobot.Quote.Data;

namespace zxcCore.zxcRobot.Monitor.DataCheck
{
    /// <summary>数据检查-风险监测信息
    /// </summary>
    public class QuoteCheck_Risk<T> : DataCheck_Quote<T> where T : Data_Quote
    {
        #region 属性及构造

        //数据分析对象 
        protected internal DataAnalyse_Trend _dataAnalyse = null;
        protected DataAnalyse_Trend_EventArgs _eventArgs = null;
        protected internal double _valueDelta = 0.0025;         //涨跌拐点判断范围

        public QuoteCheck_Risk(string tagName, IDataCache<T> dataCache, string setting) : base(tagName, dataCache, setting)
        {
            _tagAlias = "风控提醒";
            _dataAnalyse = new DataAnalyse_Trend(tagName);
            _dataAnalyse.DataAnalyse_Trend_Trigger += new DataAnalyse_Trend_EventHandler(EventHandler_DataAnalyse_Trigger);
        }
        ~QuoteCheck_Risk()
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

            //数据初始
            if (!this._dataAnalyse.IsInited)
            {
                //修正最小生效间隔
                double valueDelta = _data.IsIndex() ? _valueDelta * 1.5 : _data.GetStockType() == typeStock.Option ? _valueDelta * 20.0 : _valueDelta * 3;
                this._dataAnalyse.Init(_data.Price_Per, zxcTimeHelper.checkTimeH(dtTime).AddMinutes(25), valueDelta, _data.Price_High, _data.Price_Low);
                return true;
            }
            else
            {
                this._dataAnalyse.Analysis(_data.Value, dtTime);
            }
            return bResult;
        }


        protected internal new string getMsg_Infix()
        {
            string strMsg = "";
            if (_eventArgs != null)
            {
                DataTrend_LabelInfo pLabelInfo = _eventArgs.Data.LabelInfo;
                if (pLabelInfo.DataTrend_KeyPoint == typeDataTrend_KeyPoint.INFLECTION)
                {
                    string tag0 = pLabelInfo.DataTrend.Get_Description() + pLabelInfo.DataTrend_KeyPoint.Get_Description();
                    strMsg = string.Format("\n{0}：{1}({2}).", _tagAlias, tag0, this.getValue_str(pLabelInfo.Value));
                }
            }
            return strMsg;
        }


        //数据分析触发事件
        protected void EventHandler_DataAnalyse_Trigger(object sender, DataAnalyse_Trend_EventArgs e)
        {
            _eventArgs = e;
            //zxcConsoleHelper.Debug(true, "{0}:: {1}", DateTime.Now, e.Data.LabelInfo.DataTrend_KeyPoint.ToString());

            //组装消息
            string msg = this.getMsg_Infix();
            if (msg != "")
            {
                msg = this.getMsg_Perfix() + msg;
                msg += this.getMsg_Suffix();

                //输出、打印信息
                string usrTo = this.getUser_str();
                this.NotifyMsg(msg, usrTo);
                zxcConsoleHelper.Debug(true, "DataCheck_Risk:: {0}   ---{1}.\n{2}", this.getMsg_Perfix(), _data.DateTime, msg);
            }
        }

    }
}
