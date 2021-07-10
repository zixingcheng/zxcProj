//===============================================================================
// Copyright @ 2021 Guangzhou Yijian Life Technology Co.,Ltd. All rights reserved.
// Copyright @ 2021 广州易简生活科技有限公司.  版权所有.
//===============================================================================
// 文件名称： 
// 功能描述：Quantify_Quote --行情量化分析
// 创建标识：zxc   2021-07-04
// 修改标识： 
// 修改描述：
//===============================================================================
using System;
using System.Collections.Generic;
using zxcCore.Common;
using zxcCore.Extensions;
using zxcCore.zxcData.Analysis;
using zxcCore.zxcData.Cache.Memory;
using zxcCore.zxcRobot.Quote.Data;

namespace zxcCore.zxcRobot.Quote.Quantify
{
    /// <summary>行情量化分析
    /// </summary>
    public class Quantify_Quote : DataAnalyse_Trend
    {
        #region 属性及构造

        public string Tag
        {
            get { return _tag; }
        }


        protected internal IDataCache<Data_Quote> _DataCache = null;           //缓存数据对象
        protected internal Dictionary<typeIndex, Index> _Indexs = null;
        public Quantify_Quote(string tagName, IDataCache<Data_Quote> dataCache) : base(dataCache.DataCache_Set.Time_Frequency)
        {
            _Indexs = new Dictionary<typeIndex, Index>();
            _DataCache = dataCache;
        }

        #endregion


        /// <summary>初始指标对象
        /// </summary>
        /// <param name="typeIndex"></param>
        /// <param name="n">指标时间步长</param>
        /// <returns></returns>
        public virtual bool Init_Index(typeIndex typeIndex, int n = 14)
        {
            bool bResult = true;
            if (_DataCache == null) return false;

            //初始指标对象
            //var aa = new Index_CCI<Data_Quote>(_DataCache.DataCaches, n, _DataCache.DataCache_Set.Time_Frequency);
            Index pIndex = (Index)zxcReflectionHelper.CreateObj<Data_Quote>((Type)typeIndex.Get_AttrValue(), new object[] { _DataCache.DataCaches, n, _DataCache.DataCache_Set.Time_Frequency });
            pIndex.Calculate_All();
            _Indexs[typeIndex] = pIndex;
            return true;
        }


        //数据监测实现（具化数据对象及缓存）-观察者模式
        public virtual bool Calculate(DateTime dtTime, Data_Quote data)
        {
            bool bResult = true;
            foreach (KeyValuePair<typeIndex, Index> index in _Indexs)
            {
                bResult = bResult && (index.Value.Calculate(dtTime, data) != double.NaN);
            }
            return bResult;
        }

    }
}
