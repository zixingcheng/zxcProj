
namespace zpCore.GIS
{
    public interface IMetadataR : IMetadata
    {
        /// <summary>行数
        /// </summary>
        int Rows { get; set; }
        /// <summary>列数
        /// </summary>
        int Cols { get; set; }
        /// <summary>列数
        /// </summary>
        int Bands { get; set; }

        /// <summary>单元格大小
        /// </summary>
        double CellSize { get; set; }

        /// <summary>无数据标识
        /// </summary>
        double NoDataValue { get; set; }

        double[] ToGeoTransform();
    }
}