using OSGeo.GDAL; 
using OSGeo.OSR;
using System;
using System.Collections.Generic;
using System.Runtime.InteropServices;
using System.Text;

namespace zpCore.GIS
{
    public class GdalRead_TIFF : GdalRead_GeoJson, IGdalReadR
    {
        #region 属性及构造

        protected internal Dataset _Dataset;
        public Dataset Dataset
        {
            get { return _Dataset; }
        }

        protected internal Band _Band;
        public Band Band
        {
            get { return _Band; }
        }


        public GdalRead_TIFF() : base()
        {
            _IsRaster = true;
        }
        ~GdalRead_TIFF()
        {
            if (_Dataset != null) _Dataset.Dispose();
            if (_Band != null) _Band.Dispose();
        }

        #endregion
        
        
        protected override void InitDriver()
        {
            _DriverName = "Gtiff";
            _Driver = OSGeo.OGR.Ogr.GetDriverByName(_DriverName);
        }

        public virtual bool InitDataset(string strFilenameR, int nBandindex = 0, bool bUpdata = false)
        {
            _Dataset = Gdal.Open(strFilenameR, bUpdata ? Access.GA_Update : Access.GA_ReadOnly);
            return true;
        }

        public virtual IMetadataR GetMetadataR(int nBandIndex = 1)
        {
            if (this._Dataset == null) return null;

            //提取图像参数值
            MetadataR pMeta = new MetadataR();
            pMeta.Cols = _Dataset.RasterXSize;      //获取图像宽 
            pMeta.Rows = _Dataset.RasterYSize;      //获取图像高 
            pMeta.Bands = _Dataset.RasterCount;     //波段数 
            if (pMeta.Bands < nBandIndex - 1) return null;

            double[] adfGeoTransform = new double[6];
            _Dataset.GetGeoTransform(adfGeoTransform);
            pMeta.MinX = adfGeoTransform[0];
            pMeta.MinY = adfGeoTransform[3];
            pMeta.IsNorthern = (adfGeoTransform[1] + adfGeoTransform[4] == 0);

            int ratio = pMeta.IsNorthern ? 1 : -1;
            pMeta.CellSize = adfGeoTransform[1];
            pMeta.MaxX = pMeta.MinX + pMeta.CellSize * pMeta.Cols;
            pMeta.MaxY = pMeta.MinY + ratio * pMeta.CellSize * pMeta.Rows;

            pMeta.MaxX = Math.Round(pMeta.MaxX, 8);
            pMeta.MaxY = Math.Round(pMeta.MaxY, 8);

            double dNoData = 0;
            Band poBand = _Dataset.GetRasterBand(nBandIndex);
            poBand.GetNoDataValue(out dNoData, out _);
            pMeta.NoDataValue = dNoData;
            return pMeta;
        }
        public virtual double GetNodata(int nBandIndex = 1)
        {
            double dNoData = 0;
            Band poBand = _Dataset.GetRasterBand(0);
            poBand.GetNoDataValue(out dNoData, out _);
            return dNoData;
        }        

        public bool GetDatas(int nBandIndex, ref int[] pDatas)
        {
            if (this._Dataset == null) return false;

            //提取图像参数值
            int nDemWidth = _Dataset.RasterXSize;     //获取图像宽 
            int nDemHeight = _Dataset.RasterYSize;    //获取图像高 
            int nCount = _Dataset.RasterCount;        //波段数 
            if (nCount < nBandIndex - 1) return false;

            //读取图像数据波段
            Band poBand = _Dataset.GetRasterBand(nBandIndex);
            pDatas = new int[nDemWidth * nDemHeight];

            CPLErr err = poBand.ReadRaster(0, 0, nDemWidth, nDemHeight, pDatas, nDemWidth, nDemHeight, 4, 0);
            if (err == CPLErr.CE_Failure)
            {
                Gdal.GDALDestroyDriverManager();
                Console.WriteLine("读取栅格图像数据时出错！");
                return false;
            }

            poBand.Dispose();
            return true;
        }
        public bool GetDatas(int nBandIndex, ref float[] pDatas)
        {
            if (this._Dataset == null) return false;

            //提取图像参数值
            int nDemWidth = _Dataset.RasterXSize;     //获取图像宽 
            int nDemHeight = _Dataset.RasterYSize;    //获取图像高 
            int nCount = _Dataset.RasterCount;        //波段数 
            if (nCount < nBandIndex - 1) return false;

            //读取图像数据波段
            Band poBand = _Dataset.GetRasterBand(nBandIndex);
            pDatas = new float[nDemWidth * nDemHeight];

            CPLErr err = poBand.ReadRaster(0, 0, nDemWidth, nDemHeight, pDatas, nDemWidth, nDemHeight, 4, 0);
            if (err == CPLErr.CE_Failure)
            {
                Gdal.GDALDestroyDriverManager();
                Console.WriteLine("读取栅格图像数据时出错！");
                return false;
            }

            poBand.Dispose();
            return true;
        }
        public bool GetDatas(int nBandIndex, ref double[] pDatas)
        {
            if (this._Dataset == null) return false;

            //提取图像参数值
            int nDemWidth = _Dataset.RasterXSize;     //获取图像宽 
            int nDemHeight = _Dataset.RasterYSize;    //获取图像高 
            int nCount = _Dataset.RasterCount;        //波段数 
            if (nCount < nBandIndex - 1) return false;

            //读取图像数据波段
            Band poBand = _Dataset.GetRasterBand(nBandIndex);
            pDatas = new double[nDemWidth * nDemHeight];

            CPLErr err = poBand.ReadRaster(0, 0, nDemWidth, nDemHeight, pDatas, nDemWidth, nDemHeight, 4, 0);
            if (err == CPLErr.CE_Failure)
            {
                Gdal.GDALDestroyDriverManager();
                Console.WriteLine("读取栅格图像数据时出错！");
                return false;
            }

            poBand.Dispose();
            return true;
        }


