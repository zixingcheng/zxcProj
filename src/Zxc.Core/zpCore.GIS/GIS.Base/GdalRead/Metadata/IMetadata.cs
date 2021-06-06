
namespace zpCore.GIS
{
    public interface IMetadata
    {

        double MaxX { get; set; }
        double MinX { get; set; }
        double MaxY { get; set; }
        double MinY { get; set; }

        /// <summary>是否北半球
        /// </summary>
        bool IsNorthern { get; set; }

        double[] ToEnvelopes();
    }
}