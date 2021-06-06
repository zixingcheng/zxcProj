//===============================================================================
// Copyright @ 2012 Beijing Global Safety Technology Co.,Ltd. All rights reserved.
// Copyright @ 2012 北京辰安科技股份有限公司.  版权所有.
//===============================================================================
// 文件名称： 
// 功能描述：系统操作类_字体操作相关方法实现类 
// 创建标识：张斌   2013-01-08 
// 修改标识：
// 修改描述：
//===============================================================================

using System;
using System.DrawingCore;
using System.Windows.Forms;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using GModel.myDispose;

namespace GModel.mySysterm.myDrawingCore
{
    public class clsColor : DisposeClass
    {
        #region 标准Dispose模式

        /// <summary>
        /// 析构函数
        /// 必须，以备程序员忘记了显式调用Dispose方法
        /// </summary>
        ~clsColor()
        {
            //必须为false 
            Dispose(false);
        }

        #endregion

        #region 颜色转换

        /// <summary>将指定Rgb字串转换为颜色(自动识别颜色格式) 
        /// </summary>
        /// <param name="strColor">多种类型的颜色字符串(例如:RGB"165,42,42",ARGB"255,165,42,42",16进制"#FFEF193E",Jave颜色"0x1D2089")</param>
        /// <returns></returns>
        public static Color Trans_Color(string strColor)
        {
            Color objColor = Color.Transparent;
            try
            {
                //识别
                if (strColor.IndexOf('#') == 0)
                {
                    objColor = Trans_Color_0xColor(strColor);
                }
                else if (strColor.IndexOf("0x") == 0)
                {
                    objColor = Trans_Color_0xColor2(strColor);
                }
                else if (strColor.IndexOf(',') > 0)
                {
                    objColor = Trans_Color_RgbColor(strColor);
                }
                return objColor;
            }
            catch
            {
                throw;
            }
        }

        /// <summary>将指定Rgb字串转换为颜色 
        /// </summary>
        /// <param name="strRgb">Rgb字符串(例如:"165,42,42",ARGB"255,165,42,42")</param>
        /// <returns></returns>
        public static Color Trans_Color_RgbColor(string strRgb)
        {
            Color objColor = Color.Transparent;
            string[] strTemps = null;
            int nA, nR, nG, nB;
            try
            {
                //分解
                strTemps = strRgb.Split(',');
                if (strTemps.Length == 3)
                {
                    //依次组装RGB值
                    nR = Convert.ToInt32(strTemps[0]);
                    nG = Convert.ToInt32(strTemps[1]);
                    nB = Convert.ToInt32(strTemps[2]);
                    objColor = Color.FromArgb(nR, nG, nB);
                }
                else if (strTemps.Length == 4)
                {
                    //依次组装RGB值
                    nA = Convert.ToInt32(strTemps[0]);
                    nR = Convert.ToInt32(strTemps[1]);
                    nG = Convert.ToInt32(strTemps[2]);
                    nB = Convert.ToInt32(strTemps[3]);
                    objColor = Color.FromArgb(nA, nR, nG, nB);
                }
                else
                {
                    return objColor;
                }
                return objColor;
            }
            catch
            {
                throw;
            }
        }

        /// <summary>将指定颜色转换为对应透明颜色 
        /// </summary>
        /// <param name="dAlpha">颜色透明度(0-100之间,0为不透明,255格式的自行/255)</param>
        /// <param name="cColor">原始颜色</param>
        /// <returns></returns>
        public static Color Trans_Color_ARgbColor(double dAlpha, Color cColor)
        {
            Color objColor = Color.Transparent;
            int nA;
            try
            {
                //计算透明度
                dAlpha = 100 - dAlpha;
                if (dAlpha > 100 || dAlpha < 0)
                {
                    dAlpha = 100;
                }
                nA = (int)(dAlpha * 255 / 100);

                //计算透明色 
                if (nA != 0)
                {
                    objColor = Color.FromArgb(nA, cColor);
                }
                else
                {
                    objColor = Color.Transparent;
                }
                return objColor;
            }
            catch
            {
                throw;
            }
        }

        /// <summary>将指定颜色转换为Java用0x十六进制颜色字符串(无A值)
        /// </summary>
        /// <param name="objColor">示例"0x1D2089"</param>
        /// <returns></returns>
        public static string Trans_Color_0xColor2(Color objColor)
        {
            string strTemp = "0x";
            try
            {
                //依次组装RGB值
                strTemp = strTemp + Trans_Color_0xHex(objColor.R);
                strTemp = strTemp + Trans_Color_0xHex(objColor.G);
                strTemp = strTemp + Trans_Color_0xHex(objColor.B);
                return strTemp;
            }
            catch (Exception ex)
            {
                clsSysterm.Error(clsSysterm.NewError("将指定颜色转换为Java用0x十六进制颜色字符串", ex));
                return "";
            }
        }

