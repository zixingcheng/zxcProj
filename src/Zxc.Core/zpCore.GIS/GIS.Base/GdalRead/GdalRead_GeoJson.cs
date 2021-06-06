using OSGeo.OGR;
using System;
using System.Collections.Generic;
using System.Runtime.InteropServices;
using System.Text;

namespace zpCore.GIS
{
    public class GdalRead_GeoJson : IGdalRead
    {
        #region 属性及构造

        protected internal bool _IsRaster = false;
        public bool IsRaster
        {
            get { return _IsRaster; }
        }

        protected internal OSGeo.OGR.Driver _Driver;
        public OSGeo.OGR.Driver Driver
        {
            get { return _Driver; }
        }

        protected internal DataSource _DataSource;
        public DataSource DataSource
        {
            get { return _DataSource; }
        }

        protected internal Layer _Layer;
        public Layer Layer
        {
            get { return _Layer; }
        }

        protected internal Dictionary<string, FieldType> _Feilds;
        public Dictionary<string, FieldType> Feilds
        {
            get { return _Feilds; }
        }

        protected internal string _Coordiantes;
        public string Coordiantes
        {
            set { _Coordiantes = value; }
            get { return _Coordiantes; }
        }

        protected internal long _FeatureCount = 0;
        public long FeatureCount
        {
            set { _FeatureCount = value; }
            get { return _FeatureCount; }
        }

        /// <summary>数据源驱动类型
        /// </summary>
        protected internal string _DriverName = "";
        /// <summary>文件编码类型
        /// </summary>
        protected internal Encoding _FileEncoding = Encoding.UTF8;
        /// <summary>文件属性字段编码类型
        /// </summary>
        protected internal Encoding _FileAttrEncoding = Encoding.UTF8;

        public GdalRead_GeoJson()
        {
            _Driver = null;
            _DataSource = null;
            _Layer = null;
            _Feilds = new Dictionary<string, FieldType>();
            _Coordiantes = null;
            this.InitinalGdal();
        }
        ~GdalRead_GeoJson()
        {
            if (_Driver != null) _Driver.Dispose();
            if (_DataSource != null) _DataSource.Dispose();
            if (_Layer != null) _Layer.Dispose();
        }

        #endregion


        /// <summary>初始化Gdal
        /// </summary>
        public virtual void InitinalGdal()
        {
            OSGeo.GDAL.Gdal.SetConfigOption("GDAL_FILENAME_IS_UTF8", "YES");   // 为了支持中文路径
            OSGeo.GDAL.Gdal.SetConfigOption("SHAPE_ENCODING", "");             // 为了使属性表字段支持中文CPLSetConfigOption
            OSGeo.GDAL.Gdal.SetConfigOption("GEOGSON_ENCODING", "");           // 为了使属性表字段支持中文CPLSetConfigOption
            OSGeo.GDAL.Gdal.AllRegister();
            Ogr.RegisterAll();

            this.InitDriver();
            if (_Driver == null)
            {
            }
        }
        protected virtual void InitDriver()
        {
            _DriverName = "GeoJSON";
            try
            {
                _Driver = Ogr.GetDriverByName(_DriverName);
            }
            catch (Exception ex)
            {
                Console.WriteLine("!!002, " + ex.ToString());
                throw;
            }
            if (_Driver == null)
                Console.WriteLine("#!001, " + _DriverName);
        }

