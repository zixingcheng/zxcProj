//===============================================================================
// Copyright @ 2021 Guangzhou Yijian Life Technology Co.,Ltd. All rights reserved.
// Copyright @ 2021 广州易简生活科技有限公司.  版权所有.
//===============================================================================
// 文件名称： 
// 功能描述：QuoteData --行情数据
// 创建标识：zxc   2021-06-26
// 修改标识： 
// 修改描述：
//===============================================================================
using Newtonsoft.Json.Linq;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using zxcCore.Common;
using zxcCore.Extensions;
using zxcCore.zxcRobot.Quote.Data;

namespace zxcCore.zxcRobot.Quote
{
    public class QuoteData
    {
        #region 属性及构造 

        /// <summary>标的信息
        /// </summary>
        public StockInfo StockInfo
        {
            get; set;
        }

        protected internal DataTable_Quotes<Data_Quote> _dtQuote = null;    //行情库表对象
        public QuoteData(DataTable_Quotes<Data_Quote> pData_Quotes)
        {
            _dtQuote = pData_Quotes;
            StockInfo = _dtQuote.StockInfo;
        }
        ~QuoteData()
        {
            // 缓存数据？
        }

        #endregion


        /// <summary>查询行情(历史)
        /// </summary>
        /// <param name="endTime">结束时间</param>
        /// <param name="quoteBars">标的行情数</param>
        /// <param name="quoteTime">行情时间类型</param>
        /// <param name="autoUpdate">是否自动更新本地库表</param>
        /// <returns></returns>
        public List<Data_Quote> Query(DateTime endTime, int quoteBars = 1, typeQuoteTime quoteTime = typeQuoteTime.day, bool autoUpdate = true)
        {
            //修正时间
            if (endTime == DateTime.MinValue) endTime = DateTime.Now;

            //查询库表
            List<Data_Quote> lstQuote = _dtQuote.FindAll(e => e.DateTime <= endTime && e.QuoteTimeType == quoteTime && e.IsDel == false).OrderBy(t => t.DateTime).Take(quoteBars).ToList();

            //查询失败-启动数据检查更新
            if (autoUpdate && lstQuote.Count == 0)
            {
                lstQuote = QuoteQuery._Query.QuoteHistory(StockInfo, endTime, quoteBars, quoteTime);
                this.UpdateRange(lstQuote);
            }
            return lstQuote;
        }
        /// <summary>查询行情(历史)
        /// </summary>
        /// <param name="startTime">开始时间</param>
        /// <param name="endTime">结束时间</param>
        /// <param name="quoteTime">行情时间类型</param>
        /// <param name="autoUpdate">是否自动更新本地库表</param>
        /// <returns></returns>
        public List<Data_Quote> Query(DateTime startTime, DateTime endTime, typeQuoteTime quoteTime = typeQuoteTime.day, bool autoUpdate = true)
        {
            //修正时间
            if (endTime == DateTime.MinValue) endTime = DateTime.Now;
            if (startTime == DateTime.MinValue)
                return Query(endTime, 1, quoteTime, autoUpdate);

            //查询库表
            List<Data_Quote> lstQuote = _dtQuote.FindAll(e => e.DateTime <= endTime && e.DateTime >= startTime && e.QuoteTimeType == quoteTime && e.IsDel == false).OrderBy(t => t.DateTime).ToList();

            //查询失败-启动数据检查更新
            if (autoUpdate && lstQuote.Count == 0)
            {
                lstQuote = QuoteQuery._Query.QuoteHistory(StockInfo, startTime, endTime, quoteTime);
                this.UpdateRange(lstQuote);
            }
            return lstQuote;
        }

        /// <summary>查询行情(实时日数据)
        /// </summary>
        /// <returns></returns>
        public List<Data_Quote> Query()
        {
            //调用接口查询
            List<Data_Quote> lstQuote = QuoteQuery._Query.QuoteReal(StockInfo);
            return lstQuote;
        }


        /// <summary>更新对象集
        /// </summary>
        /// <param name="collection"></param>
        protected internal virtual void UpdateRange(List<Data_Quote> collection)
        {
            this._dtQuote.AddRange(collection);
        }

    }
}
