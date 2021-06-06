//===============================================================================
// Copyright @ 2012 Beijing Global Safety Technology Co.,Ltd. All rights reserved.
// Copyright @ 2012 北京辰安科技股份有限公司.  版权所有.
//===============================================================================
// 文件名称： 
// 功能描述：系统操作类_色带相关方法实现类 
// 创建标识：张斌   2013-01-08 
// 修改标识：
// 修改描述：
//===============================================================================
using System;
using System.DrawingCore;
using System.DrawingCore.Drawing2D;
using System.Windows.Forms;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using GModel.myDispose;
using GModel.mySysterm.myData.myAlgorithm;
using GModel.mySysterm.myDrawingCore;

namespace GModel.mySysterm.myDrawingCore
{
    public class clsColorRamp
    {
        #region 参数

        /// <summary>中断颜色集(大于两个)
        /// </summary>
        public Color[] p_Colors
        {
            get;
            set;
        }
        /// <summary>开始颜色
        /// </summary>
        public Color p_FromColor
        {
            get
            {
                if (p_Colors != null && p_Colors.Length > 1)
                {
                    return p_Colors[0];
                }
                else
                {
                    return Color.Transparent;
                }
            }
        }
        /// <summary>结束颜色
        /// </summary>
        public Color p_ToColor
        {
            get
            {
                if (p_Colors != null && p_Colors.Length > 1)
                {
                    return p_Colors[p_Colors.Length - 1];
                }
                else
                {
                    return Color.Transparent;
                }
            }
        }
        /// <summary>是否颜色渐变(默认渐变)
        /// </summary>
        public bool p_Color_Gradient
        {
            get;
            set;
        }
        /// <summary>色带宽度
        /// </summary>
        public int p_RampHeight
        {
            get;
            set;
        }
        /// <summary>色带宽度
        /// </summary>
        public int p_RampWidth
        {
            get;
            set;
        }

        protected Bitmap m_objMitmap_H = null;
        /// <summary>色带图片(横向)
        /// </summary>
        public Bitmap p_Bitmap_H
        {
            get
            {
                return m_objMitmap_H;
            }
        }
        protected Bitmap m_objMitmap_V = null;
        /// <summary>色带图片(竖向)
        /// </summary>
        public Bitmap p_Bitmap_V
        {
            get
            {
                return m_objMitmap_V;
            }
        }

        /// <summary>最大值
        /// </summary>
        public double p_MaxValue
        {
            get;
            set;
        }
        /// <summary>最小值
        /// </summary>
        public double p_MinValue
        {
            get;
            set;
        }
        /// <summary>平均值
        /// </summary>
        public double p_AverageValue
        {
            get;
            set;
        }
        /// <summary>标准差
        /// </summary>
        public double p_StandDevValue
        {
            get;
            set;
        }

        protected Color[] m_Colors = null;
        protected int[] m_nValues = null;
        protected double m_dMax = 1000;
        protected double m_dRatio = 1;

        /// <summary>构造函数
        /// </summary>
        public clsColorRamp()
        {
            try
            {
                p_RampHeight = 30;
                p_RampWidth = 500;
                p_MinValue = 0;
                p_MaxValue = 999;
                p_Colors = new Color[] { Color.Black, Color.White };
                p_Color_Gradient = true;
            }
            catch
            {
                throw;
            }
        }

        #endregion

        #region 接口

        /// <summary>提取指定值对应的色带颜色
        /// </summary>
        /// <param name="dValue">当前值</param>
        /// <returns></returns>
        public virtual Color Get_Color(double dValue)
        {
            Color objColor = Color.Transparent;
            double dIndex = 0;
            try
            {
                //值必须在最大最小值范围内
                //if (dValue < p_MinValue || dValue >= p_MaxValue)
                if (dValue < p_MinValue)
                {
                    return objColor;
                }

                //计算位置 
                dIndex = (int)Check_Value(dValue);
                //if (nValue != 0)
                //{
                //    clsSysterm.Debug_Print(nValue.ToString() + "[]" + dIndex.ToString());
                //}

                //取改位置颜色
                objColor = m_Colors[(int)dIndex];
                return objColor;
            }
            catch
            {
                throw;
            }
        }

