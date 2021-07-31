using System; 
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using System.Net.WebSockets;

namespace zxcCore.WebSocket
{
    //WebSocket连接管理对象-自定义
    public class WebSocket_Coon
    {
        //WebSocket连接对象
        public System.Net.WebSockets.WebSocket WebSocket { get; set; }


        //ID编号
        public string ID { get; set; }
        //频道
        public string Channel { get; set; }


        //消息发送
        public Task SendMessageAsync(string msgStr)
        {
            var msg = Encoding.UTF8.GetBytes(msgStr);
            return WebSocket.SendAsync(new ArraySegment<byte>(msg, 0, msg.Length), WebSocketMessageType.Text, true, CancellationToken.None);
        }

    }

}
