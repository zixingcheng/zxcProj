using System;
using System.Collections.Generic;

namespace zxcCore.zxcData.Cache.Memory
{
    /// <summary>数据缓存集管理类集中管理类
    /// </summary>
    public class DataCaches_Manager
    {
        #region 属性及构造

        /// <summary>缓存数据初始装载事件
        /// </summary>
        public event DataCacheLoad_EventHandler DataCache_Load;
        /// <summary>缓存数据检查对象初始事件
        /// </summary>
        public event DataCacheChecksInitial_EventHandler DataCacheChecks_Initial;
        /// <summary>缓存数据变动事件
        /// </summary>
        public event DataCacheChange_EventHandler DataCache_Change;
        /// <summary>缓存数据集检查对象初始事件
        /// </summary>
        public event DataCachesChecksInitial_EventHandler DataCachesChecks_Initial;
        /// <summary>缓存数据集管理对象检查对象初始事件
        /// </summary>
        public event DataCachesManageChecksInitial_EventHandler DataCachesManageChecks_Initial;


        /// <summary>因子缓存数据设置对象-主要用于统一信息
        /// </summary>
        IDataCache_Set _DataCache_Set = null;
        public IDataCache_Set DataCache_Set
        {
            get { return _DataCache_Set; }
        }

        /// <summary>因子集缓存字典
        /// </summary>
        Dictionary<string, IData_Factors> _Data_Factorss = null;
        public Dictionary<string, IData_Factors> Data_Factorss
        {
            get { return _Data_Factorss; }
        }

        /// <summary>数据缓存集管理类字典
        /// </summary>
        Dictionary<string, IDataCaches_Manage> _DataCaches_Manages = null;
        public Dictionary<string, IDataCaches_Manage> DataCaches_Manages
        {
            get { return _DataCaches_Manages; }
        }

        bool _isInited = false;
        /// <summary>
        /// </summary>
        /// <param name="dtBase">基时间</param>
        public DataCaches_Manager()
        {
            _Data_Factorss = new Dictionary<string, IData_Factors>();
            _DataCaches_Manages = new Dictionary<string, IDataCaches_Manage>();
        }
        ~DataCaches_Manager()
        {
            // 缓存数据？

            // 清理数据
            this._Data_Factorss.Clear();
            this.DataCaches_Manages.Clear();
        }

        #endregion


