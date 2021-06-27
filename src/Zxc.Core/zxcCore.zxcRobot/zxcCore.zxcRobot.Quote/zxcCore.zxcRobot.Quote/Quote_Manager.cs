//===============================================================================
// Copyright @ 2021 Guangzhou Yijian Life Technology Co.,Ltd. All rights reserved.
// Copyright @ 2021 广州易简生活科技有限公司.  版权所有.
//===============================================================================
// 文件名称： 
// 功能描述：QuoteManager --行情管理器
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
    public class Quote_Manager
    {
        /// <summary>全局行情管理器
        /// </summary>
        public static readonly Quote_Manager _Quotes = new Quote_Manager();

        #region 属性及构造

        /// <summary>行情数据对象集
        /// </summary>
        protected internal Dictionary<string, QuoteData> _quoteDatas = null;
        /// <summary>提取股票信息
        /// </summary>
        /// <param name="stockName"></param>
        /// <returns></returns>
        public QuoteData this[string stockTag]
        {
            get
            {
                return this.Get_QuoteData(stockTag);
            }
        }


        protected internal QuoteQuery _QuoteQuery = new QuoteQuery();
        /// <summary>行情查询对象
        /// </summary>
        public QuoteQuery QuoteQuery
        {
            get { return _QuoteQuery; }
        }

        protected internal StockQuery _Stocks = new StockQuery();
        /// <summary>标的查询对象
        /// </summary>
        public StockQuery Stocks
        {
            get { return _Stocks; }
        }


        public Quote_Manager()
        {
            _quoteDatas = new Dictionary<string, QuoteData>();
        }
        ~Quote_Manager()
        {
            // 缓存数据？
        }

        #endregion


        /// <summary>获取行情对象
        /// <param name="stockTag">标的标识</param>
        /// <returns></returns>
        protected internal QuoteData Get_QuoteData(string stockTag)
        {
            //校检标识 
            stockTag = Quote_Manager._Quotes.Stocks.Check_StockTag(stockTag);
            if (stockTag == "") return null;

            //提取行情对象
            QuoteData pDataQuote = null;
            if (_quoteDatas.TryGetValue(stockTag, out pDataQuote))
                return pDataQuote;


            //提取库表
            DataTable_Quotes<Data_Quote> pData_Quotes = Quote_Datas._Datas[stockTag];
            if (pData_Quotes == null) return null;

            //初始行情对象
            pDataQuote = new QuoteData(pData_Quotes);
            _quoteDatas.Add(pDataQuote.StockInfo.StockID_Tag, pDataQuote);
            return pDataQuote;
        }

    }
}
