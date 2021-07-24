using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using zxcCore.zxcData.Cache.MemoryDB;

namespace zxcCore.zxcStudy.Word
{
    /// <summary>拼音对象集类-表
    /// </summary>
    public class DataWord_Pingyin<T> : Data_Table<T> where T : Word_Pingyin
    {
        #region 属性及构造

        public DataWord_Pingyin() : base("dataWord_Pingyin")
        {
            //this._dtName = "dataUser_wx";
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
            return this.FindAll(e => (e.Pinyin == item.Pinyin || e.UID == item.UID) && e.IsDel == false);
        }

    }
}
