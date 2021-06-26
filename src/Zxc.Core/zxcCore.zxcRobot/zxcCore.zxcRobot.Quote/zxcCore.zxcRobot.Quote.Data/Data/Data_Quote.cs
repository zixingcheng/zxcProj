//===============================================================================
// Copyright @ 2021 Guangzhou Yijian Life Technology Co.,Ltd. All rights reserved.
// Copyright @ 2021 广州易简生活科技有限公司.  版权所有.
//===============================================================================
// 文件名称： 
// 功能描述：Data_Quote --行情数据类
// 创建标识：zxc   2021-06-20
// 修改标识： 
// 修改描述：
//===============================================================================
using Newtonsoft.Json.Linq;
using System;
using System.Collections.Generic;
using zxcCore.Common;
using zxcCore.Extensions;
using zxcCore.zxcDataCache.MemoryDB;

namespace zxcCore.zxcRobot.Quote.Data
{

    /// <summary>行情数据类
    /// </summary>
    public class Data_Quote : Data_Models, IData_Quote
    {
        #region 属性及构造

        /// <summary>标的名称
        /// </summary>
        public string StockName
        {
            get; set;
        }
        /// <summary>标的代码
        /// </summary>
        public string StockID
        {
            get; set;
        }
        /// <summary>标的类型
        /// </summary>
        public typeStock StockType
        {
            get; set;
        }
        /// <summary>交易所类型
        /// </summary>
        public typeStockExchange StockExchange
        {
            get; set;
        }

        /// <summary>标的代码-标签
        /// </summary>
        public string StockID_Tag
        {
            get
            {
                return StockExchange.ToString() + "." + StockID;
            }
        }

        /// <summary>前一价格(前一阶段收盘价)
        /// </summary>
        public double Price_Per
        {
            get; set;
        }
        /// <summary>开盘价
        /// </summary>
        public double Price_Open
        {
            get; set;
        }
        /// <summary>收盘价
        /// </summary>
        public double Price_Close
        {
            get; set;
        }

        /// <summary>最高价
        /// </summary>
        public double Price_High
        {
            get; set;
        }
        /// <summary>最低价
        /// </summary>
        public double Price_Low
        {
            get; set;
        }
        /// <summary>均价
        /// </summary>
        public double Price_Avg
        {
            get; set;
        }
        /// <summary>交易量
        /// </summary>
        public double TradeValume
        {
            get; set;
        }
        /// <summary>交易额
        /// </summary>
        public double TradeTurnover
        {
            get; set;
        }

        /// <summary>行情时间
        /// </summary>
        public DateTime DateTime
        {
            get; set;
        }
        /// <summary>行情数据时间类型
        /// </summary>
        public typeQuoteTime QuoteTimeType
        {
            get; set;
        }

        /// <summary>是否停牌
        /// </summary>
        public bool IsSuspended
        {
            get; set;
        }

        /// <summary>数据来源平台
        /// </summary>
        public typeQuotePlat QuotePlat
        {
            get; set;
        }


        protected internal double _value;
        /// <summary>当前价格
        /// </summary>
        public double Value
        {
            get
            {
                this.Init_ValueAll();
                return _value;
            }
        }
        protected internal double _valueRF;
        /// <summary>当前价格涨幅(相对前一收盘价涨跌幅比例)
        /// </summary>
        public double Value_RF
        {
            get
            {
                this.Init_ValueAll();
                return _valueRF;
            }
        }

        protected internal bool _isIndex { get; set; }  //师傅为指数
        protected internal bool _isInitAll = false;     //是否已初始全部数据
        public Data_Quote()
        {

        }
        ~Data_Quote()
        {
            // 缓存数据？
        }

        #endregion


        /// <summary>标的代码-标签聚宽
        /// </summary>
        public string GetStockID_TagJQ()
        {
            return StockID + "." + StockExchange.Get_AttrValue();
        }
        /// <summary>标的代码-标签新浪
        /// </summary>
        public string GetStockID_TagSina()
        {
            //区分期权标签
            if (StockType == typeStock.Option)
                return StockType.Get_Remark() + StockID;
            return StockExchange.ToString() + StockID;
        }

        /// <summary>是否为指数
        /// </summary>
        /// <returns></returns>
        public virtual bool IsIndex()
        {
            this._isIndex = (bool)this.StockType.Get_AttrValue();
            return _isIndex;
        }

