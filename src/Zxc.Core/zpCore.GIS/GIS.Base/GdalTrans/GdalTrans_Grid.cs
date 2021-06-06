using OSGeo.GDAL;
using OSGeo.OGR;
using System;
using System.Collections.Generic;
using System.Text;
using zpCore.GIS.Trans.Algorithm;

namespace zpCore.GIS.Trans
{
    public class GdalTrans_Grid : GdalTrans
    {
        #region 属性及构造

        protected internal IGdalAlg _GdalAlg = null;

        public GdalTrans_Grid(IGdalRead gdalRead, IGdalAlg gdalAlg) : base(gdalRead)
        {
            _GdalAlg = gdalAlg;
        }
        ~GdalTrans_Grid()
        {
        }

        #endregion


        public bool TransToGrid(string vectorFilename, string strAtrrName, string outFilename, double dPixCellSize = 0.0005, double dEnvelope_offsetX = 0, double dEnvelope_offsetY = 0, DataType typeData = DataType.GDT_Float64)
        {
            // 初始GdalRead
            this._GdalRead = GdalRead_Factory.CreateGdalRead(vectorFilename);
            this._GdalRead.InitDataSource(vectorFilename, Encoding.UTF8, 0, false);

            return this.TransToGrid(strAtrrName, outFilename, dPixCellSize, dEnvelope_offsetX, dEnvelope_offsetY, typeData);
        }
        public bool TransToGrid(string strAtrrName, string outFilename, double dPixCellSize = 0.0005, double dEnvelope_deltaX = 0, double dEnvelope_deltaY = 0, DataType typeData = DataType.GDT_Float64)
        {
            if (_GdalRead == null) return false;
            if (_GdalRead.Layer == null) return false;

            // 读入数组并统计出最大最小值
            int nNumPoints = (int)_GdalRead.FeatureCount;
            double[] padfX = new double[nNumPoints];
            double[] padfY = new double[nNumPoints];
            double[] padfZ = new double[nNumPoints];
            double[] pointXY = new double[2];
            Dictionary<string, string> dictFieldInfo;
            for (int i = 0; i < nNumPoints; i++)
            {
                Geometry objGeo = _GdalRead.GetGeometry(i);
                objGeo.GetPoint(0, pointXY);
                padfX[i] = pointXY[0];
                padfY[i] = pointXY[1];

                _GdalRead.GetFeildContent(i, out dictFieldInfo);
                padfZ[i] = Convert.ToDouble(dictFieldInfo[strAtrrName]);
                objGeo.Dispose();
            }

            //计算图像大小-按数据边界
            Envelope envelope = new Envelope();
            _GdalRead.Layer.GetExtent(envelope, 1);
            double[] dEnvelopes = new double[] { envelope.MinX, envelope.MaxX, envelope.MinY, envelope.MaxY };
            envelope.Dispose();

            //空间参考
            String pszWKT = "";
            _GdalRead.Layer.GetSpatialRef().ExportToWkt(out pszWKT, null);
            if (pszWKT != "") this._SpatialWKT = pszWKT;

            return TransToGrid(padfX, padfY, padfZ, dEnvelopes, outFilename, dPixCellSize, dEnvelope_deltaX, dEnvelope_deltaY, typeData);
        }
        public bool TransToGrid(double[] padfX, double[] padfY, double[] padfZ, double[] dEnvelopes, string outFilename, double dPixCellSize = 0.0005, double dEnvelope_offsetX = 0, double dEnvelope_offsetY = 0, DataType typeData = DataType.GDT_Float64)
        {
            if (padfX.Length != padfY.Length && padfX.Length != padfZ.Length) return false;

            //计算图像大小-按数据边界（dEnvelopes：MinX，MaxX，MinY，MaxY）
            int nNumPoints = padfX.Length;
            int nXSize = (int)((dEnvelopes[1] - dEnvelopes[0] + 2 * dEnvelope_offsetX) / dPixCellSize);
            int nYSize = (int)((dEnvelopes[3] - dEnvelopes[2] + 2 * dEnvelope_offsetY) / dPixCellSize);


            // 创建输出数据集，格式为GeoTiff格式
            OSGeo.GDAL.Driver poDriver = Gdal.GetDriverByName(_DstDriverName);
            Dataset poDataset = poDriver.Create(outFilename, nXSize, nYSize, 1, typeData, null);
            if (_SpatialWKT != "")
                poDataset.SetProjection(_SpatialWKT);


            // 离散点内插方法，参数生成
            string poOptions = _GdalAlg.InitOptions();
            double[] pData = new double[nXSize * nYSize];
            Gdal.GridCreate(poOptions, nNumPoints, padfX, padfY, padfZ,
                                dEnvelopes[0], dEnvelopes[1], dEnvelopes[2], dEnvelopes[3], nXSize, nYSize,
                                typeData, pData, nXSize * nYSize * 8, null, null);

            // 设置六参数
            double[] adfGeoTransform = new double[] { dEnvelopes[0] - dEnvelope_offsetX, dPixCellSize, 0, dEnvelopes[3] + dEnvelope_offsetY, 0, -dPixCellSize };
            poDataset.SetGeoTransform(adfGeoTransform);

            // 写入影像
            Band poBand = poDataset.GetRasterBand(1);
            poBand.WriteRaster(0, 0, nXSize, nYSize, pData, nXSize, nYSize, 0, 0);
            poBand.SetNoDataValue(_NoDataValue);

            poBand.FlushCache();
            poDataset.FlushCache();

            // 释放资源 关闭图像
            poBand.Dispose();
            poDriver.Dispose();
            poDataset.Dispose();
            return true;
        }

    }
}
