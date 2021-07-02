using System;
using System.Collections.Generic;
using System.Linq;

namespace zxcCore.zxcData.Cache.Memory
{
    /// <summary>数据检查-泛型
    /// </summary>
    public abstract class DataCheck<T> : IDataCheck<T>
    {
        #region 属性及构造

        protected internal string _tagAlias = "";
        protected internal string _tag = "";
        public string Tag
        {
            get { return _tag; }
        }

        protected internal IDataCache<T> _DataCache_T = null;
        protected internal IDataCache _DataCache = null;
        public IDataCache DataCache
        {
            get { return _DataCache; }
        }
        protected internal IDataCaches _DataCaches = null;
        public IDataCaches DataCaches
        {
            get { return _DataCaches; }
        }
        protected internal IDataCaches_Manage _DataCaches_Manage = null;
        public IDataCaches_Manage DataCaches_Manage
        {
            get { return _DataCaches_Manage; }
        }
        protected internal IDataCheck_Msger _Msger = null;
        public IDataCheck_Msger Msger
        {
            get { return _Msger; }
        }


        public DataCheck(string tagName, IDataCache<T> dataCache = null, IDataCheck_Msger msger = null)
        {
            _tag = tagName;
            _Msger = msger;
            _DataCache_T = dataCache;
            _DataCache = _DataCache_T;
        }
        ~DataCheck()
        {
            // 缓存数据？
        }

        #endregion


        public virtual bool InitSetting(dynamic setting)
        {
            return true;
        }

        public virtual bool InitDataCaches_Manage(IDataCaches_Manage dataCaches_Manage)
        {
            _DataCaches_Manage = dataCaches_Manage;
            return true;
        }
        public virtual bool InitDataCaches(IDataCaches dataCaches)
        {
            _DataCaches = dataCaches;
            return true;
        }
        public virtual bool InitDataCache(IDataCache dataCache)
        {
            _DataCache = dataCache;
            return true;
        }
        public virtual bool InitDataCheck_Msger(IDataCheck_Msger msger)
        {
            _Msger = msger;
            return true;
        }


        public virtual bool CheckData()
        {
            return true;
        }
        public virtual bool CheckData(DateTime dtTime, T data, IDataCache<T> dataCache = null)
        {
            return true;
        }
        public virtual bool CheckData(DateTime dtTime, T data, IDataCaches dataCaches = null)
        {
            return true;
        }
        public virtual bool CheckData(DateTime dtTime, T data, IDataCaches_Manage dataCaches_Manage = null)
        {
            return true;
        }


        //消息通知
        public virtual bool NotifyMsg(dynamic msg, string userID_To)
        {
            if (this.Msger != null)
            {
                this.Msger.NotifyMsg(msg);
            }
            return true;
        }

    }
}
