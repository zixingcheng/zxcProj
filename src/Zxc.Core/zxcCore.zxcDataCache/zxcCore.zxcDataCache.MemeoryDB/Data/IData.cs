using System;

namespace zxcCore.zxcDataCache.MemoryDB
{
    /// <summary>数据结构接口
    /// </summary>
    public interface IData
    {
        /// <summary>全局UID号
        /// </summary>
        string UID { get; set; }

        /// <summary>对象转为Json对象
        /// </summary>
        dynamic ToJson();
        /// <summary>Json对象转对象
        /// </summary>
        /// <param name="jsonData"></param>
        /// <returns></returns>
        bool FromJson(dynamic jsonData);
    }
}
