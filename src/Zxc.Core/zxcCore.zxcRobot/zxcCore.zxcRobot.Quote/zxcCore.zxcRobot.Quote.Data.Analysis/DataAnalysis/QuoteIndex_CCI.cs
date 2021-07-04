using zxcCore.Enums;
using zxcCore.zxcData.Cache.Memory;
using zxcCore.zxcRobot.Quote.Data;
using System.Collections.Generic;
using zxcCore.zxcData.Analysis.Algorithm;

namespace zxcCore.zxcData.Analysis.Quote
{
    /// <summary>行情指标CCI
    /// </summary>
    public class QuoteIndex_CCI<T> : QuoteIndex<T> where T : Data_Quote
    {
        #region 属性及构造

        public QuoteIndex_CCI(List<CacheInfo<T>> dataCacheInfos, int n = 14) :
            base(dataCacheInfos, n)
        {
        }
        ~QuoteIndex_CCI()
        {
            // 缓存数据？
        }

        #endregion


        /// <summary>计算
        /// </summary>
        /// <returns></returns>
        public override double Calculate()
        {
            //计算TP集合
            List<double> dValuesTP = new List<double>();
            foreach (var item in _DataCacheInfos)
            {
                dValuesTP.Add(this.Calculate_TP(item));
            }

            //计算MA
            Alg_MA pMA = new Alg_MA(dValuesTP, _N);
            double dMA = pMA.Calculate();

            //计算绝对偏差的平均值: 近N日（MA－收盘价）的绝对值的累计之和÷N
            Alg_AVEDEV pAVEDEV = new Alg_AVEDEV(dMA, dValuesTP, _N);
            double dMD = pAVEDEV.Calculate();

            //计算CCI: （TP－MA）÷ MD ÷ 0.015
            double dCCI = (dValuesTP[0] - dMA) / dMD / 0.015;
            return dCCI;
        }

        //计算TP
        public virtual double Calculate_TP(CacheInfo<T> pCacheInfo)
        {
            //计算TP集合: 中价等于最高价、最低价和收盘价之和除以3
            T pData = pCacheInfo.Data;
            return (pData.Price_High + pData.Price_Low + pData.Price_Close) / 3;
        }

    }

}
