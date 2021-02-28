using System;
using System.Collections.Generic;
using System.Text;
using System.IO;
using SixLabors.Fonts;
using SixLabors.ImageSharp;
using SixLabors.ImageSharp.PixelFormats;
using SixLabors.ImageSharp.Processing;
using SixLabors.ImageSharp.Drawing.Processing;


namespace zpCore.Image
{
    public class ImageColor
    {
        public static Color FromRgb(byte r, byte g, byte b)
        {
            return Color.FromRgb(r, g, b);
        }
        public static Color FromRgba(byte r, byte g, byte b, byte a)
        {
            return Color.FromRgba(r, g, b, a);
        }


        public static Color Parse(string strColor)
        {
            return Color.Parse(strColor);
        }
        public static Color ParseHex(string strHex)
        {
            return Color.ParseHex(strHex);
        }

        //颜色集
        public Color Color { set; get; }

        public ImageColor(byte r, byte g, byte b)
        {
            Color = FromRgb(r, g, b);
        }
        public ImageColor(byte r, byte g, byte b, byte a)
        {
            Color = FromRgba(r, g, b, a);
        }
        public ImageColor(string strHex)
        {
            Color = ParseHex(strHex);
        }
        public ImageColor()
        {
            Color = Color.Transparent;
        }

    }
}
