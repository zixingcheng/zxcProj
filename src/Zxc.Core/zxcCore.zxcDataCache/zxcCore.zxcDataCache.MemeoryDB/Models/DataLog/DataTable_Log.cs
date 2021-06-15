using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace zxcCore.zxcDataCache.MemoryDB
{
    /// <summary>库表对象-日志
    /// </summary>
    public class DataTable_Log<T> : Data_Table<T> where T : DataModels_Log, IData
    {
        #region 属性及构造

        public DataTable_Log() : base("sysLog")
        {
            this._isSysTable = true;
            this._isNoLog = true;
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
            return new List<T>();
        }

    }
}