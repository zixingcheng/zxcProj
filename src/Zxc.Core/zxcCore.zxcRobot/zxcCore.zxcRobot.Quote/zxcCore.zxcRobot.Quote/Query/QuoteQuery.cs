//===============================================================================
// Copyright @ 2021 Guangzhou Yijian Life Technology Co.,Ltd. All rights reserved.
// Copyright @ 2021 广州易简生活科技有限公司.  版权所有.
//===============================================================================
// 文件名称： 
// 功能描述：QuoteQuery --行情查询
// 创建标识：zxc   2021-06-26
// 修改标识： 
// 修改描述：
//===============================================================================
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using System;
using System.Collections.Generic;
using System.Text;
using zxcCore.Common;
using zxcCore.Extensions;
using zxcCore.zxcRobot.Quote.Data;
using zxcCore.zxcRobot.Quote.JQData;

namespace zxcCore.zxcRobot.Quote
{
    public class QuoteQuery
    {
        /// <summary>全局行情查询对象
        /// </summary>
        protected internal static readonly QuoteQuery _Query = new QuoteQuery();

        #region 属性及构造

        protected internal string _urlAPI_QuoteQuery = "";          //行情实时查询接口
        protected internal string _urlAPI_QuoteQueryHistory = "";   //行情实时历史查询接口

        public QuoteQuery()
        {
            //提取行情API配置
            _urlAPI_QuoteQuery = zxcConfigHelper.ConfigurationHelper.config["ZxcRobot.Quote:QuoteAPI:QueryAPI_Url"] + "";
            _urlAPI_QuoteQueryHistory = zxcConfigHelper.ConfigurationHelper.config["ZxcRobot.Quote:QuoteAPI:QueryHistoryAPI_Url"] + "";
        }
        ~QuoteQuery()
        {
            // 缓存数据？
        }

        #endregion



        /// <summary>查询实时行情
        /// </summary>
        /// <param name="stockTag">标的标识</param>
        /// <returns></returns>
        public List<Data_Quote> Query(string stockTag)
        {
            //查询标的行情对象
            QuoteData pQuoteData = Quote_Manager._Quotes[stockTag];
            if (pQuoteData == null) return null;

            return pQuoteData.Query();
        }
        /// <summary>查询实时行情
        /// </summary>
        /// <param name="pStockInfo"></param>
        /// <returns></returns>
        public List<Data_Quote> Query(StockInfo pStockInfo)
        {
            return this.Query(pStockInfo.StockID_Tag);
        }

        /// <summary>查询行情(历史)
        /// </summary>
        /// <param name="stockTag">标的标识</param>
        /// <param name="endTime">结束时间</param>
        /// <param name="quoteBars">标的行情数</param>
        /// <param name="quoteTime">行情时间类型</param>
        /// <param name="autoUpdate">是否自动更新本地库表</param>
        /// <returns></returns>
        public List<Data_Quote> Query(string stockTag, DateTime endTime, int quoteBars = 1, typeQuoteTime quoteTime = typeQuoteTime.day, bool autoUpdate = true)
        {
            //查询标的行情对象
            QuoteData pQuoteData = Quote_Manager._Quotes[stockTag];
            if (pQuoteData == null) return null;

            return pQuoteData.Query(endTime, quoteBars, quoteTime, autoUpdate);
        }
        /// <summary>查询行情(历史)
        /// </summary>
        /// <param name="stockTag">标的标识</param>
        /// <param name="startTime">开始时间</param>
        /// <param name="endTime">结束时间</param>
        /// <param name="quoteTime">行情时间类型</param>
        /// <param name="autoUpdate">是否自动更新本地库表</param>
        /// <returns></returns>
        public List<Data_Quote> Query(string stockTag, DateTime startTime, DateTime endTime, typeQuoteTime quoteTime = typeQuoteTime.day, bool autoUpdate = true)
        {
            //查询标的行情对象
            QuoteData pQuoteData = Quote_Manager._Quotes[stockTag];
            if (pQuoteData == null) return null;

            return pQuoteData.Query(startTime, endTime, quoteTime, autoUpdate);
        }



