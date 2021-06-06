using System;
using System.Collections.Generic;
using System.Text;
using System.IO;
using System.DrawingCore;
using System.DrawingCore.Imaging;
using System.DrawingCore.Drawing2D;

namespace zpCore.Image
{
    public class ImageColor
    {
        public static Color FromRgb(byte r, byte g, byte b)
        {
            return Color.FromArgb(r, g, b);
        }
        public static Color FromRgba(byte r, byte g, byte b, byte a)
        {
            return Color.FromArgb(a, r, g, b);
        }


        public static Color Parse(string strColor)
        {
            return Color.FromName(strColor);
        }
        /// <summary>[颜色：16进制转成RGB]
        /// </summary>
        /// <param name="strColor">设置16进制颜色 [返回RGB]</param>
        /// <returns></returns>
        public static Color ParseHex(string strHex)
        {
            try
            {
                if (strHex.Length == 0)
                {
                    //如果为空
                    return Color.FromArgb(0, 0, 0);     //设为黑色
                }
                else
                {
                    //转换颜色
                    return Color.FromArgb(
                        System.Int32.Parse(strHex.Substring(1, 2), System.Globalization.NumberStyles.AllowHexSpecifier),
                         System.Int32.Parse(strHex.Substring(3, 2), System.Globalization.NumberStyles.AllowHexSpecifier), System.Int32.Parse(strHex.Substring(5, 2), System.Globalization.NumberStyles.AllowHexSpecifier));
                }
            }
            catch
            {
                //设为黑色
                return Color.FromArgb(0, 0, 0);
            }
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
