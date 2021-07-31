using System;
using System.Collections.Generic;
using zxcCore.zxcRobot.Msger;

namespace zxcCore.zxcRobot.Msger
{
    /// <summary>消息已缓存事件
    /// </summary>
    /// <param name="sender"></param>
    /// <param name="e"></param>
    public delegate void MsgCached_EventHandler(object sender, MsgCached_Event e);

    public class MsgCached_Event : EventArgs
    {
        #region 属性及构造

        /// <summary>消息内容信息
        /// </summary>
        protected internal Msg _MsgInfo = null;
        public Msg MsgInfo
        {
            get { return _MsgInfo; }
        }

        public MsgCached_Event(Msg msgInfo)
        {
            _MsgInfo = msgInfo;
        }
        ~MsgCached_Event()
        {
            // 缓存数据？
        }

        #endregion
    }

}