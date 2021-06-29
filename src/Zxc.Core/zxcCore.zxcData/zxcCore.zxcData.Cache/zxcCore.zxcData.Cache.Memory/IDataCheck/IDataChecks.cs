using System;
using System.Collections.Generic;

namespace zxcCore.zxcData.Cache.Memory
{
    /// <summary>数据检查集-基类
    /// </summary>
    public interface IDataChecks
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
        /// <summary>父数据检查对象
        /// </summary>
        IDataChecks Parent { get; }
        /// <summary>消息管理（统一）
        /// </summary>
        IDataCheck_Msger Msger { get; }
        /// <summary>数据检查对象集
        /// </summary>
        Dictionary<string, IDataCheck> DataCheckss { get; }


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
        /// <summary>初始因子缓存数据
        /// </summary>
        /// <param name="dataCache">因子缓存数据对象</param>
        /// <returns></returns>
        bool InitDataCache(IDataCache dataCache);
        /// <summary>初始父级数据检查集
        /// </summary>
        /// <param name="parent"></param>
        /// <returns></returns>
        bool InitDataChecks(IDataChecks parent);


        /// <summary>初始数据检查对象
        /// </summary>
        /// <typeparam name="T"></typeparam>
        /// <param name="tagName">数据检查对象标识</param>
        /// <param name="poCheck">数据检查对象</param>
        /// <param name="isCanCover">是否允许覆盖已经存在的检查对象</param>
        /// <returns></returns>
        bool InitDataCheck<T>(string tagName, IDataCheck<T> poCheck, bool isCanCover = false);
        /// <summary>提取缓存数据检查对象
        /// </summary>
        /// <typeparam name="T"></typeparam>
        /// <param name="tagName">数据检查对象标识</param>
        /// <returns></returns>
        IDataCheck<T> GetDataCheck<T>(string tagName);


        /// <summary>缓存数据检查接口
        /// </summary>
        bool CheckDatas();
        /// <summary>缓存数据检查接口
        /// </summary>
        /// <param name="dtTime">数据时间</param>
        /// <param name="data">数据缓存对象</param>
        /// <returns></returns>
        bool CheckDatas<T>(DateTime dtTime, T data, IDataCache<T> dataCache);
        /// <summary>缓存数据检查接口
        /// </summary>
        /// <param name="dtTime">数据时间</param>
        /// <param name="data">数据缓存对象集</param>
        /// <returns></returns>
        bool CheckDatas<T>(DateTime dtTime, T data, IDataCaches dataCaches);
        /// <summary>缓存数据检查接口
        /// </summary>
        /// <param name="dtTime">数据时间</param>
        /// <param name="data">数据缓存对象集</param>
        /// <returns></returns>
        bool CheckDatas<T>(DateTime dtTime, T data, IDataCaches_Manage dataCaches_Manage);


        /// <summary>通知消息处理(统一出口)
        /// </summary>
        /// <param name="消息内容(建议格式：new { XX1 = 0, XX2 = aa })"></param>
        /// <returns></returns>
        bool NotifyMsg(dynamic msg);
    }
}
