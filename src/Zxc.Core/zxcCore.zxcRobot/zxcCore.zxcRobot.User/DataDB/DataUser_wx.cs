using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using zxcCore.zxcRobot.User;

namespace zxcCore.zxcData.Cache.MemoryDB
{
    /// <summary>数据对象集类-表
    /// </summary>
    public class DataUser_wx<T> : Data_Table<T> where T : User_Base
    {
        #region 属性及构造

        public DataUser_wx() : base("dataUser_wx")
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
            return this.FindAll(e => (e.usrID == item.usrID || e.usrName == item.usrName) && e.IsDel == false);
        }

    }
}
