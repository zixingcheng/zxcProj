//===============================================================================
// Copyright @ 2021 Guangzhou Yijian Life Technology Co.,Ltd. All rights reserved.
// Copyright @ 2021 广州易简生活科技有限公司.  版权所有.
//===============================================================================
// 文件名称： 
// 功能描述：Data_Quote_Realtime --行情数据类-实时
// 创建标识：zxc   2021-06-20
// 修改标识： 
// 修改描述：
//===============================================================================
using Newtonsoft.Json.Linq;
using System;
using System.Collections.Generic;
using zxcCore.Common;
using zxcCore.zxcData.Cache.MemoryDB;

namespace zxcCore.zxcRobot.Quote.Data
{

    /// <summary>行情数据类-实时
    /// </summary>
    public class Data_Quote_Realtime : Data_Quote_Info
    {
        #region 属性及构造

        /// <summary>买入价
        /// </summary>
        public double Price_Buy
        {
            get; set;
        }
        /// <summary>卖出价
        /// </summary>
        public double Price_Sell
        {
            get; set;
        }

        public Data_Quote_Realtime(StockInfo stockInfo = null) : base(stockInfo)
        {
        }
        ~Data_Quote_Realtime()
        {
            // 缓存数据？
        }

        #endregion


        //对象转换-由json对象
        public override bool FromJsonObj(JObject jsonData, typeQuoteTime quoteTime)
        {
            this.Price_Buy = zxcTransHelper.ToDouble(jsonData["buyPrice"]);
            this.Price_Sell = zxcTransHelper.ToDouble(jsonData["sellPrice"]);
            return base.FromJsonObj(jsonData, quoteTime);
        }

    }

}
