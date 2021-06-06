
namespace zpCore.GIS
{
    public class Metadata : IMetadata
    {
        public double MaxX { get; set; }
        public double MinX { get; set; }
        public double MaxY { get; set; }
        public double MinY { get; set; }
        public bool IsNorthern { get; set; }

        public Metadata()
        {
        }
        public virtual double[] ToEnvelopes()
        {
            double[] dEnvelopes = new double[] { MinX, MaxX, MinY, MaxY };
            return dEnvelopes;
        }
    }
}