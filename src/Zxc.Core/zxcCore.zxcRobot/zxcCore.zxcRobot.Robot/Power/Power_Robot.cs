﻿using System;
using System.Collections.Generic;
using zxcCore.Common;
using zxcCore.zxcDataCache.MemoryDB;

namespace zxcCore.zxcRobot.Robot.Power
{
    /// <summary>机器人操作功能权限类型
    /// </summary>
    public enum typePermission_PowerRobot
    {
        None = 0,
        ReadOnly = 1,
        Writable = 2,
        Modifiable = 4,
        Deleteable = 8
        //Normal = 16
    }

    /// <summary>功能权限类
    /// </summary>
    public class Power_Robot : Data_Models
    {
        #region 属性及构造

        /// <summary>机器人功能名称
        /// </summary>
        public string NameRobot
        {
            get; set;
        }
        /// <summary>群组名
        /// </summary>
        public string NameGroup
        {
            get; set;
        }
        /// <summary>用户名
        /// </summary>
        public string NameUser
        {
            get; set;
        }
        /// <summary>用户别名-消息返回用户名
        /// </summary>
        public string NameUserAlias
        {
            get; set;
        }
        /// <summary>用户平台
        /// </summary>
        public string UsrPlat
        {
            get; set;
        }

        /// <summary>用户权限类型
        /// </summary>
        public typePermission_PowerRobot UsrPermission { get; set; }
        /// <summary>绑定标签内容
        /// </summary>
        public string BindTag
        {
            get; set;
        }

        /// <summary>是否有效
        /// </summary>
        public bool IsValid
        {
            get; set;
        }


        public Power_Robot()
        {
        }
        ~Power_Robot()
        {
            // 缓存数据？
        }

        #endregion

    }
}
