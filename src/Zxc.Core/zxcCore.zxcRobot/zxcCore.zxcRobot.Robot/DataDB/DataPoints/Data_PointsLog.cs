using System;
using System.Collections.Generic;
using zxcCore.Common;
using zxcCore.zxcData.Cache.MemoryDB;

namespace zxcCore.zxcRobot.Robot.Power
{
    /// <summary>积分变动记录基类
    /// </summary>
    public class Data_PointsLog : Data_Models
    {
        #region 属性及构造

        /// <summary>积分点数--当前总数
        /// </summary>
        public double PointsNow
        {
            get; set;
        }
        /// <summary>积分点数--前一总数
        /// </summary>
        public double PointsLast
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
        /// <summary>积分缘由
        /// </summary>
        public string PointsNote
        {
            get; set;
        }
        /// <summary>积分缘由标签
        /// </summary>
        public string PointsNote_Label
        {
            get; set;
        }
        /// <summary>积分操作用户
        /// </summary>
        public string PointsUser_OP
        {
            get; set;
        }
        /// <summary>备注
        /// </summary>
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


        public Data_PointsLog()
        {
        }
        ~Data_PointsLog()
        {
            // 缓存数据？
        }

        #endregion

    }

}
