using System;
using System.Collections.Generic;
using System.Linq;
using zpCore.zpDataCache.Memory;
using zxcCore.Common;
using zxcCore.zxcRobot.DataAnalysis;
using zxcCore.zxcRobot.Quote;

namespace zxcCore.zxcRobot.Monitor.DataCheck
{
    /// <summary>数据检查-涨跌幅度固定监测
    /// </summary>
    public class DataCheck_RiseFall_Fixed<T> : DataCheck_Quote<T>
    {
        #region 属性及构造

        protected internal DataStatistics _dataStics = null;        //实时数据统计对象

        protected internal double _valueRF_last = 0;                //涨跌幅-最后
        protected internal double _valueRF_step = 0.005;            //涨跌幅监测间隔
        protected internal double _valueRF_step_last = 0;           //涨跌幅间隔-最后
        protected internal DateTime _timeRF_last = DateTime.Now;    //涨跌幅时间-最后
        protected internal int _timeInterval_last = 0;              //涨跌幅时间间隔-最后
        protected internal int _nNums = 0;                          //监测次数
        public DataCheck_RiseFall_Fixed(string tagName, IDataCache<T> dataCache, string setting) : base(tagName, dataCache, setting)
        {
            _tagAlias = "涨跌幅度";
            _dataStics = new DataStatistics();
        }
        ~DataCheck_RiseFall_Fixed()
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
            if (bResult == false) return false;

            //初始统计信息
            string msg = this.getMsg_Perfix();
            if (!_dataStics.IsInited)
            {
                //修正最小生效间隔
                double dValue_interval = _data._isIndex ? _valueRF_step * 0.4 : _data.StockType == typeStock.Option ? _valueRF_step * 4.0 : _valueRF_step;

                //初始统计信息
                _dataStics.Init(_data.Value_RF, _data.Price_High / _data.Price_Per - 1, _data.Price_Low / _data.Price_Per - 1, _data.DateTime, dValue_interval, _data.StockName);

                //组装消息
                msg += this.getMsg_Suffix();
            }
            else
            {
                //统计，无效退出
                if (!_dataStics.Statistics(_data.Value_RF, _data.DateTime)) return false;

                //涨跌超区间处理
                //int nTimes = 0;

                //组装消息
                msg += this.getMsg_Infix();
                msg += this.getMsg_Suffix();
            }

            //ConsoleHelper.Debug("dataSticsInfo: 最大：{0},最小：{1}，前值：{2}", _dataStics.Max, _dataStics.Min, _dataStics.Value_last);

            //float dValue_delta = _data._valueRF - _valueRF_last;
            ////float dValueRF_step = _data._isIndex ? _valueRF_step / 2.0f : _data._typeStock == typeStock.Option ? _valueRF_step * 5.0f : _valueRF_step;

            //if (Math.Abs(dValue_delta) > dValueRF_step)
            //{
            //    int ratio = dValue_delta > 0 ? 1 : -1;
            //    _timeInterval_last = (int)Math.Ceiling((DateTime.Now - _timeRF_last).TotalMinutes);
            //    _valueRF_step_last = dValueRF_step * ratio;
            //    _valueRF_last += _valueRF_step_last;
            //    _timeRF_last = DateTime.Now;

            //    //组装消息
            //    msg += this.getMsg_Infix();
            //    msg += this.getMsg_Suffix();

            //    //this.NotifyMsg(msg);
            //}

            //输出、打印信息
            string usrTo = _data.StockType == typeStock.Option ? "期权行情" : _data._isIndex ? "大盘行情" : "自选行情";
            //this.NotifyMsg(msg, "");
            this.NotifyMsg(msg, "@*股票监测--" + usrTo);
            zxcConsoleHelper.Debug(false, "DataCheck_RiseFall_Fixed: {0}   ---{1}.\n{2}", this.getMsg_Perfix(), _data.DateTime, msg);
            return bResult;
        }


        protected internal override string getMsg_Infix()
        {
            string tag0 = _dataStics.Value_delta > 0 ? "涨超" : "跌逾";
            int timeInterval = (int)Math.Ceiling(_dataStics.Duration_M);
            return string.Format("\n{0}：{1}分钟{2} {3}%. 前值：{4}({5})%", _tagAlias, timeInterval, tag0, Math.Round(_dataStics.Value_delta * 100, 1), Math.Round(_dataStics.Value_last * 100, 2), this.getValue_str(_dataStics.Value_Original_last));
        }

    }
}
