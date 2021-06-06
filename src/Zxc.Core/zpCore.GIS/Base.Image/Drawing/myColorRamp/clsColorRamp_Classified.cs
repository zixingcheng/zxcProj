//===============================================================================
// Copyright @ 2012 Beijing Global Safety Technology Co.,Ltd. All rights reserved.
// Copyright @ 2012 北京辰安科技股份有限公司.  版权所有.
//===============================================================================
// 文件名称： 
// 功能描述：系统操作类_色带相关方法实现类_拉伸 
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
    public class clsColorRamp_Classified : clsColorRamp
    {
        #region 参数

        /// <summary>中断值集(大于两个)
        /// </summary>
        public double[] pBreaks
        {
            get;
            set;
        }

        /// <summary>构造函数
        /// </summary>
        public clsColorRamp_Classified()
        {
            try
            {
                p_RampHeight = 30;
                p_RampWidth = 500;
                p_MinValue = 0;
                p_MaxValue = 999;
                p_Colors = new Color[] { Color.Black, Color.White };
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
        public override Color Get_Color(double dValue)
        {
            Color objColor = Color.Transparent;
            double dIndex = 0;
            try
            {
                //值必须在最大最小值范围内
                //if (dValue < p_MinValue || dValue > p_MaxValue)
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
        public override bool Create_Ramp()
        {
            bool bResult = false;
            try
            {
                //最大最小值修正
                p_MinValue = pBreaks[0];
                p_MaxValue = p_MaxValue > pBreaks[pBreaks.Length - 1] ? p_MaxValue : pBreaks[pBreaks.Length - 1];

                //调用基类方法
                bResult = base.Create_Ramp();
                return bResult;
            }
            catch
            {
                throw;
            }
        }

        /// <summary>提取指定值对应的色带颜色(标准差正态分布--纠正)
        /// </summary>
        /// <param name="dValue">当前值</param>
        /// <returns></returns>
        public override double Check_Value(double dValue)
        {
            double dMax, dMin, dIndex;
            int nLength = pBreaks.Length;
            int nIndex = 0;
            try
            {
                //极值判断
                if (dValue < pBreaks[0]) return 0;
                if (dValue > pBreaks[pBreaks.Length - 1]) return m_nValues[nLength - 1] - 1;

                //所在位置判断
                for (int i = 0; i < nLength; i++)
                {
                    if (dValue < pBreaks[i])
                    {
                        nIndex = i;
                        break;
                    }
                }

                //提取最大最小值计算索引序号
                dMin = pBreaks[nIndex - 1];
                dMax = pBreaks[nIndex];
                dIndex = (dValue - dMin) / (dMax - dMin) * (m_nValues[nIndex] - m_nValues[nIndex - 1]) + m_nValues[nIndex - 1];
                return (int)dIndex;
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
            double dCount = pBreaks.Length - 1;
            try
            {
                //重新实例颜色序号分段集组
                m_nValues = new int[pBreaks.Length];

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