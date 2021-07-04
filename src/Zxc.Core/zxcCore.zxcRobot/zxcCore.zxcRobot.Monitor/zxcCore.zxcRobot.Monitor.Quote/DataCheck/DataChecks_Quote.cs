using System;
using System.Collections.Generic;
using zxcCore.Common;
using zxcCore.zxcData.Cache.Memory;
using zxcCore.zxcRobot.Quote.Data;

namespace zxcCore.zxcRobot.Monitor.DataCheck
{
    /// <summary>数据集检查-行情
    /// </summary>
    public class DataChecks_Quote : DataChecks
    {
        #region 属性及构造

        public DataChecks_Quote(string tagName, IDataCaches dataCaches, IDataChecks parent = null, IDataCheck_Msger msger = null) : base(tagName, dataCaches, parent, msger)
        {
        }
        public DataChecks_Quote(string tagName, IDataCache dataCache, IDataChecks parent = null, IDataCheck_Msger msger = null) : base(tagName, dataCache, parent, msger)
        {
        }
        public DataChecks_Quote(string tagName, IDataCaches_Manage dataCaches_Manage, IDataChecks parent = null, IDataCheck_Msger msger = null) : base(tagName, dataCaches_Manage, parent, msger)
        {

        }

        #endregion


        //数据监测实现-观察者模式
        public override bool CheckDatas()
        {
            bool bResult = true;
            foreach (KeyValuePair<string, IDataCheck> check in _DataChecks)
            {
                bResult = check.Value.CheckData() && bResult;
            }
            return base.CheckDatas();
        }
        //数据监测实现（具化数据对象及缓存）-观察者模式
        public override bool CheckDatas<T>(DateTime dtTime, T data, IDataCache<T> dataCache)
        {
            bool bResult = true;
            foreach (KeyValuePair<string, IDataCheck> check in _DataChecks)
            {
                DataCheck_Quote<Data_Quote> dataCheck = (DataCheck_Quote<Data_Quote>)check.Value;
                if (dataCheck == null) continue;
                if (!dataCheck.IsValid) continue;

                Data_Quote pQuote = (Data_Quote)zxcReflectionHelper.ConvertToObject(data, typeof(Data_Quote));
                if (pQuote != null)
                    bResult = dataCheck.CheckData(dtTime, pQuote, (IDataCache<Data_Quote>)dataCache) && bResult;
            }
            return bResult;
        }


        //消息通知
        public override bool NotifyMsg(dynamic msg)
        {
            if (this.Msger != null)
            {
                this.NotifyMsg(msg);
            }
            return true;
        }

    }
}
