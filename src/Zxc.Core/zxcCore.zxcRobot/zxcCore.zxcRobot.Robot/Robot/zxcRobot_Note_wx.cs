using System;
using System.Collections.Generic;
using System.Globalization;
using System.IO;
using System.Xml.Linq;
using zxcCore.Common;
using zxcCore.zxcRobot.Monitor.Msg;
using zxcCore.zxcRobot.Msger;
using zxcCore.zxcRobot.User;

namespace zxcCore.zxcRobot.Robot
{
    /// <summary>机器人-消息回撤(wx)
    /// </summary>
    public class zxcRobot_Note_wx : RobotBase
    {
        #region 属性及构造

        protected internal Random _random = new Random(DateTime.Now.Millisecond);
        /// <summary>消息回复前缀
        /// </summary>
        protected internal List<string> _perfixRevoke = new List<string>()
        { "告诉你一个秘密，", "偷偷告诉你哦，", "哈哈，发现你了！", "万能的机器人告诉我，", "小样，被我发现了吧。", "别想跑哦，我看到你了，"};

        public zxcRobot_Note_wx(IUser User, string setting) : base(User, "zxcRobot_Note", "wx", setting)
        {
            _Title = "通知消息";
            _tagAlias = "通知消息";
            _CmdStr = "@@zxcRobot_Note";

            //权限信息初始
            this._Permission.ValidMaxTime = -1;
            this._Permission.IsSingleUse = true;
            this._Permission.IsBackProc = true;

            //注册功能
            if (this._Permission.IsSingleUse && this._Permission.IsBackProc)
            {
                this.Done_Regist(User, new Msg(_CmdStr), true);
            }
        }
        ~zxcRobot_Note_wx()
        {
            // 缓存数据？
        }

        #endregion

        /// <summary>初始配置信息
        /// </summary>
        /// <param name="setting"></param>
        /// <returns></returns>
        public override bool InitSetting(dynamic setting)
        {
            return true;
        }


        /// <summary>消息处理实现
        /// </summary>
        /// <returns></returns>
        public override bool HandleMsg_Do(Msg msg)
        {
            string strReturn = "";
            if (msg.msgType.ToString().ToUpper() != "NOTE") return false;

            //解析通知
            string noteTag = "";
            if (msg.msg.IndexOf("撤回了一条消息") > 0)
            {
                noteTag = "REVOKE";
                return this._Done_Revoke(msg);
            }
            else if (msg.msg.IndexOf("收到转账") > 0)
            {
                noteTag = "PAY";
                return this._Done_Pay(msg);
            }
            return false;
        }

        //消息撤回通知
        public bool _Done_Revoke(Msg msg)
        {
            //提取xml结果
            //"<sysmsg type="revokemsg"><revokemsg><session>wxid_xf3qaf1sj26622</session><oldmsgid>1137787376</oldmsgid><msgid>3098631128678888933</msgid><replacemsg><![CDATA["茶叶一主号" 撤回了一条消息]]></replacemsg></revokemsg></sysmsg>",
            XElement pElemment = msg.GetMsg_ForXml();
            if (pElemment == null) return false;

            //提取旧消息ID
            string msgID = pElemment.Element("revokemsg").Element("msgid").Value;
            List<Msg> msgs = MsgerHelper.Msger.FindMsg(e => e.msgID == msgID);
            if (msgs.Count < 1) return false;

            //返回消息通知
            int ind = _random.Next(0, _perfixRevoke.Count - 1);
            string strMsg = string.Format("{0}「{1}」撤回了条消息。\n消息内容：\"{2}\"", _perfixRevoke[ind], msg.usrNameNick, msgs[0].msg);

            ConsoleHelper.Debug(true, "消息回撤：「{1}」撤回消息：\"{1}\"", msg.usrNameNick, msgs[0].msg);
            this.NotifyMsg(strMsg, msg, "消息回撤");
            return true;
        }
        //消息转账通知
        public bool _Done_Pay(Msg msg)
        {
            return true;
        }

    }
}