        /// <summary>初始数据源
        /// </summary>
        /// <param name="strFilename">文件名</param>
        /// <param name="oFileEncoding">文件编码类型</param>
        /// <param name="nLayerindex">层序号</param>
        /// <param name="bUpdata">是否可以修改</param>
        /// <returns></returns>
        public bool CreateDataset(string strFilename, Encoding oFileEncoding, int nLayerindex = 0, bool bUpdata = false)
        {
            int bXSize, bYSize;
            int w, h;
            w = 100;
            h = 100;
            bXSize = w;
            bYSize = 1;

            Gdal.AllRegister();
            OSGeo.GDAL.Driver drv = Gdal.GetDriverByName("GTiff");
            if (drv == null)
            {
                Console.WriteLine("Can't get driver.");
                System.Environment.Exit(-1);
            }
            Console.WriteLine("Using driver " + drv.LongName);

            string[] options = new string[] { "BLOCKXSIZE=" + bXSize, "BLOCKYSIZE=" + bYSize };
            Dataset ds = drv.Create(strFilename, w, h, 1, DataType.GDT_Byte, options);
            if (ds == null)
            {
                Console.WriteLine("Can't open " + strFilename);
                System.Environment.Exit(-1);
            }

            GCP[] GCPs = new GCP[] {
                new GCP(44.5, 27.5, 0, 0, 0, "info0", "id0"),
                new GCP(45.5, 27.5, 0, 100, 0, "info1", "id1"),
                new GCP(44.5, 26.5, 0, 0, 100, "info2", "id2"),
                new GCP(45.5, 26.5, 0, 100, 100, "info3", "id3")
            };
            ds.SetGCPs(GCPs, "");

            Band ba = ds.GetRasterBand(1);
            byte[] buffer = new byte[w * h];
            for (int i = 0; i < w; i++)
            {
                for (int j = 0; j < h; j++)
                {
                    buffer[i * w + j] = (byte)(i * 256 / w);
                }
            }
            ba.WriteRaster(0, 0, w, h, buffer, w, h, 0, 0);
            ba.FlushCache();
            ds.FlushCache();
            return true;
        }
        


        //--Test
        ///******************************************************************** 函数功能：调用gdal自带exe生成等高线 输入参数： imgPath ：dem文件路径 shpPath ：等高线矢量图保存路径 dfContourInterval ：等高线间隔 备注： 需要头文件： #include "gdal_priv.h" #include "gdal_alg.h" #include "gdal_priv.h" #include "ogrsf_frmts.h" *********************************************************************/
        //public bool CalContourByGdal(string imgPath, string shpPath, double dfContourInterval)
        //{
        //    OSGeo.OGR.Ogr.RegisterAll();
        //    OSGeo.GDAL.Gdal.AllRegister();
        //    OSGeo.GDAL.Gdal.SetConfigOption("GDAL_FILENAME_IS_UTF8", "YES");   // 为了支持中文路径

        //    Dataset pInDataset = Gdal.Open(imgPath, Access.GA_ReadOnly);
        //    if (pInDataset == null)
        //    {
        //        Console.WriteLine("读取图像失败！");
        //        System.Environment.Exit(-1);
        //    }

        //    int nDemWidth = pInDataset.RasterXSize;     //获取图像宽 
        //    int nDemHeight = pInDataset.RasterYSize;    //获取图像高 
        //    int Count = pInDataset.RasterCount;         //波段数 

        //    //读取图像数据波段
        //    Band pInRasterBand = pInDataset.GetRasterBand(1);
        //    float[] pData = new float[nDemWidth * nDemHeight];

