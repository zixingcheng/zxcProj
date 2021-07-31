using System;

namespace zxcCore.WebSocket
{
    //WebSocketM交互消息对象
    public class WebSocket_Msg
    {
        //发送消息WebSocket的ID号
        public string SendClientId { get; set; }
        //发送消息WebSocket的Channel ID号
        public string SendClientChannelId { get; set; }

        //动作标识
        public string Action { get; set; }
        //消息字符串
        public string MsgStr { get; set; }
        //消息标识
        public string MsgTag { get; set; }

    }

}