        /// <summary>初始全局缓存
        /// </summary>
        /// <param name="dtBase">基时间</param>
        /// <returns></returns>
        public bool Init(DateTime dtBase)
        {
            this._Data_Factorss.Clear();
            this._DataCaches_Manages.Clear();

            //初始顶层 DataCache_Set，主要用于时间信息同步
            _DataCache_Set = new DataCache_Set("DataCaches_Manager", dtBase, typeTimeFrequency.None, -1, null);
            _isInited = true;
            return _isInited;
        }
        // 初始单个数据缓存集管理类（集中管理，如数采仪为一个集中管理类）
        public bool InitDataCaches_Manage(IData_Factors infoFactors, bool useEvent = false)
        {
            if (_isInited == false) return false;
            if (this.GetDataCaches_Manage(infoFactors) == null)
            {
                DataCaches_Manage dataManage = new DataCaches_Manage(infoFactors, _DataCache_Set);
                _DataCaches_Manages[dataManage.Tag] = dataManage;

                //注册检查集初始事件
                if (useEvent)
                {
                    dataManage.DataChecks_Initial += new DataCachesManageChecksInitial_EventHandler(EventHandler_DataCachesManageChecksInitial);
                    dataManage.Event_DataChecks_Initial();
                }
                return true;
            }
            return true;
        }
        // 按因子对象初始因子数据缓存集
        public bool InitDataCaches(IData_Factors infoFactors, IData_Factor infoFactor, bool useEvent = false)
        {
            if (_isInited == false) return false;
            IDataCaches_Manage dataManage = this.GetDataCaches_Manage(infoFactors);
            if (dataManage == null) return false;

            if (dataManage.GetDataCaches(infoFactor, false) == null)
            {
                DataCaches dataCaches = (DataCaches)dataManage.GetDataCaches(infoFactor, true);

                //注册检查集初始事件
                if (useEvent)
                {
                    dataCaches.DataChecks_Initial += new DataCachesChecksInitial_EventHandler(EventHandler_DataCachesChecksInitial);
                    dataCaches.Event_DataChecks_Initial();
                }
                return this._IndexFactors(infoFactors, infoFactor);
            }
            return true;
        }
        /// <summary>按因子对象初始因子数据缓存对象
        /// 
        /// </summary>
        /// <typeparam name="T"></typeparam>
        /// <param name="infoFactors">因子对象集</param>
        /// <param name="infoFactor">因子对象</param>
        /// <param name="tagName">标识</param>
        /// <param name="typeTimeFrequency">数据频率</param>
        /// <param name="cacheNums">缓存数据数量</param>
        /// <returns></returns>
        public bool InitDataCache<T>(IData_Factors infoFactors, IData_Factor infoFactor, string tagName, typeTimeFrequency typeTimeFrequency, int cacheNums, bool useEvent = false)
        {
            if (_isInited == false) return false;
            DataCaches dataCaches = (DataCaches)this.GetDataCaches(infoFactors, infoFactor);
            if (dataCaches == null) return false;

            if (dataCaches.GetDataCache<T>(tagName, typeTimeFrequency) == null)
            {
                DataCache<T> dataCache = (DataCache<T>)dataCaches.GetDataCache<T>(tagName, typeTimeFrequency, true, cacheNums);

                //注册事件
                if (useEvent)
                {
                    dataCache.DataCache_Load += new DataCacheLoad_EventHandler(EventHandler_DataCacheLoad);
                    dataCache.DataChecks_Initial += new DataCacheChecksInitial_EventHandler(EventHandler_DataCacheChecksInitial);
                    dataCache.DataCache_Change += new DataCacheChange_EventHandler(EventHandler_DataCacheChange);
                    dataCache.Event_DataCache_Load();
                    dataCache.Event_DataChecks_Initial();
                }
                return this._IndexFactors(infoFactors, infoFactor);
            }
            return true;
        }
        public int InitDataCache_Data<T>(IData_Factors infoFactors, IData_Factor infoFactor, string tagName, typeTimeFrequency typeTimeFrequency, Dictionary<DateTime, T> datas, bool useEvent = false)
        {
            if (_isInited == false) return -1;
            DataCaches dataCaches = (DataCaches)this.GetDataCaches(infoFactors, infoFactor);
            if (dataCaches == null) return -1;

            if (dataCaches.GetDataCache<T>(tagName, typeTimeFrequency) == null)
            {
                DataCache<T> dataCache = (DataCache<T>)dataCaches.GetDataCache<T>(tagName, typeTimeFrequency, true, 0);

                //注册事件
                if (useEvent)
                {
                    dataCache.DataCache_Load += new DataCacheLoad_EventHandler(EventHandler_DataCacheLoad);
                    dataCache.DataChecks_Initial += new DataCacheChecksInitial_EventHandler(EventHandler_DataCacheChecksInitial);
                    dataCache.DataCache_Change += new DataCacheChange_EventHandler(EventHandler_DataCacheChange);
                    dataCache.Event_DataCache_Load();
                    dataCache.Event_DataChecks_Initial();
                }
                return dataCache.InitDatas(datas);
            }
            return -1;
        }


