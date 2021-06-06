
namespace zpCore.GIS
{
    public class MetadataR : Metadata, IMetadataR
    {
        public int Rows { get; set; }
        public int Cols { get; set; }
        public int Bands { get; set; }
        public double CellSize { get; set; }
        public double NoDataValue { get; set; }


        public MetadataR()
        {
        }


        public virtual double[] ToGeoTransform()
        {
            int ratio = IsNorthern ? 1 : -1;
            double[] adfGeoTransform = new double[] { MinX, CellSize, 0, MinY, 0, ratio * CellSize, 0 };
            return adfGeoTransform;
        }

    }
}