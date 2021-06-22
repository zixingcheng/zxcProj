//===============================================================================
// Copyright @ 2021 Guangzhou Yijian Life Technology Co.,Ltd. All rights reserved.
// Copyright @ 2021 广州易简生活科技有限公司.  版权所有.
//===============================================================================
// 文件名称： 
// 功能描述：Data_Quote_Realtime_5Stalls --行情数据类-实时-5档
// 创建标识：zxc   2021-06-20
// 修改标识： 
// 修改描述：
//===============================================================================
using System;
using System.Collections.Generic;
using zxcCore.Common;
using zxcCore.zxcDataCache.MemoryDB;

namespace zxcCore.zxcRobot.Quote
{

    /// <summary>行情数据类-实时-5档
    /// </summary>
    public class Data_Quote_Realtime_5Stalls : Data_Quote_Realtime
    {
        #region 属性及构造

        /// <summary>买一价
        /// </summary>
        public double Price_Buy1
        {
            get; set;
        }
        /// <summary>买一量
        /// </summary>
        public double Volume_Buy1
        {
            get; set;
        }
        /// <summary>买二价
        /// </summary>
        public double Price_Buy2
        {
            get; set;
        }
        /// <summary>买二量
        /// </summary>
        public double Volume_Buy2
        {
            get; set;
        }
        /// <summary>买三价
        /// </summary>
        public double Price_Buy3
        {
            get; set;
        }
        /// <summary>买三量
        /// </summary>
        public double Volume_Buy3
        {
            get; set;
        }
        /// <summary>买四价
        /// </summary>
        public double Price_Buy4
        {
            get; set;
        }
        /// <summary>买四量
        /// </summary>
        public double Volume_Buy4
        {
            get; set;
        }
        /// <summary>买五价
        /// </summary>
        public double Price_Buy5
        {
            get; set;
        }
        /// <summary>买五量
        /// </summary>
        public double Volume_Buy5
        {
            get; set;
        }

        /// <summary>卖一价
        /// </summary>
        public double Price_Sell1
        {
            get; set;
        }
        /// <summary>卖一量
        /// </summary>
        public double Volume_Sell1
        {
            get; set;
        }
        /// <summary>卖二价
        /// </summary>
        public double Price_Sell2
        {
            get; set;
        }
        /// <summary>卖二量
        /// </summary>
        public double Volume_Sell2
        {
            get; set;
        }
        /// <summary>卖三价
        /// </summary>
        public double Price_Sell3
        {
            get; set;
        }
        /// <summary>卖三量
        /// </summary>
        public double Volume_Sell3
        {
            get; set;
        }
        /// <summary>卖四价
        /// </summary>
        public double Price_Sell4
        {
            get; set;
        }
        /// <summary>卖四量
        /// </summary>
        public double Volume_Sell4
        {
            get; set;
        }
        /// <summary>卖五价
        /// </summary>
        public double Price_Sell5
        {
            get; set;
        }
        /// <summary>卖五量
        /// </summary>
        public double Volume_Sell5
        {
            get; set;
        }

        public Data_Quote_Realtime_5Stalls()
        {
        }
        ~Data_Quote_Realtime_5Stalls()
        {
            // 缓存数据？
        }

        #endregion

    }

}
