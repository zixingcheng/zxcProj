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
    public class clsFont : DisposeClass
    {
        #region 标准Dispose模式

        /// <summary>
        /// 析构函数
        /// 必须，以备程序员忘记了显式调用Dispose方法
        /// </summary>
        ~clsFont()
        {
            //必须为false 
            Dispose(false);
        }

        //示例用法
        //使用静态实例的方法调用(可以留此接口，当使用频率较高时有优势，当然也可以使用静态函数),占用资源
        //使用次数少建议直接New出来直接调用，配合析构函数进行释放，不占资源
        static private clsFont ms_objClass;
        public static clsFont Instance()
        {
            if (ms_objClass == null)
            {
                //实例新静态类,并标识需释放
                ms_objClass = new clsFont();
                ms_objClass.Disposed = false;   //标识需释放 
            }
            return ms_objClass;
        }

        /// <summary>
        /// 实现Dispose释放 
        /// </summary>
        /// <param name="disposing"></param>
        protected override void Dispose(bool disposing)
        {
            try
            {
                if (Disposed)
                {
                    return;
                }

                // 清理托管资源 
                if (disposing)
                {
                    //释放实例的静态类对象 
                    ms_objClass = null;
                }

                // 清理非托管资源 

                //让类型知道自己已经被释放
                Disposed = true;
            }
            catch
            {
                throw;
            }
        }

        #endregion

        #region 公有函数

        /// <summary>提取字符串的像素长度
        /// </summary>
        /// <param name="strText">用于计算的字符串</param>
        /// <param name="objFont">指定的字体样式</param>
        /// <param name="objGraphics">GDI绘图对象</param>
        /// <returns></returns>
        public int Compute_StringWidth(string strText, Font objFont, Graphics objGraphics)
        {
            int nWidth = 0;
            try
            {
                nWidth = (int)objGraphics.MeasureString(strText, objFont).Width;
            }
            catch
            {
                throw;
            }
            return nWidth;
        }

        /// <summary>提取字符串的像素高度
        /// </summary>
        /// <param name="strText">用于计算的字符串</param>
        /// <param name="objFont">指定的字体样式</param>
        /// <param name="objGraphics">GDI绘图对象</param>
        /// <returns></returns>
        public int Compute_StringHeight(string strText, Font objFont, Graphics objGraphics)
        {
            int nHeight = 0;
            try
            {
                nHeight = (int)objGraphics.MeasureString(strText, objFont).Height;
            }
            catch
            {
                throw;
            }
            return nHeight;
        }

        /// <summary>提取字符串的像素长度
        /// </summary>
        /// <param name="strText">用于计算的字符串</param>
        /// <param name="objFont">指定的字体样式</param>
        /// <param name="objCtrl">用于创建的控件</param>
        /// <returns></returns>
        public int Compute_StringWidth(string strText, Font objFont, Control objCtrl)
        {
            int nWidth = 0;
            try
            {
                //控件校检
                if (objCtrl == null)
                {
                    objCtrl = new Control();
                }

                //宽度计算
                Graphics objGraphics = objCtrl.CreateGraphics();
                nWidth = Compute_StringWidth(strText, objFont, objGraphics);
            }
            catch
            {
                throw;
            }
            return nWidth;
        }

        /// <summary>提取字符串组最大像素长度，高度 
        /// </summary>
        /// <param name="strTexts">字符串组</param>
        /// <param name="objFont">字体</param>
        /// <param name="objGraphics">GDI绘图对象</param>
        /// <param name="nWidth">返回的最大宽度</param>
        /// <param name="nHeight">返回的最大长度</param>
        /// <returns></returns>
        public bool Compute_CtrlMaxWidth(string[] strTexts, Font objFont, Graphics objGraphics, ref int nWidth, ref int nHeight)
        {
            int nTempW = 0, nTempH = 0;
            try
            {
                //循环提取最大宽度 
                if (strTexts != null)
                {

                    for (int i = 0; i < strTexts.Length; i++)
                    {
                        nTempW = Compute_StringWidth(strTexts[i], objFont, objGraphics);
                        if (nTempW > nWidth)
                        {
                            nWidth = nTempW;
                        }

                        nTempH = Compute_StringHeight(strTexts[i], objFont, objGraphics);
                        if (nTempH > nHeight)
                        {
                            nHeight = nTempH;
                        }
                    }
                }
                return true;
            }
            catch
            {
                throw;
            }
        }

        /// <summary>提取Combox项的最大像素长度 (Combox专用)
        /// </summary>
        /// <param name="strTexts">用于计算的字符串组</param>
        /// <param name="objCtrl">用于创建的控件</param>
        /// <returns></returns>
        public int Compute_CtrlMaxWidth(string[] strTexts, Control objCtrl, int nScrollBoxWidth)
        {
            int nWidth = objCtrl.Width - nScrollBoxWidth;
            int nTemp = 0;
            try
            {
                //循环提取最大宽度 
                if (strTexts != null)
                {

                    for (int i = 0; i < strTexts.Length; i++)
                    {
                        nTemp = mySysterm.myDrawingCore.clsFont.Instance().Compute_StringWidth(strTexts[i], objCtrl.Font, objCtrl);
                        if (nTemp > nWidth)
                        {
                            nWidth = nTemp;
                        }
                    }
                }

                //与原始宽度判断 
                nWidth = nWidth + nScrollBoxWidth;
                nWidth = (nWidth < objCtrl.Width) ? objCtrl.Width : nWidth;
            }
            catch
            {
                throw;
            }
            return nWidth;
        }

        #endregion

    }
}

