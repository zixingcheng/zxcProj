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
        /// <summary>注入数据库对象
        /// </summary>
        /// <param name="dbContext"></param>
        public void SetDB(Data_DB dbContext)
        {
            _dbContext = dbContext;
        }

        //public InitData()
        //{
        //    //反序列化
        //    this = Newtonsoft.Json.JsonConvert.DeserializeObject<Data_Table<TestObj>>(strJson);
        //}

        #endregion


        /// <summary>对象是否存在
        /// </summary>
        /// <param name="item"></param>
        /// <returns></returns>
        public virtual bool IsExist(T item)
        {
            return this.Contains(item);
        }
        /// <summary>对象是否相同-重写
        /// </summary>
        /// <param name="item"></param>
        /// <returns></returns>
        public virtual bool IsSame(T item)
        {
            return this.Contains(item);
        }

        /// <summary>添加对象-剔除存在
        /// </summary>
        /// <param name="item"></param>
        /// <param name="isUnique">唯一性检查</param>
        public virtual void Add(T item, bool isUnique)
        {
            if (isUnique)
                if (this.IsExist(item)) return;
            base.Add(item);
        }
        /// <summary>添加对象集-剔除存在
        /// </summary>
        /// <param name="collection"></param>
        /// <param name="isUnique">唯一性检查</param>
        public virtual void AddRange(IEnumerable<T> collection, bool isUnique)
        {
            foreach (var item in collection)
            {
                this.Add(item, isUnique);
            }
        }


        /// <summary>更新对象集
        /// </summary>
        /// <param name="collection"></param>
        public virtual void UpdateRange(IEnumerable<T> collection)
        {
            this.AddRange(collection);
        }
        /// <summary>保存修改-缓存到文件
        /// </summary>
        /// <returns></returns>
        public virtual int SaveChanges()
        {
            int nSaved = 0;
            string strJson = this.ToJson();

            if (this._dbContext != null)
            {
                string path = this._dbContext.DirBase + "/" + typeof(T).Name;
                path = Path.GetFullPath(path);
                File.WriteAllText(path, strJson);
            }
            return nSaved;
        }


        /// <summary>转为Json对象
        /// </summary>
        /// <returns></returns>
        public virtual dynamic ToJson()
        {
            return Newtonsoft.Json.JsonConvert.SerializeObject(this);
        }

    }
}
