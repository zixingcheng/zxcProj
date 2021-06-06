using OSGeo.OGR;
using System.Collections.Generic;
using System.Text;

namespace zpCore.GIS
{
    public interface IGdalRead
    {
        /// <summary>是否为栅格数据驱动
        /// </summary>
        bool IsRaster { get; }
        /// <summary>数据驱动对象
        /// </summary>
        Driver Driver { get; }
        /// <summary>数据源对象
        /// </summary>
        DataSource DataSource { get; }
        /// <summary>层对象
        /// </summary>
        Layer Layer { get; }
        /// <summary>字段信息集
        /// </summary>
        Dictionary<string, FieldType> Feilds { get; }
        /// <summary>坐标系名称
        /// </summary>
        string Coordiantes { set; get; }
        /// <summary>要素对象数量
        /// </summary>
        long FeatureCount { set; get; }


        /// <summary>初始化Gdal
        /// </summary>
        void InitinalGdal();
        /// <summary>初始数据源
        /// </summary>
        /// <param name="strFilename">文件名</param>
        /// <param name="oFileEncoding">文件编码类型</param>
        /// <param name="nLayerindex">层序号</param>
        /// <param name="bUpdata">是否可以修改</param>
        /// <returns></returns>
        bool InitDataSource(string strFilename, Encoding oFileEncoding, int nLayerindex = 0, bool bUpdata = false);
        /// <summary>初始图层信息(注意部分只有一层)
        /// </summary>
        /// <param name="nLayerindex">层序号</param>
        /// <returns></returns>
        bool InitLayer(int nLayerindex = 0);

        /// <summary>转换数据源为指定格式
        /// </summary>
        /// <param name="dstFilePath"></param>
        /// <param name="gdalRead"></param>
        /// <returns></returns>
        bool TransDataSource(string dstFilePath, IGdalRead gdalRead);

        /// <summary>获取所有的属性字段
        /// </summary>
        /// <returns></returns>
        bool GetFeilds();
        /// <summary>获取某条数据的字段内容
        /// </summary>
        /// <param name="nIndex"></param>
        /// <param name="lstFeildString"></param>
        /// <returns></returns>
        bool GetFeildContent(int nIndex, out Dictionary<string, string> dictFieldInfo);
        /// <summary>获取某条数据的字段内容
        /// </summary>
        /// <param name="nIndex"></param>
        /// <param name="lstFeildString"></param>
        /// <param name="fileAttrEncoding">文件属性字段编码类型</param>
        /// <returns></returns>
        bool GetFeildContent(int nIndex, out Dictionary<string, string> dictFieldInfo, Encoding fileAttrEncoding);
        /// <summary>获取指定序号的几何对象
        /// </summary>
        /// <returns></returns>
        Geometry GetGeometry(int nIndex);

        /// <summary>获取属性中文信息(避免乱码)
        /// </summary>
        /// <param name="oFeature"></param>
        /// <param name="strField_Name"></param>
        /// <param name="fileAttrEncoding">文件属性字段编码类型</param>
        /// <returns></returns>
        string GetFieldAsStringNu(Feature oFeature, string strField_Name, Encoding fileAttrEncoding);


        /// <summary>提取元数据信息
        /// </summary>
        /// <returns></returns>
        IMetadata GetMetadata();
    }
}