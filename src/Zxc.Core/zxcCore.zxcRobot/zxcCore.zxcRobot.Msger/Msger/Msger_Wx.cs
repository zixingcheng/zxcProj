﻿using Newtonsoft.Json;
using System.Collections.Generic;
using zxcCore.Common;

namespace zxcCore.zxcRobot.Msger
{
    /// <summary>消息管理类
    /// </summary>
    public class Msger_Wx : Msger
    {
        #region 属性及构造

        public Msger_Wx(bool useApi = true, bool useGet = true, bool isBuffer = false, int numsBuffer = 100) : base(useApi, useGet, isBuffer, numsBuffer)
        {
            _Tag = "Wx";
            _TypeMsg = typeMsger.wx;
            if (_useApi && _url == "")
                _url = _configMsgSet.config["Msgerset:Msger_Wx:MsgAPI_Url"] + "";
            _pathMsgSwap = _configMsgSet.config["Msgerset:Msger_Wx:MsgSwap_Out"] + "";
        }
        ~Msger_Wx()
        {
            // 缓存数据？
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
            return this.CacheMsg(msg);
        }
        public override bool SendMsg(dynamic msg, string url)
        {
            if (url != "")
            {
                string jsonMsg = this.transMsg(msg);
                if (jsonMsg == "") return false;

                string statusCode;
                if (_useGet)
                    zxcNetHelper.Get_ByHttpClient(url, jsonMsg, out statusCode);
                else
                    zxcNetHelper.Post_ByHttpClient(url, jsonMsg, out statusCode);
                if (statusCode != "OK")
                    return false;
            }
            else
            {
                //直接文件交换
            }
            this.CacheMsg(msg);     //缓存消息
            return true;
        }

        protected internal virtual string transMsg(dynamic msg)
        {
            //组装消息
            IMsg pMsg = (IMsg)msg;
            if (pMsg == null) return null;

            string userName = pMsg.usrName + "" == "" ? pMsg.usrNameNick : pMsg.usrName;
            var msgWx = new
            {
                usrID = pMsg.IsUserGroup ? "" : pMsg.usrID,
                usrName = pMsg.IsUserGroup ? "" : userName,
                msgID = pMsg.msgID,
                msgType = pMsg.msgType.ToString(),
                msg = pMsg.msg.Replace("\r", "※r※").Replace("\n", "※n※").Replace("\t", "※t※").Replace("\"", "※i※"),
                groupID = pMsg.IsUserGroup ? pMsg.groupID : "",
                groupName = pMsg.IsUserGroup ? userName : "",
                usrPlat = "wx",
                time = pMsg.msgTime.Ticks
            };
            return JsonConvert.SerializeObject(msgWx);
        }

    }
}
