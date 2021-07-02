using System;
using System.Collections.Generic;

namespace zxcCore.zxcData.Cache.Memory
{
    /// <summary>缓存数据初始装载事件
    /// </summary>
    public delegate void DataCacheLoad_EventHandler(object sender, DataCache_Event e);
    /// <summary>缓存数据检查对象初始事件
    /// </summary>
    public delegate void DataCacheChecksInitial_EventHandler(object sender, DataCache_Event e);
    /// <summary>缓存数据变动事件
    /// </summary>
    public delegate void DataCacheChange_EventHandler(object sender, DataCache_Event e);


    /// <summary缓存数据通用事件对象
    /// </summary>
    public class DataCache_Event : EventArgs
    {
        #region 属性及构造

        /// <summary>缓存数据信息
        /// </summary>
        protected internal IDataCache _dataCache = null;
        public IDataCache DataCache
        {
            get { return _dataCache; }
        }

        /// <summary>缓存数据信息
        /// </summary>
        protected internal CacheInfo _cacheInfo = null;
        public CacheInfo CacheInfo
        {
            get { return _cacheInfo; }
        }

        public DataCache_Event(IDataCache dataCache, CacheInfo cacheInfo = null)
        {
            _dataCache = dataCache;
            _cacheInfo = cacheInfo;
        }
        ~DataCache_Event()
        {
            // 缓存数据？
        }

        #endregion
    }

}