        /// <summary>查询实时行情
        /// </summary>
        /// <param name="stockTag">标的标识/ID/名称</param>
        /// <returns></returns>
        protected internal List<Data_Quote> QuoteReal(string stockTag)
        {
            //查询标的 
            StockInfo pStockInfo = Quote_Manager._Quotes.Stocks.Get_StockInfo(stockTag);
            return this.QuoteReal(pStockInfo);
        }
        /// <summary>查询实时行情
        /// </summary>
        /// <param name="pStockInfo"></param>
        /// <returns></returns>
        protected internal List<Data_Quote> QuoteReal(StockInfo pStockInfo)
        {
            if (pStockInfo == null) return null;

            //调用接口-新浪
            List<Data_Quote> lstQuote = this.QuoteReal_SinaAPI(pStockInfo);
            if (lstQuote == null || lstQuote.Count == 0)
            {
                //新浪接口失败，改用聚宽接口
                lstQuote = this.QuoteReal_JQDataAPI(pStockInfo);
            }
            return lstQuote;
        }

        /// <summary>查询实时行情(新浪API)
        /// </summary>
        /// <param name="pStockInfo"></param>
        /// <returns></returns>
        protected internal List<Data_Quote> QuoteReal_SinaAPI(StockInfo pStockInfo)
        {
            //调用接口
            string statusCode;
            string result = zxcNetHelper.Get_ByHttpClient(_urlAPI_QuoteQuery, pStockInfo.StockID_TagSina, out statusCode);

            //返回解析
            JObject jsonRes = JObject.Parse(result);
            return this.TransTo_Data_Quotes(jsonRes, typeQuoteTime.real, pStockInfo);
        }
        /// <summary>查询实时行情(聚宽API)
        /// </summary>
        /// <param name="pStockInfo"></param>
        /// <returns></returns>
        protected internal List<Data_Quote> QuoteReal_JQDataAPI(StockInfo pStockInfo)
        {
            return this.QuoteHistory(pStockInfo, DateTime.Now, 1, typeQuoteTime.day);
        }



