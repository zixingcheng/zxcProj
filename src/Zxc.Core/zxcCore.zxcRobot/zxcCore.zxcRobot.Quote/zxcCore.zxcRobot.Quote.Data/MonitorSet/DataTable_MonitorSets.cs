using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using zxcCore.zxcData.Cache.MemoryDB;

namespace zxcCore.zxcRobot.Quote.Data
{
    /// <summary>数据对象集类-监测设置
    /// </summary>
    public class DataTable_MonitorSets<T> : Data_Table<T> where T : MonitorSet
    {
        #region 属性及构造

        public DataTable_MonitorSets(string dtName = "dataTable_MonitorSets") : base(dtName)
        {
            //this._dtName = string.IsNullOrEmpty(_dtName) ? "dataTable_Points" : _dtName;
            //this._isNoLog = true;
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
            return this.FindAll(e => (e.UID == item.UID && e.IsDel == false) || (e.SpiderName == item.SpiderName && e.SpiderTag == item.SpiderTag && e.IsDel == false));
        }

    }

}
