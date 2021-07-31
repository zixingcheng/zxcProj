using System;
using System.Collections.Generic;
using zxcCore.zxcRobot.Msger;

namespace zxcCore.zxcRobot.Msger
{
    /// <summary>服务器消息接收事件
    /// </summary>
    /// <param name="sender"></param>
    /// <param name="e"></param>
    public delegate void MsgReceive_EventHandler(object sender, MsgReceive_Event e);

    public class MsgReceive_Event : EventArgs
    {
        #region 属性及构造

        /// <summary>消息内容信息
        /// </summary>
        protected internal Msg _MsgInfo = null;
        public Msg MsgInfo
        {
            get { return _MsgInfo; }
        }

        public MsgReceive_Event(Msg msgInfo)
        {
            _MsgInfo = msgInfo;
        }
        ~MsgReceive_Event()
        {
            // 缓存数据？
        }

        #endregion
    }

}