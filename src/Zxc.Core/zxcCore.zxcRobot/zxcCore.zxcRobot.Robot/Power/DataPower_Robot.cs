using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using zxcCore.zxcData.Cache.MemoryDB;
using zxcCore.zxcRobot.User;

namespace zxcCore.zxcRobot.Robot.Power
{
    /// <summary>数据对象集类-机器人功能权限表
    /// </summary>
    public class DataPower_Robot<T> : Data_Table<T> where T : Power_Robot, IData
    {
        #region 属性及构造

        public DataPower_Robot() : base("dataPower_Robot")
        {
            //this._dtName = "dataPower_Robot";
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
            return this.FindAll(e => e.NameGroup == item.NameGroup && e.NameUser == item.NameUser && e.UsrPlat == item.UsrPlat && e.NameRobot == item.NameRobot && e.IsDel == false);
        }

    }
}