        /// <summary>初始数据源
        /// </summary>
        /// <param name="strFilename">文件名</param>
        /// <param name="oFileEncoding">文件编码类型</param>
        /// <param name="nLayerindex">层序号</param>
        /// <param name="bUpdata">是否可以修改</param>
        /// <returns></returns>
        public virtual bool InitDataSource(string strFilename, Encoding oFileEncoding, int nLayerindex = 0, bool bUpdata = false)
        {
            if (_Driver == null) return false;
            if (null == strFilename || strFilename.Length <= 3) return false;

            //清除图层及数据源
            if (_Layer != null)
            {
                _Layer.Dispose(); _Layer = null;
            }
            if (_DataSource != null)
            {
                _DataSource.Dispose(); _DataSource = null;
            }
            _Feilds = new Dictionary<string, FieldType>();
            _FeatureCount = 0;
            _Coordiantes = "";
            _FileEncoding = oFileEncoding;

            //载入数据源
            _DataSource = _Driver.Open(strFilename, Convert.ToInt32(bUpdata));
            if (null == _DataSource) return false;

            //载入图层
            if (nLayerindex >= 0)
                return this.InitLayer(nLayerindex);
            return true;
        }
        /// <summary>初始图层信息(注意部分只有一层)
        /// </summary>
        /// <param name="nLayerindex">层序号</param>
        /// <returns></returns>
        public virtual bool InitLayer(int nLayerindex = 0)
        {
            if (null == _DataSource) return false;
            _Feilds = new Dictionary<string, FieldType>();
            _FeatureCount = 0;
            _Coordiantes = "";

            //string filename = ds.name;
            //int iPosition = filename.LastIndexOf(@"\");
            //string sTempName = filename.Substring(iPosition + 1, filename.Length - iPosition - 4 - 1);
            //oLayer = ds.GetLayerByName(sTempName);
            _Layer = _DataSource.GetLayerByIndex(nLayerindex);
            if (_Layer == null) return false;

            _FeatureCount = _Layer.GetFeatureCount(0);
            this.GetFeilds();
            return true;
        }

        /// <summary>获取所有的属性字段
        /// </summary>
        /// <returns></returns>
        public virtual bool GetFeilds()
        {
            if (null == _Layer) return false;
            _Feilds.Clear();

            wkbGeometryType oTempGeometryType = _Layer.GetGeomType();

            FeatureDefn oDefn = _Layer.GetLayerDefn();
            int iFieldCount = oDefn.GetFieldCount();
            for (int iAttr = 0; iAttr < iFieldCount; iAttr++)
            {
                FieldDefn oField = oDefn.GetFieldDefn(iAttr);
                if (null != oField)
                {
                    _Feilds.Add(oField.GetNameRef(), oField.GetFieldType());
                }
            }
            return true;
        }

        /// <summary>获取某条数据的字段内容
        /// </summary>
        /// <param name="nIndex"></param>
        /// <param name="lstFeildString"></param>
        /// <param name="fileAttrEncoding">文件属性字段编码类型</param>
        /// <returns></returns>
        public virtual bool GetFeildContent(int nIndex, out Dictionary<string, string> dictFieldInfo)
        {
            return GetFeildContent(nIndex, out dictFieldInfo, _FileEncoding);
        }
        /// <summary>获取某条数据的字段内容
        /// </summary>
        /// <param name="nIndex"></param>
        /// <param name="lstFeildString"></param>
        /// <param name="fileAttrEncoding">文件属性字段编码类型</param>
        /// <returns></returns>
        public virtual bool GetFeildContent(int nIndex, out Dictionary<string, string> dictFieldInfo, Encoding fileAttrEncoding)
        {
            _FileAttrEncoding = fileAttrEncoding;
            dictFieldInfo = new Dictionary<string, string>();
            Feature oFeature = null;
            if ((oFeature = _Layer.GetFeature(nIndex)) != null)
            {
                FeatureDefn oDefn = _Layer.GetLayerDefn();
                int iFieldCount = oDefn.GetFieldCount();

                // 查找字段属性
                for (int iAttr = 0; iAttr < iFieldCount; iAttr++)
                {
                    FieldDefn oField = oDefn.GetFieldDefn(iAttr);
                    string strFeildName = oField.GetNameRef();
                    string strValue = "";

                    #region 获取属性字段

                    FieldType Ftype = oFeature.GetFieldType(strFeildName);
                    switch (Ftype)
                    {
                        case FieldType.OFTString:
                            strValue = GetFieldAsStringNu(oFeature, strFeildName, _FileAttrEncoding);
                            break;
                        case FieldType.OFTReal:
                            double dFValue = oFeature.GetFieldAsDouble(strFeildName);
                            strValue = dFValue.ToString();
                            break;
                        case FieldType.OFTInteger:
                            int iFValue = oFeature.GetFieldAsInteger(strFeildName);
                            strValue = iFValue.ToString();
                            break;
                        default:
                            break;
                    }
                    dictFieldInfo.Add(strFeildName, strValue);
                    #endregion
                }
            }
            return true;
        }

