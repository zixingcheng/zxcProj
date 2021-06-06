using OSGeo.GDAL;
using OSGeo.OGR;
using System;
using System.Collections.Generic;
using System.Text;
using zpCore.GIS.Trans.Algorithm;

namespace zpCore.GIS.Trans
{
    public abstract class GdalTrans : IGdalTrans
    {
        #region 属性及构造

        /// <summary>输出格网的栅格文件驱动类型
        /// </summary>
        protected internal string _DstDriverName = "Gtiff";
        public string DstDriverName
        {
            set { _DstDriverName = value; }
            get { return _DstDriverName; }
        }

        /// <summary>输出格网的栅格文件驱动类型
        /// </summary>
        protected internal double _NoDataValue = -9999;
        public double NoDataValue
        {
            set { _NoDataValue = value; }
            get { return _NoDataValue; }
        }

        /// <summary>输出格网的栅格文件坐标系
        /// </summary>
        protected internal string _SpatialWKT = "";
        public string SpatialWKT
        {
            set { _SpatialWKT = value; }
            get { return _SpatialWKT; }
        }

        protected internal IGdalRead _GdalRead = null;
        public GdalTrans(IGdalRead gdalRead)
        {
            _GdalRead = gdalRead;
        }
        ~GdalTrans()
        {
        }

        #endregion

    }
}
