using System;
using System.Collections.Generic;
using System.ComponentModel;
using zxcCore.Enums;
using zxcCore.Extensions;
using zxcCore.zxcData.Cache.MemoryDB;

namespace zxcCore.zxcRobot.Quote.Data
{
    /// <summary>行情数据日志信息(记录操作信息)
    /// </summary>
    public class LogData_Quote : Data_Models
    {
        #region 属性及构造

        /// <summary>标的名称
        /// </summary>
        public string StockName
        {
            get; set;
        }
        /// <summary>标的代码-标签
        /// </summary>
        public string StockID_Tag
        {
            get; set;
        }


        /// <summary>行情数据时间类型
        /// </summary>
        public typeTimeFrequency QuoteTimeType
        {
            get; set;
        }
        /// <summary>数据来源平台
        /// </summary>
        public typeQuotePlat QuotePlat
        {
            get; set;
        }


        /// <summary>行情数据时间-最早
        /// </summary>
        public DateTime DateTime_Min
        {
            get; set;
        }
        /// <summary>行情数据时间-最晚
        /// </summary>
        public DateTime DateTime_Max
        {
            get; set;
        }


        protected internal StockInfo stockInfo = null;
        public LogData_Quote()
        {
        }
        ~LogData_Quote()
        {
            // 缓存数据？
        }

        #endregion


        /// <summary>数据初始
        /// </summary>
        /// <param name="poData"></param>
        /// <returns></returns>
        public override bool Init(dynamic poData = null)
        {
            if (stockInfo == null)
            {
                stockInfo = Quote_Datas._Datas.Get_StockInfo(StockID_Tag);
            }
            return true;
        }

    }

}
