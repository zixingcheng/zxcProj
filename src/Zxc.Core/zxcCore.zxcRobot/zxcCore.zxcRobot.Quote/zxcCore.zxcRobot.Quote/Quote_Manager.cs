//===============================================================================
// Copyright @ 2021 Guangzhou Yijian Life Technology Co.,Ltd. All rights reserved.
// Copyright @ 2021 广州易简生活科技有限公司.  版权所有.
//===============================================================================
// 文件名称： 
// 功能描述：QuoteManager --行情管理器
// 创建标识：zxc   2021-06-26
// 修改标识： 
// 修改描述：
//===============================================================================
using Newtonsoft.Json.Linq;
using System;
using System.Collections.Generic;
using System.Text;
using zxcCore.Common;
using zxcCore.zxcRobot.Quote.Data;

namespace zxcCore.zxcRobot.Quote
{
    public class Quote_Manager
    {
        /// <summary>全局行情管理器
        /// </summary>
        public static readonly Quote_Manager _Quotes = new Quote_Manager();

        #region 属性及构造

        protected internal QuoteQuery _Query = new QuoteQuery();
        /// <summary>查询对象
        /// </summary>
        public QuoteQuery Query
        {
            get { return _Query; }
        }


        public Quote_Manager()
        {
        }
        ~Quote_Manager()
        {
            // 缓存数据？
        }

        #endregion


    }
}
