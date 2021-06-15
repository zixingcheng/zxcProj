using System;
using System.Collections.Generic;
using System.Text;
using zxcCore.zxcRobot.Msger;

namespace zxcCore.zxcRobot.Monitor.Msg
{
    /// <summary>消息处理
    /// </summary>
    public class MsgHandle
    {

        #region 属性及构造

        protected internal string _tagAlias = "";
        protected internal string _tag = "";
        public string Tag
        {
            get { return _tag; }
        }

        /// <summary>消息发送集
        /// </summary>
        protected internal List<typeMsger> _typeMsgs = new List<typeMsger>();

        public MsgHandle(string tag, string setting)
        {
            _tag = tag == "" ? "MsgHandle" : tag;
            _tagAlias = "消息处理";

            //后期优化为外部配置信息
            _typeMsgs.Add(typeMsger.wx);

            this.InitSetting(setting);
        }
        ~MsgHandle()
        {
            // 缓存数据？
        }

        #endregion


        /// <summary>初始配置信息
        /// </summary>
        /// <param name="setting"></param>
        /// <returns></returns>
        public virtual bool InitSetting(dynamic setting)
        {
            return true;
        }

        /// <summary>处理消息
        /// </summary>
        /// <param name="msg"></param>
        /// <returns></returns>
        public virtual bool HandleMsg(Msger.Msg msg)
        {
            if (!this.HandleMsg_Check(msg))
                return false;
            return this.HandleMsg_Do(msg);
        }
        /// <summary>消息检查
        /// </summary>
        /// <returns></returns>
        public virtual bool HandleMsg_Check(Msger.Msg msg)
        {
            return true;
        }
        /// <summary>消息处理实现
        /// </summary>
        /// <returns></returns>
        public virtual bool HandleMsg_Do(Msger.Msg msg)
        {
            return true;
        }

        /// <summary>消息通知
        /// </summary>
        /// <param name="msg"></param>
        /// <param name="userID_To"></param>
        /// <returns></returns>
        public virtual bool NotifyMsg(dynamic msg, string userID_To = "@*测试群", typeMsg typeMsg = typeMsg.TEXT, typeMsger typeMsger = typeMsger.wx)
        {
            if (msg + "" != null)
            {
                var pMsg = this.getMsg(msg, userID_To, false, typeMsg, typeMsger);
                if (pMsg != null)
                    MsgerHelper.Msger.SendMsg(pMsg, typeMsger);
            }
            return false;
        }


        //提取返回消息
        protected internal virtual Msger.Msg getMsg(string msg, string userID_To = "@*测试群", bool isUsrGroup = false, typeMsg typeMsg = typeMsg.TEXT, typeMsger typeMsger = typeMsger.wx, string msgTag = "")
        {
            if (msg + "" == "") return null;
            if (userID_To + "" == "") return null;
            if (typeMsger == typeMsger.None) return null;

            //组装消息
            if (!isUsrGroup)
                isUsrGroup = userID_To.Length > 2 && userID_To.Substring(0, 2) == "@*" ? true : isUsrGroup;
            Msger.Msg pMsg = new Msger.Msg()
            {
                msgID = "",
                msg = msg + "",
                msgType = typeMsg == typeMsg.NOTE ? typeMsg.TEXT : typeMsg,
                msgLink = "",
                groupID = isUsrGroup ? userID_To : "",
                usrName = userID_To,
                usrNameNick = userID_To,
                usrPlat = typeMsger,
                UserName_src = _tag,
                msgTime = DateTime.Now,
                msgTag = msgTag,
                IsUserGroup = isUsrGroup,
                IsFromRobot = true,
                IsSend = true
            };
            return pMsg;
        }
        //提取返回消息-前缀
        protected internal virtual string getMsg_Perfix(Msger.Msg msg)
        {
            //组装消息
            return "";
        }
        //提取返回消息-中缀
        protected internal virtual string getMsg_Infix(Msger.Msg msg)
        {
            return "";
        }
        //提取返回消息-后缀
        protected internal virtual string getMsg_Suffix(Msger.Msg msg)
        {
            return string.Format("\n--zxcRobot({0}) {1}", _tag, DateTime.Now.ToString("HH:mm:ss"));
        }

    }
}
