//===============================================================================
// Copyright @ 2021 Guangzhou Yijian Life Technology Co.,Ltd. All rights reserved.
// Copyright @ 2021 广州易简生活科技有限公司.  版权所有.
//===============================================================================
// 文件名称： 
// 功能描述：Data_Quote_Swap --行情数据类-数据交换
// 创建标识：zxc   2021-06-20
// 修改标识： 
// 修改描述：
//===============================================================================
using System;
using zxcCore.Extensions;
using zxcCore.zxcData.Cache.Memory;
using zxcCore.zxcRobot.Quote.Data;
using zxcCore.Common;
using Newtonsoft.Json.Linq;

namespace zxcCore.zxcRobot.Monitor
{
    /// <summary>行情数据类-数据交换
    /// </summary>
    public class Data_Quote_Swap : Data_Quote_Realtime_5Stalls
    {
        #region 属性及构造

        public string _exType { get; set; }

        public Data_Quote_Swap()
        {
        }
        public Data_Quote_Swap(StockInfo stockInfo = null) : base(stockInfo)
        {
        }

        #endregion


        //对象转换-由json对象
        public override bool FromJsonObj(JObject jsonData, typeQuoteTime quoteTime)
        {
            //基类初始
            bool bResult = base.FromJsonObj(jsonData, quoteTime);
            if (bResult)
            {
                this.QuoteTimeType = typeQuoteTime.real;                //标识为实时数据
                this._exType = this.StockExchange.ToString();
            }
            return bResult;
        }

    }

}
