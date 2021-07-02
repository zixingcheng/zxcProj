using System;
using System.Collections.Generic;
using System.Linq;

namespace zxcCore.zxcData.Cache.Memory
{
    /// <summary>数据缓存类, 最小Data单元，可缓存(数值、对象集)
    /// </summary>
    public class CacheInfo
    {
        #region 属性及构造

        protected internal DateTime _dtTime;
        /// <summary>数据时间
        /// </summary>
        public DateTime DateTime
        {
            get { return _dtTime; }
        }

        /// <summary>是否非临时数据
        /// </summary>
        public bool IsFixedData
        {
            get; set;
        }

        /// <summary>是否新数据时间(时间步里第一次)
        /// </summary>
        public bool IsNewDataTime
        {
            get; set;
        }


        public CacheInfo(DateTime dtTime)
        {
            _dtTime = dtTime;
        }
        ~CacheInfo()
        {
            // 缓存数据？

            // 清理数据
        }

        #endregion


        //设置数据固定
        public virtual bool SetData_Fixed()
        {
            this.IsFixedData = true;
            return this.IsFixedData;
        }

    }

    /// <summary>数据缓存类, 最小Data单元，可缓存(数值、对象集)
    /// </summary>
    public class CacheInfo<T> : CacheInfo
    {
        #region 属性及构造

        protected internal T _data = default(T);
        /// <summary>数据对象
        /// </summary>
        public T Data
        {
            get { return _data; }
        }

        public CacheInfo(DateTime dtTime, T data) : base(dtTime)
        {
            _data = data;
        }
        ~CacheInfo()
        {
            // 缓存数据？

            // 清理数据
        }

        #endregion

    }
}
