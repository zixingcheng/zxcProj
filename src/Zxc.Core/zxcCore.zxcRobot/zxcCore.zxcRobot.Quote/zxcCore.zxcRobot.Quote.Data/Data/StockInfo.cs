using System;
using System.Collections.Generic;
using System.ComponentModel;
using zxcCore.Common;
using zxcCore.Common.TimeSet;
using zxcCore.Enums;
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

        /// <summary>获取标的交易所信息
        /// </summary>
        public StockExchangeInfo Get_StockExchangeInfo()
        {
            return StockExchangeInfo.Get_StockExchangeInfo(this.StockExchange);
        }

    }


    /// <summary>标的交易所信息
    /// </summary>
    public class StockExchangeInfo
    {
        #region 属性及构造
        /// <summary>配置文件信息
        /// </summary>
        protected static internal zxcConfigurationHelper _configExchangeInfo = new zxcConfigurationHelper("appsettings_zxcRobot_Quote_TimeSet.json");
        /// <summary>配置文件信息
        /// </summary>
        protected static internal Dictionary<typeStockExchange, StockExchangeInfo> _stockExchangeInfos = new Dictionary<typeStockExchange, StockExchangeInfo>();


        /// <summary>标的交易所信息
        /// </summary>
        protected internal typeStockExchange _StockExchange = typeStockExchange.sh;
        public typeStockExchange StockExchange { get { return _StockExchange; } }

        /// <summary>标的交易所时间设置
        /// </summary>
        protected internal zxcTimeSets _TimeSets = null;
        public zxcTimeSets TimeSets { get { return _TimeSets; } }


        protected internal List<double> _dictTimes_H = null;
        protected internal List<double> _dictTimes_H2 = null;
        protected internal List<double> _dictTimes_Day = null;
        protected internal double _dayTimes_H = 0;
        public StockExchangeInfo(typeStockExchange stockExchange)
        {
            _StockExchange = stockExchange;
            this.Init_StockExchangeInfo(_StockExchange);
        }
        ~StockExchangeInfo()
        {
            // 缓存数据？
        }

        #endregion


        /// <summary>初始标的交易所信息
        /// </summary>
        public bool Init_StockExchangeInfo(typeStockExchange stockExchange)
        {
            string strTag = stockExchange.ToString();
            string strSet = _configExchangeInfo.config[strTag + ":timeset"];
            _TimeSets = new zxcTimeSets(strSet, strTag);

            //H
            string strSet_Hours = _configExchangeInfo.config[strTag + ":timesets:hours"];
            string[] strTemps = strSet_Hours.Replace(" ", "").Split(",");
            _dictTimes_H = new List<double>();
            foreach (var item in strTemps)
            {
                double dHour = Convert.ToDouble(item);
                _dictTimes_H.Add(dHour);
            }

            //H2
            string strSet_Hours2 = _configExchangeInfo.config[strTag + ":timesets:hours2"];
            string[] strTemps2 = strSet_Hours2.Replace(" ", "").Split(",");
            _dictTimes_H2 = new List<double>();
            foreach (var item in strTemps2)
            {
                double dHour = Convert.ToDouble(item);
                _dictTimes_H2.Add(dHour);
            }

            //Day
            string strSet_Day = _configExchangeInfo.config[strTag + ":timesets:dayofweek"];
            string[] strTemps3 = strSet_Day.Replace(" ", "").Split(",");
            _dictTimes_Day = new List<double>();
            foreach (var item in strTemps3)
            {
                double dDay = Convert.ToDouble(item);
                _dictTimes_Day.Add(dDay);
            }
            _dayTimes_H = Convert.ToDouble(_configExchangeInfo.config[strTag + ":timesets:dayhour"]);
            return true;
        }


        /// <summary>按时间频率修正时间
        /// </summary>
        /// <param name="dtBase"></param>
        /// <param name="timeFrequency"></param>
        /// <returns></returns>
        public DateTime CheckTime(DateTime dtBase, typeTimeFrequency timeFrequency)
        {
            DateTime dtTime = DateTime.MinValue;
            if (!this._TimeSets.IsValid(dtBase))
            {
                double dH = dtBase.Hour + dtBase.Minute / 60.0 + dtBase.Second / 3600.0;
                if (dH >= _dayTimes_H)
                {
                    int nH60 = (int)Math.Floor(_dayTimes_H);
                    dtBase = new DateTime(dtBase.Year, dtBase.Month, dtBase.Day, nH60, (int)((_dayTimes_H - nH60) * 60), 0);
                }
                else if (dH != 0)
                    return dtTime;
            }

            switch (timeFrequency)
            {
                case typeTimeFrequency.day:
                case typeTimeFrequency.m1:
                case typeTimeFrequency.m5:
                case typeTimeFrequency.m10:
                case typeTimeFrequency.m15:
                case typeTimeFrequency.m30:
                    dtTime = zxcTimeHelper.CheckTime(dtBase, timeFrequency, true);
                    break;
                case typeTimeFrequency.m60:
                    double dH60 = dtBase.Hour + dtBase.Minute / 60.0 + dtBase.Second / 3600.0;
                    for (int i = _dictTimes_H.Count - 1; i >= 0; i--)
                    {
                        if (dH60 >= _dictTimes_H[i])
                        {
                            int nH60 = (int)Math.Floor(_dictTimes_H[i]);
                            dtTime = new DateTime(dtBase.Year, dtBase.Month, dtBase.Day, nH60, (int)((_dictTimes_H[i] - nH60) * 60), 0);
                            break;
                        }
                    }
                    break;
                case typeTimeFrequency.m120:
                    double dH120 = dtBase.Hour + dtBase.Minute / 60.0 + dtBase.Second / 3600.0;
                    for (int i = _dictTimes_H2.Count - 1; i >= 0; i--)
                    {
                        if (dH120 >= _dictTimes_H2[i])
                        {
                            int nH60 = (int)Math.Floor(_dictTimes_H2[i]);
                            dtTime = new DateTime(dtBase.Year, dtBase.Month, dtBase.Day, nH60, (int)((_dictTimes_H2[i] - nH60) * 60), 0);
                            break;
                        }
                    }
                    break;
                case typeTimeFrequency.week:
                    if ((int)dtBase.DayOfWeek >= _dictTimes_Day[_dictTimes_Day.Count - 1])
                        dtTime = new DateTime(dtBase.Year, dtBase.Month, dtBase.Day, 0, 0, 0);
                    break;
                default:
                    break;
            }
            return dtTime;
        }


        /// <summary>提取标的交易所信息
        /// </summary>
        public static StockExchangeInfo Get_StockExchangeInfo(typeStockExchange stockExchange)
        {
            StockExchangeInfo pStockExchangeInfo = null;
            if (_stockExchangeInfos.TryGetValue(stockExchange, out pStockExchangeInfo))
            {

            }

            if (pStockExchangeInfo == null)
            {
                pStockExchangeInfo = new StockExchangeInfo(stockExchange);
                _stockExchangeInfos[stockExchange] = pStockExchangeInfo;
            }
            return pStockExchangeInfo;
        }

    }

}
