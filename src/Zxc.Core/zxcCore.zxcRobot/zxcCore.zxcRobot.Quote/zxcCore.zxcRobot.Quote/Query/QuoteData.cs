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
using zxcCore.Enums;
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

        protected internal StockExchangeInfo _infoExchange = null;          //标的交易所信息
        protected internal DataTable_Quotes<Data_Quote> _dtQuote = null;    //行情库表对象
        public QuoteData(DataTable_Quotes<Data_Quote> pData_Quotes)
        {
            _dtQuote = pData_Quotes;
            StockInfo = _dtQuote.StockInfo;
            if (StockInfo != null)
                _infoExchange = StockInfo.Get_StockExchangeInfo();
        }
        ~QuoteData()
        {
            // 缓存数据？
        }

        #endregion


        /// <summary>查询行情(实时日数据)
        /// </summary>
        /// <returns></returns>
        public List<Data_Quote> Query()
        {
            //调用接口查询
            List<Data_Quote> lstQuote = QuoteQuery._Query.QuoteReal(StockInfo);
            return lstQuote;
        }

        /// <summary>查询行情(历史)
        /// </summary>
        /// <param name="endTime">结束时间</param>
        /// <param name="quoteBars">标的行情数</param>
        /// <param name="quoteTime">行情时间类型</param>
        /// <param name="autoUpdate">是否自动更新本地库表</param>
        /// <returns></returns>
        public List<Data_Quote> Query(DateTime endTime, int quoteBars = 1, typeTimeFrequency quoteTime = typeTimeFrequency.day, bool autoUpdate = true)
        {
            //修正时间
            if (endTime == DateTime.MinValue) endTime = DateTime.Now;

            //自动更新修正数据
            if (autoUpdate)
            {
                if (!this.Query_Check(endTime.AddSeconds(-quoteBars * (int)quoteTime.Get_Value()), endTime, quoteBars, quoteTime, true))
                    return null;
            }


            //查询库表
            List<Data_Quote> lstQuote = _dtQuote.FindAll(e => e.DateTime <= endTime && e.QuoteTimeType == quoteTime && e.IsDel == false).OrderByDescending(t => t.DateTime).Take(quoteBars).ToList();
            return lstQuote;
        }
        /// <summary>查询行情(历史)
        /// </summary>
        /// <param name="startTime">开始时间</param>
        /// <param name="endTime">结束时间</param>
        /// <param name="quoteTime">行情时间类型</param>
        /// <param name="autoUpdate">是否自动更新本地库表</param>
        /// <returns></returns>
        public List<Data_Quote> Query(DateTime startTime, DateTime endTime, typeTimeFrequency quoteTime = typeTimeFrequency.day, bool autoUpdate = true)
        {
            //修正时间
            if (endTime == DateTime.MinValue) endTime = DateTime.Now;
            if (startTime == DateTime.MinValue)
                return Query(endTime, 1, quoteTime, autoUpdate);

            //自动更新修正数据
            if (autoUpdate)
            {
                if (!this.Query_Check(startTime, endTime, 0, quoteTime, true))
                    return null;
            }


            //查询库表
            List<Data_Quote> lstQuote = _dtQuote.FindAll(e => e.DateTime <= endTime && e.DateTime >= startTime && e.QuoteTimeType == quoteTime && e.IsDel == false).OrderBy(t => t.DateTime).ToList();
            return lstQuote;
        }

        protected internal bool Query_Check(DateTime startTime, DateTime endTime, int quoteBars = 0, typeTimeFrequency quoteTime = typeTimeFrequency.day, bool autoUpdate = true)
        {
            //提取日志信息、及修正时间
            LogData_Quote pLog = Quote_Datas._Datas._quotesLog.Get_LogQuote(StockInfo.StockID_Tag, quoteTime);

            if (endTime == DateTime.MinValue) endTime = pLog.DateTime_Max;
            if (startTime == DateTime.MinValue) startTime = pLog.DateTime_Min;
            DateTime dtStart = startTime;
            DateTime dtEnd = endTime;


            //行情数据日志时间区间校正
            bool bResult = true;
            List<Data_Quote> pQuotes_max = new List<Data_Quote>();
            if (pLog.DateTime_Max < endTime)
            {
                //最大时间为结束时间，日志最大时间为最小时间
                DateTime dtMin = pLog.DateTime_Max;
                DateTime dtMax = endTime;
                dtEnd = dtMax;

                pQuotes_max = QuoteQuery._Query.QuoteHistory(StockInfo, dtMin, dtMax, quoteTime);
            }

            List<Data_Quote> pQuotes_min = new List<Data_Quote>();
            if (pLog.DateTime_Min > startTime)
            {
                //最小时间为开始时间，日志最小时间为最大时间
                DateTime dtMin = startTime;
                DateTime dtMax = pLog.DateTime_Min;
                dtStart = dtMin;

                pQuotes_min = QuoteQuery._Query.QuoteHistory(StockInfo, dtMin, dtMax, quoteTime);
            }

            //数据自动更新
            if (autoUpdate)
            {
                //同步缺失数据（指定开始到记录开始，记录结束到指定结束）
                if (pQuotes_min.Count > 0)
                    bResult = bResult && this.UpdateRange(pQuotes_min, quoteTime);
                if (pQuotes_max.Count > 0)
                    bResult = bResult && this.UpdateRange(pQuotes_max, quoteTime);

                //数据量校检及自动更新补全
                if (quoteBars > 0)
                {
                    int nCount = _dtQuote.Count(e => e.DateTime <= dtEnd && e.QuoteTimeType == quoteTime && e.IsDel == false);
                    while (nCount < quoteBars)
                    {
                        //全部重新取
                        //DateTime dtEnd0 = dtStart;
                        dtStart = dtStart.AddDays(-1);

                        //List<Data_Quote> lstQuote = QuoteQuery._Query.QuoteHistory(StockInfo, dtEnd, quoteBars, quoteTime);
                        List<Data_Quote> lstQuote = QuoteQuery._Query.QuoteHistory(StockInfo, dtStart, dtEnd, quoteTime);
                        if (lstQuote.Count < 1) break;
                        bResult = bResult && this.UpdateRange(lstQuote, quoteTime);

                        //再次计算总数
                        nCount = _dtQuote.Count(e => e.DateTime <= dtEnd && e.QuoteTimeType == quoteTime && e.IsDel == false);
                    }
                    bResult = quoteBars <= nCount;
                }

                //日志信息不匹配，直接更新
                //if (dtStart < pLog.DateTime_Min || dtEnd > pLog.DateTime_Max)
                //    bResult = Quote_Datas._Datas._quotesLog.Updata_LogQuote(StockInfo.StockID_Tag, dtStart, dtEnd, quoteTime);
                return bResult;
            }
            return true;
        }


        /// <summary>更新对象集
        /// </summary>
        /// <param name="collection"></param>
        protected internal virtual bool UpdateRange(List<Data_Quote> collection, typeTimeFrequency quoteTime)
        {
            List<Data_Quote> lstTemp = new List<Data_Quote>();
            foreach (var item in collection)
            {
                //校正时间频率进行添加
                DateTime dtTime = this._infoExchange.CheckTime(item.DateTime, quoteTime);
                if (dtTime == item.DateTime)
                {
                    lstTemp.Add(item);
                }
                else
                {

                }
            }
            if (lstTemp.Count > 0)
                return this._dtQuote.AddRange(lstTemp, true, true);
            return true;
        }

    }
}
