using System;
using System.Collections.Generic;

namespace zpCore.zpDataCache.Memory
{
    /// <summary>数据检查-消息管理类
    /// </summary>
    public interface IDataCheck_Msger
    {
        /// <summary>是否缓存消息
        /// </summary>
        bool IsBuffer { get; }
        /// <summary>缓存消息数量
        /// </summary>
        int NumsBuffer { get; }
        /// <summary>数据缓存集管理类
        /// </summary>
        List<dynamic> MsgsBuffer { get; }


        /// <summary>通知消息处理(统一出口)
        /// </summary>
        /// <param name="消息内容(建议格式：new { XX1 = 0, XX2 = aa })"></param>
        /// <returns></returns>
        bool NotifyMsg(dynamic msg);
        /// <summary>消息发送(但一发送，单条单目标)
        /// </summary>
        /// <param name="msg">消息内容(建议格式：new { XX1 = 0, XX2 = aa })</param>
        /// <returns></returns>
        bool SendMsg(dynamic msg);
        /// <summary>消息日志记录
        /// </summary>
        /// <param name="msg">消息内容(建议格式：new { XX1 = 0, XX2 = aa })</param>
        /// <returns></returns>
        bool LogMsg(dynamic msg);
    }
}
