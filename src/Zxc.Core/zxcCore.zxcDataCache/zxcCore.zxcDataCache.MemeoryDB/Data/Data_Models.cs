using System;
using System.Collections.Generic;

namespace zxcCore.zxcDataCache.MemoryDB
{
    /// <summary>数据模型对象类
    /// </summary>
    public abstract class Data_Models : IData
    {
        #region 属性及构造

        protected internal string _uid = System.Guid.NewGuid().ToString();
        /// <summary>全局UID号
        /// </summary>
        public string UID
        {
            get { return _uid; }
            set { _uid = value; }
        }

        protected internal bool _isDeleted = false;
        /// <summary>是否已经删除
        /// </summary>
        public bool IsDel
        {
            get { return _isDeleted; }
            set { _isDeleted = value; }
        }

        protected internal string _perator = null;
        /// <summary>操作员
        /// </summary>
        public string Operator
        {
            get { return _perator; }
            set { _perator = value; }
        }

        protected internal DateTime _opTime;
        /// <summary>操作时间
        /// </summary>
        public DateTime OpTime
        {
            get { return _opTime; }
            set { _opTime = value; }
        }

        public Data_Models()
        {
        }

        #endregion


        public object Clone()
        {
            return MemberwiseClone();
        }

        public virtual dynamic ToJson()
        {
            string strJson = Newtonsoft.Json.JsonConvert.SerializeObject(this);
            return strJson;
        }
        public virtual bool FromJson(dynamic jsonData)
        {
            return false;
        }

    }
}
