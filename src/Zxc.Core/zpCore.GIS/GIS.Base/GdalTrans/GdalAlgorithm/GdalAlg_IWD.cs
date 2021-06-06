using OSGeo.GDAL;
using OSGeo.OGR;
using System;
using System.Collections.Generic;
using System.Text;

namespace zpCore.GIS.Trans.Algorithm
{
    public class GdalAlg_IWD: GdalAlg
    {
        #region 属性及构造

        /// <summary>加权能力
        /// </summary>
        protected internal double _Power = 20.0;
        public double Power
        {
            set { _Power = value; }
            get { return _Power; }
        }

        /// <summary>平滑参数
        /// </summary>
        protected internal double _Smoothing = 10;
        public double Smoothing
        {
            set { _Smoothing = value; }
            get { return _Smoothing; }
        }

        /// <summary>搜索椭圆的第一个半径（如果旋转角度为0，则为X轴）
        /// </summary>
        protected internal double _Radius1 = 0.5;
        public double Radius1
        {
            set { _Radius1 = value; }
            get { return _Radius1; }
        }
        /// <summary>搜索椭圆的第二半径（Y轴，如果旋转角度为0）
        /// </summary>
        protected internal double _Radius2 = 0.3;
        public double Radius2
        {
            set { _Radius2 = value; }
            get { return _Radius2; }
        }

        /// <summary>椭圆旋转角度，以度为单位（椭圆逆时针旋转）
        /// </summary>
        protected internal double _Angle = 45;
        public double RadiAngleus2
        {
            set { _Angle = value; }
            get { return _Angle; }
        }

        /// <summary>要使用的最大数据点数（搜索的点数不要超过此数字。如果发现的点较少，则网格节点被认为是空的，并将被NODATA标记填充）
        /// </summary>
        protected internal int _MaxPoints = 10;
        public int MaxPoints
        {
            set { _MaxPoints = value; }
            get { return _MaxPoints; }
        }
        /// <summary>使用的最小数据点数（如果发现的点较少，则网格节点被认为是空的，并将被NODATA标记填充。）
        /// </summary>
        protected internal int _MinPoints = 1;
        public int MinPoints
        {
            set { _MinPoints = value; }
            get { return _MinPoints; }
        }

        /// <summary>没有数据标记可填充空白点
        /// </summary>
        protected internal double _NoDataValue = -9999;
        public double NoDataValue
        {
            set { _NoDataValue = value; }
            get { return _NoDataValue; }
        }

        public GdalAlg_IWD()
        {
            _AlgName = "IDW";
            _AlgNameAlias = "反距离权重插值算法";
            _AlgOptions = "invdist";
            _AlgOption_paramTag = "invdist";
            _AlgOption_paramName = "GGA_InverseDistanceToAPower";
            _AlgOptionName = "GDALGridInverseDistanceToAPowerOptions";
        }
        ~GdalAlg_IWD()
        {
        }

        #endregion

        public override string InitOptions()
        {
            string options = this._AlgOption_paramTag;
            options += ":" + this._Power.ToString();
            options += ":" + this._Smoothing.ToString();
            options += ":" + this._Radius1.ToString();
            options += ":" + this._Radius2.ToString();
            options += ":" + this._MaxPoints.ToString();
            options += ":" + this._MinPoints.ToString();
            options += ":" + this._NoDataValue.ToString();

            this._AlgOptions = options;
            return options;
        }

    }
}