using System;
using System.Collections.Generic;
using zxcCore.Common;
using zxcCore.zxcDataCache.MemoryDB;

namespace zxcCore.zxcRobot.User
{
    /// <summary>用户平台类型
    /// </summary>
    public enum typeUserPlat
    {
        /// <summary>系统
        /// </summary>
        zxc = 0,
        /// <summary>微信
        /// </summary>
        wx = 1,
        /// <summary>微信公众号
        /// </summary>
        wxmp = 2
    }

    /// <summary>用户类
    /// </summary>
    public class User_Base : Data_Models, IUser
    {
        #region 属性及构造

        /// <summary>用户ID
        /// </summary>
        public string usrID
        {
            get; set;
        }
        /// <summary>用户电话
        /// </summary>
        public string usrPhone
        {
            get; set;
        }
        /// <summary>用户密码
        /// </summary>
        public string usrPW
        {
            get; set;
        }
        /// <summary>用户名称
        /// </summary>
        public string usrName
        {
            get; set;
        }
        /// <summary>用户名称-别名
        /// </summary>
        public string usrNameNick
        {
            get; set;
        }

        /// <summary>用户名称-备注
        /// </summary>
        public string usrNameRemarks
        {
            get; set;
        }
        /// <summary>用户名称-标签
        /// </summary>
        public string usrNameLabel
        {
            get; set;
        }
        /// <summary>用户描述
        /// </summary>
        public string usrDescribe
        {
            get; set;
        }

        /// <summary>用户平台
        /// </summary>
        public string usrPlat
        {
            get; set;
        }
        /// <summary>是否为群组
        /// </summary>
        public bool isGroup
        {
            get; set;
        }

        /// <summary>创建时间
        /// </summary>
        public DateTime creatTime
        {
            get; set;
        }
        /// <summary>修改时间
        /// </summary>
        public DateTime modifyTime
        {
            get; set;
        }


        public User_Base()
        {
        }
        ~User_Base()
        {
            // 缓存数据？
        }

        #endregion

        public virtual dynamic ToDict()
        {
            var msgWx = new
            {
                //MsgID = MsgID,
                //MsgType = MsgType,
                //MsgInfo = MsgInfo,
                //UserID_To = UserID_To,
                //UserID_Src = UserID_Src,
                //DestTypeMsger = DestTypeMsger,
                //MsgTime = MsgTime,
                //MsgLink = MsgLink
            };
            return msgWx;
        }

    }
}
