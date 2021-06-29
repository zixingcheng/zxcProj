//===============================================================================
// Copyright @ 2021 Guangzhou Yijian Life Technology Co.,Ltd. All rights reserved.
// Copyright @ 2021 广州易简生活科技有限公司.  版权所有.
//===============================================================================
// 文件名称： 
// 功能描述：Quote_Datas --行情数据库类
// 创建标识：zxc   2021-06-20
// 修改标识： 
// 修改描述：
//===============================================================================
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Linq;
using zxcCore.Common;
using zxcCore.Extensions;
using zxcCore.zxcData.Cache.MemoryDB;

namespace zxcCore.zxcRobot.Quote.Data
{
    /// <summary>用户管理类
    /// </summary>
    public class Quote_Datas : Data_DB
    {
        public static readonly Quote_Datas _Datas = new Quote_Datas("");

        #region 属性及构造

        /// <summary>库表--zxc标的信息数据表
        /// </summary>
        public DataTable_Stocks<StockInfo> _stocksZxc { get; set; }
        /// <summary>库表--zxc标的监测设置表
        /// </summary>
        public DataTable_MonitorSets<MonitorSet> _setsMoitor { get; set; }


        /// <summary>库表--zxc行情数据表集合
        /// </summary>
        protected internal Dictionary<string, DataTable_Quotes<Data_Quote>> _quotesZxc = null;

        /// <summary>行情数据表(历史)
        /// </summary>
        /// <param name="stockTag"></param>
        /// <returns></returns>
        public DataTable_Quotes<Data_Quote> this[string stockTag]
        {
            get { return this.Get_QuoteData(stockTag); }
        }


        protected internal Quote_Datas(string dirBase) : base(dirBase, typePermission_DB.Normal, true, "/Datas/DB_Quote")
        {
            this.InitStock_system();
            this._quotesZxc = new Dictionary<string, DataTable_Quotes<Data_Quote>>();
        }

        #endregion


        protected override void OnDBModelCreating()
        {
            base.OnDBModelCreating();

            //初始表信息
            _stocksZxc = new DataTable_Stocks<StockInfo>(); this.InitDBModel(_stocksZxc);
            _setsMoitor = new DataTable_MonitorSets<MonitorSet>(); this.InitDBModel(_setsMoitor);
        }

        /// <summary>初始系统标的信息
        /// </summary>
        protected void InitStock_system()
        {
            string pathStockInfo = _configDataCache.config["DataCache.MemoryDB:Quote_DB:SrcData_Stock"] + "";
            if (pathStockInfo != "")
            {
                //提取 Setting_Stock.csv 配置信息
                List<StockInfo> lstStockInfo = new List<StockInfo>();
                string[] strLines = File.ReadAllLines(pathStockInfo);
                for (int i = 1; i < strLines.Length; i++)
                {
                    if (strLines[i] == "") continue;

                    //初始标的信息
                    StockInfo pStockInfo = StockInfo.Init_StockInfo(strLines[i]);
                    if (pStockInfo == null)
                        continue;
                    lstStockInfo.Add(pStockInfo);
                }

                //加入标的表
                Stopwatch watch = new Stopwatch();
                watch.Start();
                _stocksZxc.Clear();
                _stocksZxc.AddRange(lstStockInfo, false, false, false);
                _stocksZxc.SaveChanges(true);
                watch.Stop();
                zxcConsoleHelper.Print("内存数据库::行情数据(initial) \n   >> 已初始.  -- {1}, 耗时：{0} 秒.", watch.Elapsed.TotalSeconds, DateTime.Now.ToString());
            }

        }

        /// <summary>初始系统标的信息
        /// </summary>
        protected internal DataTable_Quotes<Data_Quote> InitQuote_zxc(StockInfo pStockInfo)
        {
            if (pStockInfo == null) return null;

            DataTable_Quotes<Data_Quote> quoteZxc = new DataTable_Quotes<Data_Quote>(pStockInfo.StockID_Tag, pStockInfo);
            this.InitDBModel(quoteZxc);

            _quotesZxc.Add(pStockInfo.StockID_Tag, quoteZxc);
            return quoteZxc;
        }


        /// <summary>查询行情标的信息
        /// </summary>
        /// <param name="stockTag">标的编号(名称，或标识)</param>
        /// <returns></returns>
        public StockInfo Get_StockInfo(string stockTag)
        {
            if (stockTag.Contains("."))
            {
                StockInfo poStockInfo = Quote_Datas._Datas._stocksZxc.Find(e => e.StockID_Tag == stockTag || e.StockID_TagSina == stockTag);
                if (poStockInfo != null)
                    return poStockInfo;
            }

            string[] stockNames = stockTag.Split(".");
            StockInfo pStockInfo = this.Get_StockInfo(stockNames[0], stockNames.Length > 1 ? stockNames[1] : "");
            return pStockInfo;
        }
        /// <summary>查询行情标的信息
        /// </summary>
        /// <param name="stockID">标的编号</param>
        /// <param name="stockName">标的名称</param>
        /// <returns></returns>
        public StockInfo Get_StockInfo(string stockID, string stockName)
        {
            string stockTag = stockID;
            if (!string.IsNullOrEmpty(stockTag))
            {
                StockInfo pStockInfo = Quote_Datas._Datas._stocksZxc.Find(e => e.StockName == stockTag || e.StockID == stockTag);
                if (pStockInfo != null)
                    return pStockInfo;
            }

            stockTag = stockName;
            if (!string.IsNullOrEmpty(stockTag))
            {
                StockInfo pStockInfo = Quote_Datas._Datas._stocksZxc.Find(e => e.StockName == stockTag || e.StockID == stockTag);
                if (pStockInfo != null)
                    return pStockInfo;
            }
            return null;
        }


        /// <summary>查询行情标的信息
        /// </summary>
        /// <param name="stockID">标的编号</param>
        /// <param name="stockName">标的名称</param>
        /// <returns></returns>
        protected internal DataTable_Quotes<Data_Quote> Get_QuoteData(string stockTag)
        {
            //校检标识 
            StockInfo pStockInfo = Quote_Datas._Datas.Get_StockInfo(stockTag);
            if (pStockInfo == null)
                return null;

            DataTable_Quotes<Data_Quote> pData_Quotes = null;
            if (_quotesZxc.TryGetValue(pStockInfo.StockID_Tag, out pData_Quotes))
                return pData_Quotes;

            //初始行情表
            pData_Quotes = this.InitQuote_zxc(pStockInfo);
            return pData_Quotes;
        }

    }
}