        /// <summary>查询历史行情 
        /// </summary>
        /// <param name="stockTag">标的标识/ID/名称</param>
        /// <param name="endTime">结束时间</param>
        /// <param name="quoteBars">数据条数</param>
        /// <param name="quoteTime">时间类型</param>
        /// <returns></returns>
        protected internal List<Data_Quote> QuoteHistory(string stockTag, DateTime endTime, int quoteBars = 1, typeQuoteTime quoteTime = typeQuoteTime.day)
        {
            //查询标的 
            StockInfo pStockInfo = Quote_Manager._Quotes.Stocks.Get_StockInfo(stockTag);
            return this.QuoteHistory(pStockInfo, endTime, quoteBars, quoteTime);
        }
        /// <summary>查询历史行情 
        /// </summary>
        /// <param name="stockTag">标的标识/ID/名称</param>
        /// <param name="startTime">开始时间</param>
        /// <param name="endTime">结束时间</param>
        /// <param name="quoteTime">时间类型</param>
        /// <returns></returns>
        protected internal List<Data_Quote> QuoteHistory(string stockTag, DateTime startTime, DateTime endTime, typeQuoteTime quoteTime = typeQuoteTime.day)
        {
            //查询标的 
            StockInfo pStockInfo = Quote_Manager._Quotes.Stocks.Get_StockInfo(stockTag);
            return this.QuoteHistory(pStockInfo, startTime, endTime, quoteTime);
        }
        /// <summary>查询历史行情 
        /// </summary>
        /// <param name="pStockInfo">标的信息</param>
        /// <param name="endTime">结束时间</param>
        /// <param name="quoteBars">数据条数</param>
        /// <param name="quoteTime">时间类型</param>
        /// <returns></returns>
        protected internal List<Data_Quote> QuoteHistory(StockInfo pStockInfo, DateTime endTime, int quoteBars = 1, typeQuoteTime quoteTime = typeQuoteTime.day)
        {
            if (pStockInfo == null) return null;

            //调用接口-聚宽zxc
            List<Data_Quote> lstQuote = this.QuoteHistory_JQDataAPI_zxc(pStockInfo, endTime, quoteBars, quoteTime);
            if (lstQuote == null || lstQuote.Count == 0)
            {
                //聚宽zxc接口失败，改用聚宽python接口
                lstQuote = this.QuoteHistory_JQDataAPI(pStockInfo, endTime, quoteBars, quoteTime);
            }
            return lstQuote;
        }
        /// <summary>查询历史行情 
        /// </summary>
        /// <param name="pStockInfo">标的信息</param>
        /// <param name="startTime">开始时间</param>
        /// <param name="endTime">结束时间</param>
        /// <param name="quoteTime">时间类型</param>
        /// <returns></returns>
        protected internal List<Data_Quote> QuoteHistory(StockInfo pStockInfo, DateTime startTime, DateTime endTime, typeQuoteTime quoteTime = typeQuoteTime.day)
        {
            if (pStockInfo == null) return null;

            //调用接口-聚宽zxc
            List<Data_Quote> lstQuote = this.QuoteHistory_JQDataAPI_zxc(pStockInfo, startTime, endTime, quoteTime);
            if (lstQuote == null || lstQuote.Count == 0)
            {
                //聚宽zxc接口失败，改用聚宽python接口
                lstQuote = this.QuoteHistory_JQDataAPI(pStockInfo, startTime, endTime, quoteTime);
            }
            return lstQuote;
        }

        /// <summary>查询历史行情(聚宽API)
        /// </summary>
        /// <param name="pStockInfo">标的信息</param>
        /// <param name="endTime">结束时间</param>
        /// <param name="quoteTime">时间类型</param>
        /// <param name="quoteBars">数据条数</param>
        /// <returns></returns>
        protected internal List<Data_Quote> QuoteHistory_JQDataAPI_zxc(StockInfo pStockInfo, DateTime endTime, int quoteBars = 1, typeQuoteTime quoteTime = typeQuoteTime.day)
        {
            //调用接口
            JObject jsonRes = Quote_JQData._APIs.Get_Price(pStockInfo.StockID_TagJQ, endTime.ToString("yyyy-MM-dd HH:mm:ss"), quoteBars, quoteTime.Get_AttrValue() + "");
            return this.TransTo_Data_Quotes(jsonRes, quoteTime, pStockInfo);
        }
        /// <summary>查询历史行情(聚宽API)
        /// </summary>
        /// <param name="pStockInfo">标的信息</param>
        /// <param name="endTime">结束时间</param>
        /// <param name="quoteTime">时间类型</param>
        /// <param name="quoteBars">数据条数</param>
        /// <returns></returns>
        protected internal List<Data_Quote> QuoteHistory_JQDataAPI(StockInfo pStockInfo, DateTime endTime, int quoteBars = 1, typeQuoteTime quoteTime = typeQuoteTime.day)
        {
            //调用接口
            string statusCode;
            string param = string.Format("{0}&dataFrequency={1}&stockBars={2}&datetimeEnd={3}", pStockInfo.StockID_TagJQ, quoteTime.Get_AttrValue(), quoteBars, endTime.ToString("yyyy-MM-dd HH:mm:ss"));
            string result = zxcNetHelper.Get_ByHttpClient(_urlAPI_QuoteQueryHistory, param, out statusCode);

            //返回解析
            JObject jsonRes = JObject.Parse(result);
            return this.TransTo_Data_Quotes(jsonRes, quoteTime, pStockInfo);
        }
        /// <summary>查询历史行情(聚宽API)
        /// </summary>
        /// <param name="pStockInfo">标的信息</param>
        /// <param name="startTime">开始时间</param>
        /// <param name="endTime">结束时间</param>
        /// <param name="quoteTime">时间类型</param>
        /// <returns></returns>
        protected internal List<Data_Quote> QuoteHistory_JQDataAPI_zxc(StockInfo pStockInfo, DateTime startTime, DateTime endTime, typeQuoteTime quoteTime = typeQuoteTime.day)
        {
            //调用接口
            JObject jsonRes = Quote_JQData._APIs.Get_Price(pStockInfo.StockID_TagJQ, startTime, endTime, quoteTime.Get_AttrValue() + "");
            return this.TransTo_Data_Quotes(jsonRes, quoteTime, pStockInfo);
        }
        /// <summary>查询历史行情(聚宽API)
        /// </summary>
        /// <param name="pStockInfo">标的信息</param>
        /// <param name="startTime">开始时间</param>
        /// <param name="endTime">结束时间</param>
        /// <param name="quoteTime">时间类型</param>
        /// <returns></returns>
        protected internal List<Data_Quote> QuoteHistory_JQDataAPI(StockInfo pStockInfo, DateTime startTime, DateTime endTime, typeQuoteTime quoteTime = typeQuoteTime.day)
        {
            //调用接口
            string statusCode;
            string param = string.Format("{0}&dataFrequency={1}&datetimeStart={2}&datetimeEnd={3}", pStockInfo.StockID_TagJQ, quoteTime.Get_AttrValue(), startTime.ToString("yyyy-MM-dd HH:mm:ss"), endTime.ToString("yyyy-MM-dd HH:mm:ss"));
            string result = zxcNetHelper.Get_ByHttpClient(_urlAPI_QuoteQueryHistory, param, out statusCode);

            //返回解析
            JObject jsonRes = JObject.Parse(result);
            return this.TransTo_Data_Quotes(jsonRes, quoteTime, pStockInfo);
        }



