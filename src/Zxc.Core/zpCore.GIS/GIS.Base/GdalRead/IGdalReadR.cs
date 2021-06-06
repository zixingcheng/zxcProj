using OSGeo.GDAL;
using OSGeo.OGR;
using System.Collections.Generic;
using System.Text;

namespace zpCore.GIS
{
    public interface IGdalReadR
    {
        /// <summary>数据集对象
        /// </summary>
        Dataset Dataset { get; }
        /// <summary>当前波段
        /// </summary>
        Band Band { get; }

        /// <summary>初始数据集
        /// </summary>
        /// <param name="strFilenameR">文件名</param>
        /// <param name="nBandindex">波段号</param>
        /// <param name="bUpdata">是否可以修改</param>
        /// <returns></returns>
        bool InitDataset(string strFilenameR, int nBandindex = 0, bool bUpdata = false);

        /// <summary>获取源数据信息
        /// </summary>
        /// <param name="nBandIndex"></param>
        /// <returns></returns>
        IMetadataR GetMetadataR(int nBandIndex = 1);
        /// <summary>获取Nodata值
        /// </summary>
        /// <returns></returns>
        double GetNodata(int nBandIndex = 1);

        /// <summary>提取值集
        /// </summary>
        /// <param name="nBandIndex"></param>
        /// <param name="pDatas"></param>
        /// <returns></returns>
        bool GetDatas(int nBandIndex, ref int[] pDatas);
        bool GetDatas(int nBandIndex, ref float[] pDatas);
        bool GetDatas(int nBandIndex, ref double[] pDatas);

    }
}