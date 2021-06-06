using System;
using System.Collections.Generic;
using System.Linq;

namespace zpCore.zpDataCache.Memory
{
    /// <summary>数据集检查
    /// </summary>
    public abstract class DataChecks : IDataChecks
    {
        #region 属性及构造

        protected internal string _tag = "";
        public string Tag
        {
            get { return _tag; }
        }

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

        protected internal IDataChecks _Parent = null;
        public IDataChecks Parent
        {
            get { return _Parent; }
        }


        protected internal Dictionary<string, IDataCheck> _DataChecks = null;
        public Dictionary<string, IDataCheck> DataCheckss
        {
            get { return _DataChecks; }
        }


        public DataChecks(string tagName, IDataCaches_Manage dataCaches_Manage, IDataChecks parent = null, IDataCheck_Msger msger = null)
        {
            _tag = tagName;
            _Msger = msger;
            _Parent = parent;
            _DataCaches_Manage = dataCaches_Manage;
            _DataChecks = new Dictionary<string, IDataCheck>();
        }
        public DataChecks(string tagName, IDataCaches dataCaches, IDataChecks parent = null, IDataCheck_Msger msger = null)
        {
            _tag = tagName;
            _Msger = msger;
            _Parent = parent;
            _DataCaches = dataCaches;
            _DataChecks = new Dictionary<string, IDataCheck>();
        }
        public DataChecks(string tagName, IDataCache dataCache, IDataChecks parent = null, IDataCheck_Msger msger = null)
        {
            _tag = tagName;
            _Msger = msger;
            _Parent = parent;
            _DataCache = dataCache;
            _DataChecks = new Dictionary<string, IDataCheck>();
        }
        ~DataChecks()
        {
            // 缓存数据？
            _DataChecks.Clear();
        }

        #endregion

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
        public virtual bool InitDataChecks(IDataChecks parent)
        {
            _Parent = parent;
            return true;
        }


        public virtual bool InitDataCheck<T>(string tagName, IDataCheck<T> poCheck, bool isCanCover = false)
        {
            bool bResult = false;
            if (isCanCover)
            {
                _DataChecks[tagName] = poCheck; bResult = true;
            }
            else
            {
                //不存在时添加
                if (!_DataChecks.ContainsKey(tagName))
                {
                    _DataChecks.Add(tagName, poCheck); bResult = true;
                }
            }
            if (bResult)
            {
                if (poCheck.Msger == null)
                    bResult = poCheck.InitDataCheck_Msger(this.Msger);
            }
            return bResult;
        }
        public virtual IDataCheck<T> GetDataCheck<T>(string tagName)
        {
            IDataCheck dataCheck = null;
            if (_DataChecks.TryGetValue(tagName, out dataCheck))
            {
                //What ever you gonna do next...
            }
            return (IDataCheck<T>)dataCheck;
        }


        public virtual bool CheckDatas()
        {
            bool bResult = true;
            foreach (KeyValuePair<string, IDataCheck> check in _DataChecks)
            {
                bResult = check.Value.CheckData() && bResult;
            }
            return bResult;
        }
        public virtual bool CheckDatas<T>(DateTime dtTime, T data, IDataCache<T> dataCache)
        {
            bool bResult = true;
            foreach (KeyValuePair<string, IDataCheck> check in _DataChecks)
            {
                IDataCheck<T> dataCheck = (IDataCheck<T>)check.Value;
                bResult = dataCheck.CheckData(dtTime, data, dataCache) && bResult;
            }
            return bResult;
        }
        public virtual bool CheckDatas<T>(DateTime dtTime, T data, IDataCaches dataCaches)
        {
            bool bResult = true;
            foreach (KeyValuePair<string, IDataCheck> check in _DataChecks)
            {
                IDataCheck<T> dataCheck = (IDataCheck<T>)check.Value;
                bResult = dataCheck.CheckData(dtTime, data, dataCaches) && bResult;
            }
            return bResult;
        }
        public virtual bool CheckDatas<T>(DateTime dtTime, T data, IDataCaches_Manage dataCaches_Manage)
        {
            bool bResult = true;
            foreach (KeyValuePair<string, IDataCheck> check in _DataChecks)
            {
                IDataCheck<T> dataCheck = (IDataCheck<T>)check.Value;
                bResult = dataCheck.CheckData(dtTime, data, dataCaches_Manage) && bResult;
            }
            return bResult;
        }


        public virtual bool NotifyMsg(dynamic msg)
        {
            if (this.Msger != null)
            {
                this.NotifyMsg(msg);
            }
            return true;
        }
    }
}
