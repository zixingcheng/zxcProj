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
using System.DrawingCore;

namespace GModel.mySysterm.myDrawingCore
{
    public class clsColorRamp_Stretch : clsColorRamp
    {
        #region 参数

        /// <summary>标准差类
        /// </summary>
        private clsStandardDeviation m_clsStandEevσ = null;

        /// <summary>构造函数
        /// </summary>
        public clsColorRamp_Stretch()
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
        public override bool Create_Ramp()
        {
            bool bResult = false;
            try
            {
                //调用基类方法
                bResult = base.Create_Ramp();

                //实例标准差对象
                this.Create_StandEevσ();
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
            try
            {
                //实例标准差对象
                if (m_clsStandEevσ == null)
                {
                    this.Create_StandEevσ();
                }

                //标准差插值计算
                return m_clsStandEevσ.Check_Value(dValue);
            }
            catch
            {
                throw;
            }
        }

        /// <summary>创建标准差插值对象
        /// </summary> 
        /// <returns></returns>
        private bool Create_StandEevσ()
        {
            try
            {
                //实例标准差对象
                m_clsStandEevσ = new clsStandardDeviation();
                m_clsStandEevσ.p_MaxValue = p_MaxValue;
                m_clsStandEevσ.p_MinValue = p_MinValue;
                m_clsStandEevσ.p_AverageValue = p_AverageValue;
                m_clsStandEevσ.p_StandDevValue = p_StandDevValue;
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