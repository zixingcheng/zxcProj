using OSGeo.GDAL;
using OSGeo.OGR;
using System;
using System.Collections.Generic;
using System.Text;

namespace zpCore.GIS.Trans.Algorithm
{
    public interface IGdalAlg
    {
        /// <summary>Gdal算法名称
        /// </summary>
        string AlgName { get; }
        /// <summary>Gdal算法别名
        /// </summary>
        string AlgNameAlias { get; }
        /// <summary>Gdal算法参数字符串
        /// </summary>
        string AlgOptions { get; }

        /// <summary>初始Gdal算法参数字符串
        /// </summary>
        /// <returns></returns>
        string InitOptions();
    }
}