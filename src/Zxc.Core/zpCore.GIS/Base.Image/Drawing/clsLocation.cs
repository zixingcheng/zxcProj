//===============================================================================
// Copyright @ 2012 Beijing Global Safety Technology Co.,Ltd. All rights reserved.
// Copyright @ 2012 北京辰安科技股份有限公司.  版权所有.
//===============================================================================
// 文件名称： 
// 功能描述：系统操作类_位置操作相关方法实现类 
// 创建标识：张斌   2013-01-10 
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
    public class clsLocation : DisposeClass
    {
        #region 标准Dispose模式

        /// <summary>
        /// 析构函数
        /// 必须，以备程序员忘记了显式调用Dispose方法
        /// </summary>
        ~clsLocation()
        {
            //必须为false 
            Dispose(false);
        }

        //示例用法
        //使用静态实例的方法调用(可以留此接口，当使用频率较高时有优势，当然也可以使用静态函数),占用资源
        //使用次数少建议直接New出来直接调用，配合析构函数进行释放，不占资源
        static private clsLocation ms_objClass;
        public static clsLocation Instance()
        {
            if (ms_objClass == null)
            {
                //实例新静态类,并标识需释放
                ms_objClass = new clsLocation();
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

        #region 参数

        /// <summary>
        /// 方向枚举(上下左右指正中)
        /// </summary>
        public enum enum_Direction
        {
            上 = 1,
            下 = 5,
            左 = 7,
            右 = 3,
            左上 = 2,
            左下 = 4,
            右上 = 8,
            右下 = 6
        }

        #endregion

        #region 公有函数
         
        /// <summary>
        /// 获取控件的弹出位置(指定位置弹出,超边界则修正) 
        /// </summary>
        /// <param name="PointXY">起始的XY坐标(无依赖控件时按给定的弹出大小进行调整弹出位置)</param>
        /// <param name="nWidth">弹出控件宽</param>
        /// <param name="nHeight">弹出控件高</param>
        /// <param name="PointMargin">上下弹出修正(相对原点位移的XY坐标)</param>
        /// <param name="nPopupType">默认弹出的为位置</param>
        /// <param name="bIsUpDownOnly">是否只上下弹出(否则运行与下边界齐平)</param>
        /// <returns></returns>
        public Point GetLocation_PopupCtrl(Point PointXY, int nWidth, int nHeight, Point PointMargin, enum_Direction nPopupType, bool bIsUpDownOnly)
        {
            Rectangle rctScreen;

            try
            {
                //取屏幕有效区以备用进行位置修正  
                rctScreen = GetRectangle_TopContainer(null, false);

                //修正X坐标(如果右侧范围不够则放左侧)
                PointXY = GetLocation_PopupCtrl(PointXY, rctScreen, new Size(), new Size(nWidth, nHeight), PointMargin, bIsUpDownOnly);

                //返回起始位置
                return PointXY;
            }
            catch
            {
                return new Point(0, 0);
            }
        }

        /// <summary>
        /// 获取控件的弹出位置(指定位置弹出,超边界则修正) 
        /// </summary>
        /// <param name="objControl">依赖的控件(存在时自动修正PointXY为右上角，并依据控件大小进行必要的弹出位置修正)</param>
        /// <param name="PointXY">起始的XY坐标(无依赖控件时按给定的弹出大小进行调整弹出位置)</param>
        /// <param name="nWidth">弹出控件宽</param>
        /// <param name="nHeight">弹出控件高</param>
        /// <param name="PointMargin">上下弹出修正(相对原点位移的XY坐标)</param>
        /// <param name="nPopupType">默认弹出的为位置</param>
        /// <param name="bIsUpDownOnly">是否只上下弹出(否则运行与下边界齐平)</param>
        /// <param name="bIsInClient">是否在客户端容器弹出(否则以屏幕有效区域弹出)</param>
        /// <returns></returns>
        public Point GetLocation_PopupCtrl(Control objControl, int nWidth, int nHeight, Point PointMargin, enum_Direction nPopupType, bool bIsUpDownOnly, bool bIsInClient)
        {
            Point PointXY = Point.Empty;
            Rectangle rctScreen;

            try
            {
                //提取弹出位置 
                PointXY = GetLocation_PopupCtrl(objControl, nPopupType); ;

                //取工作区以备用进行位置修正  
                rctScreen = GetRectangle_TopContainer(objControl, bIsInClient);

                //修正X坐标(如果右侧范围不够则放左侧)
                PointXY = GetLocation_PopupCtrl(PointXY, rctScreen, objControl.Size, new Size(nWidth, nHeight), PointMargin, bIsUpDownOnly);

                //返回起始位置
                return PointXY;
            }
            catch
            {
                return new Point(0, 0);
            }
        }
        
        /// <summary>
        /// 获取控件的弹出位置(指定位置弹出,超边界则修正) 
        /// </summary>
        /// <param name="PointXY">起始的XY坐标</param>
        /// <param name="rctScreen">可用显示区域</param>
        /// <param name="objCtrlSize">依赖控件大小(存在时考虑空间间隔，如左不够变到右)</param>
        /// <param name="objShowSize">弹出控件宽,高大小</param>
        /// <param name="PointMargin">上下弹出修正(相对原点位移的XY坐标)</param>
        /// <param name="bIsUpDownOnly">是否只上下弹出(否则运行与下边界齐平)</param> 
        /// <returns></returns>
        public Point GetLocation_PopupCtrl(Point PointXY, Rectangle rctScreen, Size objCtrlSize, Size objShowSize, Point PointMargin, bool bIsUpDownOnly)
        {
            int nX, nY;
            try
            {
                //修正X坐标(如果右侧范围不够则放左侧)
                nX = PointXY.X + PointMargin.X;
                if (nX + objShowSize.Width > rctScreen.Width)
                { 
                    //起点修正为左边 
                    nX = PointXY.X + objCtrlSize.Width - PointMargin.X - objShowSize.Width;
                }

                //修正Y坐标(下范围不足则与下边界齐平)
                nY = PointXY.Y + PointMargin.Y;
                if (PointXY.Y + objShowSize.Height > rctScreen.Height)
                {
                    if (bIsUpDownOnly == true)
                    {
                        //只上下修正 
                        nY = PointXY.Y - objShowSize.Height - PointMargin.Y - objCtrlSize.Height;
                    }
                    else
                    {
                        //超过下边界，修正为齐平
                        nY = rctScreen.Height - objShowSize.Height;
                    }
                }

                //返回起始位置
                return new Point(nX, nY);
            }
            catch
            {
                return new Point(0, 0);
            }
        }

        /// <summary>
        /// 获取控件的弹出位置(无修正) 
        /// </summary>
        /// <param name="objControl">依赖的控件</param>
        /// <param name="nPopupType">弹出方位</param>
        /// <returns></returns>
        public Point GetLocation_PopupCtrl(Control objControl, enum_Direction nPopupType)
        {
            Point PointXY = Point.Empty;
            int nX = 0, nY = 0;
            try
            {
                //修正起始坐标为控件右上角 
                if (objControl == null) return Point.Empty;

                //记录修正的XY坐标
                nY = objControl.Height;
                nX = objControl.Width;

                //弹出位置Y坐标进行修正 
                switch (nPopupType)
                {
                    case enum_Direction.上:
                    case enum_Direction.右上:
                    case enum_Direction.左上:
                        nY = 0;
                        break;

                    case enum_Direction.左:
                        nY = nY / 2;
                        break;
                }

                //弹出位置X坐标进行修正 
                switch (nPopupType)
                {
                    case enum_Direction.左:
                    case enum_Direction.左上:
                    case enum_Direction.左下:
                        nX = 0;
                        break;

                    case enum_Direction.上:
                    case enum_Direction.下:
                        nX = nX / 2;
                        break;
                }

                //新弹出位置 
                PointXY = GetLocation_InTopContainer(objControl);
                PointXY = new Point(PointXY.X + nX, PointXY.Y + nY);
            }
            catch
            {
                throw;
            }
            return (PointXY);
        }

        /// <summary>
        /// 提取控件的位置(顶级容器中的位置) 
        /// </summary>
        /// <param name="objControl">指定的控件</param>
        /// <returns></returns>
        public Point GetLocation_InTopContainer(Control objControl)
        {
            Point objPoint = Point.Empty;
            Control objParent = null;
            int nX, nY;
            try
            {
                //记录当前控件起始位置 
                nX = objControl.Left;
                nY = objControl.Top;

                //递归到上个容器(最上级不处理)
                objParent = objControl.Parent;
                if (objParent.Parent != null)
                {
                    objPoint = GetLocation_InTopContainer(objParent);
                    nX = nX + objPoint.X;
                    nY = nY + objPoint.Y;
                }
            }
            catch
            {
                throw;
            }
            return (new Point(nX, nY));
        }

        /// <summary>
        /// 获取控件的弹出位置(指定位置弹出,超边界则修正) 
        /// </summary>
        /// <param name="objControl">指定的控件(无指定控件则取屏幕有效区)</param>
        /// <param name="bIsInClient">是否在客户端容器弹出(否则以屏幕有效区域弹出)</param>
        /// <returns></returns>
        public Rectangle GetRectangle_TopContainer(Control objControl, bool bIsInClient)
        {
            Rectangle rctScreen;
            try
            {
                //取工作区以进行位置修正  
                bIsInClient = (objControl == null) ? false : bIsInClient;
                if (bIsInClient == false)
                {
                    rctScreen = System.Windows.Forms.SystemInformation.WorkingArea;
                }
                else
                {
                    rctScreen = new Rectangle(Point.Empty, GetSize_TopContainer(objControl));
                }

                //返回起始位置
                return rctScreen;
            }
            catch
            {
                return new Rectangle();
            }
        }

        /// <summary>
        /// 提取顶级容器的大小
        /// </summary>
        /// <param name="objControl">指定的控件</param>
        /// <returns></returns>
        public Size GetSize_TopContainer(Control objControl)
        {
            Size objSize =new Size();
            Control objParent = null;
            try
            {
                //记录大小
                objParent = objControl.Parent;
                if (objParent != null)
                {
                    objSize = objParent.ClientSize;
                }

                //递归到上个容器(最上级不处理)
                if (objParent.Parent != null)
                {
                    objSize = GetSize_TopContainer(objParent); 
                }
            }
            catch
            {
                throw;
            }
            return (objSize);
        }


        #endregion

    }
}

