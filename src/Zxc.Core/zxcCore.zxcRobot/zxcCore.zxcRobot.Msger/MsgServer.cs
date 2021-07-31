using System;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using Newtonsoft.Json;
using zxcCore.WebSocket;

namespace zxcCore.zxcRobot.Msger
{
    /// <summary>消息服务器
    /// </summary>
    public class MsgServer
    {
        #region 属性及构造

        /// <summary>全局消息服务器
        /// </summary>
        public static readonly MsgServer _MsgServer = new MsgServer();


        /// <summary>消息已接收事件
        /// </summary>
        public event MsgReceive_EventHandler MsgReceive;

        public MsgServer()
        {
            //事件注册，服务器接收websocke消息事件触发
            WebSocket_Server.WebSocket_Msg_Trigger += new WebSocket_Msg_EventHandler(WebSocket_Msg_EventHandler);
        }
        ~MsgServer()
        {
            // 缓存数据？
        }

        #endregion


        //msg服务器接收websocke消息事件触发
        protected internal void WebSocket_Msg_EventHandler(object sender, WebSocket_Msg_EventArgs e)
        {
            if (e == null || e.Msg == null) return;

            //解析为WebSocket_Msg对象
            if (e.Msg.MsgTag == typeMsger.Sys.ToString())
            {
                try
                {
                    var msg = JsonConvert.DeserializeObject<Msg>(e.Msg.MsgStr);
                    if (msg != null)
                    {
                        msg.usrPlat = typeMsger.Sys;
                        msg._objCoon = e.Msg;
                        MsgerHelper.Msger.SendMsg(msg, typeMsger.Sys, true);
                    }
                }
                catch (Exception)
                {
                    throw;
                }
            }
        }

    }

}