        public bool InitDataChecks<T>(string tagFactors, string tagFactor, string strTag, typeTimeFrequency typeTimeFrequency, IDataChecks dataChecks)
        {
            if (tagFactors + "" == "") return false;

            //DataCaches_Manage
            IData_Factors infoFactors = this._GetFactors(tagFactors);
            if (infoFactors == null) return false;
            IDataCaches_Manage dataCaches_Manage = this.GetDataCaches_Manage(infoFactors);
            if (dataCaches_Manage == null) return false;
            if (tagFactor + "" == "")
                return dataCaches_Manage.InitDataChecks(dataChecks);

            //DataCaches
            IData_Factor infoFactor = infoFactors.GetData_Factor(tagFactor);
            if (infoFactor == null) return false;
            IDataCaches dataCaches = this.GetDataCaches(infoFactors, infoFactor);
            if (dataCaches == null) return false;

            IDataCache dataCache = dataCaches.GetDataCache<T>(strTag, typeTimeFrequency);
            if (dataCache == null)
                return dataCaches.InitDataChecks(dataChecks);
            else
                return dataCache.InitDataChecks(dataChecks);
        }
        public bool InitDataCheck<T>(string tagFactors, string tagFactor, string strTag, typeTimeFrequency typeTimeFrequency, string tagDataCheck, IDataCheck<T> dataCheck, bool isCanCover = false)
        {
            if (tagFactors + "" == "") return false;

            //DataCaches_Manage
            IData_Factors infoFactors = this._GetFactors(tagFactors);
            if (infoFactors == null) return false;
            IDataCaches_Manage dataCaches_Manage = this.GetDataCaches_Manage(infoFactors);
            if (dataCaches_Manage == null) return false;
            if (tagFactor + "" == "")
                return dataCaches_Manage.InitDataCheck<T>(tagDataCheck, dataCheck, isCanCover);

            //DataCaches
            IData_Factor infoFactor = infoFactors.GetData_Factor(tagFactor);
            if (infoFactor == null) return false;
            IDataCaches dataCaches = this.GetDataCaches(infoFactors, infoFactor);
            if (dataCaches == null) return false;

            IDataCache dataCache = dataCaches.GetDataCache<T>(strTag, typeTimeFrequency);
            if (dataCache == null)
                return dataCaches.InitDataCheck<T>(tagDataCheck, dataCheck, isCanCover);
            else
                return dataCache.InitDataCheck(tagDataCheck, dataCheck, isCanCover);
        }


        /// <summary>提取指定因子对象集的数据缓存集管理对象
        /// </summary>
        /// <param name="infoFactors">因子对象集</param>
        /// <param name="autoInit">是否自动初始</param>
        /// <returns></returns>
        public IDataCaches_Manage GetDataCaches_Manage(IData_Factors infoFactors, bool autoInit = false)
        {
            IDataCaches_Manage dataManage = null;
            if (_DataCaches_Manages.TryGetValue(infoFactors.ID, out dataManage))
            {
                //What ever you gonna do next...
            }
            if (autoInit && dataManage == null)
            {
                if (this.InitDataCaches_Manage(infoFactors, autoInit))
                    return GetDataCaches_Manage(infoFactors);
            }
            return dataManage;
        }
        /// <summary>提取指定因子对象集、因子对象的数据缓存集
        /// </summary>
        /// <param name="infoFactors">因子对象集</param>
        /// <param name="infoFactor">因子对象</param>
        /// <param name="autoInit">是否自动初始</param>
        /// <returns></returns>
        public IDataCaches GetDataCaches(IData_Factors infoFactors, IData_Factor infoFactor, bool autoInit = false)
        {
            //提取管理类
            IDataCaches_Manage dataManage = this.GetDataCaches_Manage(infoFactors, autoInit);
            if (dataManage == null) 
                return null;

            IDataCaches dataCaches = dataManage.GetDataCaches(infoFactor, false);
            if (autoInit && dataCaches == null)
            {
                if (this.InitDataCaches(infoFactors, infoFactor, autoInit))
                    return GetDataCaches(infoFactors, infoFactor);
            }
            return dataCaches;
        }
        /// <summary>按因子对象集、因子对象提取缓存数据对象
        /// </summary>
        /// <typeparam name="T"></typeparam>
        /// <param name="infoFactors">因子对象集</param>
        /// <param name="infoFactor">因子对象</param>
        /// <param name="strTag">自定义标识</param>
        /// <param name="typeTimeFrequency">时间频率</param>
        /// <param name="autoInit">不存在时是否自定初始</param>
        /// <param name="cacheNums">缓存数据数量，autoInit为false时无效</param>
        /// <returns></returns>
        public IDataCache<T> GetDataCache<T>(IData_Factors infoFactors, IData_Factor infoFactor, string strTag = "", typeTimeFrequency typeTimeFrequency = typeTimeFrequency.None, bool autoInit = false, int cacheNums = 1)
        {
            IDataCaches dataCaches = this.GetDataCaches(infoFactors, infoFactor, autoInit);
            if (dataCaches == null) 
                return null;

            IDataCache<T> dataCache = dataCaches.GetDataCache<T>(strTag, typeTimeFrequency);
            if (autoInit && dataCache == null)
            {
                if (this.InitDataCache<T>(infoFactors, infoFactor, strTag, typeTimeFrequency, cacheNums, autoInit))
                    return GetDataCache<T>(infoFactors, infoFactor);
            }

            //事件触发
            return dataCache;
        }


