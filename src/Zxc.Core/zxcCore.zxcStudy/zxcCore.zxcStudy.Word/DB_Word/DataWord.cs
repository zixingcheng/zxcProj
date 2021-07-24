using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using zxcCore.zxcData.Cache.MemoryDB;

namespace zxcCore.zxcStudy.Word
{
    /// <summary>汉字对象集类-表
    /// </summary>
    public class DataWord<T> : Data_Table<T> where T : Word
    {
        #region 属性及构造

        public DataWord() : base("dataWord")
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
            return this.FindAll(e => (e.WordStr == item.WordStr || e.UID == item.UID) && e.IsDel == false);
        }

    }
}
