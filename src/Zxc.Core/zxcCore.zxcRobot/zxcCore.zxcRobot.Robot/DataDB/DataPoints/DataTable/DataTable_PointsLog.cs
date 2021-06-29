using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using zxcCore.zxcData.Cache.MemoryDB;
using zxcCore.zxcRobot.User;

namespace zxcCore.zxcRobot.Robot.Power
{
    /// <summary>数据对象集类-积分变动记录表
    /// </summary>
    public class DataTable_PointsLog<T> : Data_Table<T> where T : Data_PointsLog
    {
        #region 属性及构造

        public DataTable_PointsLog(string dtName = "dataTable_PointsLog") : base(dtName)
        {
            //this._dtName = string.IsNullOrEmpty(_dtName) ? "dataTable_PointsLog" : _dtName;
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
            return this.FindAll(e => e.UID == item.UID && e.PointsType == item.PointsType && e.PointsUser == item.PointsUser && e.PointsNote == item.PointsNote && e.PointExChange == item.PointExChange && e.Operator == item.Operator && (e.OpTime - item.OpTime).TotalHours < 1 && e.IsDel == false);
            //return this.FindAll(e => (e.UID == item.UID && e.IsDel == false) || (e.PointsType == item.PointsType && e.PointsUser == item.PointsUser && e.PointsNote == item.PointsNote && e.PointExChange == item.PointExChange && e.Operator == item.Operator && (e.OpTime - item.OpTime).TotalHours < 1 && e.IsDel == false));
        }

    }

}
