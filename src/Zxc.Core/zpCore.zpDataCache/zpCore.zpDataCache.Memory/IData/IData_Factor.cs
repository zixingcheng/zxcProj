using System;
using System.Collections.Generic;

namespace zpCore.zpDataCache.Memory
{
    /// <summary>数据因子对象
    /// </summary>
    public interface IData_Factor
    {
        /// <summary>唯一编码-自定义，便于快速遍历
        /// </summary>
        string ID { get; set; }
        /// <summary>编码
        /// </summary>
        string Code { get; set; }
        /// <summary>名称-非必须
        /// </summary>
        string Name { get; set; }
        /// <summary>标准-非必须
        /// </summary>
        string Standard { get; set; }


        ///// <summary>数据设置管理对象-注入
        ///// </summary>
        //IDataSets_Manage_Iot DataSets { get; }
    }
}
