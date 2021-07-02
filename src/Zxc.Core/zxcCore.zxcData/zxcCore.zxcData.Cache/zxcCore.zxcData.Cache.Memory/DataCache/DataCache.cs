using System;
using System.Collections.Generic;
using System.Linq;

namespace zxcCore.zxcData.Cache.Memory
{
    /// <summary>数据缓存操作类, 最小Datas单元，可缓存(数值、对象集)
    /// </summary>
    public class DataCache<T> : IDataCache<T>
    {
        #region 属性及构造

        /// <summary>缓存数据初始装载事件
        /// </summary>
        public event DataCacheLoad_EventHandler DataCache_Load;
        /// <summary>缓存数据检查对象初始事件
        /// </summary>
        public event DataCacheChecksInitial_EventHandler DataChecks_Initial;
        /// <summary>缓存数据变动事件
        /// </summary>
        public event DataCacheChange_EventHandler DataCache_Change;


        protected internal string _id = "";
        public string ID
        {
            get { return _id; }
        }

        /// <summary>因子缓存数据设置对象
        /// </summary>
        protected internal IDataCache_Set _DataCache_Set = null;
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
        Dictionary<DateTime, CacheInfo<T>> _DataCaches = null;
        public Dictionary<DateTime, CacheInfo<T>> DataCaches
        {
            get { return _DataCaches; }
        }


        ///// <summary>数据缓存集
        ///// </summary>
        //Dictionary<DateTime, T> _DataCaches = null;
        //public Dictionary<DateTime, T> DataCaches
        //{
        //    get { return _DataCaches; }
        //}
        //List<T> _DataCaches = null;
        //public List<T> DataCaches
        //{
        //    get { return _DataCaches; }
        //}
        public DataCache(string tagName, typeTimeFrequency typeTimeFrequency, int cacheNums, IDataCache_Set srcDataCache_Set, IDataChecks dataChecks = null)
        {
            _DataCaches = new Dictionary<DateTime, CacheInfo<T>>();
            _DataCache_Set = new DataCache_Set(tagName, srcDataCache_Set.Time_Base, typeTimeFrequency, cacheNums, srcDataCache_Set.Info_Factor, srcDataCache_Set);
            _id = _DataCache_Set.ID;
            _DataChecks = dataChecks;

            //初始数据
            this.Init(DateTime.Now);
        }
        ~DataCache()
        {
            // 缓存数据？

            // 清理数据
            this.DataCaches.Clear();
        }

        #endregion


        public int Init(DateTime dtData)
        {
            _DataCaches.Clear();

            int ind = this.GetInd(dtData);
            for (int i = this._DataCache_Set.Sum_Step - 1; i >= 0; i--)
            {
                DateTime dtTime = this._DataCache_Set.Time_End.AddSeconds(-i * this._DataCache_Set.Time_Step);
                this.InitDataCache(dtTime, default(T));
            }
            return this._DataCache_Set.Sum_Step;
        }
        public int InitDatas(Dictionary<DateTime, T> datas)
        {
            foreach (KeyValuePair<DateTime, T> data in datas)
            {
                this.InitDataCache(data.Key, data.Value);
            }
            return datas.Count;
        }
        public CacheInfo<T> InitDataCache(DateTime dtTime, T data, bool bAdd = true)
        {
            DateTime dtTime_Check = _DataCache_Set.CheckTime(dtTime);
            CacheInfo<T> pCacheInfo = new CacheInfo<T>(dtTime, data);

            //执行添加
            if (bAdd)
                if (!this.SetData(pCacheInfo))
                    return null;
            return pCacheInfo;
        }


