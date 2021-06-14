using System;
using System.Collections.Generic;
using System.Linq;
using zxcCore.Common;
using zxcCore.zxcRobot.Monitor.Msg;
using zxcCore.zxcRobot.Msger;
using zxcCore.zxcRobot.User;

namespace zxcCore.zxcRobot.Robot
{
    /// <summary>命令信息
    /// </summary>
    public class RobotCmd
    {
        /// <summary>命令字符串
        /// </summary>
        public string Cmdstr
        {
            get; set;
        }

        protected internal DateTime _CmdTime = DateTime.Now;
        /// <summary>命令时间
        /// </summary>
        public DateTime CmdTime
        {
            set { _CmdTime = value; }
            get { return _CmdTime; }
        }

        protected internal Msg _MsgInfo = null;
        /// <summary>原始消息内容
        /// </summary>
        public Msg MsgInfo
        {
            set { _MsgInfo = value; }
            get { return _MsgInfo; }
        }
    }


    /// <summary>机器人-基类
    /// </summary>
    public abstract class RobotBase : MsgHandle
    {
        #region 属性及构造

        protected internal string _Title = "";
        /// <summary>说明
        /// </summary>
        public string Title
        {
            get { return _Title; }
        }
        protected internal string _CmdStr = "";
        /// <summary>启动命令
        /// </summary>
        public string CmdStr
        {
            get { return _CmdStr; }
        }


        protected internal RobotPermission _Permission = null;
        /// <summary>功能权限信息
        /// </summary>
        public RobotPermission Permission
        {
            get { return _Permission; }
        }


        protected internal IUser _User = null;
        /// <summary>归属用户
        /// </summary>
        public IUser User
        {
            get { return _User; }
        }

        protected internal List<Msg> _Msgs = new List<Msg>();
        /// <summary>归属用户
        /// </summary>
        public List<Msg> Msgs
        {
            get { return _Msgs; }
        }
        protected internal List<RobotCmd> _Cmds = new List<RobotCmd>();
        /// <summary>归属用户
        /// </summary>
        public List<RobotCmd> Cmds
        {
            get { return _Cmds; }
        }

        //参数配置节点-中间缀
        protected internal string _configMidFix = "";
        public RobotBase(IUser User, string tag, string configMidFix, string setting) : base(tag, setting)
        {
            _Title = "机器人基类";
            _tagAlias = "机器人基类";
            _CmdStr = "@@myRobot";
            _configMidFix = configMidFix;
            _User = User;

            //权限信息初始
            //this._Permission.IsValid = false;
            //this._Permission.ValidMaxTime = -1;
            //this._Permission.IsSingleUse = true;
            //this._Permission.IsBackProc = true;
            this.InitPermissions();
        }
        ~RobotBase()
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
        protected internal virtual bool InitPermissions()
        {
            string configMidFix = _configMidFix;
            if (_Permission == null)
                _Permission = new RobotPermission(_tag, configMidFix);
            return true;
        }


        /// <summary>处理消息
        /// </summary>
        /// <param name="msg"></param>
        /// <returns></returns>
        public virtual bool HandleMsg(Msg msg)
        {
            if (!this.HandleMsg_Check(msg))
                return false;

            return this.HandleMsg_Do(msg);
        }
        /// <summary>消息检查
        /// </summary>
        /// <returns></returns>
        public override bool HandleMsg_Check(Msg msg)
        {
            bool isVaild = false;
            isVaild = this._Permission.Check_Permission(msg.GetNameGroup(), msg.GetNameUser(), msg.usrPlat.ToString());
            return isVaild;
        }
        /// <summary>消息处理实现
        /// </summary>
        /// <returns></returns>
        public override bool HandleMsg_Do(Msg msg)
        {
            return true;
        }


