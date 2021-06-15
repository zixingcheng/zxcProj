using System;
using System.Collections.Generic;

namespace zxcCore.zxcRobot.Msger
{
    /// <summary>消息管理类类型
    /// </summary>
    public enum typeMsger
    {
        None = 0,
        Sys = 1,
        wx = 10,
        wxmp = 11
    }

    /// <summary>消息接口
    /// </summary>
    public interface IMsger
    {
        /// <summary>消息类型
        /// </summary>
        typeMsger TypeMsg { get; }
        /// <summary>标识
        /// </summary>
        string Tag { get; }
        /// <summary>是否缓存消息
        /// </summary>
        bool IsBuffer { get; }
        /// <summary>缓存消息数量
        /// </summary>
        int NumsBuffer { get; }
        /// <summary>数据缓存集管理类
        /// </summary>
        List<IMsg> MsgsBuffer { get; }


        /// <summary>消息发送(但一发送，单条单目标)
        /// </summary>
        /// <param name="msg">消息内容(建议格式：new { XX1 = 0, XX2 = aa })</param>
        /// <returns></returns>
        bool SendMsg(dynamic msg);
        /// <summary>消息发送(但一发送，单条单目标)
        /// </summary>
        /// <param name="msg">消息内容(建议格式：new { XX1 = 0, XX2 = aa })</param>
        /// <param name="url">接口地址</param>
        /// <returns></returns>
        bool SendMsg(dynamic msg, string url);
        /// <summary>消息日志记录
        /// </summary>
        /// <param name="msg">消息内容(建议格式：new { XX1 = 0, XX2 = aa })</param>
        /// <returns></returns>
        bool LogMsg(dynamic msg);
    }
}