        /// <summary>按因子对象集、因子对象等设置缓存数据
        /// </summary>
        /// <typeparam name="T"></typeparam>
        /// <param name="infoFactors">因子对象集</param>
        /// <param name="infoFactor">因子对象</param>
        /// <param name="strTag">自定义标识</param>
        /// <param name="dtTime">数据时间</param>
        /// <param name="data">数据(int等或class对象)</param>
        /// <param name="typeTimeFrequency">时间频率</param>
        /// <returns></returns>
        public bool SetData<T>(IData_Factors infoFactors, IData_Factor infoFactor, string strTag, DateTime dtTime, T data, typeTimeFrequency typeTimeFrequency = typeTimeFrequency.None)
        {
            IDataCache<T> dataCache = this.GetDataCache<T>(infoFactors, infoFactor, strTag, typeTimeFrequency);
            if (dataCache == null) return false;

            return dataCache.SetData(dtTime, data);
        }
        /// <summary>按因子对象集、因子对象等提取缓存数据
        /// </summary>
        /// <typeparam name="T"></typeparam>
        /// <param name="infoFactors">因子对象集</param>
        /// <param name="infoFactor">因子对象</param>
        /// <param name="strTag">自定义标识</param>
        /// <param name="dtTime">数据时间</param>
        /// <param name="typeTimeFrequency">时间频率</param>
        /// <returns></returns>
        public T GetData<T>(IData_Factors infoFactors, IData_Factor infoFactor, string strTag, DateTime dtTime, typeTimeFrequency typeTimeFrequency = typeTimeFrequency.None)
        {
            IDataCache<T> dataCache = this.GetDataCache<T>(infoFactors, infoFactor, strTag, typeTimeFrequency);
            if (dataCache == null) return default(T);

            return dataCache.GetData(dtTime);
        }


        /// <summary>按因子对象集、因子对象等设置缓存数据
        /// </summary>
        /// <typeparam name="T"></typeparam>
        /// <param name="infoFactors">因子对象集标识</param>
        /// <param name="infoFactor">因子对象标识</param>
        /// <param name="strTag">自定义标识</param>
        /// <param name="dtTime">数据时间</param>
        /// <param name="data">数据(int等或class对象)</param>
        /// <param name="typeTimeFrequency">时间频率</param>
        /// <returns></returns>
        public bool SetData<T>(string tagFactors, string tagFactor, string strTag, DateTime dtTime, T data, typeTimeFrequency typeTimeFrequency = typeTimeFrequency.None)
        {
            IData_Factors dataFactors = this._GetFactors(tagFactors);
            if (dataFactors != null)
            {
                IData_Factor dataFactor = dataFactors.GetData_Factor(tagFactor);
                if (dataFactor != null)
                    return SetData<T>(dataFactors, dataFactor, strTag, dtTime, data, typeTimeFrequency);
            }
            return false;
        }
        /// <summary>按因子对象集、因子对象等提取缓存数据
        /// </summary>
        /// <typeparam name="T"></typeparam>
        /// <param name="infoFactors">因子对象集标识</param>
        /// <param name="infoFactor">因子对象标识</param>
        /// <param name="strTag">自定义标识</param>
        /// <param name="dtTime">数据时间</param>
        /// <param name="typeTimeFrequency">时间频率</param>
        /// <returns></returns>
        public T GetData<T>(string tagFactors, string tagFactor, string strTag, DateTime dtTime, typeTimeFrequency typeTimeFrequency = typeTimeFrequency.None)
        {
            IData_Factors dataFactors = this._GetFactors(tagFactors);
            if (dataFactors != null)
            {
                IData_Factor dataFactor = dataFactors.GetData_Factor(tagFactor);
                return GetData<T>(dataFactors, dataFactor, strTag, dtTime, typeTimeFrequency);
            }
            return default(T);
        }


