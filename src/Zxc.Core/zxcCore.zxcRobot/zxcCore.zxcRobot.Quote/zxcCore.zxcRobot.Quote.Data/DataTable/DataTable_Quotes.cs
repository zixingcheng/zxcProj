using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using zxcCore.zxcData.Cache.MemoryDB;

namespace zxcCore.zxcRobot.Quote.Data
{
    /// <summary>数据对象集类-行情表
    /// </summary>
    public class DataTable_Quotes<T> : Data_Table<T> where T : Data_Quote
    {
        #region 属性及构造

        /// <summary>标的信息
        /// </summary>
        public StockInfo StockInfo
        {
            get; set;
        }

        public DataTable_Quotes(string dtName, StockInfo stockInfo) : base("dataTable_Quotes/" + dtName)
        {
            //this._dtName = string.IsNullOrEmpty(_dtName) ? "dataTable_Points" : _dtName;
            //this.Init_PointsLog();
            StockInfo = stockInfo;
        }

        #endregion


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
            return this.FindAll(e => (e.UID == item.UID && e.IsDel == false) || (e.DateTime == item.DateTime && e.QuoteTimeType == item.QuoteTimeType && e.IsDel == false));
        }

    }

}
