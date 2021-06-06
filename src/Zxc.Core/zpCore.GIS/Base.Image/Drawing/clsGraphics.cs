//===============================================================================
// Copyright @ 2012 Beijing Global Safety Technology Co.,Ltd. All rights reserved.
// Copyright @ 2012 北京辰安科技股份有限公司.  版权所有.
//===============================================================================
// 文件名称： 
// 功能描述：图形操作类_GDI操作相关 
// 创建标识：张斌   2013-10-25 
// 修改标识：
// 修改描述：
//===============================================================================

using System;
using System.DrawingCore;
using System.Windows.Forms;
using System.Collections.Generic;
using System.Linq;
using System.Text;  
using GModel.myBaseClass.myRenderer.Geometry;
using GModel.myBaseClass.myRenderer.Text;
using GModel.myBaseClass.myRenderer.Drawing;

namespace GModel.mySysterm.myDrawingCore
{
    public class clsGraphics
    {

        #region 参数

        /// <summary>GDI
        /// </summary>
        public Graphics p_objGraph
        {
            get;
            set;
        }

        public Bitmap m_objBitmap;
        /// <summary>图片
        /// </summary>
        public Bitmap p_Bitmap
        {
            get
            {
                return m_objBitmap;
            }
            set
            {
                m_objBitmap = value;

                //更新绘图对象
                if (m_objBitmap == null)
                {
                    return;
                }
                p_objGraph = Graphics.FromImage(m_objBitmap);
            }
        }

        /// <summary>字体样式
        /// </summary>
        public clss_Font_Style p_FontStyle
        {
            get;
            set;
        }

        #endregion

        #region 公有函数

        /// <summary>文字绘制
        /// </summary>
        /// <param name="objText"></param>
        public void DrawString(clssText objText)
        {
            string strText = "";
            float dX, dY;
            try
            {
                //绘制对象
                if (p_objGraph == null)
                {
                    return;
                }

                //绘制 
                strText = objText.p_Text;
                dX = (float)objText.p_Position.p_X;
                dY = (float)objText.p_Position.p_Y;
                p_objGraph.DrawString(strText, objText.p_FontStyle.p_Font, new SolidBrush(objText.p_FontStyle.p_Color),
                                        dX, dY, objText.p_FontStyle.p_Format);

            }
            catch
            {
                throw;
            }
        }

        /// <summary>绘制文字
        /// </summary>
        /// <param name="lstTexts"></param>
        public void DrawString(List<clssText> lstTexts)
        {
            try
            {
                //循环绘制
                foreach (clssText objText in lstTexts)
                {
                    DrawString(objText);
                }
            }
            catch
            {
                throw;
            }
        }

        /// <summary>生成绘制文字信息，但不绘制(字符串组位置循环间隔制定XY值，支持自使用字符串字体对应高宽)
        /// </summary>
        /// <param name="lstStrings">字符串组</param>
        /// <param name="objPoint">起始位置</param>
        /// <param name="dDeltaX">X间隔值</param>
        /// <param name="dDeltaY">Y间隔值</param>
        /// <param name="bAuto_Position">是否在XY基础上自动增加显示文字所需的最大高宽度值，以实现自适应</param>
        /// <returns></returns>
        public List<clssText> GetData_Texts(List<string> lstStrings, clss_Point objPoint, double dDeltaX, double dDeltaY, bool bAuto_Position)
        {
            List<clssText> lstTexts = new List<clssText>();
            clss_Font_Style objFontStyle = this.p_FontStyle;
            double dLeft = 0, dTop = 0;
            int nWidth = 0, nHeight = 0;
            try
            {
                //计算长度和高度 
                clsFont.Instance().Compute_CtrlMaxWidth(lstStrings.ToArray(), objFontStyle.p_Font, this.p_objGraph, ref nWidth, ref nHeight);

                //依次生成
                for (int i = 0; i < lstStrings.Count; i++)
                {
                    clssText objText = new clssText();
                    objText.p_Text = lstStrings[i];

                    //信息设置
                    objText.p_FontStyle = new clss_Font_Style();
                    objText.p_FontStyle.p_Font = objFontStyle.p_Font;
                    objText.p_FontStyle.p_Color = objFontStyle.p_Color;
                    objText.p_FontStyle.p_Format = objFontStyle.p_Format;

                    //位置信息
                    if (bAuto_Position)
                    {
                        //自动调整合适字体起始位置，依据字体样式
                        dTop = objPoint.p_Y + (nHeight + dDeltaY) * (i);
                        dLeft = objPoint.p_X + (nWidth + dDeltaX) * (i);
                    }
                    else
                    {
                        dTop = objPoint.p_Y + (dDeltaY) * (i);
                        dLeft = objPoint.p_X + (dDeltaX) * (i);
                    }
                    objText.p_Position = new clss_Point(objPoint.p_X, dTop, 0);
                    lstTexts.Add(objText);
                }

                //返回
                return lstTexts;
            }
            catch
            {
                throw;
            }
        }

        #endregion

    }
}
