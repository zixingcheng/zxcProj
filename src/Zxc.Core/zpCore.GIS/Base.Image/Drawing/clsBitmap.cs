//===============================================================================
// Copyright @ 2012 Beijing Global Safety Technology Co.,Ltd. All rights reserved.
// Copyright @ 2012 北京辰安科技股份有限公司.  版权所有.
//===============================================================================
// 文件名称： 
// 功能描述：图形操作类_图片操作相关 
// 创建标识：张斌   2013-10-25 
// 修改标识：
// 修改描述：
//===============================================================================
using System;
using System.DrawingCore;
using System.DrawingCore.Imaging;
using System.DrawingCore.Drawing2D; 
using System.Windows.Forms;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace GModel.mySysterm.myDrawingCore
{
    public class clsBitmap
    {

        #region 参数

        /// <summary>GDI
        /// </summary>
        public Graphics p_Graphics
        {
            get;
            set;
        }

        internal Bitmap m_objBitmap = null;
        /// <summary>图片
        /// </summary>
        public Bitmap p_Bitmap
        {
            get { return m_objBitmap; }
            set { m_objBitmap = value; }
        }

        /// <summary>色带
        /// </summary>
        public clsColorRamp p_Ramp
        {
            get;
            set;
        }


        internal string m_strPath = "";
        /// <summary>图片地址(只读)
        /// </summary>
        public string p_Path
        {
            get { return m_strPath; }
        }

        internal double m_dCellSize = 1;
        /// <summary>格子大小(设置会调整范围)
        /// </summary>
        public double p_CellSize
        {
            get { return m_dCellSize; }
            set
            {
                //设置范围信息
                m_dCellSize = value;
                p_Base = m_objBase;
            }
        }

        internal clssRectangle_D m_objBounds = new clssRectangle_D();
        /// <summary>图片范围对应基坐标(设置会调整基坐标,及格子大小)
        /// </summary>
        public clssRectangle_D p_Bounds
        {
            get { return m_objBounds; }
            set
            {
                //设置坐标信息
                m_objBounds = value;
                m_objBase = new clss_Point(m_objBounds.p_Left, m_objBounds.p_Bottom, 0);
                if (p_Bitmap != null)
                {
                    m_dCellSize = m_objBounds.p_Width / (p_Bitmap.Width);       //注意必须为格子数
                    //m_dCellSize = m_objBounds.p_Height / (p_Bitmap.Height);     //注意必须为格子数
                }
            }
        }

        internal clss_Point m_objBase = new clss_Point();
        /// <summary>图片绘制基坐标--左下角(设置会调整范围，且必须存在图片对象)
        /// </summary>
        public clss_Point p_Base
        {
            get { return m_objBase; }
            set
            {
                //设置范围信息
                if (p_Bitmap == null)
                {
                    m_objBounds = new clssRectangle_D();
                }
                else
                {
                    m_objBounds = new clssRectangle_D(m_objBase.p_X, m_objBase.p_Y, m_objBase.p_X + m_dCellSize * p_Bitmap.Width, m_objBase.p_Y - m_dCellSize * p_Bitmap.Height);
                }

            }
        }

        ///// <summary>构造函数
        ///// </summary>
        //public clsBitmap()
        //{
        //}

        /// <summary>构造函数
        /// </summary>
        /// <param name="nWidth">图像宽度</param>
        /// <param name="nHeight">图像高度</param>
        public clsBitmap(int nWidth, int nHeight)
        {
            p_Bitmap = new Bitmap(nWidth, nHeight);

            //范围信息
            this.Init();
        }

        #endregion

        #region 公有函数

        /// <summary>初始画布
        /// </summary>
        /// <param name="pPath">路径</param>
        /// <returns></returns>
        public virtual bool Init(string pPath)
        {
            try
            {
                //实例图片大小
                p_Bitmap = new Bitmap(pPath);

                //范围信息
                return this.Init();
            }
            catch
            {
                throw;
            }
        }

        /// <summary>初始画布
        /// </summary>
        public virtual bool Init()
        {
            try
            {
                //创建色带(默认) 
                if (p_Ramp == null)
                {
                    p_Ramp = new clsColorRamp();
                    p_Ramp.p_MinValue = 0;
                    p_Ramp.p_MaxValue = 1000;
                    p_Ramp.p_StandDevValue = 500;
                    p_Ramp.p_AverageValue = 500;
                    p_Ramp.p_Colors = new Color[] { Color.Blue, Color.Red };
                    p_Ramp.Create_Ramp();
                }

                //创建画图对象
                p_Graphics = Graphics.FromImage(p_Bitmap);
                return true;
            }
            catch
            {
                throw;
            }
        }

        /// <summary>关闭画布
        /// </summary>
        public virtual bool Close()
        {
            try
            {
                if (p_Graphics != null)
                {
                    p_Graphics.Dispose();
                }
                if (p_Bitmap != null)
                {
                    p_Bitmap.Dispose();
                }
                return true;
            }
            catch
            {
                throw;
            }
        }

        /// <summary>保存图片返回Json结果
        /// </summary>
        /// <param name="strPath"></param>
        /// <param name="pImageFormat">图片保存格式</param>
        /// <returns></returns>
        public virtual clssData_Json Save(string strPath, ImageFormat pImageFormat)
        {
            clssData_Json pJason = new clssData_Json();
            try
            {
                //透明及保存
                p_Bitmap.MakeTransparent(Color.Transparent);
                p_Bitmap.Save(strPath, pImageFormat);

                //生成Json结果
                pJason.Add_Data("Image_Width", p_Bitmap.Width.ToString());
                pJason.Add_Data("Image_Height", p_Bitmap.Height.ToString());
                pJason.Add_Data("Image_Format", pImageFormat.ToString());
                pJason.Add_Data("Image_Path", strPath);
                pJason.Add_Data("CellSize", p_CellSize);
                pJason.Add_Data("Base_Point", new clssData_Json().TransFrom_String(p_Base.ToString()));
                pJason.Add_Data("Bounds", m_objBounds.ToString());
                return pJason;
            }
            catch
            {
                throw;
            }
        }


        /// <summary>更新图片Rgb（使用byte组(32位, 依次为蓝、绿、红、A))
        /// </summary>
        /// <param name="curBitmap"></param>
        /// <param name="bytRGB">颜色byte组信息</param>
        public bool SetData(byte[] bytRGB)
        {
            try
            {
                return SetData(ref m_objBitmap, bytRGB);
            }
            catch
            {
                throw;
            }
        }

        /// <summary>使用图片更新新图片部分(指定起始位置)
        /// </summary>
        /// <param name="curBitmap"></param>
        /// <param name="nOffset_X">偏移位置X</param>
        /// <param name="nOffset_Y">偏移位置Y</param>
        public bool SetData(Bitmap curBitmap, int nOffset_X, int nOffset_Y)
        {
            byte[] bytTemps = null;
            try
            {
                //调用绘制 
                //p_Graphics.DrawImage(curBitmap, nOffset_X, nOffset_Y);
                //return true;

                //获取当前图数据
                bytTemps = GetData(curBitmap);

                //更新数据
                return SetData(ref m_objBitmap, nOffset_Y, nOffset_X, curBitmap.Width, bytTemps);
            }
            catch
            {
                throw;
            }
        }

        #endregion

        #region 公有函数--静态

        /// <summary>提取图片Rgb的Byte组(32位, 依次为蓝、绿、红、A)
        /// </summary>
        /// <param name="curBitmap"></param>
        public static byte[] GetData(Bitmap curBitmap)
        {
            BitmapData objData = null;
            byte[] bytRGB = null;
            int nWidth = curBitmap.Width;
            int nHeight = curBitmap.Height;
            int nLength = 0;
            try
            {
                //不能为空
                if (curBitmap == null)
                {
                    return bytRGB;
                }

                //实例Rgb组大小
                nLength = nHeight * 4 * nWidth;
                bytRGB = new byte[nLength];

                //提取数据
                objData = curBitmap.LockBits(new Rectangle(0, 0, nWidth, nHeight), ImageLockMode.ReadWrite, PixelFormat.Format32bppPArgb);
                System.IntPtr Scan0 = objData.Scan0;
                System.Runtime.InteropServices.Marshal.Copy(Scan0, bytRGB, 0, nLength);
                curBitmap.UnlockBits(objData);

                //返回
                return bytRGB;
            }
            catch
            {
                throw;
            }
        }

        /// <summary>更新图片Rgb（使用byte组(32位, 依次为蓝、绿、红、A))
        /// </summary>
        /// <param name="curBitmap"></param>
        /// <param name="bytRGB">颜色byte组信息</param>
        public static bool SetData(ref Bitmap curBitmap, byte[] bytRGB)
        {
            BitmapData objData = null;
            byte[] bytTemp = null;
            int nWidth, nHeight;
            int nLength = 0;
            try
            {
                //不能为空
                if (curBitmap == null)
                {
                    return false;
                }
                nWidth = curBitmap.Width;
                nHeight = curBitmap.Height;

                //实例Rgb组大小
                nLength = nHeight * 4 * nWidth;
                bytTemp = new byte[nLength];
                if (bytRGB.Length != bytTemp.Length)
                {
                    return false;
                }

                //提取数据
                objData = curBitmap.LockBits(new Rectangle(0, 0, nWidth, nHeight), ImageLockMode.ReadWrite, PixelFormat.Format32bppPArgb);
                System.IntPtr Scan0 = objData.Scan0;
                System.Runtime.InteropServices.Marshal.Copy(Scan0, bytTemp, 0, nLength);
                System.Runtime.InteropServices.Marshal.Copy(bytRGB, 0, Scan0, nLength);
                curBitmap.UnlockBits(objData);

                //返回
                return true;
            }
            catch
            {
                throw;
            }
        }

        /// <summary>更新图片Rgb（使用yte组(32位, 依次为蓝、绿、红、A)
        /// </summary>
        /// <param name="curBitmap"></param>
        /// <param name="nRowIndex">起始行号</param>
        /// <param name="nColIndex">起始列号</param>
        /// <param name="nWidthRGB">设置的数据宽度</param>
        /// <param name="bytRGB">值信息</param>
        public static bool SetData(ref Bitmap curBitmap, int nRowIndex, int nColIndex, int nWidthRGB, byte[] bytRGB)
        {
            BitmapData objData = null;
            byte[] bytTemp = null;
            int nWidth, nHeight;
            int nHeightRGB = 0;
            int nLength = 0, nLengthRGB = 0;
            try
            {
                //不能为空
                if (curBitmap == null)
                {
                    return false;
                }

                //计算传入数据
                nLengthRGB = bytRGB.Length;
                nHeightRGB = nLengthRGB / nWidthRGB / 4;

                //修正长宽(可能超出图片范围)
                nHeight = nHeightRGB + nRowIndex < curBitmap.Height ? nHeightRGB : curBitmap.Height - nRowIndex;
                nWidth = nWidthRGB + nColIndex < curBitmap.Width ? nWidthRGB : curBitmap.Width - nColIndex;
                nLength = nHeight * 4 * nWidth;
                bytTemp = GetData(curBitmap);

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
                objData = curBitmap.LockBits(new Rectangle(nColIndex, nRowIndex, nWidth, nHeight), ImageLockMode.ReadWrite, PixelFormat.Format32bppPArgb);
                System.IntPtr Scan0 = objData.Scan0;
                System.Runtime.InteropServices.Marshal.Copy(bytTemp, 0, Scan0, nLength);
                curBitmap.UnlockBits(objData);

                //返回
                return true;
            }
            catch
            {
                throw;
            }
        }

        /// <summary>自动调整大小(未完善)
        /// </summary>
        /// <param name="curBitmap"></param>
        public static void dd2(Bitmap curBitmap)
        {
            Bitmap objTemp;
            try
            {
                if (curBitmap != null)
                {
                    int width = curBitmap.Width;
                    int height = curBitmap.Height;
                    int length = height * 4 * width;
                    byte[] RGB = new byte[length];

                    BitmapData data = curBitmap.LockBits(new Rectangle(0, 0, width, height), ImageLockMode.ReadWrite, PixelFormat.Format32bppPArgb);
                    System.IntPtr Scan0 = data.Scan0;
                    System.Runtime.InteropServices.Marshal.Copy(Scan0, RGB, 0, length);
                    //double gray = 0;
                    //for (int i = 0; i < RGB.Length; i = i + 3)
                    //{
                    //    gray = RGB[i + 2] * 0.3 + RGB[i + 1] * 0.59 + RGB[i] * 0.11;
                    //    RGB[i + 2] = RGB[i + 1] = RGB[i] = (byte)gray;
                    //}
                    System.Runtime.InteropServices.Marshal.Copy(RGB, 0, Scan0, length);
                    curBitmap.UnlockBits(data);

                    //新图生成
                    int nHeight = height / 2;
                    int nW = 50;
                    objTemp = new Bitmap(width, height + nW);
                    int nLength = objTemp.Height * 4 * objTemp.Width;
                    byte[] objDataNew_RGB = new byte[nLength];
                    BitmapData objDataNew = objTemp.LockBits(new Rectangle(0, 0, objTemp.Width, objTemp.Height), ImageLockMode.ReadWrite, PixelFormat.Format32bppPArgb);
                    System.IntPtr nScan = objDataNew.Scan0;
                    int nTride = objDataNew.Stride;
                    int nLength3 = objTemp.Height * nTride;

                    System.Runtime.InteropServices.Marshal.Copy(nScan, objDataNew_RGB, 0, nLength);

                    int nMid = (nHeight) * nTride;
                    int nMid2 = nW * nTride;
                    for (int i = 0; i < nMid; i = i + 1)
                    {
                        objDataNew_RGB[i] = RGB[i];
                    }

                    for (int i = nMid; i < nMid + nMid2; i = i + 1)
                    {
                        objDataNew_RGB[i] = RGB[i];
                    }

                    for (int i = nMid + nMid2; i < nLength; i = i + 1)
                    {
                        objDataNew_RGB[i] = RGB[i - nMid2];
                    }

                    System.Runtime.InteropServices.Marshal.Copy(objDataNew_RGB, 0, nScan, nLength);
                    objTemp.UnlockBits(objDataNew);

                    Font objFont = new Font("微软雅黑", 16);
                    Brush objBrush = new SolidBrush(Color.Black);
                    Graphics objGraph = Graphics.FromImage(objTemp);
                    StringFormat objFormat = new StringFormat(); ;
                    objFormat.Alignment = StringAlignment.Far;
                    objGraph.DrawString("PM10:", objFont, objBrush, 100, 10, objFormat);
                    //<li><span class="box_left">PM10:</span><span class="box_right">0.080mg/m³</span></li>

                    string strPath = @"E:\Test\test3.png";
                    objTemp.MakeTransparent();
                    objTemp.Save(strPath, System.DrawingCore.Imaging.ImageFormat.Png);
                }

            }
            catch
            {
                throw;
            }
        }

        #region 裁剪缩放相关

        /// <summary>图片缩放
        /// </summary>
        /// <param name="pBitmap">被裁剪图片</param>
        /// <param name="nNew_Width">新宽度</param>
        /// <param name="nNew_Height">新高度</param>
        /// <returns></returns>
        public static Bitmap Image_Resize(Bitmap pBitmap, int nNew_Width, int nNew_Height)
        {
            Bitmap objBitmap = null;
            Graphics objGraph = null;
            try
            {
                //不能为空
                if (pBitmap == null)
                {
                    return null;
                }

                //实例新图
                objBitmap = new Bitmap(nNew_Width, nNew_Height);
                objGraph = Graphics.FromImage(objBitmap);

                //缩放-插值
                objGraph.InterpolationMode = InterpolationMode.HighQualityBicubic;
                objGraph.DrawImage(pBitmap, new Rectangle(0, 0, nNew_Width, nNew_Height), new Rectangle(0, 0, pBitmap.Width, pBitmap.Height), GraphicsUnit.Pixel);
                objGraph.Dispose();

                //返回
                return objBitmap;
            }
            catch
            {
                throw;
            }
        }

        /// <summary>图片裁剪
        /// </summary>
        /// <param name="pBitmap">被裁剪图片</param>
        /// <param name="pRect">裁剪范围</param>
        /// <returns></returns>
        public static Bitmap Image_Cut(Bitmap pBitmap, Rectangle pRect)
        {
            Bitmap objBitmap = null;
            Graphics objGraph = null;
            try
            {
                //不能为空
                if (pBitmap == null)
                {
                    return null;
                }

                //裁剪区域检查、校正
                if (pRect.Left > pBitmap.Width || pRect.Top > pBitmap.Height)
                {
                    return null;
                }

                //超宽、超高修正
                if (pRect.Right > pBitmap.Width)
                {
                    pRect.Width = pBitmap.Width - pRect.Left;
                }
                if (pRect.Bottom > pBitmap.Height)
                {
                    pRect.Height = pBitmap.Height - pRect.Top;
                }

                //裁剪
                objBitmap = new Bitmap(pRect.Width, pRect.Height);
                objGraph = Graphics.FromImage(objBitmap);
                objGraph.DrawImage(pBitmap, new Rectangle(0, 0, pRect.Width, pRect.Height), pRect, GraphicsUnit.Pixel);
                objGraph.Dispose();

                //返回
                return objBitmap;
            }
            catch
            {
                throw;
            }
        }

        /// <summary>图片旋转
        /// </summary>
        /// <param name="pBitmap">被旋转图片</param>
        /// <param name="dRotate">旋转角度</param>
        /// <returns></returns>
        public static Bitmap Image_Rotate(Bitmap pBitmap, double dRotate)
        {
            Bitmap objBitmap = null;
            Graphics objGraph = null;
            Rectangle pRect, pRectNew;
            Point pOffset, pCenter;

            double dRadian = clsGeometry.TransTo_Radian(dRotate);
            double dCos = Math.Cos(dRadian);
            double dSin = Math.Sin(dRadian);
            int nw, nh, nW, nH;
            try
            {
                //不能为空
                if (pBitmap == null)
                {
                    return null;
                }

                //得到原图大小
                nw = pBitmap.Width;
                nh = pBitmap.Height;
                pRect = new Rectangle(0, 0, nw, nh);

                //目标位图大小
                nW = (int)(Math.Max(Math.Abs(nw * dCos - nh * dSin), Math.Abs(nw * dCos + nh * dSin)));
                nH = (int)(Math.Max(Math.Abs(nw * dSin - nh * dCos), Math.Abs(nw * dSin + nh * dCos)));

                objBitmap = new Bitmap(nW, nH);
                objGraph = Graphics.FromImage(objBitmap);
                objGraph.InterpolationMode = InterpolationMode.HighQualityBilinear;
                objGraph.SmoothingMode = SmoothingMode.HighQuality;

                //偏移计算
                pOffset = new Point((nW - nw) / 2, (nH - nh) / 2);

                //构造显示区域，让图像的中心与窗口一致
                pRectNew = new Rectangle(pOffset.X, pOffset.Y, nw, nh);
                pCenter = new Point(pRectNew.X + pRectNew.Width / 2, pRectNew.Y + pRectNew.Height / 2);

                //旋转
                objGraph.TranslateTransform(pCenter.X, pCenter.Y);
                objGraph.RotateTransform((float)dRotate);

                //恢复图像在水平和垂直方向的平移
                objGraph.TranslateTransform(-pCenter.X, -pCenter.Y);
                objGraph.DrawImage(pBitmap, pRectNew);

                //重置所有变化
                objGraph.ResetTransform();
                objGraph.Save();
                objGraph.Dispose();

                //返回
                return objBitmap;
            }
            catch
            {
                throw;
            }
        }

        #endregion

        #region 格式转换

        /// <summary>将图片转换为灰度图 
        /// </summary>
        /// <param name="curBitmap"></param>
        //public static Bitmap Trans_ToGray(Bitmap curBitmap)
        //{
        //    Bitmap pBitmap = null;
        //    Graphics pGraphics = null;
        //    ImageAttributes pIA = new ImageAttributes();
        //    ColorMatrix pCM;
        //    try
        //    {
        //        //不能为空
        //        if (curBitmap == null)
        //        {
        //            return null;
        //        }

        //        //示例新图
        //        pBitmap = new Bitmap(curBitmap.Width, curBitmap.Height, PixelFormat.Format16bppGrayScale);
        //        pGraphics = Graphics.FromImage(pBitmap);

        //        //构建颜色分量矩阵
        //        float[][] pMatrix_Color ={
        //                                     new float[]{0.299f,0.299f,0.299f,0,0},
        //                                     new float[]{0.587f,0.587f,0.587f,0,0},
        //                                     new float[]{0.114f,0.114f,0.114f,0,0},
        //                                     new float[]{0,0,0,1,0},
        //                                     new float[]{0,0,0,0,1},
        //                                  };
        //        pCM = new ColorMatrix(pMatrix_Color);


        //        //设置信息并重新绘制
        //        pIA.SetColorMatrix(pCM, ColorMatrixFlag.Default, ColorAdjustType.Bitmap);
        //        pGraphics.DrawImage(curBitmap, new Rectangle(0, 0, curBitmap.Width, curBitmap.Height), 0, 0, curBitmap.Width, curBitmap.Height, GraphicsUnit.Pixel, pIA);

        //        //返回
        //        pGraphics.Dispose();
        //        return pBitmap;
        //    }
        //    catch
        //    {
        //        throw;
        //    }
        //}

        /// <summary>将图片转换为灰度图 
        /// </summary>
        /// <param name="curBitmap"></param>
        public static Bitmap Trans_ToGray(Bitmap curBitmap)
        {
            Bitmap pBitmap = null;
            BitmapData objData = null;
            byte[] bytRGB = null, bytGray = null;

            int nWidth, nHeight, nStride, nOffset, nLength, nChannel;
            int nPosScan = 0, nPosDst = 0;
            try
            {
                //不能为空
                if (curBitmap == null)
                {
                    return null;
                }

                //提取数据
                objData = curBitmap.LockBits(new Rectangle(0, 0, curBitmap.Width, curBitmap.Height), ImageLockMode.ReadOnly, curBitmap.PixelFormat);
                curBitmap.Save(@"F:\Working\张斌\工作文档\GIS数据库\myTest\Leak_Flood_admin__160902161557122.tif", ImageFormat.Tiff);


                //获取图像参数
                nChannel = Get_CountChannel(curBitmap.PixelFormat);
                nWidth = objData.Width;
                nHeight = objData.Height;
                nStride = objData.Stride;               //扫描线宽度
                nOffset = nStride - nWidth * nChannel;  //显示宽度与扫描线宽度的间隙
                nLength = nStride * nHeight;            //内存区间大小


                //拷贝源数据
                bytRGB = new byte[nLength];
                System.Runtime.InteropServices.Marshal.Copy(objData.Scan0, bytRGB, 0, nLength);

                //分配及计算灰度数组
                bytGray = new Byte[nWidth * nHeight];
                for (int i = 0; i < nHeight; i++)
                {
                    for (int j = 0; j < nWidth; j++)
                    {
                        double dTemp = bytRGB[nPosScan++] * 0.11 + bytRGB[nPosScan++] * 0.59 + bytRGB[nPosScan++] * 0.3;
                        nPosScan++;
                        bytGray[nPosDst++] = (byte)dTemp;
                    }

                    //跳过每行未用空间字节
                    nPosScan += nOffset;
                }

                //更新数据及内存解锁
                System.Runtime.InteropServices.Marshal.Copy(bytRGB, 0, objData.Scan0, nLength);
                curBitmap.UnlockBits(objData);

                //构建8位灰度图并返回
                pBitmap = Build_BitmapGray(bytGray, nWidth, nHeight);
                return pBitmap;
            }
            catch
            {
                throw;
            }
        }

        /// <summary>构建灰度图
        /// </summary>
        /// <param name="bytGray">灰度图数据</param>
        /// <param name="nWidth"></param>
        /// <param name="nHeigh"></param>
        /// <returns></returns>
        public static Bitmap Build_BitmapGray(byte[] bytGray, int nWidth, int nHeight)
        {
            Bitmap pBitmap = null;
            BitmapData objData = null;
            byte[] bytGray_Value = null;

            int nOffset, nLength;
            int nPosScan = 0, nPosDst = 0;
            try
            {
                //构建8位灰度图
                pBitmap = new Bitmap(nWidth, nHeight, PixelFormat.Format16bppGrayScale);

                //锁定内存操作
                objData = pBitmap.LockBits(new Rectangle(0, 0, nWidth, nHeight), ImageLockMode.WriteOnly, pBitmap.PixelFormat);


                //获取图像参数
                nOffset = objData.Stride - objData.Width;    //计算每行未用空间字节数
                nLength = objData.Stride * objData.Height;   //内存区间大小

                clsTrans.TransTo_Bytes(0.1f);

                //为图像赋值
                bytGray_Value = new Byte[nLength];
                for (int i = 0; i < nHeight; i++)
                {
                    for (int j = 0; j < nWidth; j++)
                    {
                        bytGray_Value[nPosScan++] = bytGray[nPosDst++];
                    }

                    //跳过每行未用空间字节
                    nPosScan += nOffset;
                }

                //更新数据及内存解锁
                System.Runtime.InteropServices.Marshal.Copy(bytGray_Value, 0, objData.Scan0, nLength);
                pBitmap.UnlockBits(objData);

                //修改生成位图的索引
                ColorPalette pCP;
                using (Bitmap bmp = new Bitmap(1, 1, PixelFormat.Format8bppIndexed))
                {
                    pCP = bmp.Palette;
                }

                //修改索引表
                for (int i = 0; i < 256; i++)
                {
                    pCP.Entries[i] = Color.FromArgb(i, i, i);
                }
                pBitmap.Palette = pCP;

                //返回
                return pBitmap;
            }
            catch
            {
                throw;
            }
        }

        /// <summary>像素通道数(几个8位)
        /// </summary>
        /// <param name="pPixelFormat">像素类型</param>
        /// <returns></returns>
        public static int Get_CountChannel(PixelFormat pPixelFormat)
        {
            int nWidth;
            try
            {
                switch (pPixelFormat)
                {
                    case PixelFormat.Format8bppIndexed:
                        nWidth = 1;
                        break;

                    case PixelFormat.Format24bppRgb:
                        nWidth = 3;
                        break;

                    case PixelFormat.Format32bppArgb:
                    case PixelFormat.Format32bppRgb:
                    case PixelFormat.Format32bppPArgb:
                        nWidth = 4;
                        break;

                    default:
                        nWidth = 0;
                        break;
                }
                return nWidth;
            }
            catch
            {
                throw;
            }
        }

        #endregion

        #endregion

    }
}
