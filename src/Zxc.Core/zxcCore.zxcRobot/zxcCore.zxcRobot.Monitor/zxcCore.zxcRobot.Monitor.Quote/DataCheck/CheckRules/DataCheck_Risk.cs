using System;
using System.Collections.Generic;
using System.Linq;
using zxcCore.zxcData.Cache.Memory;
using zxcCore.Common;
using zxcCore.zxcData.Analysis;
using zxcCore.zxcRobot.Quote;
using zxcCore.zxcRobot.Quote.Data;

namespace zxcCore.zxcRobot.Monitor.DataCheck
{
    /// <summary>数据检查-风险监测信息
    /// </summary>
    public class DataCheck_Risk<T> : DataCheck_Quote<T>
    {
        #region 属性及构造

        //数据分析对象 
        protected internal DataAnalyse_KeyPoints _dataAnalyse = null;
        protected DataAnalyse_KeyPoints_EventArgs _eventArgs = null;
        protected internal double _valueDelta = 0.0025;         //涨跌拐点判断范围

        public DataCheck_Risk(string tagName, IDataCache<T> dataCache, string setting) : base(tagName, dataCache, setting)
        {
            _tagAlias = "风控提醒";
            _dataAnalyse = new DataAnalyse_KeyPoints(tagName);
            _dataAnalyse.DataAnalyse_Trigger += new DataAnalyse_KeyPoints_EventHandler(EventHandler_DataAnalyse_Trigger);
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
                //修正最小生效间隔
                double valueDelta = _data.IsIndex() ? _valueDelta * 1.5 : _data.StockType == typeStock.Option ? _valueDelta * 20.0 : _valueDelta * 3;
                this._dataAnalyse.Init(_data.Price_Per, _data.Price_Per, zxcTimeHelper.checkTimeH(dtTime).AddMinutes(25), _data.Price_High, _data.Price_Low, valueDelta);
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
                if (_eventArgs.MonitorType == typeKeyPoints.BREAK)
                {
                    string tag0 = _eventArgs.MonitorType2 > 0 ? "上涨拐点" : "下降拐点";
                    strMsg = string.Format("\n{0}：{1}({2}).", _tagAlias, tag0, this.getValue_str(_eventArgs.Value));
                }
            }
            return strMsg;
        }


        //数据分析触发事件
        protected void EventHandler_DataAnalyse_Trigger(object sender, DataAnalyse_KeyPoints_EventArgs e)
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
                string usrTo = this.getUser_str();
                this.NotifyMsg(msg, usrTo);
                zxcConsoleHelper.Debug(true, "DataCheck_Risk:: {0}   ---{1}.\n{2}", this.getMsg_Perfix(), _data.DateTime, msg);
            }
        }

    }
}
