using System;
using System.Collections.Generic;
using zxcCore.Common;
using zxcCore.zxcData.Cache.MemoryDB;

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

        /// <summary>用户自定义设置信息
        /// </summary>
        public List<Power_Robot_UserSet> UserSets
        {
            get; set;
        }


        public Power_Robot()
        {
            UserSets = new List<Power_Robot_UserSet>();
        }
        ~Power_Robot()
        {
            // 缓存数据？
        }

        #endregion

    }

    /// <summary>功能权限-用户外部设置信息
    /// </summary>
    public class Power_Robot_UserSet
    {
        #region 属性及构造

        /// <summary>自定义设置标签
        /// </summary>
        public string SetTag
        {
            get; set;
        }
        /// <summary>自定义设置内容
        /// </summary>
        public string SetValue
        {
            get; set;
        }

        /// <summary>自定义设置对应权限
        /// </summary>
        public typePermission_PowerRobot SetPermission
        {
            get; set;
        }

        /// <summary>自定义设置备注
        /// </summary>
        public string SetLabel
        {
            get; set;
        }
        /// <summary>自定义设置备注解释
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


        public Power_Robot_UserSet()
        {
        }
        ~Power_Robot_UserSet()
        {
            // 缓存数据？
        }

        #endregion

        public object Clone()
        {
            return MemberwiseClone();
        }

    }

}
