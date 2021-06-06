using System;
using System.Collections.Generic;

namespace zpCore.zpDataCache.Memory
{
    /// <summary>数据缓存-基类
    /// </summary>
    public interface IDataCache
    {
        /// <summary>唯一因子编码-自定义，便于快速遍历
        /// </summary>
        string ID { get; }
        /// <summary>因子缓存数据设置对象
        /// </summary>
        IDataCache_Set DataCache_Set { get; }
        ///// <summary>数据缓存集
        ///// </summary>
        ////List<T> DataCaches { get; }
        ////Dictionary<DateTime, IData<T>> DataCaches { get; }


        /// <summary>初始数据检查集
        /// </summary>
        /// <param name="poChecks">数据检查集对象</param>
        /// <returns></returns>
        bool InitDataChecks(IDataChecks poChecks);
        /// <summary>初始数据检查对象
        /// </summary>
        /// <param name="dataCheck">数据检查对象</param>
        /// <returns></returns>
        bool InitDataCheck(string tagName, IDataCheck dataCheck, bool isCanCover = false);

        /// <summary>缓存数据检查接口
        /// </summary>
        bool CheckData();
    }

    /// <summary>数据缓存
    /// </summary>
    public interface IDataCache<T> : IDataCache
    {
        /// <summary>数据检查集
        /// </summary>
        IDataChecks DataChecks { get; }

        /// <summary>按指定时间初始缓存数据
        /// </summary>
        /// <param name="dtData"></param>
        /// <returns></returns>
        int Init(DateTime dtData);
        /// <summary>初始数据(加载后的缓存数据统一初始，不参与判断等处理)
        /// </summary>
        /// <param name="datas"></param>
        /// <returns></returns>
        int InitDatas(Dictionary<DateTime, T> datas);
        /// <summary>按时间标识设置数据
        /// </summary>
        /// <param name="dtTime"></param>
        /// <param name="data"></param>
        /// <returns></returns>
        bool SetData(DateTime dtTime, T data);
        //bool SetData(DateTime dtData, T value);
        /// <summary>设置最后数据缓存时间
        /// </summary>
        /// <param name="dtLast"></param>
        /// <returns></returns>
        bool SetLastTime(DateTime dtLast);


        /// <summary>提取缓存数据
        /// </summary>
        /// <param name="dtData"></param>
        /// <returns></returns>
        T GetData(DateTime dtData);
        /// <summary>按数据长度提取缓存数据集
        /// </summary>
        /// <param name="dtStart"></param>
        /// <param name="dtEnd"></param>
        /// <returns></returns>
        List<T> GetDatas(DateTime dtStart, DateTime dtEnd);


        /// <summary>缓存数据检查接口
        /// </summary>
        /// <param name="dtTime">数据时间</param>
        /// <param name="data">数据</param>
        /// <returns></returns>
        bool CheckData(DateTime dtTime, T data);
    }
}
