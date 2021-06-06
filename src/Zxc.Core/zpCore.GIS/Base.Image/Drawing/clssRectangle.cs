//===============================================================================
// Copyright @ 2013 Beijing Global Safety Technology Co.,Ltd. All rights reserved.
// Copyright @ 2013 北京辰安科技股份有限公司.  版权所有.
//===============================================================================
// 文件名称： 
// 功能描述：图形操作类_矩形范围   
// 创建标识：张斌   2016-08-25
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

namespace GModel.mySysterm.myDrawingCore
{
    
    /// <summary>图形操作类_矩形范围
    /// </summary>
    public class clssRectangle
    {
        #region 参数

        /// <summary>最上(只读)
        /// </summary>
        public int p_Top
        {
            get
            {
                return m_Rect.Top;
            }
        }

        /// <summary>最左(只读)
        /// </summary>
        public int p_Left
        {
            get
            {
                return m_Rect.Left;
            }
        }

        /// <summary>最下(只读)
        /// </summary>
        public int p_Bottom
        {
            get
            {
                return m_Rect.Bottom;
            }
        }

        /// <summary>最右(只读)
        /// </summary>
        public int p_Right
        {
            get
            {
                return m_Rect.Right;
            }
        }


        /// <summary>宽度(只读)
        /// </summary>
        public int p_Width
        {
            get
            {
                return m_Rect.Width;
            }
        }
        /// <summary>高度(只读)
        /// </summary>
        public int p_Height
        {
            get
            {
                return m_Rect.Height;
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

                //实例XYZ值
                List<string> lstTemps = clsTrans.TransTo_List(m_strPointString);
                if (lstTemps.Count > 3)
                {
                    Create(clsTrans.TransTo_Int(lstTemps[0]), clsTrans.TransTo_Int(lstTemps[1]), clsTrans.TransTo_Int(lstTemps[2]), clsTrans.TransTo_Int(lstTemps[3]));
                }
            }
        }

        /// <summary>是否为空矩形
        /// </summary>
        public bool IsEmpty
        {
            get
            {
                return m_Rect.IsEmpty;
            }
        }

        /// <summary>系统矩形结构
        /// </summary>
        protected internal Rectangle m_Rect = Rectangle.Empty;
        protected internal clssRectangle m_Right_Rect = null;
        /// <summary>右接矩形(存在则为左右连接模式,以右矩形表示连接部分)
        /// </summary>
        public clssRectangle p_Right_Rect
        {
            get
            {
                return m_Right_Rect;
            }
        }


        /// <summary>空对象
        /// </summary>
        public static readonly clssRectangle Empty = new clssRectangle();

        /// <summary>构造函数
        /// </summary>
        public clssRectangle()
        {
        }

