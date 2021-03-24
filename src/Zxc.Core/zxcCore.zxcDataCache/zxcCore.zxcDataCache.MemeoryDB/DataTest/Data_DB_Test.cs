using System;
using System.Collections.Generic;
using System.IO;

namespace zxcCore.zxcDataCache.MemoryDB.Test
{
    /// <summary>数据对象集类-数据库-测试
    /// </summary>
    public class Data_DB_Test : Data_DB
    {
        #region 属性及构造

        /// <summary>库表
        /// </summary>
        public Data_Table<Data_TestObj> Data_Test { get; set; }

        public Data_DB_Test(string dirBase) : base(dirBase)
        {
        }

        #endregion

        protected override void OnModelCreating()
        {
            base.OnModelCreating();

            Data_Test = new Data_Table<Data_TestObj>(); this.InitModel(Data_Test);

            Data_Test = this.OnModelCreating<Data_TestObj>();

        }


    }
}
