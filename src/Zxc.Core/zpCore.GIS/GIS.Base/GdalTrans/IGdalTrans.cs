namespace zpCore.GIS.Trans
{
    public interface IGdalTrans
    {
        /// <summary>结果数据驱动类型
        /// </summary>
        string DstDriverName { get; set; }
        /// <summary>结果数据坐标系
        /// </summary>
        string SpatialWKT { get; set; }
        /// <summary>无数据标识
        /// </summary>
        double NoDataValue { get; set; }
    }
}