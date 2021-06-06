using OSGeo.GDAL;
using OSGeo.OGR;
using System;
using System.Collections.Generic;
using System.Text;
using zpCore.GIS.Trans.Algorithm;

namespace zpCore.GIS.Trans
{
    public class GdalTrans_Clip : GdalTrans
    {
        #region 属性及构造

        public GdalTrans_Clip(IGdalRead gdalRead = null) : base(gdalRead)
        {
        }
        ~GdalTrans_Clip()
        {
        }

        #endregion


        public bool ClipRaster(string vectorFilename, string strWhere, string srcRasterFilename, int srcRasterBandIndex, string dstRasterFilename, double dstNoData = -9999)
        {
            Dataset poDataset = Gdal.Open(srcRasterFilename, Access.GA_ReadOnly);
            return ClipRaster(vectorFilename, strWhere, poDataset, srcRasterBandIndex, dstRasterFilename, dstNoData);
        }
        public bool ClipRaster(string vectorFilename, string strWhere, Dataset poDataset, int srcRasterBandIndex, string dstRasterFilename, double dstNoData = -9999)
        {
            if (poDataset == null) return false;

            //提取Nodata
            int nNoData = 0;
            double dNoData = 0;
            Band poBand = poDataset.GetRasterBand(srcRasterBandIndex);
            poBand.GetNoDataValue(out dNoData, out nNoData);

            //组装参数( "O_Name='南城区'" )
            List<string> lstOptions = new List<string>() { "-srcnodata", dNoData.ToString(), "-dstnodata", dstNoData.ToString(), "-of", _DstDriverName, "-cutline", vectorFilename };
            if (strWhere != "")
            {
                lstOptions.Add("-cwhere");
                lstOptions.Add(strWhere);
            }

            //调用裁剪
            GDALWarpAppOptions objOption = new GDALWarpAppOptions(lstOptions.ToArray());
            Dataset poResDataset = OSGeo.GDAL.Gdal.Warp(dstRasterFilename, new Dataset[] { poDataset }, objOption, null, null);
            if (poResDataset != null)
            {
                poResDataset.Dispose();
                return true;
            }
            return false;
        }

    }
}
