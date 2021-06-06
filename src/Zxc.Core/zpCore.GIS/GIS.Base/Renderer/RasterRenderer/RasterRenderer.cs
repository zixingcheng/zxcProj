using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using System;
using System.Collections.Generic; 
using System.Linq;
using System.DrawingCore;
using zpCore.Image;
using System.IO;

namespace zpCore.GIS.Renderer
{

    public abstract class RasterRenderer : Renderer, IRasterRenderer
    {
        #region 属性及构造

        protected internal Color _ColorNodata = Color.Transparent;
        /// <summary>Nodata的颜色
        /// </summary>
        public Color ColorNodata
        {
            get { return _ColorNodata; }
        }

        protected internal ImageObj _Image_legend = null;
        public ImageObj Image_Legend
        {
            get { return _Image_legend; }
        }

        protected internal ImageColor _ImageColorNodata = null;
        protected internal IGdalReadR _GdalReadR = null;
        public RasterRenderer(IGdalReadR gdalReadR) : base(null)
        {
            _IsRaster = true;
            _GdalReadR = gdalReadR;
            _ImageColorNodata = new ImageColor(_ColorNodata.R, _ColorNodata.G, _ColorNodata.B, _ColorNodata.A);
        }
        ~RasterRenderer()
        {
        }

        #endregion

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
            //提取数据信息
            if (_GdalReadR == null) return false;
            IMetadataR pMetadata = _GdalReadR.GetMetadataR(1);

            //绘图 
            if (img == null)
                if (_Image == null)
                    _Image = new ImageObj(pMetadata.Cols, pMetadata.Rows);
                else
                    _Image = img;
            _Metadata = pMetadata;
            return true;
        }

        public virtual bool Create_Legend(string path, string name)
        {
            //提取legendInfo
            string[] colors = null;
            string[] titlesInfo = null;
            this.InitRenderInfos("titlesInfo", ref titlesInfo, "legendInfo");
            this.InitRenderInfos("colorsInfo", ref colors, "legendInfo");

            //计算图例区间
            ImageColor pBackground = new ImageColor("#192734");
            int fontSize = 18, titleH = 46;
            int nOffset_x = 10, nOffset_y = 10, nStepX = 10, nStepY = 10;
            int nW_legend = 60, nH_legend = 20;
            int nH = colors.Length * (nH_legend + nStepY) - nStepY + nOffset_y * 2 + nStepX + titleH;
            int nW = nW_legend + nOffset_x * 2 + nW_legend + nStepY * 2;
            int nNum = colors.Length - 1;

            string pathLengend = Directory.GetCurrentDirectory() + "/ModelData/Image/GIS/Legend.png";
            _Image_legend = new ImageObj();
            _Image_legend.Create(pathLengend, nW, nH);
            for (int i = 0; i < colors.Length; i++)
            {
                _Image_legend.DrawPolygon(nOffset_x, nOffset_y + titleH + i * (nH_legend + nStepY), _ImageColors[nNum - i].Color, 1, nW_legend, nH_legend, false);
                _Image_legend.DrawText(nOffset_x + nW_legend + nStepX, nOffset_y + titleH + i * (nH_legend + nStepY), _ImageColors[nNum - i].Color, titlesInfo[i], null, 11, true, false, Alignment.Near, Alignment.Near);
            }
            _Image_legend.DrawText(nW / 2, nOffset_y, pBackground.Color, "图例", null, fontSize, true, false, Alignment.Center, Alignment.Near);
            if (name + "" != "")
                _Image_legend.Name = name;
            return _Image_legend.Save(path);
        }
        public virtual ImageObj Create_Scale(float length = 10000, string unit = "km")
        {
            string pathScale = Directory.GetCurrentDirectory() + "/ModelData/Image/GIS/Scale.png";
            ImageObj imgScale = new ImageObj(100, 100);

            //计算图例区间
            double W = _Metadata.MaxX - _Metadata.MinX;
            double ratioScale = W * 111000 / _Image.Width;
            int nPixels = (int)(length / ratioScale);

            var font = imgScale.defaultFont(11, "");
            var sizeText = imgScale.Graphic.MeasureString(unit, font);
            int nOffset_x = 10, nOffset_y = 8;
            int nW = nPixels + nOffset_x * 3 + (int)sizeText.Width;
            int nH = nOffset_y * 3 + (int)sizeText.Height;
            imgScale.Create(pathScale, nPixels, nOffset_y);

            //绘制
            ImageColor pColor = new ImageColor("#192734");
            ImageObj img = new ImageObj(nW, nH);
            img.DrawImage(nOffset_x, nOffset_y + (int)sizeText.Height, imgScale, 1);

            int hUnit = nOffset_y + (int)(sizeText.Height - imgScale.Height / 2 - 1);
            img.DrawText(nOffset_x * 2 + nPixels, hUnit, pColor.Color, unit, font, 0, true, false, Alignment.Near, Alignment.Near);

            int hDis = (int)(sizeText.Height / 2 - 1);
            img.DrawText(nOffset_x, hDis, pColor.Color, "0", font, 0, true, false, Alignment.Center, Alignment.Near);
            img.DrawText(nOffset_x + nPixels / 2 / 2, hDis, pColor.Color, (length / 1000 / 2 / 2).ToString(), font, 0, true, false, Alignment.Center, Alignment.Near);
            img.DrawText(nOffset_x + nPixels / 2, hDis, pColor.Color, (length / 1000 / 2).ToString(), font, 0, true, false, Alignment.Center, Alignment.Near);
            img.DrawText(nOffset_x + nPixels, hDis, pColor.Color, (length / 1000).ToString(), font, 0, true, false, Alignment.Center, Alignment.Near);
            return img;
        }
    }
}