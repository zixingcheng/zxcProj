using zxcCore.Enums;
using zxcCore.zxcData.Cache.Memory;
using zxcCore.zxcRobot.Quote.Data;
using System.Collections.Generic;

namespace zxcCore.zxcData.Analysis.Quote
{
    /// <summary>行情指标基类
    /// </summary>
    public class QuoteIndex
    {
        #region 属性及构造

        public int _N = 14;
        /// <summary>N日
        /// </summary>
        public int N { get { return _N; } }


        public QuoteIndex(int n = 14)
        {
            _N = n;
        }

        #endregion

    }


    /// <summary>行情指标基类
    /// </summary>
    public class QuoteIndex<T> : QuoteIndex where T : Data_Quote
    {
        #region 属性及构造

        protected internal List<CacheInfo<T>> _DataCacheInfos = null;
        public QuoteIndex(List<CacheInfo<T>> dataCacheInfos, int n = 14) :
            base(n)
        {
            _DataCacheInfos = dataCacheInfos;
        }
        ~QuoteIndex()
        {
            // 缓存数据？
        }

        #endregion

        /// <summary>初始计算值
        /// </summary>
        /// <returns></returns>
        public virtual bool Init(List<CacheInfo<T>> dataCacheInfos)
        {
            _DataCacheInfos = dataCacheInfos;
            return _DataCacheInfos.Count == _N;
        }

        /// <summary>计算
        /// </summary>
        /// <returns></returns>
        public virtual double Calculate()
        {
            return double.NaN;
        }

    }

}
