using System;
using zpCore.zpDataCache.Memory;

namespace zxcCore.zxcRobot.Monitor
{
    /// <summary>消息类型
    /// </summary>
    public enum typeStock
    {
        /// <summary>股票
        /// </summary>
        Stock = 0,
        /// <summary>指数
        /// </summary>
        Index = 1,
        /// <summary>期权
        /// </summary>
        Option = 2
    }

    /// <summary>数据对象类-Quote
    /// </summary>
    public class Data_Quote : Data_Base
    {
        #region 属性及构造

        DateTime _dtTime;
        public DateTime Time
        {
            get { return _dtTime; }
        }
        float _value;
        public float Value
        {
            get { return _value; }
        }

        public string id { get; set; }
        public string idTag { get; set; }
        public string name { get; set; }
        public float openPrice { get; set; }
        public float preClose { get; set; }
        public float lastPrice { get; set; }
        public float highPrice { get; set; }
        public float lowPrice { get; set; }
        public float buyPrice { get; set; }
        public float sellPrice { get; set; }
        public int tradeValume { get; set; }
        public float tradeTurnover { get; set; }

        public int buy1Volume { get; set; }
        public float buy1Price { get; set; }
        public int buy2Volume { get; set; }
        public float buy2Price { get; set; }
        public int buy3Volume { get; set; }
        public float buy3Price { get; set; }
        public int buy4Volume { get; set; }
        public float buy4Price { get; set; }
        public int buy5Volume { get; set; }
        public float buy5Price { get; set; }

        public int sell1Volume { get; set; }
        public float sell1Price { get; set; }
        public int sell2Volume { get; set; }
        public float sell2Price { get; set; }
        public int sell3Volume { get; set; }
        public float sell3Price { get; set; }
        public int sell4Volume { get; set; }
        public float sell4Price { get; set; }
        public int sell5Volume { get; set; }
        public float sell5Price { get; set; }

        public typeStock _typeStock { get; set; }
        public bool _isIndex { get; set; }
        public string _exType { get; set; }
        public float _avgValue { get; set; }
        public float _valueRF { get; set; }
        public Data_Quote()
        {
        }

        #endregion


        //对象转换-由json对象
        public override bool FromJson(dynamic jsonData)
        {
            this.id = Convert.ToString(jsonData["id"]);
            this.idTag = Convert.ToString(jsonData["idTag"]);
            this.name = Convert.ToString(jsonData["name"]);
            this.openPrice = (float)Convert.ToDouble(jsonData["openPrice"]);
            this.preClose = (float)Convert.ToDouble(jsonData["preClose"]);
            this.lastPrice = (float)Convert.ToDouble(jsonData["lastPrice"]);
            this.highPrice = (float)Convert.ToDouble(jsonData["highPrice"]);
            this.lowPrice = (float)Convert.ToDouble(jsonData["lowPrice"]);
            this.buyPrice = (float)Convert.ToDouble(jsonData["buyPrice"]);
            this.sellPrice = (float)Convert.ToDouble(jsonData["sellPrice"]);
            this.tradeValume = Convert.ToInt32(jsonData["tradeValume"]);
            this.tradeTurnover = (float)Convert.ToDouble(jsonData["tradeTurnover"]);

            this.buy1Volume = Convert.ToInt32(jsonData["buy1Volume"]);
            this.buy1Price = (float)Convert.ToDouble(jsonData["buy1Price"]);
            this.buy2Volume = Convert.ToInt32(jsonData["buy2Volume"]);
            this.buy2Price = (float)Convert.ToDouble(jsonData["buy2Price"]);
            this.buy3Volume = Convert.ToInt32(jsonData["buy3Volume"]);
            this.buy3Price = (float)Convert.ToDouble(jsonData["buy3Price"]);
            this.buy4Volume = Convert.ToInt32(jsonData["buy4Volume"]);
            this.buy4Price = (float)Convert.ToDouble(jsonData["buy4Price"]);
            this.buy5Volume = Convert.ToInt32(jsonData["buy5Volume"]);
            this.buy5Price = (float)Convert.ToDouble(jsonData["buy5Price"]);

            this.sell1Volume = Convert.ToInt32(jsonData["sell1Volume"]);
            this.sell1Price = (float)Convert.ToDouble(jsonData["sell1Price"]);
            this.sell2Volume = Convert.ToInt32(jsonData["sell2Volume"]);
            this.sell2Price = (float)Convert.ToDouble(jsonData["sell2Price"]);
            this.sell3Volume = Convert.ToInt32(jsonData["sell3Volume"]);
            this.sell3Price = (float)Convert.ToDouble(jsonData["sell3Price"]);
            this.sell4Volume = Convert.ToInt32(jsonData["sell4Volume"]);
            this.sell4Price = (float)Convert.ToDouble(jsonData["sell4Price"]);
            this.sell5Volume = Convert.ToInt32(jsonData["sell5Volume"]);
            this.sell5Price = (float)Convert.ToDouble(jsonData["sell5Price"]);

            this._value = this.lastPrice;
            this._valueRF = this._value / this.preClose - 1;
            this._avgValue = this.tradeTurnover / this.tradeValume;
            this._exType = this.idTag.Split(".")[0];
            this._dtTime = Convert.ToDateTime(jsonData["datetime"]);
            if ((name.IndexOf("购") > 0 || name.IndexOf("沽") > 0) && name.IndexOf("月") > 0)
            {
                _typeStock = typeStock.Option;
            }
            else if (name.IndexOf("指数") > 0 || name.IndexOf("ETF") > 0)
            {
                this._isIndex = true; _typeStock = typeStock.Index;
            }
            return true;
        }
    }
}
