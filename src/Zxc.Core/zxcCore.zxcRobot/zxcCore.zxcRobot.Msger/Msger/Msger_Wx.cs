using Newtonsoft.Json;
using System.Collections.Generic;
using zxcCore.Common;

namespace zxcCore.zxcRobot.Msger
{
    /// <summary>消息管理类
    /// </summary>
    public class Msger_Wx : Msger
    {
        #region 属性及构造

        protected internal string _url = "";
        protected internal bool _useApi;
        protected internal bool _useGet;
        public Msger_Wx(bool useApi = true, bool useGet = true, bool isBuffer = false, int numsBuffer = 100) : base(isBuffer, numsBuffer)
        {
            _Tag = "Wx";
            _TypeMsg = typeMsger.Wx;
            _useApi = useApi;
            _useGet = useGet;
            if (_url == "")
                _url = _configMsgSet.config["Msgerset:Msger_Wx:url_API"] + "";
        }
        ~Msger_Wx()
        {
            // 缓存数据？
            _MsgsBuffer.Clear();
        }

        #endregion


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
        public override bool SendMsg(dynamic msg)
        {
            if (_useApi)
                return SendMsg(msg, _url);
            return true;
        }
        public override bool SendMsg(dynamic msg, string url)
        {
            if (url != "")
            {
                string jsonMsg = this.transMsg(msg);
                if (jsonMsg == "") return false;

                string statusCode;
                if (_useGet)
                    NetHelper.Get_ByHttpClient(url, jsonMsg, out statusCode);
                else
                    NetHelper.Post_ByHttpClient(url, jsonMsg, out statusCode);
                if (statusCode != "OK")
                    return false;
            }
            return true;
        }

        protected internal virtual string transMsg(dynamic msg)
        {
            //组装消息
            IMsg pMsg = (IMsg)msg;
            if (pMsg == null) return null;

            var msgWx = new
            {
                usrID = pMsg.IsUserGroup ? "" : pMsg.UserID_To,
                usrName = pMsg.IsUserGroup ? "" : pMsg.UserID_To,
                msgID = pMsg.MsgID,
                msgType = pMsg.MsgType.ToString(),
                msg = pMsg.MsgInfo.Replace("\r", "※r※").Replace("\n", "※n※").Replace("\t", "※t※"),

                groupID = pMsg.IsUserGroup ? pMsg.UserID_To : "",
                groupName = pMsg.IsUserGroup ? pMsg.UserID_To : "",
                usrPlat = "wx",
                time = pMsg.MsgTime.Ticks
            };
            return JsonConvert.SerializeObject(msgWx);
        }
    }
}
