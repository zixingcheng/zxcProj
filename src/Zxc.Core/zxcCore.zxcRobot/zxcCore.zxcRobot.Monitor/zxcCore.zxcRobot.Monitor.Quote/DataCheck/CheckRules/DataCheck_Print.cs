﻿using System;
using System.Collections.Generic;
using System.Linq;
using zxcCore.zxcData.Cache.Memory;
using zxcCore.Common;
using zxcCore.zxcRobot.Quote.Data;

namespace zxcCore.zxcRobot.Monitor.DataCheck
{
    /// <summary>数据检查-打印行情信息
    /// </summary>
    public class DataCheck_Print<T> : DataCheck_Quote<T> where T : Data_Quote
    {
        #region 属性及构造

        public DataCheck_Print(string tagName, IDataCache<T> dataCache, string setting) : base(tagName, dataCache, setting)
        {
            _tagAlias = "实时打印";
        }
        ~DataCheck_Print()
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

            //打印信息
            zxcConsoleHelper.Debug(false, "DataCheck_Print: {0}   ---{1}.", this.getMsg_Perfix(), _data.DateTime);
            return bResult;
        }
    }
}
