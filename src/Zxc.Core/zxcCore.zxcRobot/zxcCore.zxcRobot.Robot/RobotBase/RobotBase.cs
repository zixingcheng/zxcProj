using System;
using System.Collections.Generic;
using System.Linq;
using zxcCore.Common;
using zxcCore.zxcRobot.Monitor.Msg;
using zxcCore.zxcRobot.Msger;
using zxcCore.zxcRobot.Robot.Power;
using zxcCore.zxcRobot.User;

namespace zxcCore.zxcRobot.Robot
{
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
        protected internal bool _checkAllMsg = false;
        protected internal bool _hasTitle = false;
        /// <summary>配置文件信息
        /// </summary>
        protected internal zxcConfigurationHelper _configDataCache = new zxcConfigurationHelper("appsettings.json");
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
            this.Init_Permissions();
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
        public override bool Init_Setting(dynamic setting)
        {
            return true;
        }
        //初始用户功能权限
        protected internal virtual bool Init_Permissions()
        {
            string configMidFix = _configMidFix;
            if (_Permission == null)
                _Permission = new RobotPermission(_tag, configMidFix);
            return true;
        }
        //用户功能权限判断
        protected internal bool _Check_Permission_usr(typePermission_PowerRobot usrPermission, Msg msg, Power_Robot pPower = null)
        {
            //提取权限设置
            bool bPermission = false;
            if (pPower == null)
                pPower = _Permission.Get_Permission(_Permission._configTag, msg.GetNameGroup(), msg.GetNameUser(), msg.usrPlat.ToString());
            if (pPower != null)
            {
                //权限判断
                if ((usrPermission & pPower.UsrPermission) == usrPermission)
                {
                    bPermission = true;
                }
            }

            //无操作权限提示
            if (bPermission == false)
            {
                this.NotifyMsg("权限不足，请联系管理员！", msg, "权限检测(" + this.Title + ")");
            }
            return bPermission;
        }

        //初始机器人功能命令信息
        protected internal virtual RobotCmd Init_CmdInfo(Msg msg)
        {
            if (msg == null) return null;

            //解析命令
            string strCmd = msg.msg.Trim();
            if (strCmd.Length < 2) return null;
            if (!_checkAllMsg && strCmd.Substring(0, 1) != "@") return null;

            //提取命令头
            string perfixCmd = strCmd.Substring(0, 2);
            bool bStartCmd = strCmd.Length >= _CmdStr.Length && strCmd.Substring(0, _CmdStr.Length) == _CmdStr;
            if (perfixCmd != "@@" && perfixCmd != "@*")
            {
                //@个人
                if (!_checkAllMsg)
                    return null;
                else
                    perfixCmd = "";
            }

            //解析命令
            string[] strCmds = strCmd.Split(perfixCmd);
            string strCmdtemp = strCmds.Length <= 1 ? strCmds[0] : strCmds[1];
            strCmds = strCmdtemp.Split(" ");
            strCmd = strCmds[0];

            //启动命令检测
            if (bStartCmd)
            {
                strCmd = "@@" + strCmd;
                if (strCmds.Length - 1 != 1) return null;
                if (strCmd != _CmdStr) return null;
            }

            //解析命令
            Power_Robot pPower = _Permission.Get_Permission(_Permission._configTag, msg.GetNameGroup(), msg.GetNameUser(), msg.usrPlat.ToString());
            RobotCmd_Infos cmdInfos = this._Init_CmdInfo(strCmds, pPower);

            //初始命令信息
            RobotCmd pRobotCmd = new RobotCmd(strCmd, msg, cmdInfos);
            //_Cmds.Add(pRobotCmd);                    //记录命令信息
            return pRobotCmd;
        }
        protected internal virtual RobotCmd_Infos _Init_CmdInfo(string[] strCmds, Power_Robot powerRobot)
        {
            return new RobotCmd_Infos(strCmds, powerRobot);
        }


