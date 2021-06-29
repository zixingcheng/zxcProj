using System;
using System.Collections.Generic;
using System.Linq;

namespace zxcCore.zxcData.Cache.Memory
{
    /// <summary>数据缓存集，数据缓存操作类集合，因子
    /// </summary>
    public class DataCaches : IDataCaches
    {
        #region 属性及构造

        string _id = "";
        public string ID
        {
            get { return _id; }
        }

        /// <summary>因子缓存数据设置对象
        /// </summary>
        IDataCache_Set _DataCache_Set = null;
        public IDataCache_Set DataCache_Set
        {
            get { return _DataCache_Set; }
        }

        /// <summary>数据检查集
        /// </summary>
        protected internal IDataChecks _DataChecks = null;
        public IDataChecks DataChecks
        {
            get { return _DataChecks; }
        }

        /// <summary>数据缓存集
        /// </summary>
        Dictionary<string, IDataCache> _DataCaches = null;
        public Dictionary<string, IDataCache> DataCachess
        {
            get { return _DataCaches; }
        }


        public DataCaches(IData_Factor info_Factor, IDataCache_Set srcDataCache_Set, IDataChecks dataChecks = null)
        {
            _DataCache_Set = new DataCache_Set(info_Factor.ID, srcDataCache_Set.Time_Base, typeTimeFrequency.None, 0, info_Factor, srcDataCache_Set);
            _id = _DataCache_Set.ID;
            dataChecks = _DataChecks;

            _DataCaches = new Dictionary<string, IDataCache>();
        }
        ~DataCaches()
        {
            // 缓存数据？

            // 清理数据
            this._DataCaches.Clear();
        }

        #endregion


        public bool InitDataCache<T>(string tagName, typeTimeFrequency typeTimeFrequency, int cacheNums)
        {
            string tag = this.GetTagName(typeTimeFrequency, tagName);
            if (this.GetDataCache<T>(tag) == null)
            {
                DataCache<T> data = new DataCache<T>(tag, typeTimeFrequency, cacheNums, _DataCache_Set);
                _DataCaches[data.ID] = data;
                return true;
            }
            return false;
        }
        public IDataCache<T> GetDataCache<T>(string tagName, typeTimeFrequency typeTimeFrequency = typeTimeFrequency.None, bool autoInit = false, int cacheNums = 1)
        {
            IDataCache data = null;
            string tag = this.GetTagName(typeTimeFrequency, tagName);
            if (_DataCaches.TryGetValue(tag, out data))
            {
                //What ever you gonna do next...
            }
            if (autoInit && data == null)
            {
                if (InitDataCache<T>(tagName, typeTimeFrequency, cacheNums))
                    return GetDataCache<T>(tagName, typeTimeFrequency);
            }
            return (IDataCache<T>)data;
        }


        public bool InitDataChecks(IDataChecks poChecks)
        {
            this._DataChecks = poChecks;
            if (this._DataChecks.DataCaches == null)
                this._DataChecks.InitDataCaches(this);
            return true;
        }
        public bool InitDataCheck<T>(string tagName, IDataCheck<T> dataCheck, bool isCanCover = false)
        {
            if (_DataChecks != null)
            {
                IDataCheck<T> pDataCheck = (IDataCheck<T>)dataCheck;
                if (pDataCheck == null) return false;

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
        public bool CheckData<T>(DateTime dtTime, T data, IDataCache<T> dataCache = null)
        {
            //以检查集的方式统一管理--观察者模式
            if (_DataChecks != null)
            {
                bool bResult = _DataChecks.CheckDatas(dtTime, data, dataCache);
                if (bResult && this._DataChecks.Parent != null)
                {
                    if (this._DataChecks.Parent.DataCaches_Manage != null)
                    {
                        bResult = this._DataChecks.Parent.DataCaches_Manage.CheckData<T>(dtTime, data, this);
                    }
                }
                return bResult;
            }
            return false;
        }

        // 初始单个
        public void Init_Set(IDataSet setInfo)
        {
        }
        //public List<typeTimeFrequency> GetTimeFrequencys()
        //{
        //    List<typeTimeFrequency> types = new List<typeTimeFrequency>();
        //    //List<IDataSet> sets = this._DataCaches.get.GetDataSets(this._id, "");
        //    //foreach (var item in sets)
        //    //{
        //    //    DataSet_TypeTime_Iot<T> set = (DataSet_TypeTime_Iot<T>)item;
        //    //    if (set != null)
        //    //    {
        //    //        types.Add(set.Type_DataTime);
        //    //    }
        //    //}
        //    return types;
        //}

        public string GetTagName(typeTimeFrequency typeTimeFrequency, string strTag = "")
        {
            return this.DataCache_Set.GetTagName(typeTimeFrequency, strTag);
        }
    }
}
