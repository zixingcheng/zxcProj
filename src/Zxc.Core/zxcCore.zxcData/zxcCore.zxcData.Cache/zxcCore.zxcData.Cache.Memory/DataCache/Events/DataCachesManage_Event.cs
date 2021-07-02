using System;
using System.Collections.Generic;

namespace zxcCore.zxcData.Cache.Memory
{
    ///// <summary>数据缓存集管理类初始装载事件
    ///// </summary>
    //public delegate void DataCachesManageLoad_EventHandler(object sender, DataCachesManage_Event e);
    /// <summary>数据缓存集管理类检查对象初始事件
    /// </summary>
    public delegate void DataCachesManageChecksInitial_EventHandler(object sender, DataCachesManage_Event e);
    ///// <summary>数据缓存集管理类变动事件
    ///// </summary>
    //public delegate void DataCachesManageChange_EventHandler(object sender, DataCachesManage_Event e);


    /// <summary数据缓存集通用事件对象
    /// </summary>
    public class DataCachesManage_Event : EventArgs
    {
        #region 属性及构造

        /// <summary>数据缓存集管理类
        /// </summary>
        protected internal DataCaches_Manage _dataCaches_Manage = null;
        public DataCaches_Manage DataCaches_Manage
        {
            get { return _dataCaches_Manage; }
        }


        public DataCachesManage_Event(DataCaches_Manage dataCaches_Manage)
        {
            _dataCaches_Manage = dataCaches_Manage;
        }
        ~DataCachesManage_Event()
        {
            // 缓存数据？
        }

        #endregion
    }

}