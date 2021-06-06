using OSGeo.GDAL;
using OSGeo.OGR;
using System;
using System.Collections.Generic;
using System.IO;
using System.Text;
using zpCore.Common;
using zpCore.GIS.Trans.Algorithm;

namespace zpCore.GIS
{
    public class GdalCommon
    {
        public static int rand = 0;
        public static ConfigurationHelper configGisBase = new ConfigurationHelper("appsettings_gisBase.json");
        public static string psDirData_BaseGis = configGisBase.config["GisSetOptions:GisDataDirs:BaseDir"] + "";
        public static string psDirData_OutputGis = configGisBase.config["GisSetOptions:GisDataDirs:OutputDir"] + "";
        public static string psDirData_OutputImage = configGisBase.config["GisSetOptions:GisDataDirs:OutputDir"] + "";

        public static void RegisterAll()
        {
            OSGeo.OGR.Ogr.RegisterAll();
            OSGeo.GDAL.Gdal.AllRegister();
            OSGeo.GDAL.Gdal.SetConfigOption("GDAL_FILENAME_IS_UTF8", "YES");   // 为了支持中文路径
            OSGeo.GDAL.Gdal.SetConfigOption("SHAPE_ENCODING", "");             // 为了使属性表字段支持中文CPLSetConfigOption
            OSGeo.GDAL.Gdal.SetConfigOption("GEOGSON_ENCODING", "");           // 为了使属性表字段支持中文CPLSetConfigOption
        }

        public static string GetFile_Division(string strDivision)
        {
            Division pDivision = new Division(strDivision);

            //行政编码
            if (strDivision.Length == 12 && Convert.ToInt32(strDivision.Substring(0, 2)) > 0)
            {
                return GetFile_DivisionCode(strDivision);
            }

            //中文名称
            string pathDivision = psDirData_BaseGis + "/BaseGis/Divisions/" + pDivision.Name + "/";
            if (pDivision._Childs != null)
            {
                pathDivision += "/" + pDivision._Childs[0].Name;
                if (pDivision._Childs[0].Childs != null)
                {
                    pathDivision += "/" + pDivision._Childs[0]._Childs[0].Name;
                }
            }
            pathDivision += "/";
            pathDivision = pathDivision.Replace("//", "/");
            return pathDivision;
        }
        public static string GetFile_DivisionCode(string strDivision)
        {
            //行政编码
            string pathDivision = psDirData_BaseGis + "/BaseGis/Divisions/";
            if (strDivision.Length == 12 && Convert.ToInt32(strDivision.Substring(0, 2)) > 0)
            {
                List<string> lstTemp = new List<string>();
                lstTemp.Add(strDivision.Substring(0, 2));
                lstTemp.Add(strDivision.Substring(2, 2));
                lstTemp.Add(strDivision.Substring(4, 2));
                lstTemp.Add(strDivision.Substring(6, 3));
                lstTemp.Add(strDivision.Substring(9, 3));

                foreach (var item in lstTemp)
                {
                    if (item == "00") break;
                    pathDivision += item + "/";
                }
            }
            pathDivision = pathDivision.Replace("//", "/");
            return pathDivision;
        }

        public static string CreateName(string baseDirect, string perffix, string suffix)
        {
            rand += 1;
            int ind = rand;
            //Console.WriteLine(ind.ToString());

            DateTime dtNow = DateTime.Now;
            string newName = $@"{perffix}_{dtNow:yyyyMMdd}_{dtNow:HHmmss}_{dtNow:ffff}_" + ind.ToString();
            string path = $@"{baseDirect}/{newName}{suffix}";

            while (Directory.Exists(path))
            {
                dtNow.AddMilliseconds(1);
                newName = $@"{perffix}_{dtNow:yyyyMMdd}_{dtNow:HHmmss}_{dtNow:ffff}";
                path = $@"{baseDirect}/{newName}{suffix}";
            }
            if (rand > 1000) rand = 0;
            return newName;
        }

    }
}
