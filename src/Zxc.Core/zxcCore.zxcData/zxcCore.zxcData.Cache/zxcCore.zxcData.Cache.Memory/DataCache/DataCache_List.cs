using System;
using System.Collections.Generic;

namespace zpCore.zpDataCache.Memory
{
    /// <summary>数据缓存操作类
    /// </summary>
    class DataCache<T> : IDataCache<T>
    {
        #region 属性及构造

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

        /// <summary>数据缓存集
        /// </summary>
        //Dictionary<DateTime, IData<T>> _DataCaches = null;
        //public Dictionary<DateTime, IData<T>> DataCaches
        //{
        //    get { return _DataCaches; }
        //}

        List<T> _DataCaches = null;
        public List<T> DataCaches
        {
            get { return _DataCaches; }
        }

        public DataCache(string tagName, typeTimeFrequency typeTimeFrequency, int cacheNums, IDataCache_Set srcDataCache_Set)
        {
            _DataCaches = new List<T>();
            _DataCache_Set = new DataCache_Set(tagName, srcDataCache_Set.Time_Base, typeTimeFrequency, cacheNums, srcDataCache_Set.Info_Factor);
            _id = _DataCache_Set.ID;
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
            //_DataCaches = new Dictionary<DateTime, IData_Iot<T>>();

            int ind = this.GetInd(dtData);
            for (int i = 0; i < this._DataCache_Set.Sum_Step; i++)
            {
                this._DataCaches.Add(default(T));
            }
            return this._DataCache_Set.Sum_Step;
        }

        public bool SetData(DateTime dtTime, T data)
        {
            int ind = this.GetInd(dtTime);
            int indLast = this.GetInd(_DataCache_Set.Time_Last);
            if(ind )
            this._DataCaches[ind] = data;
            return this.SetLastTime(dtTime);
        }
        public bool SetLastTime(DateTime dtLast)
        {
            if (dtLast > this._DataCache_Set.Time_Last)
                this._DataCache_Set.SetLastTime(dtLast);
            return false;
        }

        public T GetData(DateTime dtData)
        {
            int ind = this.GetInd(dtData);
            T value = _DataCaches[ind];
            return value;
        }
        public List<T> GetDatas(DateTime dtStart, DateTime dtEnd)
        {
            List<T> datas = new List<T>();
            List<int> inds = this._DataCache_Set.GetInds(dtStart, dtEnd);
            foreach (var item in inds)
            {
                datas.Add(DataCaches[item]);
            }
            return datas;
        }

        public int GetInd(DateTime dtData)
        {
            return this._DataCache_Set.GetInd(dtData);
        }
        public DateTime GetDateTime(int ind)
        {
            return this._DataCache_Set.GetDateTime(ind);
        }

        public bool CheckData()
        {
            return true;
        }
    }
}
