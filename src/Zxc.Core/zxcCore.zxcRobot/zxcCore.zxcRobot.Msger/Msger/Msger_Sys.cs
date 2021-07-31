using Newtonsoft.Json;
using System;
using System.Collections.Generic;
using System.Threading;
using System.Threading.Tasks;
using zxcCore.Common;
using zxcCore.WebSocket;

namespace zxcCore.zxcRobot.Msger
{
    /// <summary>消息管理类-系统(msgServer)
    /// </summary>
    public class Msger_Sys : Msger
    {
        #region 属性及构造

        /// <summary>消息已接收事件
        /// </summary>
        public event MsgReceive_EventHandler MsgReceive;


        protected internal WebSocket_Client _msgClient = new WebSocket_Client();
        public Msger_Sys(bool useApi = true, bool useGet = true, bool isBuffer = false, int numsBuffer = 100) : base(false, false, isBuffer, numsBuffer)
        {
            _Tag = "Sys";
            _TypeMsg = typeMsger.Sys;
            _url = "127.0.0.1:5001";
            _url = _configMsgSet.config["Msgerset:Msger_Sys:MsgServer_IP"] + ":" + _configMsgSet.config["Msgerset:Msger_Sys:MsgServer_Port"];

            //建立连接,并初始
            if (MsgServer._MsgServer != null)
                _msgClient.WebSocket_Msg_Trigger += new WebSocket_Msg_EventHandler(MsgSys_EventHandler);
        }
        ~Msger_Sys()
        {
            // 缓存数据？
        }

        #endregion


        //消息接收开始
        public virtual bool Start(int dlayTime = 60)
        {
            if (!_msgClient.IsConnect)
            {
                Task<bool> _taskStart = null;     //任务进程
                if (_taskStart == null || _taskStart.Status != TaskStatus.Running)
                {
                    _taskStart = Task.Run(() => _msgClient.Start(_url));
                }
            }

            //等待连接成功
            while (!_msgClient.IsConnect && dlayTime > 0)
            {
                Thread.Sleep(1000);
                dlayTime--;
            }
            return true;
        }


        //消息
        //Msg pMsg = new Msg()
        //{
        //    MsgID = "",
        //    MsgInfo = msg + "",
        //    MsgType = typeMsg.TEXT,
        //    MsgLink = "",
        //    UserID_To = userID_To,
        //    IsUserGroup = userID_To.Substring(0, 2) == "@*" ? true : false,
        //    DestTypeMsger = new List<typeMsger>() { typeMsger.Wx },
        //    UserID_Src = "System",
        //    MsgTime = DateTime.Now
        //};
        public override bool SendMsg(dynamic msg, bool useMsgServer = false)
        {
            //组装消息
            Msg _msg = (Msg)msg;
            if (_msg == null) return false;

            _msg.usrPlat = typeMsger.Sys;
            if (useMsgServer)
            {
                WebSocket_Msg pMsg = _msg._objCoon;
                if (pMsg != null)
                {
                    WebSocket_Server.SendMessageAsync(pMsg.SendClientId, this.transMsg(_msg), pMsg.Action, pMsg.MsgTag);
                }
                else
                {
                    this._msgClient.SendMessageAsync(this.transMsg(_msg), "", _msg.usrPlat.ToString());
                }
            }
            else
            {
                WebSocket_Msg pMsg = _msg._objCoon;
                if (pMsg != null)
                {
                    this._msgClient.SendMessageAsync(this.transMsg(_msg), pMsg.Action, pMsg.MsgTag);
                }
                else
                {
                    this._msgClient.SendMessageAsync(this.transMsg(_msg), "", _msg.usrPlat.ToString());
                }
            }
            return this.CacheMsg(msg);
        }
        public override bool SendMsg(dynamic msg, string url)
        {
            return false;
        }


        //msg客户端接收websocke消息事件触发
        protected internal void MsgSys_EventHandler(object sender, WebSocket_Msg_EventArgs e)
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
                        if (this.MsgReceive != null)
                        {
                            MsgReceive_Event pArgs = new MsgReceive_Event(msg);
                            this.MsgReceive(sender, pArgs);
                        }
                    }
                }
                catch (Exception)
                {
                    //throw;
                }
            }
        }

    }
}
