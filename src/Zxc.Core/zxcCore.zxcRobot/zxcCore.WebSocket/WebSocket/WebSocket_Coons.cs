using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace zxcCore.WebSocket
{
    //WebSocket连接管理对象集-自定义
    public class WebSocket_Coons
    {
        //WebSocket连接集
        private static List<WebSocket_Coon> _clients = new List<WebSocket_Coon>();


        //添加WebSocket连接
        public static void Add(WebSocket_Coon client)
        {
            _clients.Add(client);
        }
        //移除WebSocket连接
        public static void Remove(WebSocket_Coon client)
        {
            _clients.Remove(client);
        }
        //提取WebSocket连接
        public static WebSocket_Coon Get(string clientId)
        {
            var client = _clients.FirstOrDefault(c => c.ID == clientId);
            return client;
        }


        //提取频道所有连接信息
        public static List<WebSocket_Coon> GetChannelClients(string idChannel)
        {
            var client = _clients.Where(c => c.Channel == idChannel);
            return client.ToList();
        }

    }

}
