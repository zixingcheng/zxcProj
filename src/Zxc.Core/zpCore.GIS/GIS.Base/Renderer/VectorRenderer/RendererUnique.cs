using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using System;
using System.Collections.Generic;
using System.Drawing;
using System.Linq;
using zpCore.Image;

namespace zpCore.GIS.Renderer
{

    public abstract class RendererUnique : Renderer
    {
        #region 属性及构造

        public RendererUnique(IGdalRead gdalRead) : base(gdalRead)
        {
            this._RenderType = emRenderType.Unique;
        }
        ~RendererUnique()
        {
        }

        #endregion

        protected internal override string InitParam_Test()
        {
            var jsonParams_Test = new
            {
                rendererType = "Unique",
                rendererInfo = new
                {
                    valuesInfo = new[] { "1" },
                    colorsInfo = new[] { "#008000", "#FFFF00", "#FFA500", "#FF0000", "#800080", "8E236B" },
                    //colorsInfo = new[] { "绿色", "黄色", "橙色", "红色", "紫色", "褐红色" },   //'深褐红色': "#8E236B"
                },
                legendInfo = new
                {
                    titlesInfo = new[] { "0-50", "50-100", "100-150", "150-200", "200-300", "300-500" },
                    colorsInfo = new[] { "#008000", "#FFFF00", "#FFA500", "#FF0000", "#800080", "#8E236B" }
                }
            };
            return JsonConvert.SerializeObject(jsonParams_Test);
        }
        

        public override bool Render(ImageObj img = null)
        {
            //初始颜色对象集
            for (int i = 0; i < _Colors.Length; i++)
            {
                _ImageColors.Add(new ImageColor(_Colors[i]));
            }

            _Result = new JObject();
            _Result["params"] = _Params;
            _Result["renderer"] = new JObject();
            return true;
        }
        public override ImageColor GetColor(double value)
        {
            return null;
        }
    }
}