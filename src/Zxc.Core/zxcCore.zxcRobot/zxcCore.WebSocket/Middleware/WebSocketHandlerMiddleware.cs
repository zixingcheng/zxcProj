using Microsoft.AspNetCore.Http;
using Newtonsoft.Json;
using System;
using System.Net.WebSockets;
using System.Text;
using System.Threading;
using System.Threading.Tasks;

namespace zxcCore.WebSocket
{
    //中间件-WebSocket
    public class WebSocketHandlerMiddleware
    {
        private readonly RequestDelegate _next;
        public WebSocketHandlerMiddleware(RequestDelegate next)
        {
            _next = next;
            //_logger = loggerFactory.CreateLogger<WebsocketHandlerMiddleware>();
        }


        //处理WebSocket初始
        public async Task Invoke(HttpContext context)
        {
            if (context.Request.Path == "/ws")
            {
                if (context.WebSockets.IsWebSocketRequest)
                {
                    //初始新连接对象
                    System.Net.WebSockets.WebSocket webSocket = await context.WebSockets.AcceptWebSocketAsync();
                    string clientId = Guid.NewGuid().ToString(); ;
                    var wsClient = new WebSocket_Coon
                    {
                        ID = clientId,
                        WebSocket = webSocket
                    };
                    try
                    {
                        //握手通信告知连接ID号
                        await WebSocket_Server.SendMessageAsync(wsClient, "clientId", "handshake", "");
                        //开始处理消息监听
                        await Handle(wsClient);
                    }
                    catch (Exception ex)
                    {
                        await context.Response.WriteAsync("closed");
                    }
                }
                else
                {
                    context.Response.StatusCode = 404;
                }
            }
            else
            {
                await _next(context);
            }
        }
        //处理WebSocket消息
        private async Task Handle(WebSocket_Coon webSocket)
        {
            WebSocket_Coons.Add(webSocket);         //缓存连接对象
            WebSocketReceiveResult result = null;
            do
            {
                //循环接收数据
                var buffer = new byte[1024 * 1];
                result = await webSocket.WebSocket.ReceiveAsync(new ArraySegment<byte>(buffer), CancellationToken.None);
                if (result.MessageType == WebSocketMessageType.Text && !result.CloseStatus.HasValue)
                {
                    //接收到数据，开始处理
                    var msgString = Encoding.UTF8.GetString(buffer).Trim();
                    try
                    {
                        //解析为WebSocket_Msg对象
                        var msg = JsonConvert.DeserializeObject<WebSocket_Msg>(msgString);
                        if (msg != null && msg.SendClientId == webSocket.ID)
                        {
                            HandleMessage(msg);
                        }
                    }
                    catch (Exception)
                    {
                        continue;
                    }
                }
            }
            while (!result.CloseStatus.HasValue);
            WebSocket_Coons.Remove(webSocket);
        }

        //处理WebSocket消息路由
        private void HandleMessage(WebSocket_Msg msg)
        {
            var client = WebSocket_Coons.Get(msg.SendClientId);
            switch (msg.Action.ToLower())
            {
                case "@*join*@":
                    client.Channel = msg.MsgStr;
                    break;
                case "@*leave*@":
                    //置空Channel,模拟关闭连接
                    client.Channel = "";
                    client.WebSocket.CloseAsync(WebSocketCloseStatus.NormalClosure, "", CancellationToken.None);
                    WebSocket_Coons.Remove(client);
                    break;
                default:
                    break;
            }
            WebSocket_Server.HandleMsg_Event(msg);
        }

    }

}