        /// <summary>初始全部值(简单换算数据)
        /// </summary>
        /// <returns></returns>
        protected internal virtual bool Init_ValueAll()
        {
            if (_isInitAll) return true;

            this._value = this.Price_Close;                             //当前价格
            this._valueRF = this._value / this.Price_Per - 1;           //当前价格涨跌幅
            this.Price_Avg = this.TradeTurnover / this.TradeValume;     //均价（累计，如果当前时间段，注意重写）

            this.IsIndex();
            return this.Check_StockInfo();
        }
        protected internal virtual bool Check_StockInfo()
        {
            StockInfo pStockInfo = QuoteManager._Quotes._stocksZxc.Find(e => e.StockName == StockName || e.StockID == StockID);
            if (pStockInfo == null)
                return false;

            //同步信息
            StockType = pStockInfo.StockType;
            StockExchange = pStockInfo.StockExchange;
            if (StockType == typeStock.Index)
                this.Price_Avg = 0;
            return true;
        }

        //提取固定行情消息头
        public virtual string GetMsg_Perfix()
        {
            //组装消息
            string tagRF = Value_RF == 0 ? "平" : (Value_RF > 0 ? "涨" : "跌");
            string tagUnit = _isIndex ? "" : "元";
            int digits = _isIndex ? 3 : 2;
            string msg = string.Format("{0}：{1}{2}, {3} {4}%.", StockName, Math.Round(Value, digits), tagUnit, tagRF, Math.Round(Value_RF * 100, 2));
            return msg;
        }
        /// <summary>提取值字符串（含单位，指数没有单位）
        /// </summary>
        /// <returns></returns>
        public virtual string GetValue_str(double dValue)
        {
            //组装消息
            string tagUnit = _isIndex ? "" : "元";
            int digits = _isIndex ? 3 : 2;
            string strValue = string.Format("{0}{1}", Math.Round(dValue, digits), tagUnit);
            return strValue;
        }


        //对象转换-由json对象
        public new bool FromJson(dynamic jsonData)
        {
            return FromJson(jsonData, typeQuoteTime.none);
        }
        //对象转换-由json对象
        public virtual bool FromJson(JObject jsonData, typeQuoteTime quoteTime)
        {
            //this.StockID_Tag = Convert.ToString(jsonData["idTag"]); 
            this.StockID = Convert.ToString(jsonData["id"]);
            this.StockName = Convert.ToString(jsonData["name"]);
            this.Price_Open = zxcTransHelper.ToDouble(jsonData["openPrice"]);
            this.Price_Per = zxcTransHelper.ToDouble(jsonData["preClose"]);
            this.Price_Close = zxcTransHelper.ToDouble(jsonData["lastPrice"]);
            this.Price_High = zxcTransHelper.ToDouble(jsonData["highPrice"]);
            this.Price_Low = zxcTransHelper.ToDouble(jsonData["lowPrice"]);
            this.TradeValume = (int)zxcTransHelper.ToDouble(jsonData["tradeValume"]);
            this.TradeTurnover = zxcTransHelper.ToDouble(jsonData["tradeTurnover"]);

            this.DateTime = Convert.ToDateTime(jsonData["datetime"]);

            this.QuoteTimeType = quoteTime;
            if (quoteTime == typeQuoteTime.none)
            {
                string strQuoteTimeType = jsonData["quoteTimeType"] + "";
                if (strQuoteTimeType != "")
                    this.QuoteTimeType = (typeQuoteTime)Enum.Parse(typeof(typeQuoteTime), strQuoteTimeType);
            }

            string strQuotePlat = jsonData["quotePlat"] + "";
            if (strQuotePlat != "")
                this.QuotePlat = (typeQuotePlat)Enum.Parse(typeof(typeQuotePlat), strQuotePlat);

            //同步标的信息,初始全部值
            this.Init_ValueAll();
            return true;
        }

        public virtual dynamic ToDict()
        {
            var msgWx = new
            {
                //MsgID = MsgID,
                //MsgType = MsgType,
                //MsgInfo = MsgInfo,
                //UserID_To = UserID_To,
                //UserID_Src = UserID_Src,
                //DestTypeMsger = DestTypeMsger,
                //MsgTime = MsgTime,
                //MsgLink = MsgLink
            };
            return msgWx;
        }

    }

}
