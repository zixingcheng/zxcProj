﻿//===============================================================================
// Copyright @ 2021 Guangzhou Yijian Life Technology Co.,Ltd. All rights reserved.
// Copyright @ 2021 广州易简生活科技有限公司.  版权所有.
//===============================================================================
// 文件名称： 
// 功能描述：Data_Quote_Swap --行情数据类-数据交换
// 创建标识：zxc   2021-06-20
// 修改标识： 
// 修改描述：
//===============================================================================
using System;
using zxcCore.Extensions;
using zpCore.zpDataCache.Memory;
using zxcCore.zxcRobot.Quote;

namespace zxcCore.zxcRobot.Monitor
{
    /// <summary>行情数据类-数据交换
    /// </summary>
    public class Data_Quote_Swap : Data_Quote_Realtime_5Stalls
    {
        #region 属性及构造

        public bool _isIndex { get; set; }
        public string _exType { get; set; }

        public Data_Quote_Swap()
        {
        }

        #endregion


        //对象转换-由json对象
        public override bool FromJson(dynamic jsonData)
        {
            //this.StockID_Tag = Convert.ToString(jsonData["idTag"]);
            this.StockID = Convert.ToString(jsonData["id"]);
            this.StockName = Convert.ToString(jsonData["name"]);
            this.Price_Open = (float)Convert.ToDouble(jsonData["openPrice"]);
            this.Price_Per = (float)Convert.ToDouble(jsonData["preClose"]);
            this.Price_Close = (float)Convert.ToDouble(jsonData["lastPrice"]);
            this.Price_High = (float)Convert.ToDouble(jsonData["highPrice"]);
            this.Price_Low = (float)Convert.ToDouble(jsonData["lowPrice"]);
            this.Price_Buy = (float)Convert.ToDouble(jsonData["buyPrice"]);
            this.Price_Sell = (float)Convert.ToDouble(jsonData["sellPrice"]);
            this.TradeValume = Convert.ToInt32(jsonData["tradeValume"]);
            this.TradeTurnover = (float)Convert.ToDouble(jsonData["tradeTurnover"]);

            this.Volume_Buy1 = Convert.ToInt32(jsonData["buy1Volume"]);
            this.Price_Buy1 = (float)Convert.ToDouble(jsonData["buy1Price"]);
            this.Volume_Buy2 = Convert.ToInt32(jsonData["buy2Volume"]);
            this.Price_Buy2 = (float)Convert.ToDouble(jsonData["buy2Price"]);
            this.Volume_Buy3 = Convert.ToInt32(jsonData["buy3Volume"]);
            this.Price_Buy3 = (float)Convert.ToDouble(jsonData["buy3Price"]);
            this.Volume_Buy4 = Convert.ToInt32(jsonData["buy4Volume"]);
            this.Price_Buy4 = (float)Convert.ToDouble(jsonData["buy4Price"]);
            this.Volume_Buy5 = Convert.ToInt32(jsonData["buy5Volume"]);
            this.Price_Buy5 = (float)Convert.ToDouble(jsonData["buy5Price"]);

            this.Volume_Sell1 = Convert.ToInt32(jsonData["sell1Volume"]);
            this.Price_Sell1 = (float)Convert.ToDouble(jsonData["sell1Price"]);
            this.Volume_Sell2 = Convert.ToInt32(jsonData["sell2Volume"]);
            this.Price_Sell2 = (float)Convert.ToDouble(jsonData["sell2Price"]);
            this.Volume_Sell3 = Convert.ToInt32(jsonData["sell3Volume"]);
            this.Price_Sell3 = (float)Convert.ToDouble(jsonData["sell3Price"]);
            this.Volume_Sell4 = Convert.ToInt32(jsonData["sell4Volume"]);
            this.Price_Sell4 = (float)Convert.ToDouble(jsonData["sell4Price"]);
            this.Volume_Sell5 = Convert.ToInt32(jsonData["sell5Volume"]);
            this.Price_Sell5 = (float)Convert.ToDouble(jsonData["sell5Price"]);
            this.DateTime = Convert.ToDateTime(jsonData["datetime"]);

            //同步标的信息,初始全部值
            this.Init_ValueAll();
            this.QuoteTimeType = typeQuoteTime.real;                //标识为实时数据
            this._exType = this.StockExchange.ToString();
            this._isIndex = this.IsIndex();
            return true;
        }
    }

}
