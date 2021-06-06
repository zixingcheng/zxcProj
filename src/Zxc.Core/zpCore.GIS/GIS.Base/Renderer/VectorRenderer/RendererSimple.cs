using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using OSGeo.OGR;
using System;
using System.Collections.Generic;
using System.Drawing;
using System.Linq;
using zpCore.Image;

namespace zpCore.GIS.Renderer
{

    public abstract class RendererSimple : Renderer
    {
        #region 属性及构造

        protected internal ImageColor _color = null;
        public RendererSimple(IGdalRead gdalRead) : base(gdalRead)
        {
            this._RenderType = emRenderType.Simple;
        }
        ~RendererSimple()
        {
        }

        #endregion

        protected internal override string InitParam_Test()
        {
            var jsonParams_Test = new
            {
                rendererType = "Simple",
                rendererInfo = new
                {
                    valuesInfo = new[] { "1" },
                    colorsInfo = new[] { "#008000" },
                    //colorsInfo = new[] { "绿色", "黄色", "橙色", "红色", "紫色", "褐红色" },   //'深褐红色': "#8E236B"
                },
                legendInfo = new
                {
                    titlesInfo = new[] { "0-50" },
                    colorsInfo = new[] { "#008000" }
                }
            };
            return JsonConvert.SerializeObject(jsonParams_Test);
        }


        public override bool Render(ImageObj img = null)
        {
            DateTime dtStart = DateTime.Now;
            bool bResult = base.Render(img);
            bResult = bResult & Render_Draw(img);

            DateTime dtEnd = DateTime.Now;
            Console.WriteLine(string.Format("{0}渲染耗时 {1}s!", this.RenderType, (dtEnd - dtStart).TotalSeconds));
            return true;
        }
        public override bool Render_Draw(ImageObj img = null)
        {
            //提取元数据、初始绘图对象
            if (base.Render_Draw(img) == false) return false;
            if (_Metadata == null) return false;

            //循环绘制
            for (int i = 0; i < _GdalRead.FeatureCount; i++)
            {
                Geometry pGeometry = _GdalRead.GetGeometry(i);

            }
            return true;
        }
        protected bool DrawGeometry(Geometry pGeometry, ImageColor _color)
        {
            //pGeometry.

            //ImageColor pColor = null;
            //for (int j = 0; j < pMetadata.Cols; j++)
            //{
            //    pColor = GetColor(datas[i * pMetadata.Cols + j]);
            //    _Image.Draw(j, i, pColor.Color);
            //};
            return true;
        }

        public override ImageColor GetColor(double value)
        {
            if (_color != null) return _color;
            if (_Colors != null && _Colors.Length > 0)
                _color = new ImageColor(_Colors[0]);
            else
                _color = new ImageColor();
            return _color;
        }
    }
}