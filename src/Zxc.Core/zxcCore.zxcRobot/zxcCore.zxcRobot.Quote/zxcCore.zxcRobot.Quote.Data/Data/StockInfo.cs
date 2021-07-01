using System;
using System.Collections.Generic;
using System.ComponentModel;
using zxcCore.Extensions;
using zxcCore.zxcData.Cache.MemoryDB;

namespace zxcCore.zxcRobot.Quote.Data
{
    /// <summary>交易所类型
    /// </summary>
    public enum typeStockExchange
    {
        /// <summary>无
        /// </summary>
        none = 0,
        /// <summary>上海证券交易所
        /// </summary>
        [EnumAttr("上海证券交易所", "XSHG"), EnumArea("CN"), EnumRemark("中国A股")]
        sh = 1,
        /// <summary>深圳证券交易所
        /// </summary>
        [EnumAttr("深圳证券交易所", "XSHE"), EnumArea("CN"), EnumRemark("中国A股")]
        sz = 2
    }

    /// <summary>标的类型
    /// </summary>
    public enum typeStock
    {
        [EnumAttr("股票", false), Description("股票")]
        /// <summary>股票
        /// </summary>
        Stock = 0,
        [EnumAttr("指数", true), Description("指数")]
        /// <summary>指数
        /// </summary>
        Index = 1,
        [EnumAttr("ETF基金", true), Description("ETF基金")]
        /// <summary>ETF基金
        /// </summary>
        ETF = 10,
        [EnumAttr("期权", false), Description("期权"), EnumRemark("CON_OP")]
        /// <summary>期权
        /// </summary>
        Option = 20
    }


    /// <summary>标的信息
    /// </summary>
    public class StockInfo : Data_Models
    {
        #region 属性及构造

        /// <summary>标的名称
        /// </summary>
        public string StockName
        {
            get; set;
        }
        /// <summary>标的名称-拼音首字母
        /// </summary>
        public string StockName_En
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
        /// <summary>标的代码-标签聚宽
        /// </summary>
        public string StockID_TagJQ
        {
            get
            {
                return StockID + "." + StockExchange.Get_AttrValue();
            }
        }
        /// <summary>标的代码-标签新浪
        /// </summary>
        public string StockID_TagSina
        {
            get
            {
                //区分期权标签
                if (StockType == typeStock.Option)
                    return StockType.Get_Remark() + "_" + StockID;
                return StockExchange.ToString() + StockID;
            }
        }

        /// <summary>是否停牌
        /// </summary>
        public bool IsSuspended
        {
            get; set;
        }

        public StockInfo()
        {
        }
        ~StockInfo()
        {
            // 缓存数据？
        }

        #endregion


        /// <summary>初始标的信息
        /// </summary>
        public static StockInfo Init_StockInfo(string strLine)
        {
            string[] strTemps = strLine.Split(",");
            if (strTemps.Length < 5) return null;

            string strStockType = strTemps[4] == "opt" ? "Option" : strTemps[4];
            typeStockExchange pStockExchange = (typeStockExchange)Enum.Parse(typeof(typeStockExchange), strTemps[0]);
            typeStock pStockType = (typeStock)Enum.Parse(typeof(typeStock), strStockType, true);
            StockInfo pStockInfo = new StockInfo()
            {
                StockExchange = pStockExchange,
                StockID = strTemps[1],
                StockName = strTemps[2],
                StockName_En = strTemps[3],
                StockType = pStockType
            };
            return pStockInfo;
        }

    }

}
