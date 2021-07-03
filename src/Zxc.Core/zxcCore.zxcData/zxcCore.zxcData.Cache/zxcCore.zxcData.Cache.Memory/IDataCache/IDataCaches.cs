using System;
using System.Collections.Generic;
using zxcCore.Enums;

namespace zxcCore.zxcData.Cache.Memory
{
    /// <summary>数据缓存集
    /// </summary>
    public interface IDataCaches
    {
        /// <summary>唯一因子编码-自定义，便于快速遍历
        /// </summary>
        string ID { get; }
        /// <summary>数据缓存管理类
        /// </summary>
        IDataCache_Set DataCache_Set { get; }

        /// <summary>数据缓存
        /// </summary>
        Dictionary<string, IDataCache> DataCachess { get; }

        /// <summary>按标识初始缓存数据对象
        /// </summary>
        /// <typeparam name="T"></typeparam>
        /// <param name="tagName">标识</param>
        /// <param name="typeTimeFrequency">时间频率</param>
        /// <param name="cacheNums">缓存数据数量</param>
        /// <returns></returns>
        bool InitDataCache<T>(string tagName, typeTimeFrequency typeTimeFrequency, int cacheNums);
        /// <summary>按标识提取缓存数据对象
        /// </summary>
        /// <typeparam name="T"></typeparam>
        /// <param name="tagName">标识</param>
        /// <param name="typeTimeFrequency">时间频率</param>
        /// <param name="autoInit">不存在时是否自定初始</param>
        /// <param name="cacheNums">缓存数据数量，autoInit为false时无效</param>
        /// <returns></returns>
        IDataCache<T> GetDataCache<T>(string tagName, typeTimeFrequency typeTimeFrequency = typeTimeFrequency.none, bool autoInit = false, int cacheNums = 1);
        /// <summary>提取标识，统一标识格式
        /// </summary>
        /// <param name="typeTimeFrequency">时间频率</param>
        /// <param name="strTag">自定义标识，参与统一标识组装</param>
        /// <returns></returns>
        string GetTagName(typeTimeFrequency typeTimeFrequency, string strTag = "");


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
        bool CheckData<T>(DateTime dtTime, T data, IDataCache<T> dataCache = null);


        //List<typeTimeFrequency> GetTimeFrequencys();
        //IDatas_Iot<T> GetDatas(typeTimeFrequency dataType);
    }
}
