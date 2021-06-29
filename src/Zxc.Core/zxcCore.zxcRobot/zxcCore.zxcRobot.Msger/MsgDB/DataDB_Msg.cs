using System;
using System.Collections.Generic;
using System.IO;
using zxcCore.zxcData.Cache.MemoryDB;

namespace zxcCore.zxcRobot.Msger
{
    /// <summary>数据对象集类-数据库-消息库
    /// </summary>
    public class DataDB_Msg : Data_DB
    {
        #region 属性及构造

        /// <summary>库表
        /// </summary>
        public DataTable_Msg<Msg> Data_Msg { get; set; }

        public DataDB_Msg(string dirBase) : base(dirBase)
        {
        }

        #endregion

        protected override void OnDBModelCreating()
        {
            base.OnDBModelCreating();

            Data_Msg = new DataTable_Msg<Msg>(); this.InitDBModel(Data_Msg);
        }


    }
}
