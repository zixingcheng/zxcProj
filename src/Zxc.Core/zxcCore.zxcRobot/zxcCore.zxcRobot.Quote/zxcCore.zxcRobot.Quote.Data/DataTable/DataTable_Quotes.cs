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
            this._isNoDel = true;
        }

        #endregion


        /// <summary>更新行情日志信息
        /// </summary>
        /// <param name="collection">行情数据集</param>
        /// <param name="isDel">是否为删除</param>
        /// <returns></returns>
        public virtual bool Updata_LogQuote(IEnumerable<T> collection, bool isDel = false)
        {
            //计算行情数据时间段范围
            Data_Quote pQuote = collection.First();
            if (pQuote == null) return false;
            StockInfo pStockInfo = pQuote.GetStockInfo();
            if (pStockInfo == null) return false;

            //更新日志
            DateTime dtMax = collection.Max(e => e.DateTime);
            DateTime dtMin = collection.Min(e => e.DateTime);
            return Quote_Datas._Datas._quotesLog.Updata_LogQuote(pStockInfo.StockID_Tag, dtMin, dtMax, pQuote.QuoteTimeType, pQuote.QuotePlat, isDel);
        }



        /// <summary>添加对象集-剔除存在
        /// </summary>
        /// <param name="collection"></param>
        /// <param name="isUnique">唯一性检查</param>
        public override bool AddRange(IEnumerable<T> collection, bool isUnique = true, bool bUpdata = false, bool bCacheData = true)
        {
            bool bResult = base.AddRange(collection, isUnique, bUpdata, bCacheData);
            if (bResult == false) return bResult;

            return this.Updata_LogQuote(collection);
        }
        /// <summary>删除对象集
        /// </summary>
        /// <param name="collection"></param>
        public override bool DeleteRange(IEnumerable<T> collection)
        {
            bool bResult = base.DeleteRange(collection);
            if (bResult == false) return bResult;

            return this.Updata_LogQuote(collection);
        }
        /// <summary>更新对象集
        /// </summary>
        /// <param name="collection"></param>
        public override bool UpdateRange(IEnumerable<T> collection, bool bCacheData = true)
        {
            bool bResult = base.UpdateRange(collection, bCacheData);
            if (bResult == false) return bResult;

            return this.Updata_LogQuote(collection);
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
            return this.FindAll(e => (e.UID == item.UID && e.IsDel == false) || (e.DateTime == item.DateTime && e.QuoteTimeType == item.QuoteTimeType && e.IsDel == false));
        }

    }

}
