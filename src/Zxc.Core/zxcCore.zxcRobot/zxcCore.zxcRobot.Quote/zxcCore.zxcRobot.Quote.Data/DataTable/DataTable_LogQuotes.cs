using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using zxcCore.Enums;
using zxcCore.zxcData.Cache.MemoryDB;

namespace zxcCore.zxcRobot.Quote.Data
{
    /// <summary>数据对象集类-行情信息记录表
    /// </summary>
    public class DataTable_LogQuotes<T> : Data_Table<T> where T : LogData_Quote
    {
        #region 属性及构造

        public DataTable_LogQuotes(string dtName = "dataTable_LogQuotes") : base(dtName)
        {
            //this._dtName = string.IsNullOrEmpty(_dtName) ? "dataTable_Points" : _dtName;
            this._isNoLog = true;
        }

        #endregion


        /// <summary>更新行情数据时间区间日志信息
        /// </summary>
        /// <param name="stockID_Tag">标的标签</param>
        /// <param name="dtTime_Start">数据开始时间</param>
        /// <param name="dtTime_End">数据结束时间</param>
        /// <param name="quoteTimeType">时间频率类型</param>
        /// <param name="quotePlat">行情来源平台</param>
        /// <returns></returns>
        public virtual bool Updata_LogQuote(string stockID_Tag, DateTime dtTime_Start, DateTime dtTime_End, typeTimeFrequency quoteTimeType, typeQuotePlat quotePlat = typeQuotePlat.JQDataAPI_zxc, bool isDel = false)
        {
            //查询
            LogData_Quote pLog = this.Get_LogQuote(stockID_Tag, quoteTimeType, quotePlat);
            if (pLog == null) return false;

            //比对时间
            if (!isDel)
            {
                if (pLog.DateTime_Max == pLog.DateTime_Min
                    || (pLog.DateTime_Max > dtTime_Start && pLog.DateTime_Max < dtTime_End)
                    || (pLog.DateTime_Min > dtTime_Start && pLog.DateTime_Min < dtTime_End))
                {
                    //更新记录时间区间
                    if (pLog.DateTime_Min > dtTime_Start)
                        pLog.DateTime_Min = dtTime_Start;
                    if (pLog.DateTime_Max < dtTime_End)
                        pLog.DateTime_Max = dtTime_End;
                    this.Add((T)pLog, true, true);
                }
            }
            else
            {
                //需完善
            }
            return true;
        }


        /// <summary>提取数据日志信息对象
        /// </summary>
        /// <param name="stockID_Tag">标的标签</param>
        /// <param name="quoteTimeType">时间频率类型</param>
        /// <param name="quotePlat">行情来源平台</param>
        /// <param name="autoInit">自动初始</param>
        /// <returns></returns>
        public virtual T Get_LogQuote(string stockID_Tag, typeTimeFrequency quoteTimeType, typeQuotePlat quotePlat = typeQuotePlat.JQDataAPI_zxc, bool autoInit = true)
        {
            //查询
            List<T> lstLogs = this.FindAll(e => e.StockID_Tag == stockID_Tag && e.QuoteTimeType == quoteTimeType && e.QuotePlat == quotePlat);
            if (lstLogs.Count != 1)
            {
                if (!autoInit) return default(T);

                //初始新对象 
                T pLog = (T)new LogData_Quote()
                {
                    StockID_Tag = stockID_Tag,
                    QuoteTimeType = quoteTimeType,
                    QuotePlat = quotePlat,
                    DateTime_Min = DateTime.Now,
                    DateTime_Max = DateTime.Now
                };
                this.Add(pLog);     //添加记录
                return pLog;
            }
            return lstLogs[0];
        }


        /// <summary>对象是否存在
        /// </summary>
        /// <param name="item"></param>
        /// <returns></returns>
        public override bool IsExist(T item)
        {
            return this.Contains(item) || this.IsSame(item);
        }
        /// <summary>查询相同对象-重写
        /// </summary>
        /// <param name="item"></param>
        /// <returns></returns>
        public override List<T> Query_Sames(T item)
        {
            return this.FindAll(e => (e.UID == item.UID && e.IsDel == false) || (e.StockID_Tag == item.StockID_Tag && e.IsDel == false));
        }

    }

}
