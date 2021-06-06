using System.DrawingCore;
using zpCore.Image;

namespace zpCore.GIS.Renderer
{
    public interface IRasterRenderer : IRenderer
    {
        /// <summary>Nodata的颜色
        /// </summary>
        Color ColorNodata { get; }
        /// <summary>渲染图的图例
        /// </summary>
        ImageObj Image_Legend { get; }

        bool Create_Legend(string path, string name);
        ImageObj Create_Scale(float length = 10000, string unit = "km");
    }
}