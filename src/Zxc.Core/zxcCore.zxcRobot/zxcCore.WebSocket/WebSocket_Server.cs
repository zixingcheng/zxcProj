//===============================================================================
// Copyright @ 2021 Guangzhou Yijian Life Technology Co.,Ltd. All rights reserved.
// Copyright @ 2021 广州易简生活科技有限公司.  版权所有.
//===============================================================================
// 文件名称： 
// 功能描述：WebSocket_Server --Server消息触发事件
// 创建标识：zxc   2021-07-30
// 修改标识： 
// 修改描述：
//===============================================================================
using Newtonsoft.Json;
using System;
using System.Collections.Generic;
using System.Net.WebSockets;
using System.Text;
using System.Threading;
using System.Threading.Tasks;

namespace zxcCore.WebSocket
{
    /// <summary>WebSocketServer消息触发事件
    /// </summary>
    public class WebSocket_Server
    {
        #region 属性及构造

        /// <summary>WebSocket消息触发事件
        /// </summary>
        public static event WebSocket_Msg_EventHandler WebSocket_Msg_Trigger;

        #endregion


        //消息发送
        public static Task SendMessageAsync(WebSocket_Coon coon, string msgStr, string action = "", string msgTag = "")
        {
            if (coon == null) return null;
            WebSocket_Msg pMsg = new WebSocket_Msg()
            {
                Action = action,
                MsgStr = msgStr,
                MsgTag = msgTag,
                SendClientId = coon.ID,
                SendClientChannelId = coon.Channel
            };

            var msg = JsonConvert.SerializeObject(pMsg);
            var msgBytes = Encoding.UTF8.GetBytes(msg);
            return coon.WebSocket.SendAsync(new ArraySegment<byte>(msgBytes, 0, msgBytes.Length), WebSocketMessageType.Text, true, CancellationToken.None);
        }
        public static Task SendMessageAsync(string coonID, string msgStr, string action = "", string msgTag = "")
        {
            WebSocket_Coon coon = WebSocket_Coons.Get(coonID);
            return SendMessageAsync(coon, msgStr, action, msgTag);
        }

        //消息处理事件
        protected internal static bool HandleMsg_Event(WebSocket_Msg msg)
        {
            if (WebSocket_Msg_Trigger != null)
            {
                WebSocket_Msg_EventArgs pArgs = new WebSocket_Msg_EventArgs(msg);
                WebSocket_Msg_Trigger(null, pArgs);
                return true;
            }
            return true;
        }

    }

}
