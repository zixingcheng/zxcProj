//===============================================================================
// Copyright @ 2021 Guangzhou Yijian Life Technology Co.,Ltd. All rights reserved.
// Copyright @ 2021 广州易简生活科技有限公司.  版权所有.
//===============================================================================
// 文件名称： 
// 功能描述：DataDB_Robot --机器人缓存数据库
// 创建标识：zxc   2021-06-14
// 修改标识： 
// 修改描述：
//===============================================================================
using System.Collections.Generic;
using zxcCore.zxcDataCache.MemoryDB;
using zxcCore.zxcRobot.Monitor.Msg;
using zxcCore.zxcRobot.Robot.Power;

namespace zxcCore.zxcRobot.Robot
{
    /// <summary>机器人缓存数据库
    /// </summary>
    public class DataDB_Robot : Data_DB
    {
        #region 属性及构造

        /// <summary>库表--机器人功能授权信息表
        /// </summary>
        protected internal DataPower_Robot<Power_Robot> _powerRobot { get; set; }
        /// <summary>库表--成长积分表
        /// </summary>
        protected internal DataTable_Points_Growth<Data_Points> _growthPoints { get; set; }

        protected internal DataDB_Robot() : base("", typePermission_DB.Normal, true, "/Datas/DB_Robot")
        {
        }
        ~DataDB_Robot()
        {
            // 缓存数据？

            // 清理数据
        }

        #endregion

        /// <summary>初始库表信息
        /// </summary>
        protected override void OnDBModelCreating()
        {
            base.OnDBModelCreating();

            //初始库表信息
            _powerRobot = new DataPower_Robot<Power_Robot>(); this.InitDBModel(_powerRobot);
            _growthPoints = new DataTable_Points_Growth<Data_Points>(); this.InitDBModel(_growthPoints); _growthPoints.Init_PointsLog();
        }

    }
}
