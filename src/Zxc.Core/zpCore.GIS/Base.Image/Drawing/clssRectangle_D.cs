//===============================================================================
// Copyright @ 2013 Beijing Global Safety Technology Co.,Ltd. All rights reserved.
// Copyright @ 2013 北京辰安科技股份有限公司.  版权所有.
//===============================================================================
// 文件名称： 
// 功能描述：图形操作类_矩形范围   
// 创建标识：张斌   2016-01-08
// 修改标识：
// 修改描述：
//===============================================================================
using System;
using System.DrawingCore;
using System.DrawingCore.Drawing2D;
using System.Collections.Generic;
using System.Linq;
using System.DrawingCore;
using System.Text;

using GModel.mySysterm.myTrans;
using GModel.myBaseClass.myRenderer.Geometry;

namespace GModel.mySysterm.myDrawingCore
{
    
    /// <summary>图形操作类_矩形范围
    /// </summary>
    public class clssRectangle_D
    {
        #region 参数

        protected double m_dTop = 0;
        /// <summary>最上(只读)
        /// </summary>
        public double p_Top
        {
            get
            {
                return m_dTop;
            }
        }

        protected double m_dLeft = 0;
        /// <summary>最左(只读)
        /// </summary>
        public double p_Left
        {
            get
            {
                return m_dLeft;
            }
        }

        protected double m_dBottom = 0;
        /// <summary>最下(只读)
        /// </summary>
        public double p_Bottom
        {
            get
            {
                return m_dBottom;
            }
        }

        protected double m_dRight = 0;
        /// <summary>最右(只读)
        /// </summary>
        public double p_Right
        {
            get
            {
                return m_dRight;
            }
        }


        protected double m_dWidth = 0;
        /// <summary>宽度(只读)
        /// </summary>
        public double p_Width
        {
            get
            {
                return m_dWidth;
            }
        }
        protected double m_dHeight = 0;
        /// <summary>高度(只读)
        /// </summary>
        public double p_Height
        {
            get
            {
                return m_dHeight;
            }
        }

        /// <summary>XYZ值(x,y,z)
        /// </summary>
        private string m_strPointString = "";
        /// <summary>XYZ值(p_Left,p_Bottom,p_Right,p_Top)
        /// </summary>
        public string p_PointString
        {
            get
            {
                m_strPointString = this.ToString();
                return m_strPointString;
            }
            set
            {
                m_strPointString = value;
                if (m_strPointString == "") return;

                //实例XYZ值
                List<string> lstTemps = clsTrans.TransTo_List(m_strPointString);
                if (lstTemps.Count > 3)
                {
                    Create(clsTrans.TransTo_Double(lstTemps[0]), clsTrans.TransTo_Double(lstTemps[1]), clsTrans.TransTo_Double(lstTemps[2]), clsTrans.TransTo_Double(lstTemps[3]));
                }
            }
        }

        /// <summary>是否为空矩形
        /// </summary>
        public bool IsEmpty
        {
            get
            {
                if (m_dLeft == 0 && m_dBottom == 0 && m_dRight == 0 && m_dTop == 0)
                {
                    return true;
                }
                else
                {
                    return false;
                }
            }
        }

        protected internal clssRectangle_D m_Right_Rect = null;
        /// <summary>右接矩形(存在则为左右连接模式,以右矩形表示连接部分)
        /// </summary>
        public clssRectangle_D p_Right_Rect
        {
            get
            {
                return m_Right_Rect;
            }
        }

        /// <summary>空对象
        /// </summary>
        public static readonly clssRectangle_D Empty = new clssRectangle_D();

        /// <summary>构造函数
        /// </summary>
        public clssRectangle_D()
        {
        }

        /// <summary>构造函数（指定上下左右边界）
        /// </summary>
        /// <param name="dLeft"></param>
        /// <param name="dBottom"></param>
        /// <param name="dRight"></param>
        /// <param name="dTop"></param>
        public clssRectangle_D(double dLeft, double dBottom, double dRight, double dTop)
        {
            try
            {
                //创建
                this.Create(dLeft, dBottom, dRight, dTop);
            }
            catch (Exception ex)
            {
                GModel.mySysterm.clsSysterm.Error(ex);
            }
        }

        /// <summary>强制转换为其他类
        /// </summary>
        /// <param name="pRectangle">矩形范围</param>
        /// <returns></returns>
        public static explicit operator RectangleF(clssRectangle_D pRectangle)
        {
            RectangleF pRect;
            try
            {
                //必须存在 
                pRect = new RectangleF((float)pRectangle.p_Left, (float)pRectangle.p_Top, (float)pRectangle.p_Width, (float)pRectangle.p_Height);
                return pRect;
            }
            catch
            {
                throw;
            }
        }

        /// <summary>强制转换为其他类
        /// </summary>
        /// <param name="pRectangle">矩形范围</param>
        /// <returns></returns>
        public static explicit operator Rectangle(clssRectangle_D pRectangle)
        {
            Rectangle pRect;
            try
            {
                //必须存在 
                pRect = new Rectangle((int)pRectangle.p_Left, (int)pRectangle.p_Top, (int)pRectangle.p_Width, (int)pRectangle.p_Height);
                return pRect;
            }
            catch
            {
                throw;
            }
        }

