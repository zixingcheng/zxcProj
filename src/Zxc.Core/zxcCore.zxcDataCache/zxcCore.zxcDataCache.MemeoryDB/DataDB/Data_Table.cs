using System;
using System.Collections.Generic;
using System.IO;

namespace zxcCore.zxcDataCache.MemoryDB
{
    /// <summary>数据对象集类-表
    /// </summary>
    public class Data_Table<T> : List<T> where T : class, IData
    {
        #region 属性及构造

        /// <summary>数据库对象
        /// </summary>
        protected internal Data_DB _dbContext { get; set; }

        public Data_Table()
        {
        }

        //public InitData()
        //{
        //    //反序列化
        //    this = Newtonsoft.Json.JsonConvert.DeserializeObject<Data_Table<TestObj>>(strJson);
        //}

        #endregion


        public new void AddRange(IEnumerable<T> collection)
        {
            this.AddRange(collection);
        }
        public virtual void UpdateRange(IEnumerable<T> collection)
        {
            this.AddRange(collection);
        }
        public virtual int SaveChanges()
        {
            int nSaved = 0;
            string strJson = Newtonsoft.Json.JsonConvert.SerializeObject(this);

            if (this._dbContext != null)
            {
                string path = this._dbContext.DirBase + "/" + typeof(T).Name;
                path = Path.GetFullPath(path);
                File.WriteAllText(path, strJson);
            }
            return nSaved;
        }


        public virtual dynamic ToJson()
        {
            return null;
        }
        public virtual bool FromJson(dynamic jsonData)
        {
            return false;
        }

    }
}
