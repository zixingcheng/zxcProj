using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using zxcCore.zxcData.Cache.MemoryDB;
using zxcCore.zxcRobot.User;

namespace zxcCore.zxcRobot.Robot.Power
{
    /// <summary>数据对象集类-积分表
    /// </summary>
    public class DataTable_Points_Growth<T> : DataTable_Points<T> where T : Data_Points
    {
        #region 属性及构造

        public DataTable_Points_Growth(string dtName = "dataTable_Points_growth") : base(dtName)
        {
            //this._dtName = string.IsNullOrEmpty(_dtName) ? "dataTable_Points_Growth" : _dtName;
            _pointsType = "growth";
        }

        #endregion

        /// <summary>初始相关表--积分记录表
        /// </summary>
        /// <returns></returns>
        public override bool Init_PointsLog(string dtLogName = "")
        {
            return base.Init_PointsLog("dataTable_PointsLog_growth");
        }

    }

}
