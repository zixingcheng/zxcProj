using OSGeo.OGR;
using System;
using System.Collections.Generic;
using System.Text;

namespace zpCore.GIS
{
    public class GdalRead_Factory
    {
        public static IGdalRead CreateGdalRead(string filePath)
        {
            OSGeo.OGR.DataSource poDataSource = OSGeo.OGR.Ogr.Open(filePath, 0);
            string strDriverName = poDataSource.GetDriver().GetName();

            IGdalRead pGdalRead = null;
            switch (strDriverName)
            {
                case "GeoJSON":
                    pGdalRead = new GdalRead_GeoJson();
                    break;
                case "ESRI Shapefile":
                    pGdalRead = new GdalRead_SHP();
                    break;
                default:
                    break;
            }

            poDataSource.Dispose();
            return pGdalRead;
        }
    }
}