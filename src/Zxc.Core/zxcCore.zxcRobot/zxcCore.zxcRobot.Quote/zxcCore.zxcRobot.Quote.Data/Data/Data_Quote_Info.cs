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
using zxcCore.zxcData.Cache.MemoryDB;

namespace zxcCore.zxcRobot.Quote.Data
{

    /// <summary>行情数据类-含信息
    /// </summary>
    public class Data_Quote_Info : Data_Quote
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


        protected internal bool _isIndex { get; set; }  //师傅为指数
        public Data_Quote_Info()
        {

        }
        ~Data_Quote_Info()
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
        protected internal override bool Init_ValueAll()
        {
            _isInitAll = base.Init_ValueAll();
            _isInitAll = true;
            return this.Check_StockInfo();
        }
        protected internal virtual bool Check_StockInfo()
        {
            StockInfo pStockInfo = Quote_Datas._Datas.Get_StockInfo(StockID, StockName);
            if (pStockInfo == null)
                return false;

            //同步信息
            StockName = pStockInfo.StockName;
            StockID = pStockInfo.StockID;
            StockType = pStockInfo.StockType;
            StockExchange = pStockInfo.StockExchange;
            if (StockType == typeStock.Index)
                this.Price_Avg = 0;
            return true;
        }

        //提取固定行情消息头
        public override string GetMsg_Perfix()
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
        public override string GetValue_str(double dValue)
        {
            //组装消息
            string tagUnit = _isIndex ? "" : "元";
            int digits = _isIndex ? 3 : 2;
            string strValue = string.Format("{0}{1}", Math.Round(dValue, digits), tagUnit);
            return strValue;
        }


        //对象转换-由json对象
        public override bool FromJsonObj(JObject jsonData, typeQuoteTime quoteTime)
        {
            this.StockID = Convert.ToString(jsonData["id"]);
            this.StockName = Convert.ToString(jsonData["name"]);
            return base.FromJsonObj(jsonData, quoteTime);
        }

    }

}