        public virtual Geometry GetGeometry(int nIndex)
        {
            if (null == _Layer) return null;
            try
            {
                Feature oFeature = null;
                oFeature = _Layer.GetFeature(nIndex);
                if (oFeature == null) return null;

                Geometry oGeometry = oFeature.GetGeometryRef();
                if (oGeometry == null)
                {
                    oFeature.Dispose();
                    return null;
                }
                return oGeometry;

                //wkbGeometryType oGeometryType = oGeometry.GetGeometryType();
                //oGeometry.ExportToWkt(out _Coordiantes);

                //string[] options = new string[1];
                //_Coordiantes = oGeometry.ExportToJson(null);

                //double[] options2 = new double[];
                //oGeometry.GetPoint(0,)

                //switch (oGeometryType)
                //{
                //    case wkbGeometryType.wkbPoint:
                //        oGeometry.ExportToWkt(out sCoordiantes);
                //        sCoordiantes = sCoordiantes.ToUpper().Replace("POINT (", "").Replace(")", "");
                //        break;
                //    case wkbGeometryType.wkbPoint25D:
                //        oGeometry.ExportToWkt(out sCoordiantes);
                //        sCoordiantes = sCoordiantes.ToUpper().Replace("POINT(", "").Replace(")","");
                //        break;
                //    case wkbGeometryType.wkbLineString:
                //    case wkbGeometryType.wkbLinearRing:
                //        oGeometry.ExportToWkt(out sCoordiantes);
                //        sCoordiantes = sCoordiantes.ToUpper().Replace("LINESTRING (", "").Replace(")", "");
                //        break;
                //    default:
                //        break;
                //}
                //return false;
            }
            catch (NullReferenceException e)
            {
                var s = e.ToString();
                Console.WriteLine($"{s}");
                return null;
            }
        }
        public virtual IMetadata GetMetadata()
        {
            if (this._Layer == null) return null;

            //计算图像大小-按数据边界
            OSGeo.OGR.Envelope envelope = new OSGeo.OGR.Envelope();
            this._Layer.GetExtent(envelope, 1);

            //提取图像参数值
            MetadataR pMeta = new MetadataR();
            pMeta.MinX = Math.Round(envelope.MinX, 8);
            pMeta.MaxX = Math.Round(envelope.MaxX, 8);
            pMeta.MinY = Math.Round(envelope.MinY, 8);
            pMeta.MaxY = Math.Round(envelope.MaxY, 8);
            pMeta.IsNorthern = (pMeta.MinY > 0);
            return pMeta;
        }

        public virtual bool TransDataSource(string dstFilePath, IGdalRead gdalRead)
        {
            if (null == gdalRead) return false;
            if (null == gdalRead.Driver) return false;
            try
            {
                OSGeo.OGR.DataSource ds = gdalRead.Driver.CopyDataSource(this._DataSource, dstFilePath, null);
                if (ds == null) return false;
                ds.FlushCache();
                ds.Dispose();
            }
            catch (NullReferenceException e)
            {
                return false;
            }
            return true;
        }


        //解决属性乱码问题
        [DllImport("ogr_wrap", EntryPoint = "CSharp_OSGeofOGR_Feature_GetFieldAsString__SWIG_1___")]
        public extern static System.IntPtr Feature_GetFieldAsString__SWIG_1(HandleRef jarg1, string jarg2);

        /// <summary>获取属性中文信息(避免乱码)
        /// </summary>
        /// <param name="oFeature"></param>
        /// <param name="strField_Name"></param>
        /// <param name="FileEncoding">文件属性字段编码类型</param>
        /// <returns></returns>
        public virtual string GetFieldAsStringNu(Feature oFeature, string strField_Name, Encoding fileAttrEncoding)
        {
            var result = Feature_GetFieldAsString__SWIG_1(Feature.getCPtr(oFeature), strField_Name);

            String strRes = "";
            if (fileAttrEncoding == Encoding.ASCII)
                strRes = Marshal.PtrToStringAnsi(result);
            else if (_FileEncoding == Encoding.UTF8)
                strRes = Marshal.PtrToStringUTF8(result);
            else if (_FileEncoding == Encoding.Unicode)
                strRes = Marshal.PtrToStringUni(result);
            return strRes;
        }

    }
}