        /// <summary>将指定Java用0x十六进制颜色字符串转换为颜色(无A值) 
        /// </summary>
        /// <param name="strColor">颜色字符串，示例"0x1D2089"</param>
        /// <returns></returns> 
        public static Color Trans_Color_0xColor2(string strColor)
        {
            Color objColor = Color.Transparent;
            int nR, nG, nB;
            try
            {
                //依次组装RGB值 
                nR = Trans_Color_0xHex(strColor.Substring(2, 2));
                nG = Trans_Color_0xHex(strColor.Substring(4, 2));
                nB = Trans_Color_0xHex(strColor.Substring(6, 2));
                objColor = Color.FromArgb(nR, nG, nB);
                return objColor;
            }
            catch
            {
                throw;
            }
        }

        /// <summary>将指定颜色转换为十六进制颜色(例如"#FFEF193E") 
        /// </summary>
        /// <param name="objColor">/param>
        /// <returns></returns> 
        public static string Trans_Color_0xColor(Color objColor)
        {
            string strTemp = "#";
            try
            {
                //依次组装RGB值
                strTemp = strTemp + Trans_Color_0xHex(objColor.A);
                strTemp = strTemp + Trans_Color_0xHex(objColor.R);
                strTemp = strTemp + Trans_Color_0xHex(objColor.G);
                strTemp = strTemp + Trans_Color_0xHex(objColor.B);
                return strTemp;
            }
            catch
            {
                throw;
            }
        }

        /// <summary>将十六进制颜色转换为RGB颜色 
        /// </summary>
        /// <param name="strRgb">Rgb字符串(例如"#FFEF193E")</param>
        /// <returns></returns> 
        public static Color Trans_Color_0xColor(string strColor)
        {
            Color objColor = Color.Transparent;
            int nA, nR, nG, nB;
            try
            {
                //依次组装RGB值
                nA = Trans_Color_0xHex(strColor.Substring(1, 2));
                nR = Trans_Color_0xHex(strColor.Substring(3, 2));
                nG = Trans_Color_0xHex(strColor.Substring(5, 2));
                nB = Trans_Color_0xHex(strColor.Substring(7, 2));
                objColor = Color.FromArgb(nA, nR, nG, nB);
                return objColor;
            }
            catch
            {
                throw;
            }
        }

        /// <summary>转换颜色值为十六进制值,自动补零（0-255）
        /// </summary>
        /// <returns></returns>
        public static string Trans_Color_0xHex(int nValue)
        {
            string strTemp = "0x";
            try
            {
                //依次组装RGB值
                strTemp = Microsoft.VisualBasic.Conversion.Hex(nValue);
                if (strTemp.Length == 1)
                {
                    strTemp = "0" + strTemp;
                }
                return strTemp;
            }
            catch (Exception ex)
            {
                clsSysterm.Error(clsSysterm.NewError("转换颜色值为十六进制值,自动补零（0-255）", ex));
                return "";
            }
        }

        /// <summary>转换16进制字符为10进制值
        /// </summary>
        /// <returns></returns>
        public static int Trans_Color_0xHex(string strValue)
        {
            int nColor = 0;
            try
            {
                //依次组装RGB值
                nColor = Convert.ToInt32(strValue, 16); //FF为被转值 
                return nColor;
            }
            catch (Exception ex)
            {
                clsSysterm.Error(clsSysterm.NewError("转换颜色值为十六进制值,自动补零（0-255）", ex));
                return -1;
            }
        }

        /// <summary>提取Rgb颜色的最大最小值 
        /// </summary>
        /// <param name="objColor">指定的颜色</param>
        /// <param name="nMax">三色素分量最大值</param>
        /// <param name="nMin">三色素分量最小值</param>
        /// <returns></returns>
        public static bool Trans_Color_GetRgbMax(Color objColor, ref int nMax, ref int nMin)
        {
            //取最大最小分量 
            if (objColor.R > objColor.G)
            {
                nMax = objColor.R;
                nMin = objColor.G;
            }
            else
            {
                nMax = objColor.G;
                nMin = objColor.R;
            }
            if (nMax < objColor.B)
            {
                nMax = objColor.B;
            }
            if (nMin > objColor.B)
            {
                nMin = objColor.B;
            }
            return true;
        }

        #endregion

    }
}
