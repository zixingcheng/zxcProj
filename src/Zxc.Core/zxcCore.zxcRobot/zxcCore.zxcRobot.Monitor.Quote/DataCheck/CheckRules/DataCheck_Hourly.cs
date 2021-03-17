﻿using System;
using System.Collections.Generic;
using System.Linq;
using zpCore.zpDataCache.Memory;
using zxcCore.Common;

namespace zxcCore.zxcRobot.Monitor.DataCheck
{
    /// <summary>数据检查-整点行情信息
    /// </summary>
    public class DataCheck_Hourly<T> : DataCheck_Quote<T>
    {
        #region 属性及构造

        //上个时间
        protected internal DateTime _dtLast = TimeHelper.checkTimeD(DateTime.Now);
        protected internal DateTime _dtNow = DateTime.Now;
        protected internal int _timeInterval = 30;              //时间间隔（分钟）

        public DataCheck_Hourly(string tagName, IDataCache<T> dataCache, string setting) : base(tagName, dataCache, setting)
        {
            _tagAlias = "整点播报";
        }
        ~DataCheck_Hourly()
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

            //整点（30分钟）
            _dtNow = TimeHelper.checkTimeM(dtTime);
            if ((_dtNow - _dtLast).Minutes < 1) return bResult;
            if (_dtNow.Minute % _timeInterval != 0) return bResult;
            _dtLast = _dtNow;

            //组装消息
            string msg = this.getMsg_Perfix();
            msg += this.getMsg_Infix();
            msg += this.getMsg_Suffix();

            //输出、打印信息
            string usrTo = _data._typeStock == typeStock.Option ? "期权行情" : _data._isIndex ? "大盘行情" : "自选行情";
            this.NotifyMsg(msg, "@*股票监测--" + usrTo);
            ConsoleHelper.Debug("DataCheck_Hourly: {0}   ---{1}.\n{2}", this.getMsg_Perfix(), _data.Time, msg);
            return bResult;
        }


        protected internal override string getMsg_Infix()
        {
            return string.Format("\n{0}：{1}", _tagAlias, _dtNow.ToString("HH:mm:00"));
        }
    }
}
