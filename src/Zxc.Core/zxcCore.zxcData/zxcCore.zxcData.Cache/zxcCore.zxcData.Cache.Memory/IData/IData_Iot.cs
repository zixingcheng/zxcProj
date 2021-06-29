using System;
using System.Collections.Generic;

namespace zxcCore.zxcData.Cache.Memory
{
    /// <summary>数据结构-IOT
    /// </summary>
    interface IData_Iot<T> : IData<T>
    {
        /// <summary>数据时间
        /// </summary>
        DateTime Time { get; set; }
    }
}
