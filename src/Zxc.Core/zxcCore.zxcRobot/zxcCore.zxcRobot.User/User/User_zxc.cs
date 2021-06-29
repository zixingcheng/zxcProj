using System;
using System.Collections.Generic;
using zxcCore.Common;
using zxcCore.zxcData.Cache.MemoryDB;

namespace zxcCore.zxcRobot.User
{
    /// <summary>用户账户类型
    /// </summary>
    public enum typeUser
    {
        /// <summary>游客用户
        /// </summary>
        guest = 0,
        /// <summary>普通用户
        /// </summary>
        user = 1,
        /// <summary>会员用户
        /// </summary>
        memberuser = 10,
        /// <summary>管理员
        /// </summary>
        admin = 110,
        /// <summary>系统管理员
        /// </summary>
        sysadmin = 111,
    }

    /// <summary>用户类
    /// </summary>
    public class User_zxc : User_Base
    {
        #region 属性及构造

        /// <summary>用户账户类型
        /// </summary>
        public typeUser usrType
        {
            get; set;
        }
        /// <summary>用户地址
        /// </summary>
        public string usrAddr
        {
            get; set;
        }
        /// <summary>用户性别
        /// </summary>
        public string usrSex
        {
            get; set;
        }
        /// <summary>用户年龄
        /// </summary>
        public string usrAge
        {
            get; set;
        }

        /// <summary>用户名-微信
        /// </summary>
        public string usrName_wx
        {
            get; set;
        }
        ///// <summary>用户名-微信公众号
        ///// </summary>
        //public string usrName_wxmp
        //{
        //    get; set;
        //}

        public User_zxc()
        {
            usrPlat = "zxc";
        }
        ~User_zxc()
        {
            // 缓存数据？
        }

        #endregion

    }
}