        /// <summary>按指定起止色，色带大小创建色带
        /// </summary>
        /// <param name="nValue">当前值</param>
        /// <returns></returns>
        public virtual bool Create_Ramp()
        {
            Color objColor = Color.Transparent;
            try
            {
                //色带初始
                if (p_Colors == null)
                {
                    p_Colors = new Color[] { Color.Black, Color.White };
                }

                //计算分段序号集及变换比例
                m_dRatio = Math.Abs(p_MaxValue - p_MinValue) / m_dMax;
                this.Creat_BreakIndexs();

                //创建返回色带图
                m_objMitmap_H = Create_Ramp((int)m_dMax, p_RampHeight, p_Colors);
                m_Colors = new Color[(int)m_dMax];
                for (int i = 0; i < m_dMax; i++)
                {
                    m_Colors[i] = m_objMitmap_H.GetPixel(i, 0);
                }

                //创建返回缩略图
                if (p_RampWidth > p_RampHeight)
                {
                    //横向
                    m_objMitmap_H = Create_Ramp(p_RampWidth * 10, p_RampHeight, p_Colors);
                    m_objMitmap_H = new Bitmap(m_objMitmap_H, p_RampWidth, p_RampHeight);

                    m_objMitmap_V = clsBitmap.Image_Rotate(m_objMitmap_H, 90);
                }
                else
                {
                    //纵向
                    m_objMitmap_V = Create_Ramp(p_RampHeight * 10, p_RampWidth, p_Colors);
                    m_objMitmap_V = new Bitmap(m_objMitmap_V, p_RampHeight, p_RampWidth);

                    m_objMitmap_H = clsBitmap.Image_Rotate(m_objMitmap_V, 90);
                }
                return true;
            }
            catch
            {
                throw;
            }
        }

        /// <summary>按指定起止色，色带大小创建色带
        /// </summary>
        /// <param name="nMax">X最大值</param>
        /// <param name="nHeight">图片高度</param>
        /// <param name="Colors">渐变颜色集合</param>
        /// <returns></returns>
        public virtual Bitmap Create_Ramp(int nMax, int nHeight, Color[] Colors)
        {
            byte[] bytDatas = null;
            byte[] bytTemps = null;
            Bitmap objMitmap = null;
            Bitmap objMitmap2 = null;
            Graphics objGraphics = null;
            LinearGradientBrush objBrush;
            Rectangle objRect;

            Color objColor = Color.Transparent;
            Color cFromColor, cToColor;
            double nCount = Colors.Length - 1;
            int nStart, nEnd;
            try
            {
                //实例图片大小
                objMitmap = new Bitmap(nMax, nHeight);
                bytDatas = new byte[nHeight * 4 * nMax];

                //循环所有
                for (int i = 1; i <= nCount; i++)
                {
                    //参数提取
                    cFromColor = Colors[i - 1];
                    cToColor = p_Color_Gradient ? Colors[i] : cFromColor;
                    nStart = (int)((i - 1) / nCount * nMax);
                    nEnd = (int)(i / nCount * nMax);

                    //实例图片
                    objMitmap2 = new Bitmap(nEnd - nStart, nHeight);
                    objGraphics = Graphics.FromImage(objMitmap2);

                    //渐变画刷
                    objRect = new Rectangle(0, 0, nEnd - nStart, nHeight);
                    objBrush = new LinearGradientBrush(objRect, cFromColor, cToColor, LinearGradientMode.Horizontal);

                    //绘制图片 
                    objGraphics.FillRectangle(objBrush, objRect);
                    objGraphics.Save();

                    //装载数据 
                    bytTemps = clsBitmap.GetData(objMitmap2);
                    clsBitmap.SetData(ref objMitmap, 0, nStart, nEnd - nStart, bytTemps);
                }

                objGraphics.Dispose();
                return objMitmap;
            }
            catch
            {
                throw;
            }
        }

        /// <summary>提取指定值对应的颜色(未实现)
        /// </summary>
        /// <param name="dValue">当前值</param>
        /// <returns></returns>
        public virtual double Check_Value(double dValue)
        {
            try
            {
                //标准差插值计算
                return 0;
            }
            catch
            {
                throw;
            }
        }

        /// <summary>计算分段颜色对应的细分总颜色数序号分段集
        /// </summary>
        /// <returns></returns>
        protected virtual bool Creat_BreakIndexs()
        {
            double dCount = p_Colors.Length - 1;
            try
            {
                //重新实例颜色序号分段集组
                m_nValues = new int[p_Colors.Length];

                //计算(自然分段)
                m_nValues[0] = 0;
                for (int i = 1; i <= dCount; i++)
                {
                    m_nValues[i] = (int)(i / dCount * m_dMax);
                }
                return true;
            }
            catch
            {
                throw;
            }
        }

        #endregion

    }
}