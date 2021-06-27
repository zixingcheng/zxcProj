//===============================================================================
// Copyright @ 2021 Guangzhou Yijian Life Technology Co.,Ltd. All rights reserved.
// Copyright @ 2021 广州易简生活科技有限公司.  版权所有.
//===============================================================================
// 文件名称： 
// 功能描述：StockQuery --标的查询
// 创建标识：zxc   2021-06-26
// 修改标识： 
// 修改描述：
//===============================================================================
using Newtonsoft.Json.Linq;
using System;
using System.Collections.Generic;
using System.Text;
using zxcCore.Common;
using zxcCore.Extensions;
using zxcCore.zxcRobot.Quote.Data;

namespace zxcCore.zxcRobot.Quote
{
    public class StockQuery
    {

        #region 属性及构造 

        /// <summary>提取股票信息
        /// </summary>
        /// <param name="stockName"></param>
        /// <returns></returns>
        public StockInfo this[string stockTag]
        {
            get
            {
                return this.Get_StockInfo(stockTag);
            }
        }


        public StockQuery()
        {
            //提取行情API配置
        }
        ~StockQuery()
        {
            // 缓存数据？
        }

        #endregion

        /// <summary>查询行情标的信息
        /// </summary>
        /// <param name="stockTag">标的编号(名称，或标识)</param>
        /// <returns></returns>
        public StockInfo Get_StockInfo(string stockTag)
        {
            string[] stockNames = stockTag.Split(".");
            StockInfo pStockInfo = Quote_Datas._Datas.Get_StockInfo(stockNames[0], stockNames.Length > 1 ? stockNames[1] : "");
            return pStockInfo;
        }


        /// <summary>校正标识名称
        /// </summary>
        /// <param name="stockTag">标的标识/编号/名称</param>
        /// <returns></returns>
        public string Check_StockTag(string stockTag)
        {
            //校检标识名称
            StockInfo pStockInfo = this.Get_StockInfo(stockTag);
            if (pStockInfo == null) return "";
            return pStockInfo.StockID_Tag;
        }

    }

}
