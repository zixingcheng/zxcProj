using System;
using System.Collections.Generic;
using System.Linq;
using zpCore.zpDataCache.Memory;
using zxcCore.zxcRobot.DataAnalysis;
using zxcCore.Common;
using zxcCore.zxcRobot.Quote;

namespace zxcCore.zxcRobot.Monitor.DataCheck
{
    /// <summary>数据检查-风险监测信息
    /// </summary>
    public class DataCheck_Risk<T> : DataCheck_Quote<T>
    {
        #region 属性及构造

        //数据分析对象 
        protected internal DataAnalyse _dataAnalyse = null;
        protected DataAnalyse_EventArgs _eventArgs = null;

        public DataCheck_Risk(string tagName, IDataCache<T> dataCache, string setting) : base(tagName, dataCache, setting)
        {
            _tagAlias = "风控提醒";
            _dataAnalyse = new DataAnalyse(tagName);
            _dataAnalyse.DataAnalyse_Trigger += new DataAnalyse_EventHandler(EventHandler_DataAnalyse_Trigger);
        }
        ~DataCheck_Risk()
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
            if (this._dataAnalyse.Datas.Values.Count == 0)
            {
                this._dataAnalyse.Init(_data.Price_Per, _data.Price_Per, zxcTimeHelper.checkTimeH(dtTime).AddMinutes(25), _data.Price_High, _data.Price_Low, 0.0025);
                return true;
            }
            else
            {
                this._dataAnalyse.Analysis(_data.Value, dtTime);
            }
            return bResult;
        }


        protected internal override string getMsg_Infix()
        {
            string strMsg = "";
            if (_eventArgs != null)
            {
                if (_eventArgs.MonitorType == typeMonitor.BREAK)
                {
                    string tag0 = _eventArgs.MonitorType2 > 0 ? "上涨拐点" : "下降拐点";
                    strMsg = string.Format("\n{0}：{1}({2}).", _tagAlias, tag0, Math.Round(_eventArgs.Value, 3));
                }
            }
            return strMsg;
        }


        //数据分析触发事件
        protected void EventHandler_DataAnalyse_Trigger(object sender, DataAnalyse_EventArgs e)
        {
            _eventArgs = e;
            zxcConsoleHelper.Debug(true, "{0}:: {1}", DateTime.Now, e.MonitorType.ToString());

            //组装消息
            string msg = this.getMsg_Infix();
            if (msg != "")
            {
                msg = this.getMsg_Perfix() + msg;
                msg += this.getMsg_Suffix();

                //输出、打印信息
                string usrTo = _data.StockType == typeStock.Option ? "期权行情" : _data._isIndex ? "大盘行情" : "自选行情";
                this.NotifyMsg(msg, "@*股票监测--" + usrTo);
                zxcConsoleHelper.Debug(true, "DataCheck_Hourly:: {0}   ---{1}.\n{2}", this.getMsg_Perfix(), _data.DateTime, msg);
            }
        }
    }
}
