using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using zxcCore.zxcDataCache.MemoryDB;

namespace zxcCore.zxcDataCache.MemoryDB.Test
{
    public class DataModels_Test : Data_Models
    {
        public int Id { get; set; }
        public string Id_str { get; set; }
    }


    /// <summary>数据对象集类-表
    /// </summary>
    public class DataTable_TestObj<T> : Data_Table<T> where T : DataModels_Test
    {
        #region 属性及构造

        public DataTable_TestObj() : base("dataTest")
        {
            //Data_Test = new Data_Table<Data_TestObj>(); this.InitModel(Data_Test);
            //this._dtName = "dataTest";
        }

        #endregion


        /// <summary>对象是否存在
        /// </summary>
        /// <param name="item"></param>
        /// <returns></returns>
        public override bool IsExist(T item)
        {
            return this.Contains(item) || this.IsSame(item);
        }
        /// <summary>查询相同对象-重写
        /// </summary>
        /// <param name="item"></param>
        /// <returns></returns>
        public override List<T> Query_Sames(T item)
        {
            return this.FindAll(e => e.Id == item.Id && e.IsDel == false);
        }

    }
}