using System;
using System.Collections.Generic;
using System.Text;
using System.IO;
using SixLabors.Fonts;
using SixLabors.ImageSharp;
using SixLabors.ImageSharp.PixelFormats;
using SixLabors.ImageSharp.Processing;
using SixLabors.ImageSharp.Drawing.Processing;


namespace zxcCore.Image
{
    public class ImageObj
    {
        #region 属性及构造

        protected internal string _Name = "zxcCore.Image";
        public string Name
        {
            set { _Name = value; }
            get { return _Name; }
        }
        protected internal string _Suffix = ".png";
        public string Suffix
        {
            set { _Suffix = value; }
            get { return _Suffix; }
        }

        protected internal Image<Rgba32> _imageObj = null;
        public Image<Rgba32> Image
        {
            get { return _imageObj; }
        }


        public ImageObj()
        {
        }
        public ImageObj(int nWidth, int nHeight)
        {
            this.Create(nWidth, nHeight);
        }
        ~ImageObj()
        {
            Dispose();
        }
        public void Dispose()
        {
            if (_imageObj != null)
            {
                _imageObj.Dispose();
                _imageObj = null;
            }
        }

        #endregion

        public bool Create(int nWidth, int nHeight)
        {
            this.Dispose();
            _imageObj = new Image<Rgba32>(nWidth, nHeight, Color.White);
            return true;
        }
        public bool Save(string pathFloder)
        {
            if (_imageObj == null) return false;
            string path = pathFloder + "/" + _Name + _Suffix;
            _imageObj.Save(path);
            return true;
        }

        public bool DrawText(int x, int y, Color pColor, string text, Font font = null, int fontSize = 18, bool left = true, bool bottom = true)
        {
            if (_imageObj == null) return false;
            if (font == null)
            {
                FontCollection fonts = new FontCollection();
                FontFamily fontfamily = fonts.Install("Fonts/OpenSans-Regular.TTF");   //装载字体(ttf)
                font = new Font(fontfamily, fontSize, FontStyle.Regular);              //20号,加粗
            }

            //获取该文件绘制所需的大小,精确绘制
            var size = TextMeasurer.Measure(text, new RendererOptions(font));
            var deltaX = left ? 0 : -size.Width;
            var deltaY = !bottom ? 0 : -size.Height;
            _imageObj.Mutate(xx => xx.DrawText(text, font, pColor, new PointF(x + deltaX, y + deltaY)));
            return true;
        }
        public bool Draw(int x, int y, Color pColor, float thickness = 1, int w = 1, int h = 1)
        {
            if (_imageObj == null) return false;
            _imageObj.Mutate(xx => xx.Draw(pColor, thickness, new RectangleF(x, y, w, h)));
            return true;
        }
        public bool DrawLine(PointF[] points, Color pColor, float thickness = 1)
        {
            if (_imageObj == null) return false;
            _imageObj.Mutate(xx => xx.DrawLines(pColor, thickness, points));
            return true;
        }
        public bool DrawBeziers(PointF[] points, Color pColor, float thickness = 1)
        {
            if (_imageObj == null) return false;
            _imageObj.Mutate(xx => xx.DrawBeziers(pColor, thickness, points));
            return true;
        }

    }
}
