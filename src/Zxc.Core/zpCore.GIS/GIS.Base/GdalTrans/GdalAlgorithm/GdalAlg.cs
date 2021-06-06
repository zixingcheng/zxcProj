using OSGeo.GDAL;
using OSGeo.OGR;
using System;
using System.Collections.Generic;
using System.Text;

namespace zpCore.GIS.Trans.Algorithm
{
    public abstract class GdalAlg : IGdalAlg
    {
        #region 属性及构造

        protected internal string _AlgName = "";
        public string AlgName
        {
            get { return _AlgName; }
        }

        protected internal string _AlgNameAlias = "";
        public string AlgNameAlias
        {
            get { return _AlgNameAlias; }
        }

        protected internal string _AlgOptions = "";
        public string AlgOptions
        {
            get
            {
                return _AlgOptions;
            }
        }
        
        protected internal string _AlgOption_paramTag = "";
        protected internal string _AlgOption_paramName = "";
        protected internal string _AlgOptionName = "";

        public GdalAlg()
        {
            _AlgOptions = "";
        }
        ~GdalAlg()
        {
        }
        #endregion

        public virtual string InitOptions()
        {
            return _AlgOptions;
        }

    }
}