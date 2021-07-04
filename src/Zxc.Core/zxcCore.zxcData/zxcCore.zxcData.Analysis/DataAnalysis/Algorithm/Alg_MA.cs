//===============================================================================
// Copyright @ 2021 Guangzhou Yijian Life Technology Co.,Ltd. All rights reserved.
// Copyright @ 2021 广州易简生活科技有限公司.  版权所有.
//===============================================================================
// 文件名称： 
// 功能描述：Alg_MA --均值算法
// 创建标识：zxc   2021-07-04
// 修改标识： 
// 修改描述：
//===============================================================================
using zxcCore.Enums;
using System.Collections.Generic;

namespace zxcCore.zxcData.Analysis.Algorithm
{
    /// <summary>行情指标MA
    /// </summary>
    public class Alg_MA
    {
        #region 属性及构造

        public int _N = 14;
        /// <summary>N日
        /// </summary>
        public int N { get { return _N; } }


        protected internal List<double> _Datas = null;
        public Alg_MA(List<double> datas, int n = 14)
        {
            _N = n;
            _Datas = datas;
        }
        ~Alg_MA()
        {
            // 缓存数据？
        }

        #endregion


        /// <summary>计算
        /// </summary>
        /// <returns></returns>
        public virtual double Calculate()
        {
            if (_Datas.Count == _N)
            {
                double dSum = 0;
                foreach (var item in _Datas)
                {
                    dSum += item;
                }
                return dSum / _N;
            }
            return double.NaN;
        }

    }

}
