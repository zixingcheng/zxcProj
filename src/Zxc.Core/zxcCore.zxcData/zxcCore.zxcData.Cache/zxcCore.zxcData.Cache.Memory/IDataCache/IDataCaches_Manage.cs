using System;
using System.Collections.Generic;

namespace zxcCore.zxcData.Cache.Memory
{
    /// <summary>数据缓存集管理类
    /// </summary>
    public interface IDataCaches_Manage
    {
        /// <summary>标识
        /// </summary>
        string Tag { get; }
        /// <summary>数据缓存管理类
        /// </summary>
        IDataCache_Set DataCache_Set { get; }
        /// <summary>因子集合信息
        /// </summary>
        IData_Factors Data_Factors { get; }

        /// <summary>数据管理对象--缓存数据集统一处理
        /// </summary>
        Dictionary<string, IDataCaches> DataCaches { get; }

        /// <summary>按因子对象初始因子数据缓存集
        /// </summary>
        /// <param name="infoFactor">因子对象</param>
        /// <returns></returns>
        bool InitDataCaches(IData_Factor infoFactor);
        /// <summary>按因子对象初始因子数据缓存对象
        /// 
        /// </summary>
        /// <typeparam name="T"></typeparam>
        /// <param name="infoFactor">因子对象</param>
        /// <param name="tagName">标识</param>
        /// <param name="typeTimeFrequency">数据频率</param>
        /// <param name="cacheNums">缓存数据数量</param>
        /// <returns></returns>
        bool InitDataCache<T>(IData_Factor infoFactor, string tagName, typeTimeFrequency typeTimeFrequency, int cacheNums);

        /// <summary>按因子提取因子数据缓存集
        /// </summary>
        /// <param name="infoFactor">因子对象</param>
        /// <param name="autoInit">是否自动初始，缓存不存在时</param>
        /// <returns></returns>
        IDataCaches GetDataCaches(IData_Factor infoFactor, bool autoInit = false);
        /// <summary>按因子对象提取缓存数据对象
        /// </summary>
        /// <typeparam name="T"></typeparam>
        /// <param name="infoFactor">因子对象</param>
        /// <param name="strTag">自定义标识</param>
        /// <param name="typeTimeFrequency">时间频率</param>
        /// <param name="autoInit">不存在时是否自定初始</param>
        /// <param name="cacheNums">缓存数据数量，autoInit为false时无效</param>
        /// <returns></returns>
        IDataCache<T> GetDataCache<T>(IData_Factor infoFactor, string strTag = "", typeTimeFrequency typeTimeFrequency = typeTimeFrequency.None, bool autoInit = false, int cacheNums = 1);

        /// <summary>按因子对象设置缓存数据
        /// </summary>
        /// <typeparam name="T"></typeparam>
        /// <param name="infoFactor">因子对象</param>
        /// <param name="strTag">自定义标识</param>
        /// <param name="dtTime">时间</param>
        /// <param name="data">数据</param>
        /// <param name="typeTimeFrequency">时间频率</param>
        /// <returns></returns>
        bool SetData<T>(IData_Factor infoFactor, string strTag, DateTime dtTime, T data, typeTimeFrequency typeTimeFrequency = typeTimeFrequency.None);
        /// <summary>按因子对象提取缓存数据
        /// </summary>
        /// <typeparam name="T"></typeparam>
        /// <param name="infoFactor">因子对象</param>
        /// <param name="strTag">自定义标识</param>
        /// <param name="dtTime">时间</param>
        /// <param name="typeTimeFrequency">时间频率</param>
        /// <returns></returns>
        T GetData<T>(IData_Factor infoFactor, string strTag, DateTime dtTime, typeTimeFrequency typeTimeFrequency = typeTimeFrequency.None);


        /// <summary>初始数据检查集
        /// </summary>
        /// <param name="poChecks">数据检查集对象</param>
        /// <returns></returns>
        bool InitDataChecks(IDataChecks poChecks);
        /// <summary>初始数据检查对象
        /// </summary>
        /// <param name="dataCheck">数据检查对象</param>
        /// <returns></returns>
        bool InitDataCheck<T>(string tagName, IDataCheck<T> dataCheck, bool isCanCover = false);

        /// <summary>缓存数据检查接口
        /// </summary>
        bool CheckData();
        /// <summary>缓存数据检查接口
        /// </summary>
        /// <param name="dtTime">数据时间</param>
        /// <param name="data">数据</param>
        /// <returns></returns>
        bool CheckData<T>(DateTime dtTime, T data, IDataCaches dataCaches = null);
    }
}
