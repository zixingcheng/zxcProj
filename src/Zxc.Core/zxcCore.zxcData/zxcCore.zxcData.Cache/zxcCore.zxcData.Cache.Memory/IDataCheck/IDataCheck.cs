using System;
using System.Collections.Generic;

namespace zxcCore.zxcData.Cache.Memory
{
    /// <summary>数据检查-基类
    /// </summary>
    public interface IDataCheck
    {
        /// <summary>标识名称
        /// </summary>
        string Tag { get; }
        /// <summary>数据缓存集管理类
        /// </summary>
        IDataCaches_Manage DataCaches_Manage { get; }
        /// <summary>因子缓存数据集
        /// </summary>
        IDataCaches DataCaches { get; }
        /// <summary>因子缓存数据
        /// </summary>
        IDataCache DataCache { get; }
        /// <summary>消息管理（统一）
        /// </summary>
        IDataCheck_Msger Msger { get; }

        /// <summary>初始设置
        /// </summary>
        /// <param name="setting"></param>
        /// <returns></returns>
        bool InitSetting(dynamic setting);

        /// <summary>初始数据缓存集管理类
        /// </summary>
        /// <param name="dataCaches_Manage"></param>
        /// <returns></returns>
        bool InitDataCaches_Manage(IDataCaches_Manage dataCaches_Manage);
        /// <summary>初始因子缓存数据集
        /// </summary>
        /// <param name="poChecks">因子缓存数据集</param>
        /// <returns></returns>
        bool InitDataCaches(IDataCaches dataCaches);
        /// <summary>初始因子缓存数据集
        /// </summary>
        /// <param name="dataCache">因子缓存数据集对象</param>
        /// <returns></returns>
        bool InitDataCache(IDataCache dataCache);
        /// <summary>初始消息管理 
        /// </summary>
        /// <param name="dataCache">消息管理 对象</param>
        /// <returns></returns>
        bool InitDataCheck_Msger(IDataCheck_Msger msger);
        /// <summary>缓存数据检查接口
        /// </summary>
        bool CheckData();

        /// <summary>通知消息处理(统一出口)
        /// </summary>
        /// <param name="消息内容(建议格式：new { XX1 = 0, XX2 = aa })"></param>
        /// <returns></returns>
        bool NotifyMsg(dynamic msg, string userID_To);
    }

    /// <summary>数据检查-泛型
    /// </summary>
    public interface IDataCheck<T> : IDataCheck
    {
        /// <summary>缓存数据检查接口
        /// </summary>
        /// <param name="dtTime">数据时间</param>
        /// <param name="data">数据</param>
        /// <returns></returns>
        bool CheckData(DateTime dtTime, T data, IDataCache<T> dataCache = null);
        /// <summary>缓存数据检查接口
        /// </summary>
        /// <param name="dtTime">数据时间</param>
        /// <param name="data">数据</param>
        /// <returns></returns>
        bool CheckData(DateTime dtTime, T data, IDataCaches dataCaches = null);
        /// <summary>缓存数据检查接口
        /// </summary>
        /// <param name="dtTime">数据时间</param>
        /// <param name="data">数据</param>
        /// <returns></returns>
        bool CheckData(DateTime dtTime, T data, IDataCaches_Manage dataCaches_Manage = null);
    }
}
