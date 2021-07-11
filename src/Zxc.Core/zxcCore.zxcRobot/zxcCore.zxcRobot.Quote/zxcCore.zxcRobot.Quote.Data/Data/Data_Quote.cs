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
using zxcCore.Enums;
using zxcCore.Extensions;
using zxcCore.zxcData.Cache.MemoryDB;

namespace zxcCore.zxcRobot.Quote.Data
{

    /// <summary>行情数据类
    /// </summary>
    public class Data_Quote : Data_Models, IData_Quote
    {
        #region 属性及构造

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

        /// <summary>涨停价
        /// </summary>
        public double Price_Limit_H
        {
            get; set;
        }
        /// <summary>跌停价
        /// </summary>
        public double Price_Limit_L
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

        /// <summary>行情数据时间类型
        /// </summary>
        public typeTimeFrequency QuoteTimeType
        {
            get; set;
        }
        /// <summary>数据来源平台
        /// </summary>
        public typeQuotePlat QuotePlat
        {
            get; set;
        }

        /// <summary>行情时间
        /// </summary>
        public DateTime DateTime
        {
            get; set;
        }
        /// <summary>是否停牌
        /// </summary>
        public bool IsSuspended
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

        protected internal double _valueTimes = 1;          //实际值与原始值倍数（期权为10000倍）
        protected internal bool _isInitAll = false;         //是否已初始全部数据
        protected internal StockInfo _stockInfo = null;     //绑定的标的信息
        public Data_Quote(StockInfo stockInfo = null)
        {
            _stockInfo = stockInfo;
        }
        ~Data_Quote()
        {
            // 缓存数据？
        }

        #endregion


        /// <summary>初始全部值(简单换算数据)
        /// </summary>
        /// <returns></returns>
        protected internal virtual bool Init_ValueAll()
        {
            if (_isInitAll) return true;

            this._value = this.Price_Close;                             //当前价格
            this._valueRF = this._value / this.Price_Per - 1;           //当前价格涨跌幅
            this.Price_Avg = this.TradeTurnover / this.TradeValume;     //均价（累计，如果当前时间段，注意重写）
            this.Price_Avg = Math.Round(this.Price_Avg, 6);

            _isInitAll = true;
            return _isInitAll;
        }

        /// <summary>是否为指数
        /// </summary>
        /// <returns></returns>
        public virtual bool IsIndex()
        {
            if (_stockInfo == null) return false;
            return (bool)_stockInfo.StockType.Get_AttrValue();
        }

        //提取标的信息
        public virtual bool SetStockInfo(StockInfo pStockInfo)
        {
            _stockInfo = pStockInfo;
            return true;
        }
        //提取标的信息
        public virtual StockInfo GetStockInfo()
        {
            return _stockInfo;
        }
        /// <summary>提取标的类型
        /// </summary>
        /// <returns></returns>
        public virtual typeStock GetStockType()
        {
            if (_stockInfo == null) return typeStock.Stock;
            return _stockInfo.StockType;
        }
        /// <summary>提取标的名称
        /// </summary>
        /// <returns></returns>
        public virtual string GetStockName()
        {
            if (_stockInfo == null) return "";
            return _stockInfo.StockName;
        }

        //提取固定行情消息头
        public virtual string GetMsg_Perfix()
        {
            if (_stockInfo != null)
            {
                //组装消息
                string tagRF = Value_RF == 0 ? "平" : (Value_RF > 0 ? "涨" : "跌");
                string tagUnit = _stockInfo.StockType == typeStock.Index ? "" : "元";
                int digits = _stockInfo.StockType == typeStock.Index ? 3 : 2;
                string msg = string.Format("{0}：{1}{2}, {3} {4}%.", _stockInfo.StockName, Math.Round(Value, digits), tagUnit, tagRF, Math.Round(Value_RF * 100, 2));
                return msg;
            }
            return "";
        }
        /// <summary>提取值字符串（含单位，指数没有单位）
        /// </summary>
        /// <returns></returns>
        public virtual string GetValue_str(double dValue)
        {
            string tagUnit = _stockInfo.StockType == typeStock.Index ? "" : "元";
            int digits = _stockInfo.StockType == typeStock.Index ? 3 : 2;

            string strValue = string.Format("{0}{1}", Math.Round(dValue, digits), tagUnit);
            return strValue;
        }


        //修正行情时间
        public bool Check_DateTime()
        {
            if (this.DateTime.Hour == 9 && this.DateTime.Minute < 30)
            {
                this.DateTime = this.DateTime.AddMinutes(30 - this.DateTime.Minute);
                this.DateTime = zxcTimeHelper.CheckTime(this.DateTime, this.QuoteTimeType, false);
            }
            return true;
        }


        //对象转换-由json对象
        public new bool FromJson(dynamic jsonData)
        {
            return FromJsonObj(jsonData, typeTimeFrequency.none);
        }
        //对象转换-由json对象
        public virtual bool FromJsonObj(JObject jsonData, typeTimeFrequency quoteTime)
        {
            //修正倍数
            if (_stockInfo != null && _stockInfo.StockType == typeStock.Option)
                _valueTimes = 10000;

            //this.StockID_Tag = Convert.ToString(jsonData["idTag"]); 
            this.Price_Open = zxcTransHelper.ToDouble(jsonData["openPrice"]) * _valueTimes;
            this.Price_Per = zxcTransHelper.ToDouble(jsonData["preClose"]) * _valueTimes;
            this.Price_Close = zxcTransHelper.ToDouble(jsonData["lastPrice"]) * _valueTimes;

            this.Price_Limit_H = zxcTransHelper.ToDouble(jsonData["high_limit"]) * _valueTimes;
            this.Price_Limit_L = zxcTransHelper.ToDouble(jsonData["low_limit"]) * _valueTimes;

            this.Price_High = zxcTransHelper.ToDouble(jsonData["highPrice"]) * _valueTimes;
            this.Price_Low = zxcTransHelper.ToDouble(jsonData["lowPrice"]) * _valueTimes;
            this.Price_Avg = zxcTransHelper.ToDouble(jsonData["avg"]) * _valueTimes;
            this.TradeValume = (int)zxcTransHelper.ToDouble(jsonData["tradeValume"]);
            this.TradeTurnover = zxcTransHelper.ToDouble(jsonData["tradeTurnover"]);

            this.DateTime = Convert.ToDateTime(jsonData["datetime"]);
            this.IsSuspended = zxcTransHelper.ToBoolean(jsonData["paused"]);

            this.QuoteTimeType = quoteTime;
            if (quoteTime == typeTimeFrequency.none)
            {
                string strQuoteTimeType = jsonData["quoteTimeType"] + "";
                if (strQuoteTimeType != "")
                    this.QuoteTimeType = (typeTimeFrequency)Enum.Parse(typeof(typeTimeFrequency), strQuoteTimeType);
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

        public new object Clone()
        {
            return MemberwiseClone();
        }

    }

}
