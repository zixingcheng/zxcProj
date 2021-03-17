using System;
using System.Collections.Generic;
using zxcCore.Common;

namespace zxcCore.zxcRobot.Msger
{
    /// <summary>消息类
    /// </summary>
    public class Msg : IMsg
    {
        #region 属性及构造

        /// <summary>消息ID
        /// </summary>
        public string MsgID
        {
            get; set;
        }
        /// <summary>消息类型
        /// </summary>
        public typeMsg MsgType
        {
            get; set;
        }
        /// <summary>消息内容
        /// </summary>
        public string MsgInfo
        {
            get; set;
        }
        /// <summary>消息链接
        /// </summary>
        public string MsgLink
        {
            get; set;
        }
        /// <summary>消息目标用户
        /// </summary>
        public string UserID_To
        {
            get; set;
        }
        /// <summary>目标用户是否为群组
        /// </summary>
        public bool IsUserGroup
        {
            get; set;
        }
        /// <summary>消息源用户
        /// </summary>
        public string UserID_Src
        {
            get; set;
        }
        /// <summary>消息的发送类型集合
        /// </summary>
        public List<typeMsger> DestTypeMsger
        {
            get; set;
        }
        /// <summary>消息时间
        /// </summary>
        public DateTime MsgTime
        {
            get; set;
        }

        public Msg()
        {
            DestTypeMsger = new List<typeMsger>();
        }
        ~Msg()
        {
            // 缓存数据？
            DestTypeMsger.Clear();
        }

        #endregion

        public virtual dynamic ToDict()
        {
            var msgWx = new
            {
                MsgID = MsgID,
                MsgType = MsgType,
                MsgInfo = MsgInfo,
                UserID_To = UserID_To,
                UserID_Src = UserID_Src,
                DestTypeMsger = DestTypeMsger,
                MsgTime = MsgTime,
                MsgLink = MsgLink
            };
            return msgWx;
        }
    }
}
