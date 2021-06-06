using OSGeo.OGR;
using System.Collections.Generic;
using System.Text;

namespace zpCore.GIS.Renderer
{
    public class Renderer_Factory
    {
        public static IRenderer CreateRenderer(emRenderType RenderType, IGdalRead gdalRead)
        {
            IRenderer pRender = null;
            IGdalReadR gdalReadR = (IGdalReadR)gdalRead;
            switch (RenderType)
            {
                case emRenderType.Classify:
                    if (gdalReadR != null)
                        pRender = new RasterRendererClassify(gdalReadR);
                    break;
                default:
                    break;
            }
            return pRender;
        }
    }
}