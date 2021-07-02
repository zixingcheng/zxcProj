using System;
using System.Collections.Generic;

namespace zxcCore.zxcData.Cache.Memory
{
    /// <summary>数据缓存集管理类
    /// </summary>
    public class DataCaches_Manage : IDataCaches_Manage
    {
        #region 属性及构造

        /// <summary>缓存数据检查对象初始事件
        /// </summary>
        public event DataCachesManageChecksInitial_EventHandler DataChecks_Initial;


        public string Tag { get; }

        /// <summary>因子缓存数据设置对象
        /// </summary>
        IDataCache_Set _DataCache_Set = null;
        public IDataCache_Set DataCache_Set
        {
            get { return _DataCache_Set; }
        }

        IData_Factors _Data_Factors = null;
        public IData_Factors Data_Factors
        {
            get { return _Data_Factors; }
        }

        /// <summary>数据检查集
        /// </summary>
        protected internal IDataChecks _DataChecks = null;
        public IDataChecks DataChecks
        {
            get { return _DataChecks; }
        }

        /// <summary>因子缓存数据设置对象
        /// </summary>
        Dictionary<string, IDataCaches> _DataCaches = null;
        public Dictionary<string, IDataCaches> DataCaches
        {
            get { return _DataCaches; }
        }

        /// <summary>
        /// </summary>
        /// <param name="dtBase">基时间</param>
        public DataCaches_Manage(IData_Factors info_Factors, IDataCache_Set srcDataCache_Set, IDataChecks dataChecks = null)
        {
            Tag = info_Factors.ID;
            _DataCache_Set = new DataCache_Set(Tag, srcDataCache_Set.Time_Base, typeTimeFrequency.None, 0, info_Factors, srcDataCache_Set);
            _DataChecks = dataChecks;
            _DataCaches = new Dictionary<string, IDataCaches>();
        }
        ~DataCaches_Manage()
        {
            // 缓存数据？

            // 清理数据
            this._DataCaches.Clear();
        }

        #endregion


        // 初始单个
        public bool InitDataCaches(IData_Factor infoFactor)
        {
            if (this.GetDataCaches(infoFactor) == null)
            {
                DataCaches data = new DataCaches(infoFactor, _DataCache_Set);
                _DataCaches[data.ID] = data;
                return true;
            }
            return true;
        }
        public bool InitDataCache<T>(IData_Factor infoFactor, string tagName, typeTimeFrequency typeTimeFrequency, int cacheNums)
        {
            IDataCaches dataCaches = this.GetDataCaches(infoFactor);
            if (dataCaches == null)
            {
                if (InitDataCaches(infoFactor))
                {
                    dataCaches = this.GetDataCaches(infoFactor);
                    if (dataCaches == null) return false;
                }
            }
            return dataCaches.InitDataCache<T>(tagName, typeTimeFrequency, cacheNums);
        }


        public IDataCaches GetDataCaches(IData_Factor infoFactor, bool autoInit = false)
        {
            IDataCaches dataCaches = null;
            if (_DataCaches.TryGetValue(infoFactor.ID, out dataCaches))
            {
                //What ever you gonna do next...
            }
            if (autoInit && dataCaches == null)
            {
                if (InitDataCaches(infoFactor))
                    return GetDataCaches(infoFactor);
            }
            return dataCaches;
        }
        public IDataCache<T> GetDataCache<T>(IData_Factor infoFactor, string strTag = "", typeTimeFrequency typeTimeFrequency = typeTimeFrequency.None, bool autoInit = false, int cacheNums = 1)
        {
            IDataCaches dataCaches = GetDataCaches(infoFactor, autoInit);
            if (dataCaches == null) return null;

            IDataCache<T> data = dataCaches.GetDataCache<T>(strTag, typeTimeFrequency, autoInit, cacheNums);
            return data;
        }


        public bool SetData<T>(IData_Factor infoFactor, string strTag, DateTime dtTime, T data, typeTimeFrequency typeTimeFrequency = typeTimeFrequency.None)
        {
            IDataCache<T> dataCache = GetDataCache<T>(infoFactor, strTag, typeTimeFrequency);
            if (dataCache == null) return false;

            return dataCache.SetData(dtTime, data);
        }
        public T GetData<T>(IData_Factor infoFactor, string strTag, DateTime dtTime, typeTimeFrequency typeTimeFrequency = typeTimeFrequency.None)
        {
            IDataCache<T> dataCache = GetDataCache<T>(infoFactor, strTag, typeTimeFrequency);
            if (dataCache == null) return default(T);

            return dataCache.GetData(dtTime);
        }


        public bool InitDataChecks(IDataChecks poChecks)
        {
            this._DataChecks = poChecks;
            if (this._DataChecks.DataCaches_Manage == null)
                this._DataChecks.InitDataCaches_Manage(this);
            return true;
        }
        public bool InitDataCheck<T>(string tagName, IDataCheck<T> dataCheck, bool isCanCover = false)
        {
            if (_DataChecks != null)
            {
                _DataChecks.InitDataCheck<T>(tagName, (IDataCheck<T>)dataCheck, isCanCover);
            }
            return true;
        }


        public bool CheckData()
        {
            //以检查集的方式统一管理--观察者模式
            if (_DataChecks != null)
                return _DataChecks.CheckDatas();
            return true;
        }
        public bool CheckData<T>(DateTime dtTime, T data, IDataCaches dataCaches = null)
        {
            //以检查集的方式统一管理--观察者模式
            if (_DataChecks != null)
            {
                bool bResult = _DataChecks.CheckDatas(dtTime, data, dataCaches);
                if (bResult && this._DataChecks.Parent != null)
                {
                    if (this._DataChecks.Parent.DataCaches_Manage != null)
                    {
                        //向上递归终止，暂不需要实现最顶层的DataCheck
                        //bResult = this._DataChecks.Parent.DataCaches_Manager.CheckData<T>(dtTime, data, this);
                    }
                }
                return bResult;
            }
            return true;
        }


        //缓存数据检查对象初始事件--便于外部统一设置检查对象
        public bool Event_DataChecks_Initial()
        {
            if (this.DataChecks_Initial != null)
            {
                DataCachesManage_Event pArgs = new DataCachesManage_Event(this); 
                try
                {
                    this.DataChecks_Initial(null, pArgs);
                }
                catch (Exception)
                {
                    throw;
                }
            }
            return true;
        }

    }
}