        /// <summary>构造函数（指定上下左右边界）
        /// </summary>
        /// <param name="nLeft"></param>
        /// <param name="nBottom"></param>
        /// <param name="nRight"></param>
        /// <param name="nTop"></param>
        public clssRectangle(int nLeft, int nBottom, int nRight, int nTop)
        {
            try
            {
                //创建
                this.Create(nLeft, nTop, nRight, nBottom);
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
        public static explicit operator RectangleF(clssRectangle pRectangle)
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
        public static explicit operator Rectangle(clssRectangle pRectangle)
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

        /// <summary>创建矩形范围
        /// </summary>
        /// <param name="rect">矩形对象</param>
        public bool Create(Rectangle rect)
        {
            try
            {
                //记录值
                m_Rect = rect;
                return true;
            }
            catch
            {
                throw;
            }
        }

        /// <summary>创建矩形范围（指定上下左右边界,注意顺序,注意上下坐标值可能上大下小）
        /// </summary>
        /// <param name="nLeft"></param>
        /// <param name="nTop"></param>
        /// <param name="nRight"></param>
        /// <param name="nBottom"></param>
        public bool Create(int nLeft, int nBottom, int nRight, int nTop)
        {
            try
            {
                //记录值
                m_Rect = new Rectangle(nLeft, nTop, nRight - nLeft, Math.Abs(nBottom - nTop));
                return true;
            }
            catch
            {
                throw;
            }
        }

        /// <summary>将指定区域分块
        /// </summary> 
        /// <param name="nSize_Block_R">分块行高</param>
        /// <param name="nSize_Block_C">分块列宽</param>
        /// <param name="nMax">行最大块数</param>
        /// <param name="bBase_Zero">是否从0,0开始计算</param>
        /// <returns></returns>
        public virtual List<Rectangle> Block(int nSize_Block_R, int nSize_Block_C, int nMax, bool bBase_Zero = false)
        {
            List<Rectangle> rectBlocks = new List<System.DrawingCore.Rectangle>();
            Rectangle rectBlock;
            Rectangle rectArea = new System.DrawingCore.Rectangle(0, 0, m_Rect.Width, m_Rect.Height);

            int nRows, nCols, nCols_Block, nLeft, nTop;
            int nBase_X = 0, nBase_Y = 0;
            try
            {
                //计算行列块数
                nCols_Block = nSize_Block_C * nMax;
                nRows = (int)Math.Ceiling(1.0 * m_Rect.Height / nSize_Block_R);
                nCols = (int)Math.Ceiling(1.0 * m_Rect.Width / nCols_Block);

                //基点调整
                if (bBase_Zero == false)
                {
                    nBase_X = this.p_Left;
                    nBase_Y = this.p_Top;
                    rectArea = m_Rect;
                }

                //分区行分段 (均逐分区行扫描)
                for (int i = 0; i < nRows; i++)
                {
                    for (int j = 0; j < nCols; j++)
                    {
                        //示例分区
                        nLeft = nBase_X + j * nCols_Block;
                        nTop = nBase_Y + i * nSize_Block_R;
                        rectBlock = new System.DrawingCore.Rectangle(nLeft, nTop, nCols_Block, nSize_Block_R);

                        //与原区叠加
                        rectBlock.Intersect(rectArea);
                        rectBlocks.Add(rectBlock);
                    }
                }
                return rectBlocks;
            }
            catch
            {
                throw;
            }
        }


        /// <summary>计算重合部分
        /// </summary>
        /// <returns></returns>
        public virtual bool Intersect(Rectangle recArea)
        {
            try
            {
                m_Rect.Intersect(recArea);
                return true;
            }
            catch
            {
                throw;
            }
        }

        /// <summary>合并
        /// </summary>
        /// <returns></returns>
        public virtual bool Merge(Rectangle recArea)
        {
            int nLeft, nBottom, nRight, nTop;
            try
            {
                //为空则直接复制
                if (m_Rect == Rectangle.Empty)
                {
                    m_Rect = recArea;
                }
                else
                {
                    //计算XY最大最小值 
                    nLeft = m_Rect.Left < recArea.Left ? m_Rect.Left : recArea.Left;
                    nRight = m_Rect.Right > recArea.Right ? m_Rect.Right : recArea.Right;

                    nTop = m_Rect.Top < recArea.Top ? m_Rect.Top : recArea.Top;
                    nBottom = m_Rect.Bottom > recArea.Bottom ? m_Rect.Bottom : recArea.Bottom;

                    //重建边框
                    this.Create(nLeft, nBottom, nRight, nTop);
                }
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
                return m_Rect;
            }
            catch
            {
                throw;
            }
        }


        /// <summary>将类转换为字符串(Json格式)
        /// </summary>
        /// <returns></returns>
        public override string ToString()
        {
            try
            {
                m_strPointString = string.Format("{0},{1},{2},{3}", p_Left, p_Bottom, p_Right, p_Top);
                return m_strPointString;
            }
            catch
            {
                throw;
            }
        }

        #endregion

    }
}