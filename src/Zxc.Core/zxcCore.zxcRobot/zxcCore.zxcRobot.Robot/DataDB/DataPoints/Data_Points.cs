using System;
using System.Collections.Generic;
using zxcCore.Common;
using zxcCore.zxcData.Cache.MemoryDB;

namespace zxcCore.zxcRobot.Robot.Power
{
    /// <summary>积分对象基类
    /// </summary>
    public class Data_Points : Data_Models
    {
        #region 属性及构造

        /// <summary>积分类型
        /// </summary>
        public string PointsType
        {
            get; set;
        }
        /// <summary>积分用户
        /// </summary>
        public string PointsUser
        {
            get; set;
        }

        /// <summary>积分点数--总
        /// </summary>
        public double PointsNum
        {
            get; set;
        }
        /// <summary>积分点数-变动
        /// </summary>
        public double PointExChange
        {
            get; set;
        }
        /// <summary>关联ID(前一个操作基ID)
        /// </summary>
        public string RelID
        {
            get; set;
        }

        public string Remark
        {
            get; set;
        }
        /// <summary>是否有效
        /// </summary>
        public bool IsValid
        {
            get; set;
        }


        public Data_Points()
        {
        }
        ~Data_Points()
        {
            // 缓存数据？
        }

        #endregion

    }
}
