using System;
using System.Collections.Generic;
using System.IO;

namespace zxcCore.zxcDataCache.MemoryDB.Test
{
    /// <summary>数据对象集类-数据库-测试
    /// </summary>
    public class DataDB_Test : Data_DB
    {
        #region 属性及构造

        /// <summary>库表
        /// </summary>
        public DataTable_TestObj<DataModels_Test> Data_Test { get; set; }

        public DataDB_Test(string dirBase) : base(dirBase)
        {
        }

        #endregion

        protected override void OnDBModelCreating()
        {
            base.OnDBModelCreating();

            Data_Test = new DataTable_TestObj<DataModels_Test>(); this.InitDBModel(Data_Test);
        }


    }
}
