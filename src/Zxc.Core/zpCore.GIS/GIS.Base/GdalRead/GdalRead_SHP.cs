using OSGeo.GDAL;
using OSGeo.OGR;
using System;
using System.Collections.Generic;
using System.Runtime.InteropServices;

namespace zpCore.GIS
{
    public class GdalRead_SHP: GdalRead_GeoJson
    {
        public GdalRead_SHP() : base()
        {
        }
        protected override void InitDriver()
        {
            _DriverName = "ESRI Shapefile";
            _Driver = Ogr.GetDriverByName(_DriverName);
        }
    }
}