        /// <summary>索引因子集对象（便于用标识查找因子集）
        /// </summary>
        /// <param name="infoFactors">因子对象集</param>
        /// <param name="infoFactor">因子对象</param>
        /// <returns></returns>
        protected bool _IndexFactors(IData_Factors infoFactors, IData_Factor infoFactor)
        {
            if (infoFactors == null) return false;
            if (this._GetFactors(infoFactors.ID) == null)
                _Data_Factorss.Add(infoFactors.ID, infoFactors);
            return infoFactors.IndexData_Factor(infoFactor);
        }
        /// <summary>提取指定标识的因子集对象
        /// </summary>
        /// <param name="strTag"></param>
        /// <returns></returns>
        public IData_Factors _GetFactors(string strTag)
        {
            if (strTag + "" == "") return null;

            IData_Factors pFactors = null;
            if (_Data_Factorss.TryGetValue(strTag, out pFactors))
            {
            }
            return pFactors;
        }
        public IData_Factor _GetFactor(string strTagFactors, string strTag)
        {
            IData_Factors pFactors = _GetFactors(strTagFactors);
            if (pFactors == null) return null;
            return pFactors.GetData_Factor(strTag);
        }


        //缓存数据初始装载事件
        public virtual void EventHandler_DataCacheLoad(object sender, DataCache_Event e)
        {
            //事件转发-外部实现
            if (this.DataCache_Load != null)
            {
                try
                {
                    this.DataCache_Load(sender, e);
                }
                catch (Exception)
                {
                    throw;
                }
            }
        }
        //缓存数据检查对象初始事件
        public virtual void EventHandler_DataCacheChecksInitial(object sender, DataCache_Event e)
        {
            //事件转发-外部实现
            if (this.DataCacheChecks_Initial != null)
            {
                try
                {
                    this.DataCacheChecks_Initial(sender, e);
                }
                catch (Exception)
                {
                    throw;
                }
            }
        }
        //缓存数据变动事件
        public virtual void EventHandler_DataCacheChange(object sender, DataCache_Event e)
        {
            //事件转发-外部实现
            if (this.DataCache_Change != null)
            {
                try
                {
                    this.DataCache_Change(sender, e);
                }
                catch (Exception)
                {
                    throw;
                }
            }
        }
        //缓存数据集检查对象初始事件
        public virtual void EventHandler_DataCachesChecksInitial(object sender, DataCaches_Event e)
        {
            //事件转发-外部实现
            if (this.DataCachesChecks_Initial != null)
            {
                try
                {
                    this.DataCachesChecks_Initial(sender, e);
                }
                catch (Exception)
                {
                    throw;
                }
            }
        }
        //缓存数据集管理对象检查对象初始事件
        public virtual void EventHandler_DataCachesManageChecksInitial(object sender, DataCachesManage_Event e)
        {
            //事件转发-外部实现
            if (this.DataCachesManageChecks_Initial != null)
            {
                try
                {
                    this.DataCachesManageChecks_Initial(sender, e);
                }
                catch (Exception)
                {
                    throw;
                }
            }
        }

    }
}
