//===============================================================================
// Copyright @ 2021 Guangzhou Yijian Life Technology Co.,Ltd. All rights reserved.
// Copyright @ 2021 广州易简生活科技有限公司.  版权所有.
//===============================================================================
// 文件名称： 
// 功能描述：Data_Quote_Realtime_5Stalls --行情数据类-实时-5档
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

    /// <summary>行情数据类-实时-5档
    /// </summary>
    public class Data_Quote_Realtime_5Stalls : Data_Quote_Realtime
    {
        #region 属性及构造

        /// <summary>买一价
        /// </summary>
        public double Price_Buy1
        {
            get; set;
        }
        /// <summary>买一量
        /// </summary>
        public double Volume_Buy1
        {
            get; set;
        }
        /// <summary>买二价
        /// </summary>
        public double Price_Buy2
        {
            get; set;
        }
        /// <summary>买二量
        /// </summary>
        public double Volume_Buy2
        {
            get; set;
        }
        /// <summary>买三价
        /// </summary>
        public double Price_Buy3
        {
            get; set;
        }
        /// <summary>买三量
        /// </summary>
        public double Volume_Buy3
        {
            get; set;
        }
        /// <summary>买四价
        /// </summary>
        public double Price_Buy4
        {
            get; set;
        }
        /// <summary>买四量
        /// </summary>
        public double Volume_Buy4
        {
            get; set;
        }
        /// <summary>买五价
        /// </summary>
        public double Price_Buy5
        {
            get; set;
        }
        /// <summary>买五量
        /// </summary>
        public double Volume_Buy5
        {
            get; set;
        }

        /// <summary>卖一价
        /// </summary>
        public double Price_Sell1
        {
            get; set;
        }
        /// <summary>卖一量
        /// </summary>
        public double Volume_Sell1
        {
            get; set;
        }
        /// <summary>卖二价
        /// </summary>
        public double Price_Sell2
        {
            get; set;
        }
        /// <summary>卖二量
        /// </summary>
        public double Volume_Sell2
        {
            get; set;
        }
        /// <summary>卖三价
        /// </summary>
        public double Price_Sell3
        {
            get; set;
        }
        /// <summary>卖三量
        /// </summary>
        public double Volume_Sell3
        {
            get; set;
        }
        /// <summary>卖四价
        /// </summary>
        public double Price_Sell4
        {
            get; set;
        }
        /// <summary>卖四量
        /// </summary>
        public double Volume_Sell4
        {
            get; set;
        }
        /// <summary>卖五价
        /// </summary>
        public double Price_Sell5
        {
            get; set;
        }
        /// <summary>卖五量
        /// </summary>
        public double Volume_Sell5
        {
            get; set;
        }

        public Data_Quote_Realtime_5Stalls(StockInfo stockInfo = null) : base(stockInfo)
        {
        }
        ~Data_Quote_Realtime_5Stalls()
        {
            // 缓存数据？
        }

        #endregion


        //对象转换-由json对象
        public override bool FromJsonObj(JObject jsonData, typeQuoteTime quoteTime)
        {
            if (base.FromJsonObj(jsonData, quoteTime))
            {
                this.Volume_Buy1 = (int)zxcTransHelper.ToDouble(jsonData["buy1Volume"]);
                this.Price_Buy1 = zxcTransHelper.ToDouble(jsonData["buy1Price"]) * _valueTimes;
                this.Volume_Buy2 = (int)zxcTransHelper.ToDouble(jsonData["buy2Volume"]);
                this.Price_Buy2 = zxcTransHelper.ToDouble(jsonData["buy2Price"]) * _valueTimes;
                this.Volume_Buy3 = (int)zxcTransHelper.ToDouble(jsonData["buy3Volume"]);
                this.Price_Buy3 = zxcTransHelper.ToDouble(jsonData["buy3Price"]) * _valueTimes;
                this.Volume_Buy4 = (int)zxcTransHelper.ToDouble(jsonData["buy4Volume"]);
                this.Price_Buy4 = zxcTransHelper.ToDouble(jsonData["buy4Price"]) * _valueTimes;
                this.Volume_Buy5 = (int)zxcTransHelper.ToDouble(jsonData["buy5Volume"]);
                this.Price_Buy5 = zxcTransHelper.ToDouble(jsonData["buy5Price"]) * _valueTimes;

                this.Volume_Sell1 = (int)zxcTransHelper.ToDouble(jsonData["sell1Volume"]);
                this.Price_Sell1 = zxcTransHelper.ToDouble(jsonData["sell1Price"]) * _valueTimes;
                this.Volume_Sell2 = (int)zxcTransHelper.ToDouble(jsonData["sell2Volume"]);
                this.Price_Sell2 = zxcTransHelper.ToDouble(jsonData["sell2Price"]) * _valueTimes;
                this.Volume_Sell3 = (int)zxcTransHelper.ToDouble(jsonData["sell3Volume"]);
                this.Price_Sell3 = zxcTransHelper.ToDouble(jsonData["sell3Price"]) * _valueTimes;
                this.Volume_Sell4 = (int)zxcTransHelper.ToDouble(jsonData["sell4Volume"]);
                this.Price_Sell4 = zxcTransHelper.ToDouble(jsonData["sell4Price"]) * _valueTimes;
                this.Volume_Sell5 = (int)zxcTransHelper.ToDouble(jsonData["sell5Volume"]);
                this.Price_Sell5 = zxcTransHelper.ToDouble(jsonData["sell5Price"]);
                this.DateTime = Convert.ToDateTime(jsonData["datetime"]);
                return true;
            }
            return false;
        }

    }

}
