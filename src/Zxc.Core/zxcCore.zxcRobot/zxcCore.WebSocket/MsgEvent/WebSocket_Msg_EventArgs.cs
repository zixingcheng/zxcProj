using System;
using System.Collections.Generic;
using System.Text;

namespace zxcCore.WebSocket
{
    /// <summary>WebSocket消息触发事件
    /// </summary>
    /// <param name="sender"></param>
    /// <param name="e"></param>
    public delegate void WebSocket_Msg_EventHandler(object sender, WebSocket_Msg_EventArgs e);


    /// <summary>WebSocket消息触发事件Args
    /// </summary>
    public class WebSocket_Msg_EventArgs : EventArgs
    {
        #region 属性及构造

        /// <summary>有效差值范围
        /// </summary>
        protected internal WebSocket_Msg _msg = null;
        public WebSocket_Msg Msg { get { return _msg; } }


        public WebSocket_Msg_EventArgs(WebSocket_Msg msg = null)
        {
            _msg = msg;
        }
        ~WebSocket_Msg_EventArgs()
        {
            // 缓存数据？
        }

        #endregion
    }

}