        //    CPLErr err = pInRasterBand.ReadRaster(0, 0, nDemWidth, nDemHeight, pData, nDemWidth, nDemHeight, 4, 0);
        //    if (err == CPLErr.CE_Failure)
        //    {
        //        Console.WriteLine("读取DEM图像数据时出错！");
        //        Gdal.GDALDestroyDriverManager();
        //        System.Environment.Exit(-1);
        //    }

        //    //判断图像中是否有异常值，并获取异常值实际值
        //    float fNoData = 0;
        //    int nIdx;
        //    for (int i = 0; i < nDemHeight; i++)
        //    {
        //        for (int j = 0; j < nDemWidth; j++)
        //        {
        //            nIdx = i * nDemWidth + j;
        //            if (pData[nIdx] <= -9999)
        //            {
        //                fNoData = pData[nIdx];
        //            }
        //        }
        //    }


        //    //创建矢量图
        //    //OSGeo.OGR.Driver poDriver = Ogr.GetDriverByName("GeoJSON");
        //    //if (poDriver == null)
        //    //{
        //    //    Console.WriteLine("ESRI Shapefile driver not available.");
        //    //    System.Environment.Exit(-1);
        //    //}

        //    ////载入数据源
        //    ////Dataset poDS = poDriver.Create(shpPath, 0, 0, 0, DataType.GDT_Unknown, null);   //创建数据源
        //    //DataSource poDS = poDriver.CreateDataSource(shpPath, null);
        //    //if (poDS == null)
        //    //{
        //    //    Console.WriteLine("Creation of output file failed.");
        //    //    System.Environment.Exit(-1);
        //    //}

        //    //SpatialReference poSpatialRef = new SpatialReference(pInDataset.GetProjectionRef());
        //    //Layer poLayer = poDS.CreateLayer("Elevation", poSpatialRef, wkbGeometryType.wkbLineString, null);
        //    //if (poLayer == null)
        //    //{
        //    //    Console.WriteLine("Layer creation failed.");
        //    //    System.Environment.Exit(-1);
        //    //}

        //    //FieldDefn oFieldDef = new FieldDefn("Elevation", FieldType.OFTInteger);    //在矢量图中创建高程值字段
        //    //if (poLayer.CreateField(oFieldDef, 1) != Ogr.OGRERR_NONE)
        //    //{
        //    //    Console.WriteLine("创建矢量图层属性表失败！");
        //    //    poDS.Dispose();
        //    //    pInDataset.Dispose();
        //    //    System.Environment.Exit(-1);
        //    //}

        //    ////根据图像波段生成矢量图等高线
        //    //if (fNoData == 0)
        //    //{
        //    //    //Gdal.ContourGenerate(pInRasterBand, 2, 5, 0, null, 0, 0, poLayer, -1, 0, null, null);
        //    //    //string[] options = new string[] {
        //    //    //    "LEVEL_INTERVAL = " + 30.ToString(),
        //    //    //    "LEVEL_BASE = " + 0.ToString(),
        //    //    //    "LEVEL_EXP_BASE = " + 1.ToString(),
        //    //    //    "NODATA = " + 0.ToString(),
        //    //    //    "POLYGONIZE = " + false.ToString()
        //    //    //};
        //    //    string[] options = new string[] { "LEVEL_INTERVAL=" + 5, "LEVEL_BASE=" + 5, "NODATA=0", "POLYGONIZE=YES" };
        //    //    Gdal.ContourGenerateEx(pInRasterBand, poLayer, options, null, null);
        //    //}
        //    //else //有异常值时，不对异常值进行处理
        //    //{
        //    //    //Gdal.ContourGenerate(pInRasterBand, dfContourInterval, 0, 0, null, 1, fNoData, poLayer, -1, 0, null, null);
        //    //    string[] options = new string[] { "LEVEL_INTERVAL=" + 5, "LEVEL_BASE=" + 5, "NODATA=" + fNoData, "POLYGONIZE=YES", "ELEV_FIELD_MIN=0", "ELEV_FIELD_MAX=0", "FIXED_LEVELS=[20,30,40,50,60,100]" };
        //    //    Gdal.ContourGenerateEx(pInRasterBand, poLayer, options, null, null);
        //    //}
        //    //
        //    //poDS.Dispose();
        //    //pInDataset.Dispose();
        //    return true;
        //}

        //public void GDALGridTest(string filename, string strAtrrName, string outputfullname)
        //{
        //    // 读取Geojson内容，
        //    IGdalRead gdalRead_GeoJson = new GdalRead_GeoJson();
        //    gdalRead_GeoJson.InitDataSource(filename, Encoding.UTF8, 0, false);

