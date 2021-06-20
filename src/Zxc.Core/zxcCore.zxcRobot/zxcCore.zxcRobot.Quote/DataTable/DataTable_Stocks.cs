using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using zxcCore.zxcDataCache.MemoryDB;

namespace zxcCore.zxcRobot.Quote
{
    /// <summary>数据对象集类-行情表
    /// </summary>
    public class DataTable_Stocks<T> : Data_Table<T> where T : StockInfo
    {
        #region 属性及构造

        public DataTable_Stocks(string dtName = "dataTable_Stocks") : base(dtName)
        {
            //this._dtName = string.IsNullOrEmpty(_dtName) ? "dataTable_Points" : _dtName;
            this._isNoLog = true;
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
            return this.FindAll(e => (e.UID == item.UID && e.IsDel == false) || (e.StockID == item.StockID && e.StockExchange == item.StockExchange && e.IsDel == false));
        }

    }

}