        /// <summary>转换json行情数据为行情对象集
        /// </summary>
        /// <param name="jsonRes">json行情数据对象</param>
        /// <returns></returns>
        protected internal List<Data_Quote> TransTo_Data_Quotes(JObject jsonRes, typeQuoteTime quoteTime, StockInfo pStockInfo = null)
        {
            //数据检查
            if (jsonRes == null) return null;
            if (jsonRes["result"].ToString() == "False")
                return null;

            //循环解析文件json数据
            List<Data_Quote> lstDataQuote = new List<Data_Quote>();
            JArray jsonDatas = (JArray)jsonRes["datas"];
            if (jsonDatas != null)
            {
                //循环生成数据对象
                string platSrc = jsonRes["datasPlat"] + "";
                foreach (var jsonData in jsonDatas)
                {
                    Data_Quote pDataQuote = null;
                    switch (quoteTime)
                    {
                        case typeQuoteTime.none:
                            break;
                        case typeQuoteTime.real:
                            pDataQuote = new Data_Quote_Realtime_5Stalls(pStockInfo);
                            break;
                        default:
                            pDataQuote = new Data_Quote(pStockInfo);
                            break;
                    }
                    if (pDataQuote == null) continue;

                    //转换为行情数据对象
                    //if (platSrc == typeQuotePlat.JQDataAPI_zxc.ToString())
                    //{
                    //    pDataQuote = JsonConvert.DeserializeObject<Data_Quote_Info>(JsonConvert.SerializeObject(jsonData));
                    //    pDataQuote.QuoteTimeType = quoteTime;
                    //    lstDataQuote.Add(pDataQuote);
                    //}
                    if (pDataQuote.FromJson(jsonData))
                    {
                        pDataQuote.QuoteTimeType = quoteTime;
                        lstDataQuote.Add(pDataQuote);
                    }
                }
            }
            return lstDataQuote;
        }

    }

}