        public bool SetData(DateTime dtTime, T data)
        {
            //未做重复性验证 
            CacheInfo<T> pCacheInfo = this.InitDataCache(dtTime, data);
            if (pCacheInfo == null)
                return false;
            return true;
        }
        public bool SetData(CacheInfo<T> pCacheInfo)
        {
            if (pCacheInfo == null) return false;

            //缓存数据对象
            pCacheInfo.IsNewDataTime = this.DataCache_Set.IsNewDataTime(pCacheInfo.DateTime);     // 数据变动状态判断
            _DataCaches[pCacheInfo.DateTime] = pCacheInfo;


            //数据变更事件
            if (this.DataCache_Change != null)
            {
                DataCache_Event pArgs = new DataCache_Event(this, pCacheInfo);
                try
                {
                    this.DataCache_Change(null, pArgs);
                }
                catch (Exception)
                {
                    throw;
                }
            }

            //更新数据设置与检查执行
            bool bResult = this.SetLastTime(pCacheInfo.DateTime) && this.CheckData(pCacheInfo.DateTime, pCacheInfo.Data);
            return bResult;
        }
        public bool SetLastTime(DateTime dtLast)
        {
            if (dtLast > this._DataCache_Set.Time_Last)
                this._DataCache_Set.SetLastTime(dtLast);

            //校正缓存数量
            while (_DataCaches.Count > _DataCache_Set.Sum_Step)
            {
                _DataCaches.Remove(_DataCaches.Keys.First());
            }
            return true;
        }

        public T GetData(DateTime dtTime)
        {
            DateTime dtTime_Check = _DataCache_Set.CheckTime(dtTime);

            CacheInfo<T> value;
            _DataCaches.TryGetValue(dtTime_Check, out value);
            return value.Data;
        }
        public List<T> GetDatas(DateTime dtStart, DateTime dtEnd)
        {
            List<T> datas = new List<T>();
            List<int> inds = this._DataCache_Set.GetInds(dtStart, dtEnd);
            foreach (var item in inds)
            {
                DateTime dtTime = _DataCache_Set.GetDateTime(item);
                datas.Add(GetData(dtTime));
            }
            return datas;
        }

        public int GetInd(DateTime dtData)
        {
            return -1;
        }
        public DateTime GetDateTime(int ind)
        {
            return new DateTime();
        }


        public bool CheckData()
        {
            //以检查集的方式统一管理--观察者模式
            if (_DataChecks != null)
                return _DataChecks.CheckDatas();
            return true;
        }
        public bool CheckData(DateTime dtTime, T data)
        {
            //以检查集的方式统一管理--观察者模式
            if (_DataChecks != null)
            {
                bool bResult = _DataChecks.CheckDatas(dtTime, data, this);
                if (bResult && this._DataChecks.Parent != null)
                {
                    if (this._DataChecks.Parent.DataCaches != null)
                    {
                        bResult = this._DataChecks.Parent.DataCaches.CheckData<T>(dtTime, data, this);
                    }
                }
                return bResult;
            }
            return true;
        }


        public bool InitDataChecks(IDataChecks poChecks)
        {
            this._DataChecks = poChecks;
            if (this._DataChecks.DataCache == null)
                this._DataChecks.InitDataCache(this);
            return true;
        }
        public bool InitDataCheck(string tagName, IDataCheck dataCheck, bool isCanCover = false)
        {
            if (_DataChecks != null)
            {
                IDataCheck<T> pDataCheck = (IDataCheck<T>)dataCheck;
                if (pDataCheck == null) return false;

                pDataCheck.InitDataCache(this);
                _DataChecks.InitDataCheck<T>(tagName, pDataCheck, isCanCover);
            }
            return true;
        }


        //触发数据装载事件--便于外部统一装载数据
        public bool Event_DataCache_Load()
        {
            if (this.DataCache_Load != null)
            {
                DataCache_Event pArgs = new DataCache_Event(this, null); 
                try
                {
                    this.DataCache_Load(null, pArgs);
                }
                catch (Exception)
                {
                    throw;
                }
            }
            return true;
        }
        //缓存数据检查对象初始事件--便于外部统一设置检查对象
        public bool Event_DataChecks_Initial()
        {
            if (this.DataChecks_Initial != null)
            {
                DataCache_Event pArgs = new DataCache_Event(this, null); ;
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
