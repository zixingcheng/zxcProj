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
using Newtonsoft.Json.Linq;
using System;
using System.Collections.Generic;
using System.Text;
using zxcCore.Common;
using zxcCore.zxcRobot.Quote.Data;

namespace zxcCore.zxcRobot.Quote
{
    public class QuoteQuery
    {

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
        /// <param name="pStockInfo"></param>
        /// <returns></returns>
        public List<Data_Quote> QuoteReal(string stockTag)
        {
            //查询标的 
            string[] stockNames = stockTag.Split(".");
            StockInfo pStockInfo = Quote_Datas.Get_StockInfo(stockNames[0], stockNames.Length > 1 ? stockNames[1] : "");
            return this.QuoteReal(pStockInfo);
        }
        /// <summary>查询实时行情
        /// </summary>
        /// <param name="pStockInfo"></param>
        /// <returns></returns>
        public List<Data_Quote> QuoteReal(StockInfo pStockInfo)
        {
            if (pStockInfo == null) return null;

            //调用接口-新浪
            List<Data_Quote> lstQuote = this.QuoteReal_By_SinaAPI(pStockInfo);
            if (lstQuote == null || lstQuote.Count == 0)
            {
                //新浪接口失败，改用聚宽接口
                lstQuote = this.QuoteReal_By_JQDataAPI(pStockInfo);
            }
            return lstQuote;
        }

        /// <summary>查询实时行情(新浪API)
        /// </summary>
        /// <param name="pStockInfo"></param>
        /// <returns></returns>
        protected internal List<Data_Quote> QuoteReal_By_SinaAPI(StockInfo pStockInfo)
        {
            //调用接口
            string statusCode;
            string result = zxcNetHelper.Get_ByHttpClient(_urlAPI_QuoteQuery, pStockInfo.StockID_TagSina, out statusCode);

            //返回解析
            JObject jsonRes = JObject.Parse(result);
            if (jsonRes["result"].ToString() == "False")
                return null;

            //循环解析文件json数据
            List<Data_Quote> lstDataQuote = new List<Data_Quote>();
            JArray jsonDatas = (JArray)jsonRes["datas"];
            if (jsonDatas != null)
            {
                //循环生成数据对象
                foreach (var jsonData in jsonDatas)
                {
                    Data_Quote_Realtime_5Stalls pDataQuote = new Data_Quote_Realtime_5Stalls();
                    if (pDataQuote.FromJson(jsonData))
                        lstDataQuote.Add(pDataQuote);
                }
            }
            return lstDataQuote;
        }
        /// <summary>查询实时行情(聚宽API)
        /// </summary>
        /// <param name="pStockInfo"></param>
        /// <returns></returns>
        protected internal List<Data_Quote> QuoteReal_By_JQDataAPI(StockInfo pStockInfo)
        {
            //调用接口
            string statusCode;
            string param = pStockInfo.StockID_TagJQ + "&dataFrequency=1d&stockBars=1";
            string result = zxcNetHelper.Get_ByHttpClient(_urlAPI_QuoteQueryHistory, param, out statusCode);

            //返回解析
            JObject jsonRes = JObject.Parse(result);
            if (jsonRes["result"].ToString() == "False")
                return null;

            //循环解析文件json数据
            List<Data_Quote> lstDataQuote = new List<Data_Quote>();
            JArray jsonDatas = (JArray)jsonRes["datas"];
            if (jsonDatas != null)
            {
                //循环生成数据对象
                foreach (var jsonData in jsonDatas)
                {
                    Data_Quote_Realtime_5Stalls pDataQuote = new Data_Quote_Realtime_5Stalls();
                    if (pDataQuote.FromJson(jsonData))
                        lstDataQuote.Add(pDataQuote);
                }
            }
            return lstDataQuote;
        }

    }
}
