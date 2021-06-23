//===============================================================================
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
using zxcCore.Common;

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
            this.Price_Open = zxcTransHelper.ToDouble(jsonData["openPrice"]);
            this.Price_Per = zxcTransHelper.ToDouble(jsonData["preClose"]);
            this.Price_Close = zxcTransHelper.ToDouble(jsonData["lastPrice"]);
            this.Price_High = zxcTransHelper.ToDouble(jsonData["highPrice"]);
            this.Price_Low = zxcTransHelper.ToDouble(jsonData["lowPrice"]);
            this.Price_Buy = zxcTransHelper.ToDouble(jsonData["buyPrice"]);
            this.Price_Sell = zxcTransHelper.ToDouble(jsonData["sellPrice"]);
            this.TradeValume = (int)zxcTransHelper.ToDouble(jsonData["tradeValume"]);
            this.TradeTurnover = zxcTransHelper.ToDouble(jsonData["tradeTurnover"]);

            this.Volume_Buy1 = (int)zxcTransHelper.ToDouble(jsonData["buy1Volume"]);
            this.Price_Buy1 = zxcTransHelper.ToDouble(jsonData["buy1Price"]);
            this.Volume_Buy2 = (int)zxcTransHelper.ToDouble(jsonData["buy2Volume"]);
            this.Price_Buy2 = zxcTransHelper.ToDouble(jsonData["buy2Price"]);
            this.Volume_Buy3 = (int)zxcTransHelper.ToDouble(jsonData["buy3Volume"]);
            this.Price_Buy3 = zxcTransHelper.ToDouble(jsonData["buy3Price"]);
            this.Volume_Buy4 = (int)zxcTransHelper.ToDouble(jsonData["buy4Volume"]);
            this.Price_Buy4 = zxcTransHelper.ToDouble(jsonData["buy4Price"]);
            this.Volume_Buy5 = (int)zxcTransHelper.ToDouble(jsonData["buy5Volume"]);
            this.Price_Buy5 = zxcTransHelper.ToDouble(jsonData["buy5Price"]);

            this.Volume_Sell1 = (int)zxcTransHelper.ToDouble(jsonData["sell1Volume"]);
            this.Price_Sell1 = zxcTransHelper.ToDouble(jsonData["sell1Price"]);
            this.Volume_Sell2 = (int)zxcTransHelper.ToDouble(jsonData["sell2Volume"]);
            this.Price_Sell2 = zxcTransHelper.ToDouble(jsonData["sell2Price"]);
            this.Volume_Sell3 = (int)zxcTransHelper.ToDouble(jsonData["sell3Volume"]);
            this.Price_Sell3 = zxcTransHelper.ToDouble(jsonData["sell3Price"]);
            this.Volume_Sell4 = (int)zxcTransHelper.ToDouble(jsonData["sell4Volume"]);
            this.Price_Sell4 = zxcTransHelper.ToDouble(jsonData["sell4Price"]);
            this.Volume_Sell5 = (int)zxcTransHelper.ToDouble(jsonData["sell5Volume"]);
            this.Price_Sell5 = zxcTransHelper.ToDouble(jsonData["sell5Price"]);
            this.DateTime = Convert.ToDateTime(jsonData["datetime"]);

            //同步标的信息,初始全部值
            this.Init_ValueAll();
            this.QuoteTimeType = typeQuoteTime.real;                //标识为实时数据
            this._exType = this.StockExchange.ToString();
            this._isIndex = this.IsIndex();
            return true;
        }


        public virtual string getMsg_Perfix()
        {
            //组装消息
            string tagRF = Value_RF == 0 ? "平" : (Value_RF > 0 ? "涨" : "跌");
            string tagUnit = _isIndex ? "" : "元";
            int digits = _isIndex ? 3 : 2;
            double value = StockType == typeStock.Option ? Value * 10000 : Value;
            string msg = string.Format("{0}：{1}{2}, {3} {4}%.", StockName, Math.Round(value, digits), tagUnit, tagRF, Math.Round(Value_RF * 100, 2));
            return msg;
        }
        /// <summary>提取值字符串（含单位，指数没有单位）
        /// </summary>
        /// <returns></returns>
        public virtual string getValue_str(double dValue)
        {
            //组装消息
            string tagUnit = _isIndex ? "" : "元";
            int digits = _isIndex ? 3 : 2;
            double value = StockType == typeStock.Option ? dValue * 10000 : dValue;
            string strValue = string.Format("{0}{1}", Math.Round(value, digits), tagUnit);
            return strValue;
        }

    }

}
