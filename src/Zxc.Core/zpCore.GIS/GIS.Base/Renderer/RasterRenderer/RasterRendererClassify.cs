using Newtonsoft.Json;
using System;
using System.Collections.Generic;
using System.Numerics;
using System.Threading.Tasks;
using zpCore.Image;

namespace zpCore.GIS.Renderer
{

    public class RasterRendererClassify : RasterRenderer
    {
        #region 属性及构造

        public RasterRendererClassify(IGdalReadR GdalReadR) : base(GdalReadR)
        {
            this._RenderType = emRenderType.Classify;
        }
        ~RasterRendererClassify()
        {
        }

        #endregion

        protected internal override string InitParam_Test()
        {
            var jsonParams_Test = new
            {
                rendererType = "Classify",
                rendererInfo = new
                {
                    breaksInfo = new[] { 0, 50, 100, 150, 200, 300, 400, int.MaxValue },
                    levelsInfo = new[] { "一级", "二级", "三级", "四级", "五级", "六级" },
                    titlesInfo = new[] { "优", "良", "轻度污染", "中度污染", "重度污染", "严重污染" },
                    colorsInfo = new[] { "#008000", "#FFFF00", "#FFA500", "#FF0000", "#800080", "8E236B" },
                    //colorsInfo = new[] { "绿色", "黄色", "橙色", "红色", "紫色", "褐红色" },   //'深褐红色': "#8E236B"
                }
            };
            return JsonConvert.SerializeObject(jsonParams_Test);
        }

        protected internal override bool InitValues()
        {
            return true;
        }

        public override bool Render_Draw(ImageObj img = null)
        {
            //提取元数据、初始绘图对象
            if (base.Render_Draw(img) == false) return false;
            IMetadataR pMetadata = (IMetadataR)_Metadata;
            if (pMetadata == null) return false;

            //循环绘制
            ImageColor pColor = null;
            float[] datas = null;
            bool bResult = _GdalReadR.GetDatas(1, ref datas);
            for (int i = 0; i < pMetadata.Rows; i++)
            {
                for (int j = 0; j < pMetadata.Cols; j++)
                {
                    pColor = GetColor(datas[i * pMetadata.Cols + j]);
                    //Task.Run(() => _Image.Draw(i, j, pColor.Color));
                    _Image.Draw(j, i, pColor.Color);
                };
                //Task.Run(() => Draws(pMetadata, i, datas));
            }
            return bResult;
        }
        protected bool Draws(IMetadataR pMetadata, int i, float[] datas)
        {
            ImageColor pColor = null;
            for (int j = 0; j < pMetadata.Cols; j++)
            {
                pColor = GetColor(datas[i * pMetadata.Cols + j]);
                _Image.Draw(j, i, pColor.Color);
            };
            return true;
        }

        public override ImageColor GetColor(double value)
        {
            if (_Breaks != null)
            {
                for (int i = 1; i < _Breaks.Length - 1; i++)
                {
                    if (value >= _Breaks[i - 1] && value < _Breaks[i])
                        return _ImageColors[i - 1];
                }
            }
            return _ImageColorNodata;
        }

        public override bool Output(string path, string name)
        {
            if (name + "" != "")
                _Image.Name = name;
            bool bResult = _Image.Save(path) && base.Output(path, _Image.Name + _Image.Suffix);
            return bResult;
        }
    }
}