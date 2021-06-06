using OSGeo.GDAL;
using OSGeo.OGR;
using OSGeo.OSR;
using System;
using System.Collections.Generic;
using System.Text;
using zpCore.GIS.Trans.Algorithm;

namespace zpCore.GIS.Trans
{
    public class GdalTrans_Raster : GdalTrans
    {
        #region 属性及构造

        public GdalTrans_Raster(IGdalRead gdalRead) : base(gdalRead)
        {
        }
        ~GdalTrans_Raster()
        {
        }

        #endregion

        public bool TransToRaster(string vectorFilename, string strAtrrName, string dstRasterFile, double[] dEnvelopes, double dPixCellSize = 0.0005, double dEnvelope_offsetX = 0, double dEnvelope_offsetY = 0, string driverName = "GTiff", DataType typeData = DataType.GDT_Float32)
        {
            // 初始GdalRead
            this._GdalRead = GdalRead_Factory.CreateGdalRead(vectorFilename);
            this._GdalRead.InitDataSource(vectorFilename, Encoding.UTF8, 0, false);
            if (this._GdalRead == null || this._GdalRead.Layer == null)
            {
                Console.WriteLine(vectorFilename + " open failed.");
                return false;
            }

            return this.TransToRaster(strAtrrName, dstRasterFile, dEnvelopes, dPixCellSize, dEnvelope_offsetX, dEnvelope_offsetY, driverName, typeData);
        }

        public bool TransToRaster(string strAtrrName, string dstRasterFile, double[] dEnvelopes, double dPixCellSize = 0.0005, double dEnvelope_offsetX = 0, double dEnvelope_offsetY = 0, string driverName = "GTiff", DataType typeData = DataType.GDT_Float32)
        {
            //载入矢量数据
            if (this._GdalRead == null || this._GdalRead.Layer == null)
            {
                Console.WriteLine("vectorFile open failed.");
                return false;
            }
            if (dEnvelopes == null || dEnvelopes.Length == 0)
            {
                //计算图像大小-按数据边界
                Envelope envelope = new Envelope();
                _GdalRead.Layer.GetExtent(envelope, 1);
                dEnvelopes = new double[] { envelope.MinX, envelope.MaxX, envelope.MinY, envelope.MaxY };
                envelope.Dispose();
            }

            //计算图像大小-按数据边界（dEnvelopes：MinX，MaxX，MinY，MaxY）
            int nXSize = (int)((dEnvelopes[1] - dEnvelopes[0] + 2 * dEnvelope_offsetX) / dPixCellSize);
            int nYSize = (int)((dEnvelopes[3] - dEnvelopes[2] + 2 * dEnvelope_offsetY) / dPixCellSize);

            //计算六参数
            double[] adfGeoTransform = new double[] { dEnvelopes[0] - dEnvelope_offsetX, dPixCellSize, 0, dEnvelopes[3] + dEnvelope_offsetY, 0, -dPixCellSize };


            //创建目标栅格数据
            Dataset poDstDataset = Gdal.GetDriverByName(driverName).Create(dstRasterFile, nXSize, nYSize, 1, typeData, null);
            if (poDstDataset == null)
            {
                Console.WriteLine(dstRasterFile + " create failed.");
                return false;
            }
            poDstDataset.SetGeoTransform(adfGeoTransform);
            poDstDataset.SetSpatialRef(this._GdalRead.Layer.GetSpatialRef());

            Band poBand = poDstDataset.GetRasterBand(1);
            poBand.SetNoDataValue(_NoDataValue);

            //RasterizeLayer矢量创建栅格
            int[] nBands = new int[] { 1 };
            double[] urnValues = new double[] { 1 };
            List<string> lstOptions = new List<string>() { };
            if (strAtrrName != "")
                lstOptions.Add("ATTRIBUTE:" + strAtrrName);
            //lstOptions.Add("ALL_TOUCHED=TRUE");

            int nRes = Gdal.RasterizeLayer(poDstDataset, 1, nBands, this._GdalRead.Layer, IntPtr.Zero, IntPtr.Zero, 1, urnValues, lstOptions.ToArray(), null, null);

            // 写入影像
            poBand.FlushCache();
            poDstDataset.FlushCache();

            // 释放资源 关闭图像
            poBand.Dispose();
            poDstDataset.Dispose();
            return true;
        }

    }
}
