//===============================================================================
// Copyright @ 2021 Guangzhou Yijian Life Technology Co.,Ltd. All rights reserved.
// Copyright @ 2021 广州易简生活科技有限公司.  版权所有.
//===============================================================================
// 文件名称： 
// 功能描述：QuoteIndex_MA --行情指标MA计算
// 创建标识：zxc   2021-07-04
// 修改标识： 
// 修改描述：
//===============================================================================
using zxcCore.Enums;
using zxcCore.zxcData.Cache.Memory;
using zxcCore.zxcRobot.Quote.Data;
using System.Collections.Generic;

namespace zxcCore.zxcData.Analysis.Quote
{
    /// <summary>行情指标MA计算
    /// </summary>
    public class QuoteIndex_MA<T> : QuoteIndex<T> where T : Data_Quote
    {
        #region 属性及构造

        public QuoteIndex_MA(List<CacheInfo<T>> dataCacheInfos, int n = 14) :
            base(dataCacheInfos, n)
        {
        }
        ~QuoteIndex_MA()
        {
            // 缓存数据？
        }

        #endregion


        /// <summary>计算
        /// </summary>
        /// <returns></returns>
        public override double Calculate()
        {
            if (_DataCacheInfos.Count == _N)
            {
                double dSum = 0;
                foreach (var item in _DataCacheInfos)
                {
                    dSum += item.Data.Price_Avg;
                }
                return dSum / _N;
            }
            return double.NaN;
        }

    }

}
