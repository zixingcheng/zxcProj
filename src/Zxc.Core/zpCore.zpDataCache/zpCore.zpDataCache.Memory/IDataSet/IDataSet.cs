using System;
using System.Collections.Generic;

namespace zpCore.zpDataCache.Memory
{
    /// <summary>
    /// 数据设置对象接口-IOT
    /// </summary>
    public interface IDataSet
    {
        /// <summary>
        /// 标识名称
        /// </summary>
        string Tag_Name { get; }


        /// <summary>配置转为字符串
        /// </summary>
        string ToString();
        /// <summary>字符串转配置
        /// </summary>
        void FromString();
    }
}