        /// <summary>消息处理注册
        /// </summary>
        /// <param name="usr">用户对象</param>
        /// <param name="bRegistOut">是否反注册</param>
        /// <returns></returns>
        public virtual string Done_Regist(IUser usr, Msg msg, bool bRegistOut = false)
        {
            if (msg == null) return "";
            if (msg.msg != _CmdStr) return "";

            //实例命令信息
            RobotCmd pCmd = new RobotCmd()
            {
                MsgInfo = msg,
                Cmdstr = this._CmdStr
            };
            _Cmds.Add(pCmd);

            //创建返回消息
            string strReturn = this._Title_User_Regist(usr, bRegistOut);
            if (this.NotifyMsg(strReturn, msg))
            {
                return strReturn;
            }
            return "";
        }


        /// <summary>消息通知
        /// </summary>
        /// <param name="msg"></param>
        /// <param name="userID_To"></param>
        /// <returns></returns>
        public virtual bool NotifyMsg(dynamic msg, Msg msgSrc)
        {
            if (msg + "" != null)
            {
                Msg pMsg = _ReturnMsg(msg, msgSrc);
                if (pMsg != null)
                    return MsgerHelper.Msger.SendMsg(pMsg, pMsg.usrPlat);
                //else
                //    ConsoleHelper.Debug(true, msg);
            }
            return false;
        }
        /// <summary>返回消息
        /// </summary>
        /// <param name="text"></param>
        /// <param name="msgSrc"></param>
        /// <returns></returns>
        public virtual Msg _ReturnMsg(string text, Msg msgSrc)
        {
            return _ReturnMsg(text, msgSrc, msgSrc.msgType);
        }
        /// <summary>返回消息
        /// </summary>
        /// <param name="text"></param>
        /// <param name="msgSrc"></param>
        /// <param name="typeMsg"></param>
        /// <returns></returns>
        public virtual Msg _ReturnMsg(string text, Msg msgSrc, typeMsg typeMsg)
        {
            string userID_To = msgSrc.UserName_src;
            typeMsger typeMsger = msgSrc.usrPlat;

            Msg pMsgR = this.getMsg(text, userID_To, msgSrc.IsUserGroup, typeMsg, typeMsger);
            return pMsgR;
        }

        /// <summary>用户注册功能提示信息
        /// </summary>
        /// <param name="usr"></param>
        /// <param name="bRegist"></param>
        /// <param name="bRegistOut"></param>
        /// <returns></returns>
        public virtual string _Title_User_Regist(IUser usr, bool bRegist = false, bool bRegistOut = false)
        {
            string strTitle = "机器人管理器::" + this._Title + "(robot)";
            string strReturn = "";
            if (this._Permission.IsRunning)
            {
                if (bRegist || bRegistOut)
                {
                    if (bRegistOut == false)
                    {
                        strReturn += "已注册" + this._Title_User_Opened() + "  -- " + _Cmds[0].CmdTime.ToString() + ".";
                    }
                    else
                    {
                        strReturn += "已注销" + this._Title_User_Opened() + "  -- " + _Cmds[_Cmds.Count - 1].CmdTime.ToString() + ".";
                    }
                }
                else
                {
                    this._Permission.IsRunning = false;      //标识运行结束
                    strReturn += "已关闭" + this._Title_User_Opened() + "  -- " + _Cmds[0].CmdTime.ToString() + ".";
                }
            }
            else
            {
                this.InitSetting("");                       //初始基础信息
                this._Permission.IsRunning = true;          //标识运行
                this._Permission.TimeStartRun = DateTime.Now;
                strReturn += "已注册" + this._Title_User_Opened() + "  -- " + _Cmds[_Cmds.Count - 1].CmdTime.ToString() + ".";
            }

            ConsoleHelper.Print(false, strTitle);
            ConsoleHelper.Debug(false, strReturn);
            return strTitle + "\n\t" + strReturn;
        }
        /// <summary>用户注册时消息
        /// </summary>
        /// <returns></returns>
        public virtual string _Title_User_Opened()
        {
            return "";
        }
        /// <summary>用户反注册时消息
        /// </summary>
        /// <returns></returns>
        public virtual string _Title_User_Closed()
        {
            return "";
        }

    }
}
