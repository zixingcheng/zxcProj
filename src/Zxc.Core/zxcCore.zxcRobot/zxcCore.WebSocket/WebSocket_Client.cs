//===============================================================================
// Copyright @ 2021 Guangzhou Yijian Life Technology Co.,Ltd. All rights reserved.
// Copyright @ 2021 广州易简生活科技有限公司.  版权所有.
//===============================================================================
// 文件名称： 
// 功能描述：WebSocket_Client --Client消息触发事件
// 创建标识：zxc   2021-07-30
// 修改标识： 
// 修改描述：
//===============================================================================
using System;
using System.Text;
using System.Threading;
using System.Net.WebSockets;
using System.Threading.Tasks;
using Newtonsoft.Json;

namespace zxcCore.WebSocket
{
    /// <summary>WebSocketClient消息触发事件
    /// </summary>
    public class WebSocket_Client
    {
        #region 属性及构造

        /// <summary>WebSocket消息触发事件
        /// </summary>
        public event WebSocket_Msg_EventHandler WebSocket_Msg_Trigger;

        //ID编号
        public string ID { get; set; }
        //频道
        public string Channel { get; set; }
        //标识是否连接
        public bool IsConnect { get; set; }


        protected internal ClientWebSocket _webSocket = new ClientWebSocket();
        protected internal CancellationToken _cancellation = new CancellationToken();
        protected internal bool _isStop = false;
        protected internal Task<bool> _taskHandle = null;     //任务进程
        public WebSocket_Client()
        {

        }
        #endregion


        //连接初始
        public async Task<bool> ConnectAsync(string url)
        {
            //建立连接
            var urlPath = string.Format("ws://{0}/ws", url);
            await _webSocket.ConnectAsync(new Uri(urlPath), _cancellation);
            await this.SendMessageAsync("", "@*join*@");

            //等待握手信息返回
            await this.Handle();
            return true;
        }

        /// <summary>开始数据接收
        /// </summary>
        /// <returns></returns>
        public async Task<bool> Start(string url = null)
        {
            if (!string.IsNullOrEmpty(url))
            {
                await ConnectAsync(url);
            }

            if (_taskHandle == null || _taskHandle.Status != TaskStatus.Running)
            {
                _taskHandle = Task.Run(() => HandleThread());
            }
            return true;
        }
        /// <summary>停止数据接收
        /// </summary>
        /// <returns></returns>
        public virtual bool Stop()
        {
            if (_taskHandle != null)
            {
                _taskHandle.Dispose();
                _taskHandle = null;
            }
            return true;
        }

        //消息监听开始
        public async Task<bool> HandleThread()
        {
            while (!_isStop)
            {
                //循环接受数据并处理数据
                try
                {
                    await this.Handle();
                }
                catch (Exception)
                {
                    continue;
                }
            }
            return true;
        }


        //消息发送
        public Task SendMessageAsync(string msgStr, string action = "", string msgTag = "")
        {
            WebSocket_Msg pMsg = new WebSocket_Msg()
            {
                Action = action,
                MsgStr = msgStr,
                MsgTag = msgTag,
                SendClientId = this.ID,
                SendClientChannelId = this.Channel
            };

            var msg = JsonConvert.SerializeObject(pMsg);
            var msgBytes = Encoding.UTF8.GetBytes(msg);
            return _webSocket.SendAsync(new ArraySegment<byte>(msgBytes, 0, msgBytes.Length), WebSocketMessageType.Text, true, CancellationToken.None);
        }


        //处理WebSocket消息
        protected internal async Task Handle()
        {
            //循环接受数据
            var result = new byte[1024];
            await _webSocket.ReceiveAsync(new ArraySegment<byte>(result), new CancellationToken());

            //接收到数据，开始处理
            var msgString = Encoding.UTF8.GetString(result, 0, result.Length);
            //解析为WebSocket_Msg对象
            var msg = JsonConvert.DeserializeObject<WebSocket_Msg>(msgString);
            if (msg != null)
            {
                this.HandleMsg_Event(msg);
            }
        }
        //消息处理事件
        protected internal bool HandleMsg_Event(WebSocket_Msg msg)
        {
            if (WebSocket_Msg_Trigger != null && msg != null)
            {
                WebSocket_Msg_EventArgs pArgs = new WebSocket_Msg_EventArgs(msg);

                //接收握手信息 
                if (msg.Action == "handshake")
                {
                    this.ID = msg.SendClientId;
                    this.IsConnect = true;
                }
                else
                {
                    WebSocket_Msg_Trigger(this, pArgs);
                }
                return true;
            }
            return true;
        }

    }

}
