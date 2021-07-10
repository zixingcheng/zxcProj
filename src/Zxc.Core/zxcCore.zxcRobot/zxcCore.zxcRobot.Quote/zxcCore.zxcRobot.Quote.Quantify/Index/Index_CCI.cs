using System;
using System.Collections.Generic;
using System.Linq;
using zxcCore.Enums;
using zxcCore.zxcData.Analysis.Quote;
using zxcCore.zxcData.Cache.Memory;
using zxcCore.zxcRobot.Quote.Data;

namespace zxcCore.zxcRobot.Quote.Quantify
{
    /// <summary>行情指标CCI
    /// </summary>
    public class Index_CCI<T> : Index<T> where T : Data_Quote
    {
        #region 属性及构造

        public Index_CCI(Dictionary<DateTime, CacheInfo<T>> dataCacheInfos, int n = 14, typeTimeFrequency timeFrequency = typeTimeFrequency.m15) :
            base(dataCacheInfos, n, timeFrequency)
        {
        }
        ~Index_CCI()
        {
            // 缓存数据？
        }

        #endregion


        /// <summary>计算所有
        /// </summary>
        /// <returns></returns>
        public override bool Calculate_All()
        {
            //提取可用计算时间，并循环计算
            List<DateTime> lstTime = _DataCacheInfos.Keys.OrderByDescending(e => e).Take(_DataCacheInfos.Count - _N).ToList();
            lstTime.Reverse();      //调整为升序

            bool bResult = true;
            foreach (var item in lstTime)
            {
                bResult = bResult && this.Calculate(item) != double.NaN;
            }
            return bResult;
        }
        /// <summary>计算所有
        /// </summary>
        /// <returns></returns>
        public override double Calculate()
        {
            return double.NaN;
        }
        /// <summary>计算指定时间指标
        /// </summary>
        /// <param name="dtNow"></param>
        /// <param name="data">当前时间数据</param>
        /// <returns></returns>
        public override double Calculate(DateTime dtNow, Data_Quote data = null)
        {
            //筛选指定时间指标计算数据
            List<CacheInfo<T>> lstQuote = _DataCacheInfos.Values.Where(e => e.DateTime <= dtNow).OrderByDescending(e => e.DateTime).Take(_N).ToList();


            //初始指标计算对象
            QuoteIndex_CCI<T> pIndex_CCI = new QuoteIndex_CCI<T>(null, _N);
            if (pIndex_CCI.Init(lstQuote))
            {
                //指标计算
                double dCCI = pIndex_CCI.Calculate();

                this.CacheIndex(dCCI, dtNow);
                return dCCI;
            }
            return double.NaN;
        }

        /// <summary>缓存指标值
        /// </summary>
        /// <returns></returns>
        public override bool CacheIndex(double dIndex, DateTime dtNow)
        {
            _valueIndexs[dtNow] = dIndex;
            return true;
        }

    }

}