        //    // 读入数组并统计出最大最小值
        //    int nPoints = (int)gdalRead_GeoJson.FeatureCount;
        //    double[] padfX = new double[nPoints];
        //    double[] padfY = new double[nPoints];
        //    double[] padfZ = new double[nPoints];
        //    double[] pointXY = new double[2];
        //    for (int i = 0; i < nPoints; i++)
        //    {
        //        OSGeo.OGR.Geometry objGeo = gdalRead_GeoJson.GetGeometry(i);
        //        objGeo.GetPoint(0, pointXY);
        //        padfX[i] = pointXY[0];
        //        padfY[i] = pointXY[1];

        //        Dictionary<string, string> dictFieldInfo;
        //        gdalRead_GeoJson.GetFeildContent(i, out dictFieldInfo);
        //        padfZ[i] = Convert.ToDouble(dictFieldInfo[strAtrrName]);
        //    }

        //    //计算图像大小-按数据边界
        //    OSGeo.OGR.Envelope envelope = new OSGeo.OGR.Envelope();
        //    gdalRead_GeoJson.Layer.GetExtent(envelope, 1);

        //    double pixResoultion = 0.0005;         //设置分辨率
        //    int nXSize = (int)((envelope.MaxX - envelope.MinX) / pixResoultion);
        //    int nYSize = (int)((envelope.MaxY - envelope.MinY) / pixResoultion);

        //    //空间参考
        //    String pszWKT = "";
        //    gdalRead_GeoJson.Layer.GetSpatialRef().ExportToWkt(out pszWKT, null);
        //    //SpatialReference spatialReference = new SpatialReference("");
        //    //spatialReference.ImportFromEPSG(4326);              //wgs84地理坐标系
        //    //spatialReference.ExportToWkt(out pszWKT, null);
        //    //spatialReference.Dispose();


        //    // 离散点内插方法，使用反距离权重插值法
        //    //GDALGridInverseDistanceToAPowerOptions* poOptions = new GDALGridInverseDistanceToAPowerOptions();
        //    //GDALGridInverseDistanceToAPowerOptions

        //    //poOptions->dfPower = 2;
        //    //poOptions->dfRadius1 = 20;
        //    //poOptions->dfRadius2 = 15;



        //    // 创建输出数据集，格式为GeoTiff格式
        //    OSGeo.GDAL.Driver pDriver = Gdal.GetDriverByName("Gtiff");
        //    Dataset poDataset = pDriver.Create(outputfullname, nXSize, nYSize, 1, DataType.GDT_Float64, null);
        //    poDataset.SetProjection(pszWKT);
            
        //    // 离散点内插方法，使用反距离权重插值法。使用其他的插值算法，这里换成其他的，还有下面的GDALGridCreate函数的对应参数
        //    //GDALGridCreate(GGA_InverseDistanceToAPower, poOptions, nPoints, padfX, padfY, padfZ,
        //    //    dfXMin, dfXMax, dfYMin, dfYMax, nXSize, nYSize, GDT_Byte, pData, NULL, NULL);
        //    string poOptions = "invdist:power=2:smoothing=1:radius1=20:radius1=15:nodata=-9999";
        //    Band band2 = poDataset.GetRasterBand(1);
        //    double[] pData = new double[nXSize * nYSize];
        //    Gdal.GridCreate(poOptions, nPoints, padfX, padfY, padfZ,
        //        envelope.MinX, envelope.MaxX, envelope.MinY, envelope.MaxY, nXSize, nYSize, DataType.GDT_Float64, pData, nXSize * nYSize * 8, null, null);



        //    // 设置六参数
        //    double[] adfGeoTransform = new double[] { envelope.MinX, pixResoultion, 0, envelope.MaxY, 0, -pixResoultion };
        //    poDataset.SetGeoTransform(adfGeoTransform);

        //    // 写入影像
        //    Band band = poDataset.GetRasterBand(1);
        //    band.WriteRaster(0, 0, nXSize, nYSize, pData, nXSize, nYSize, 0, 0);
            


        //    band.FlushCache();
        //    poDataset.FlushCache();

        //    string outputfullname3 = @"D:\myCode\zxcProj\src\Zxc.Core\zpCore.zpGis\zpCore.zpGis_Base\Data\test030.tif";
        //    string outputfullname4 = @"D:\myCode\zxcProj\src\Zxc.Core\zpCore.zpGis\zpCore.zpGis_Base\Data\Shape\Geojson\_shape.geojson";
        //    string[] options = new string[] { "-srcnodata", "0", "-dstnodata", "-9999", "-of", "GTiff", "-cutline", outputfullname4, "-cwhere", "O_Name='南城区'" };
        //    GDALWarpAppOptions objOption = new GDALWarpAppOptions(options);
        //    OSGeo.GDAL.Gdal.Warp(outputfullname3, new Dataset[] { poDataset }, objOption, null, null);


        //    // 释放资源 关闭图像
        //    band.Dispose();
        //    pDriver.Dispose();
        //    poDataset.Dispose();
        //}

    }
}
