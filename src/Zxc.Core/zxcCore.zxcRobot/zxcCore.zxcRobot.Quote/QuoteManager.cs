//===============================================================================
// Copyright @ 2021 Guangzhou Yijian Life Technology Co.,Ltd. All rights reserved.
// Copyright @ 2021 广州易简生活科技有限公司.  版权所有.
//===============================================================================
// 文件名称： 
// 功能描述：zxcRobot --行情数据类
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
using zxcCore.zxcDataCache.MemoryDB;

namespace zxcCore.zxcRobot.Quote
{
    /// <summary>用户管理类
    /// </summary>
    public class QuoteManager : Data_DB
    {
        public static readonly QuoteManager _Quotes = new QuoteManager("");

        #region 属性及构造

        /// <summary>库表--zxc标的信息数据表
        /// </summary>
        /// 
        public DataTable_Stocks<StockInfo> _stocksZxc { get; set; }
        /// <summary>库表--zxc行情数据表
        /// </summary>
        /// 
        public DataTable_Quotes<Data_Quote> _quoteZxc { get; set; }

        protected internal QuoteManager(string dirBase) : base(dirBase, typePermission_DB.Normal, true, "/Datas/DB_Quote")
        {
            this.InitStock_system();
        }

        #endregion


        protected override void OnDBModelCreating()
        {
            base.OnDBModelCreating();

            //初始表信息
            _stocksZxc = new DataTable_Stocks<StockInfo>(); this.InitDBModel(_stocksZxc);
            _quoteZxc = new DataTable_Quotes<Data_Quote>(); this.InitDBModel(_quoteZxc);
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
                Console.WriteLine("转化成Json（100000）耗时：" + watch.Elapsed.TotalMilliseconds);
            }

        }


        /// <summary>查询行情标的信息
        /// </summary>
        /// <param name="stockID">标的编号</param>
        /// <param name="stockName">标的名称</param>
        /// <returns></returns>
        public static StockInfo Get_StockInfo(string stockID, string stockName)
        {
            string stockTag = stockID;
            if (!string.IsNullOrEmpty(stockTag))
            {
                StockInfo pStockInfo = QuoteManager._Quotes._stocksZxc.Find(e => e.StockName == stockTag || e.StockID == stockTag);
                if (pStockInfo != null)
                    return pStockInfo;
            }

            stockTag = stockName;
            if (!string.IsNullOrEmpty(stockTag))
            {
                StockInfo pStockInfo = QuoteManager._Quotes._stocksZxc.Find(e => e.StockName == stockTag || e.StockID == stockTag);
                if (pStockInfo != null)
                    return pStockInfo;
            }
            return null;
        }

    }
}
