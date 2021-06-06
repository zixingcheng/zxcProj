using OSGeo.GDAL;
using OSGeo.OGR;
using OSGeo.OSR;
using System;
using System.Collections.Generic;
using System.Text;
using zpCore.GIS.Trans.Algorithm;

namespace zpCore.GIS.Trans
{
    public class GdalTrans_Contour : GdalTrans
    {
        #region 属性及构造

        public GdalTrans_Contour(IGdalRead gdalRead) : base(gdalRead)
        {
        }
        ~GdalTrans_Contour()
        {
        }

        #endregion


        /// <summary>等值线提取
        /// </summary>
        /// <param name="srcRasterFilename"></param>
        /// <param name="dstVectorFilename"></param>
        /// <param name="dfContourInterval"></param>
        /// <returns></returns>
        public bool ContourGenerate(string srcRasterFilename, string dstVectorFilename, int nBandIndex = 1, double[] dLevelIntervals = null, double dLevelBase = 0, bool isPolygon = true, string driverName = "GeoJSON")
        {
            Dataset pInDataset = Gdal.Open(srcRasterFilename, Access.GA_ReadOnly);
            if (pInDataset == null)
            {
                Console.WriteLine("读取图像失败！");
                System.Environment.Exit(-1);
            }
            return ContourGenerate(dstVectorFilename, "", pInDataset, 1, dLevelIntervals, dLevelBase, isPolygon, driverName);
        }
        public bool ContourGenerate(string dstVectorFilename, string strAtrrName, Dataset pInDataset, int nBandIndex = 1, double[] dLevelIntervals = null, double dLevelBase = 0, bool isPolygon = true, string driverName = "GeoJSON")
        {
            if (pInDataset == null) return false;            

            //提取图像参数值
            int nDemWidth = pInDataset.RasterXSize;     //获取图像宽 
            int nDemHeight = pInDataset.RasterYSize;    //获取图像高 
            int nCount = pInDataset.RasterCount;        //波段数 

            //读取图像数据波段
            Band poBand = pInDataset.GetRasterBand(nBandIndex);
            float[] pData = new float[nDemWidth * nDemHeight];

            CPLErr err = poBand.ReadRaster(0, 0, nDemWidth, nDemHeight, pData, nDemWidth, nDemHeight, 4, 0);
            if (err == CPLErr.CE_Failure)
            {
                Gdal.GDALDestroyDriverManager();
                Console.WriteLine("读取DEM图像数据时出错！");
                return false;
            }

            //判断图像中是否有异常值，并获取异常值实际值
            float fNoData = 0;
            int nIdx;
            for (int i = 0; i < nDemHeight; i++)
            {
                for (int j = 0; j < nDemWidth; j++)
                {
                    nIdx = i * nDemWidth + j;
                    if (pData[nIdx] <= -9999)
                    {
                        fNoData = pData[nIdx];
                    }
                }
            }


            //创建矢量图
            OSGeo.OGR.Driver poDriver = Ogr.GetDriverByName(driverName);
            if (poDriver == null)
            {
                Console.WriteLine(driverName + " driver not available.");
                return false;
            }

            //载入数据源
            DataSource poDS = poDriver.CreateDataSource(dstVectorFilename, null);
            if (poDS == null)
            {
                Console.WriteLine("Creation of output file failed.");
                return false;
            }

            SpatialReference poSpatialRef = new SpatialReference(pInDataset.GetProjectionRef());
            Layer poLayer = poDS.CreateLayer("Contour", poSpatialRef, wkbGeometryType.wkbLineString, null);
            if (poLayer == null)
            {
                Console.WriteLine("Layer creation failed.");
                return false;
            }

            if (strAtrrName == "") strAtrrName = "Elevation";
            FieldDefn oFieldDef = new FieldDefn(strAtrrName, FieldType.OFTInteger);    //在矢量图中创建高程值字段
            if (poLayer.CreateField(oFieldDef, 1) != Ogr.OGRERR_NONE)
            {
                Console.WriteLine("创建矢量图层属性表失败！");
                poDS.Dispose();
                pInDataset.Dispose();
                return false;
            }


            //组装参数
            List<string> lstOptions = new List<string>() { };
            if (dLevelIntervals == null)
                lstOptions.Add("LEVEL_INTERVAL=" + 0);
            else
            {
                if (dLevelIntervals.Length == 1)
                    lstOptions.Add("LEVEL_INTERVAL=" + dLevelIntervals[1]);
                else
                {
                    lstOptions.Add("FIXED_LEVELS=[" + string.Join(",", dLevelIntervals) + "]");
                }
            }
            lstOptions.Add("LEVEL_BASE=" + dLevelBase);
            lstOptions.Add("NODATA=" + fNoData);
            lstOptions.Add("POLYGONIZE=" + (isPolygon ? "YES" : "NO"));
            if (isPolygon)
            {
                lstOptions.Add("ELEV_FIELD_MAX=0");
                lstOptions.Add("ELEV_FIELD_MIN=0");
            }

            //根据图像波段生成矢量图等高线
            //Gdal.ContourGenerate(pInRasterBand, dfContourInterval, 0, 0, null, 1, fNoData, poLayer, -1, 0, null, null);
            //string[] options = new string[] { "LEVEL_INTERVAL=" + 5, "LEVEL_BASE=" + 5, "NODATA=" + fNoData, "POLYGONIZE=YES", "ELEV_FIELD_MIN=0", "ELEV_FIELD_MAX=0", "FIXED_LEVELS=[20,30,40,50,60,100]" };
            Gdal.ContourGenerateEx(poBand, poLayer, lstOptions.ToArray(), null, null);

            //释放资源
            poDS.Dispose();
            poLayer.Dispose();
            poDriver.Dispose();
            pInDataset.Dispose();
            return true;
        }

    }
}
