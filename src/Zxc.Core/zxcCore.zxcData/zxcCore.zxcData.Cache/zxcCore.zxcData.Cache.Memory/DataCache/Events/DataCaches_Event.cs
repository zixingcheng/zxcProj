using System;
using System.Collections.Generic;

namespace zxcCore.zxcData.Cache.Memory
{
    ///// <summary>缓存数据集初始装载事件
    ///// </summary>
    //public delegate void DataCachesLoad_EventHandler(object sender, DataCaches_Event e);
    /// <summary>缓存数据集检查对象初始事件
    /// </summary>
    public delegate void DataCachesChecksInitial_EventHandler(object sender, DataCaches_Event e);
    ///// <summary>缓存数据集变动事件
    ///// </summary>
    //public delegate void DataCachesChange_EventHandler(object sender, DataCaches_Event e);


    /// <summary数据缓存集通用事件对象
    /// </summary>
    public class DataCaches_Event : EventArgs
    {
        #region 属性及构造

        /// <summary>缓存数据信息
        /// </summary>
        protected internal DataCaches _dataCaches = null;
        public DataCaches DataCaches
        {
            get { return _dataCaches; }
        }


        public DataCaches_Event(DataCaches dataCaches)
        {
            _dataCaches = dataCaches;
        }
        ~DataCaches_Event()
        {
            // 缓存数据？
        }

        #endregion
    }

}