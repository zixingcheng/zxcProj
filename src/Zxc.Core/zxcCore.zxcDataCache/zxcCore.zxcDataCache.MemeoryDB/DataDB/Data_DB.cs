using System;
using System.Collections.Generic;
using System.IO;

namespace zxcCore.zxcDataCache.MemoryDB
{
    /// <summary>数据对象集类-数据库
    /// </summary>
    public class Data_DB
    {
        #region 属性及构造

        /// <summary>数据库路径
        /// </summary>
        public string DirBase { get; set; }

        public Data_DB(string dirBase)
        {
            DirBase = dirBase;
            this.OnModelCreating();
        }

        #endregion


        protected virtual void OnModelCreating()
        {

        }
        protected virtual Data_Table<T> OnModelCreating<T>() where T : class, IData
        {
            string path = this.DirBase + "/" + typeof(T).Name;
            path = Path.GetFullPath(path);

            //反序列化
            Data_Table<T> Data_Table = new Data_Table<T>();
            string strJson = "";
            if (File.Exists(path))
            {
                strJson = File.ReadAllText(path);
                Data_Table = Newtonsoft.Json.JsonConvert.DeserializeObject<Data_Table<T>>(strJson);
            }
            Data_Table._dbContext = this;
            return Data_Table;
        }


    }
}
