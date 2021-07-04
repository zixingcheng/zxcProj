//===============================================================================
// Copyright @ 2021 Guangzhou Yijian Life Technology Co.,Ltd. All rights reserved.
// Copyright @ 2021 广州易简生活科技有限公司.  版权所有.
//===============================================================================
// 文件名称： 
// 功能描述：Alg_AVEDEV --绝对偏差的平均值
// 创建标识：zxc   2021-07-04
// 修改标识： 
// 修改描述：
//===============================================================================
using System;
using System.Collections.Generic;
using zxcCore.Enums;

namespace zxcCore.zxcData.Analysis.Algorithm
{
    /// <summary>绝对偏差的平均值
    /// </summary>
    public class Alg_AVEDEV
    {
        #region 属性及构造

        public int _N = 14;
        /// <summary>N日
        /// </summary>
        public int N { get { return _N; } }


        protected internal List<double> _Datas = null;
        protected internal double _DataBase = 0;
        public Alg_AVEDEV(double dataBase, List<double> datas, int n = 14)
        {
            _N = n;
            _Datas = datas;
            _DataBase = dataBase;
        }
        ~Alg_AVEDEV()
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
                    dSum += Math.Abs(item - _DataBase);
                }
                return dSum / _N;
            }
            return double.NaN;
        }

    }

}
