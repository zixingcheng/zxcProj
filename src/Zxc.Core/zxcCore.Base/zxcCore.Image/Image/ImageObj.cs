using System;
using System.Collections.Generic;
using System.Text;
using System.IO;
using System.DrawingCore;
using System.DrawingCore.Imaging;
using System.DrawingCore.Drawing2D;
using System.DrawingCore.Text;

namespace zxcCore.Image
{
    public enum Alignment
    {
        Near = 0,
        Center = 1,
        Far = 2
    }

    public class ImageObj
    {
        #region 属性及构造

        protected internal string _Name = "zpCore.Image";
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

        protected internal Bitmap _imageObj = null;
        public Bitmap Image
        {
            get { return _imageObj; }
        }
        protected internal Graphics _imgGraphic = null;
        public Graphics Graphic
        {
            get { return _imgGraphic; }
        }

        public int Width { get; set; }
        public int Height { get; set; }

        protected internal PrivateFontCollection _fontCollection;
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
                _imgGraphic.Dispose();
                _imgGraphic = null;
                _imageObj = null;
            }
        }

        #endregion

        public bool Create(int nWidth, int nHeight)
        {
            this.Dispose();
            Width = nWidth;
            Height = nHeight;

            _imageObj = new Bitmap(nWidth, nHeight);
            _imgGraphic = Graphics.FromImage(_imageObj);
            _imgGraphic.CompositingMode = CompositingMode.SourceOver;
            _imgGraphic.CompositingQuality = CompositingQuality.HighQuality;
            _imgGraphic.InterpolationMode = InterpolationMode.HighQualityBicubic;
            _imgGraphic.SmoothingMode = SmoothingMode.AntiAlias;                    //使绘图质量最高，即消除锯齿
            _imgGraphic.TextRenderingHint = TextRenderingHint.AntiAlias;
            return true;
        }
        public bool Save(string pathFloder)
        {
            if (_imageObj == null) return false;

            string path = pathFloder + "/" + _Name + _Suffix;
            _imageObj.Save(path, ImageFormat.Png);
            return true;
        }


        /// <summary>更新图片Rgb（使用byte组(32位, 依次为蓝、绿、红、A))
        /// </summary>
        /// <param name="curBitmap"></param>
        /// <param name="bytRGB">颜色byte组信息</param>
        public bool SetData(byte[] bytRGB)
        {
            if (_imageObj == null) return false;    //不能为空

            byte[] bytTemp = null;
            int nWidth = Width, nHeight = Height;
            int nLength = 0;
            try
            {
                //实例Rgb组大小
                nLength = nHeight * 4 * nWidth;
                if (bytRGB.Length != nLength) return false;

                //提取数据
                bytTemp = new byte[nLength];
                BitmapData objData = _imageObj.LockBits(new Rectangle(0, 0, nWidth, nHeight), ImageLockMode.ReadWrite, PixelFormat.Format32bppPArgb);
                System.IntPtr Scan0 = objData.Scan0;
                System.Runtime.InteropServices.Marshal.Copy(Scan0, bytTemp, 0, nLength);
                System.Runtime.InteropServices.Marshal.Copy(bytRGB, 0, Scan0, nLength);
                _imageObj.UnlockBits(objData);

                //返回
                return true;
            }
            catch
            {
                throw;
            }
            finally
            {
                bytTemp = null;
            }
        }
        /// <summary>更新图片Rgb（使用yte组(32位, 依次为蓝、绿、红、A)
        /// </summary>
        /// <param name="curBitmap"></param>
        /// <param name="nRowIndex">起始行号</param>
        /// <param name="nColIndex">起始列号</param>
        /// <param name="nWidthRGB">设置的数据宽度</param>
        /// <param name="bytRGB">值信息</param>
        public bool SetData(int nRowIndex, int nColIndex, int nWidthRGB, byte[] bytRGB)
        {
            if (_imageObj == null) return false;    //不能为空

            byte[] bytTemp = null;
            int nWidth, nHeight;
            int nHeightRGB = 0;
            int nLength = 0, nLengthRGB = 0;
            try
            {
                //计算传入数据
                nLengthRGB = bytRGB.Length;
                nHeightRGB = nLengthRGB / nWidthRGB / 4;

                //修正长宽(可能超出图片范围)
                nHeight = nHeightRGB + nRowIndex < this.Height ? nHeightRGB : this.Height - nRowIndex;
                nWidth = nWidthRGB + nColIndex < this.Width ? nWidthRGB : this.Width - nColIndex;
                nLength = nHeight * 4 * nWidth;
                bytTemp = this.GetData();

                //装载数据
                int nOffset = 0, nOffset2 = 0;
                for (int i = 0; i < nHeight; i++)
                {
                    nOffset = 4 * i * nWidth;               //整体数据行偏移 
                    nOffset2 = 4 * i * nWidthRGB;           //传入数据行偏移
                    for (int j = 0; j < nWidth; j++)
                    {
                        bytTemp[nOffset + j * 4] = bytRGB[nOffset2 + 4 * j];
                        bytTemp[nOffset + j * 4 + 1] = bytRGB[nOffset2 + 4 * j + 1];
                        bytTemp[nOffset + j * 4 + 2] = bytRGB[nOffset2 + 4 * j + 2];
                        bytTemp[nOffset + j * 4 + 3] = bytRGB[nOffset2 + 4 * j + 3];
                    }
                }

                //提取数据
                BitmapData objData = _imageObj.LockBits(new Rectangle(nColIndex, nRowIndex, nWidth, nHeight), ImageLockMode.ReadWrite, PixelFormat.Format32bppPArgb);
                System.IntPtr Scan0 = objData.Scan0;
                System.Runtime.InteropServices.Marshal.Copy(bytTemp, 0, Scan0, nLength);
                _imageObj.UnlockBits(objData);

                //返回
                return true;
            }
            catch
            {
                throw;
            }
        }
        /// <summary>提取图片Rgb的Byte组(32位, 依次为蓝、绿、红、A)
        /// </summary>
        /// <param name="curBitmap"></param>
        public byte[] GetData()
        {
            if (_imageObj == null) return null;    //不能为空

            byte[] bytRGB = null;
            int nWidth = Width, nHeight = Height;
            int nLength = 0;
            try
            {
                //实例Rgb组大小
                nLength = nHeight * 4 * nWidth;
                bytRGB = new byte[nLength];

                //提取数据
                BitmapData objData = _imageObj.LockBits(new Rectangle(0, 0, nWidth, nHeight), ImageLockMode.ReadWrite, PixelFormat.Format32bppPArgb);
                System.IntPtr Scan0 = objData.Scan0;
                System.Runtime.InteropServices.Marshal.Copy(Scan0, bytRGB, 0, nLength);
                _imageObj.UnlockBits(objData);

                //返回
                return bytRGB;
            }
            catch
            {
                throw;
            }
        }


        public bool Draw(int x, int y, Color pColor, float thickness = 1, int w = 1, int h = 1)
        {
            if (_imgGraphic == null) return false;

            if (w == 1 && h == 1)
                _imageObj.SetPixel(x, y, pColor);
            else
                return this.DrawPolygon(x, y, pColor, thickness, w, h, false);
            return true;
        }

        public bool DrawLines(PointF pointS, PointF pointE, Color pColor, float thickness = 1)
        {
            if (_imgGraphic == null) return false;
            Pen objPen = new Pen(pColor, thickness);
            _imgGraphic.DrawLine(objPen, pointS, pointE);
            return true;
        }
        public bool DrawLines(PointF[] points, Color pColor, float thickness = 1)
        {
            if (_imgGraphic == null) return false;
            Pen objPen = new Pen(pColor, thickness);
            _imgGraphic.DrawLines(objPen, points);
            return true;
        }
        public bool DrawPolygon(int x, int y, Color pColor, float thickness = 1, int w = 1, int h = 1, bool isLine = true)
        {
            if (_imgGraphic == null) return false;

            PointF[] points = new PointF[4];
            points[0] = new PointF(x, y);
            points[1] = new PointF(x + w, y);
            points[2] = new PointF(x + w, y + h);
            points[3] = new PointF(x, y + h);

            if (isLine)
            {
                Pen objPen = new Pen(pColor, thickness);
                _imgGraphic.DrawPolygon(objPen, points);
            }
            else
            {
                Brush objBrush = new SolidBrush(pColor);
                _imgGraphic.FillPolygon(objBrush, points);
            }
            return true;
        }
        public bool DrawBeziers(PointF[] points, Color pColor, float thickness = 1)
        {
            if (_imgGraphic == null) return false;
            Pen objPen = new Pen(pColor, thickness);
            _imgGraphic.DrawBeziers(objPen, points);
            return true;
        }

        public bool DrawText(int x, int y, Color pColor, string text, Font font = null, float fontSize = 18, bool directionLeftToRight = true, bool directionVertical = false, Alignment alignment = Alignment.Near, Alignment lineAlignment = Alignment.Near)
        {
            if (_imageObj == null || _imgGraphic == null) return false;
            if (text + "" == "") return false;

            Font objFont = font != null ? font : this.defaultFont(fontSize);
            Brush objBrush = new SolidBrush(pColor);
            StringFormat objFormat = new StringFormat();
            if (alignment == Alignment.Center)
                objFormat.Alignment = StringAlignment.Center;
            else
            {
                if (alignment == Alignment.Near)
                    objFormat.Alignment = StringAlignment.Near;
                else
                    objFormat.Alignment = StringAlignment.Far;
            }

            //计算精确绘制位置 
            var size = _imgGraphic.MeasureString(text, objFont);
            PointF point = new PointF(0, 0);
            if (directionLeftToRight)
            {
                if (!directionVertical)
                {
                    if (alignment == Alignment.Near)
                    {
                        point.X = 0;
                    }
                    else if (alignment == Alignment.Center)
                    {
                        point.X = 0;
                    }
                    else if (alignment == Alignment.Far)
                    {
                        point.X = size.Width;
                    }

                    if (lineAlignment == Alignment.Near)
                    {
                        point.Y = 0;
                    }
                    else if (lineAlignment == Alignment.Center)
                    {
                        point.Y = -size.Height / 2;
                    }
                    else if (lineAlignment == Alignment.Far)
                    {
                        point.Y = size.Height;
                    }
                }
                else
                {
                    if (alignment == Alignment.Near)
                    {
                        point.Y = 0;
                    }
                    else if (alignment == Alignment.Center)
                    {
                        point.Y = -size.Height / 2;
                    }
                    else if (alignment == Alignment.Far)
                    {
                        point.Y = -size.Height;
                    }

                    if (lineAlignment == Alignment.Near)
                    {
                        point.X = 0;
                    }
                    else if (lineAlignment == Alignment.Center)
                    {
                        point.X = size.Width / 2;
                    }
                    else if (lineAlignment == Alignment.Far)
                    {
                        point.X = size.Width;
                    }
                }
            }
            else
            {
                if (!directionVertical)
                {
                    if (alignment == Alignment.Near)
                    {
                        point.X = size.Width;
                    }
                    else if (alignment == Alignment.Center)
                    {
                        point.X = -size.Width / 2;
                    }
                    else if (alignment == Alignment.Far)
                    {
                        point.X = 0;
                    }

                    if (lineAlignment == Alignment.Near)
                    {
                        point.Y = 0;
                    }
                    else if (lineAlignment == Alignment.Center)
                    {
                        point.Y = -size.Height / 2;
                    }
                    else if (lineAlignment == Alignment.Far)
                    {
                        point.Y = size.Height;
                    }
                }
                else
                {
                    if (alignment == Alignment.Near)
                    {
                        point.Y = 0;
                    }
                    else if (alignment == Alignment.Center)
                    {
                        point.Y = -size.Height / 2;
                    }
                    else if (alignment == Alignment.Far)
                    {
                        point.Y = size.Height;
                    }

                    if (lineAlignment == Alignment.Near)
                    {
                        point.X = size.Width;
                    }
                    else if (lineAlignment == Alignment.Center)
                    {
                        point.X = -size.Width / 2;
                    }
                    else if (lineAlignment == Alignment.Far)
                    {
                        point.X = 0;
                    }
                }
            }

            _imgGraphic.DrawString(text, objFont, objBrush, x + point.X, y + point.Y, objFormat);
            return true;
        }
        public bool DrawImage(int x, int y, ImageObj img, float opacity = 1)
        {
            if (_imgGraphic == null) return false;
            _imgGraphic.DrawImage(img._imageObj, new Point(x, y));
            return true;
        }

        public Font defaultFont(float fontSize, string fontName = "Regular", FontStyle fontStyle = FontStyle.Regular)
        {
            Font objFont = null;
            fontName = "微软雅黑";
            if (fontName == "")
            {
                //if (_fontCollection == null)
                //{
                //    //Bug::会导致卡死，问题原因不明。
                //    _fontCollection = new PrivateFontCollection();
                //    _fontCollection.AddFontFile("Fonts/OpenSans-Regular.TTF");          //装载字体(ttf)
                //}
                //objFont = new Font(_fontCollection.Families[0], fontSize, fontStyle);
            }
            else
                objFont = new Font(fontName, fontSize, fontStyle);
            return objFont;
        }
    }
}