        #endregion

        #region 公有函数

        /// <summary>创建矩形范围（指定上下左右边界,注意顺序,注意上下坐标值可能上大下小）
        /// </summary>
        /// <param name="dLeft"></param>
        /// <param name="dTop"></param>
        /// <param name="dRight"></param>
        /// <param name="dBottom"></param>
        public bool Create(double dLeft, double dBottom, double dRight, double dTop)
        {
            try
            {
                //记录值
                m_dLeft = dLeft;
                m_dTop = dTop;
                m_dRight = dRight;
                m_dBottom = dBottom;
                m_dWidth = m_dRight - m_dLeft;
                m_dHeight = Math.Abs(m_dBottom - m_dTop);

                return true;
            }
            catch
            {
                throw;
            }
        }

        /// <summary>创建矩形范围（由点集合，可以累加创建）
        /// </summary>
        /// <param name="pPoint">点</param>
        public bool Create(clss_Point pPoint)
        {
            clss_Points pPoints = null;
            try
            {
                //生成点集
                pPoints = new clss_Points();
                pPoints.Add(pPoint);

                //调用
                return this.Create(pPoints);
            }
            catch
            {
                throw;
            }
        }
        /// <summary>创建矩形范围（由点集合，可以累加创建）
        /// </summary>
        /// <param name="pPoints">点集</param>
        public bool Create(clss_Points pPoints)
        {
            clss_Point pPoint = null;
            double dMax_X = m_dRight == 0 ? double.MinValue : m_dRight;
            double dMin_X = m_dLeft == 0 ? double.MaxValue : m_dLeft;
            double dMax_Y = m_dBottom == 0 ? double.MinValue : m_dBottom;
            double dMin_Y = m_dTop == 0 ? double.MaxValue : m_dTop;
            double dDelta_W = 0, dDelta_H = 0;
            int nLength = 0;
            try
            {
                //循环所有获取XY最大最小值
                nLength = pPoints.p_Points.Count;
                for (int i = 0; i < nLength; i++)
                {
                    pPoint = pPoints.p_Points[i];

                    //获取X最大最小值
                    if (dMax_X < pPoint.p_X)
                    {
                        dMax_X = pPoint.p_X;
                    }
                    else if (dMin_X > pPoint.p_X)
                    {
                        dMin_X = pPoint.p_X;
                    }

                    //获取X最大最小值
                    if (dMax_Y < pPoint.p_Y)
                    {
                        dMax_Y = pPoint.p_Y;
                    }
                    else if (dMin_Y > pPoint.p_Y)
                    {
                        dMin_Y = pPoint.p_Y;
                    }
                }

                //放大边界，避免画图有不可见部分
                dDelta_W = (dMax_X - dMin_X) * 0.05;
                dDelta_H = (dMax_Y - dMin_Y) * 0.05;

                //修正后的范围
                m_dLeft = dMin_X - dDelta_W;
                m_dTop = dMin_Y - dDelta_H;
                m_dRight = dMax_X + dDelta_W;
                m_dBottom = dMax_Y + dDelta_H;
                m_dWidth = m_dRight - m_dLeft;
                m_dHeight = Math.Abs(m_dBottom - m_dTop);
                return true;
            }
            catch
            {
                throw;
            }
        }


        /// <summary>将类转换为字符串(,分隔)
        /// </summary>
        /// <returns></returns>
        public override string ToString()
        {
            try
            {
                m_strPointString = string.Format("{0},{1},{2},{3}", m_dLeft, m_dBottom, m_dRight, m_dTop);
                return m_strPointString;
            }
            catch
            {
                throw;
            }
        }

        /// <summary>计算重合部分
        /// </summary>
        /// <returns></returns>
        public virtual bool Intersect(RectangleF recArea)
        {
            try
            {

                return true;
            }
            catch
            {
                throw;
            }
        }

        /// <summary>转换为Rectangle
        /// </summary>
        /// <returns></returns>
        public virtual Rectangle ToRectangle()
        {
            try
            {
                return new System.DrawingCore.Rectangle((int)m_dLeft, (int)m_dTop, (int)m_dWidth, (int)m_dHeight);
            }
            catch
            {
                throw;
            }
        }


        /// <summary>将几何对象转换为画布坐标
        /// </summary>
        /// <param name="pPoint">点对象</param>
        /// <param name="pRect_Map">画布边框</param>
        /// <returns></returns>
        public virtual clss_Point Trans_ToMap(clss_Point pPoint, clssRectangle_D pRect_Map)
        {
            clss_Point pPoint_T = new clss_Point();
            double dRatio_X, dRatio_Y;
            try
            {
                //计算X,Y在数据框的坐标比例
                dRatio_X = (pPoint.p_X - p_Left) / p_Width;
                dRatio_Y = (pPoint.p_Y - p_Top) / p_Height;     //上大下小

                //计算画布坐标值
                pPoint_T.p_X = pRect_Map.m_dLeft + dRatio_X * pRect_Map.p_Width;
                pPoint_T.p_Y = pRect_Map.p_Top - dRatio_Y * pRect_Map.p_Height;
                return pPoint_T;
            }
            catch
            {
                throw;
            }
        }

        #endregion

    }
}
