using Newtonsoft.Json.Linq;
using System;
using System.ComponentModel;
using zxcCore.Extensions;

namespace zxcCore.zxcRobot.Quote.Data
{

    /// <summary>行情数据接口
    /// </summary>
    public interface IData_Quote_Info : IData_Quote
    {
        string StockID { get; set; }
        string StockName { get; set; }
        typeStock StockType { get; set; }
        typeStockExchange StockExchange { get; set; }
        string StockID_Tag { get; }

        bool IsIndex();
    }

}