        /// <summary>处理消息
        /// </summary>
        /// <param name="msg"></param>
        /// <returns></returns>
        public override bool HandleMsg(Msg msg)
        {
            //解析命令
            RobotCmd pRobotCmd = this.Init_CmdInfo(msg);
            if (pRobotCmd == null) return false;
            if (!pRobotCmd.CmdInfos.IsVaild) return false;

            //剔除非命令触发（全命令触发类型）
            if (!_checkAllMsg && pRobotCmd.CmdInfos.Cmdstrs.Length <= 1)
                return false;

            //权限检查
            if (!this.HandleMsg_Check(msg))
                return false;

            //启动命令-注册/反注册
            if (pRobotCmd.Cmdstr == _CmdStr)
            {
                this.Done_Regist(null, pRobotCmd.MsgInfo, !this._Permission.IsRunning);
                _Cmds.Add(pRobotCmd);                    //记录命令信息
                return true;
            }

            //消息处理
            if (this.HandleMsg_Do(pRobotCmd))
            {
                _Cmds.Add(pRobotCmd);                    //记录命令信息
                return true;
            }
            return false;
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
        public virtual bool HandleMsg_Do(RobotCmd pRobotCmd)
        {
            return true;
        }


        /// <summary>消息处理注册
        /// </summary>
        /// <param name="usr">用户对象</param>
        /// <param name="bRegistOut">是否反注册</param>
        /// <returns></returns>
        public virtual string Done_Regist(IUser usr, Msg msg, bool bRegistOut = false, bool bSysTrigger = true)
        {
            if (msg == null) return "";
            if (msg.msg != _CmdStr) return "";

            //实例命令信息
            if (bSysTrigger)
            {
                RobotCmd pCmd = new RobotCmd(_CmdStr, msg);
                _Cmds.Add(pCmd);
            }

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
        public virtual bool NotifyMsg(dynamic msg, Msg msgSrc, string msgTag = "", typeMsg typeMsg = typeMsg.NONE)
        {
            if (msg + "" != null)
            {
                Msg pMsg = _ReturnMsg(msg, msgSrc, msgTag, typeMsg);
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
        public virtual Msg _ReturnMsg(string text, Msg msgSrc, string msgTag = "", typeMsg typeMsg = typeMsg.NONE)
        {
            return _ReturnMsg(text, msgSrc, typeMsg == typeMsg.NONE ? msgSrc.msgType : typeMsg, msgTag);
        }
        /// <summary>返回消息
        /// </summary>
        /// <param name="text"></param>
        /// <param name="msgSrc"></param>
        /// <param name="typeMsg"></param>
        /// <returns></returns>
        public virtual Msg _ReturnMsg(string text, Msg msgSrc, typeMsg typeMsg, string msgTag = "")
        {
            string userID_To = msgSrc.UserName_src;
            typeMsger typeMsger = msgSrc.usrPlat;

            //修正消息
            bool isGroup = msgSrc.IsUserGroup;
            string usrGroup = msgSrc.GetNameGroup();
            string usrName = msgSrc.GetNameUser();
            if (_Permission.Check_Permission_SysUsr(usrName, msgSrc.usrPlat.ToString()) ||
                !this._Permission.Check_Permission_SingleSet(usrGroup, usrName, msgSrc.usrPlat.ToString()))
            {
                //查询用户信息--系统管理员屏蔽
                userID_To = "filehelper";       //非独立设置调整为发送Helper
                isGroup = false;

                //修正消息内容，现实群组信息
                string strTag = string.IsNullOrEmpty(msgTag) ? _Title : msgTag;
                if (msgSrc.IsUserGroup)
                {
                    string strMsg_Group = string.Format("{0}：〖{1}〗\n", strTag, msgSrc.GetNameGroup());
                    text = strMsg_Group + text;
                }
                else
                {
                    string strMsg_Group = string.Format("{0}：『{1}』\n", strTag, msgSrc.GetNameUser());
                    text = strMsg_Group + text;
                }
            }
            else
            {
                //添加文件头
                if (_hasTitle)
                {
                    if (typeMsg == typeMsg.TEXT)
                    {
                        string strTag = string.IsNullOrEmpty(msgTag) ? _Title : msgTag;
                        if (!strTag.Contains("：")) strTag += "：";
                        text = strTag + "\n" + text;
                    }
                }
            }

            //生成消息
            Msg pMsgR = this.getMsg(text, userID_To, isGroup, typeMsg, typeMsger, msgTag);
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
                        strReturn += "已注册." + this._Title_User_Opened() + "  -- " + _Cmds[0].CmdTime.ToString() + ".";
                    }
                    else
                    {
                        strReturn += "已注销." + this._Title_User_Opened() + "  -- " + _Cmds[_Cmds.Count - 1].CmdTime.ToString() + ".";
                    }
                }
                else
                {
                    this._Permission.IsRunning = false;      //标识运行结束
                    strReturn += "已关闭." + this._Title_User_Opened() + "  -- " + _Cmds[0].CmdTime.ToString() + ".";
                }
            }
            else
            {
                this.Init_Setting("");                       //初始基础信息
                this._Permission.IsRunning = true;           //标识运行
                this._Permission.TimeStartRun = DateTime.Now;
                strReturn += "已注册." + this._Title_User_Opened() + "  -- " + _Cmds[_Cmds.Count - 1].CmdTime.ToString() + ".";
            }

            zxcConsoleHelper.Print(false, strTitle);
            zxcConsoleHelper.Debug(false, strReturn);
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
