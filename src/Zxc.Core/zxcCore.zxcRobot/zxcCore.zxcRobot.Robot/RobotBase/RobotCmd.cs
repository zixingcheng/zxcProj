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

        protected internal RobotCmd_Infos _CmdInfos = null;
        /// <summary>解析后消息内容
        /// </summary>
        public RobotCmd_Infos CmdInfos
        {
            get { return _CmdInfos; }
        }

        public RobotCmd(string cmdstr, Msg msgInfo, RobotCmd_Infos cmdInfos = null)
        {
            Cmdstr = cmdstr;
            _MsgInfo = msgInfo;
            this.Init_CmdInfos(cmdInfos);
        }
        ~RobotCmd()
        {
            // 缓存数据？
        }

        /// <summary>初始解析后消息内容
        /// </summary>
        /// <param name="cmdInfos"></param>
        /// <returns></returns>
        public bool Init_CmdInfos(RobotCmd_Infos cmdInfos = null)
        {
            _CmdInfos = cmdInfos;
            return true;
        }
    }


    /// <summary>命令信息集合
    /// </summary>
    public class RobotCmd_Infos
    {
        #region 属性及构造

        /// <summary>命令字符串
        /// </summary>
        public string Cmdstr
        {
            get; set;
        }
        /// <summary>命令字符串集
        /// </summary>
        public string[] Cmdstrs
        {
            get; set;
        }

        /// <summary>点数
        /// </summary>
        public int PointsNum
        {
            get; set;
        }

        /// <summary>标记的用户标签
        /// </summary>
        public string NoteUserTag
        {
            get; set;
        }
        /// <summary>标记信息
        /// </summary>
        public string NoteInfo
        {
            get; set;
        }

        /// <summary>备注信息
        /// </summary>
        public string Remark
        {
            get; set;
        }

        /// <summary>机器人功能权限设置信息
        /// </summary>
        public Power_Robot PowerRobot
        {
            get; set;
        }


        public RobotCmd_Infos(string[] strCmds, Power_Robot powerRobot)
        {
            this.Init_Power(powerRobot);
            this.Init(strCmds);
        }
        ~RobotCmd_Infos()
        {
            // 缓存数据？
        }

        #endregion

        /// <summary>初始命令信息-外部重写
        /// </summary>
        /// <returns></returns>
        public virtual bool Init(string[] strCmds)
        {
            Cmdstrs = strCmds;
            Cmdstr = strCmds[0];
            return true;
        }

        /// <summary>初始机器人功能权限设置信息
        /// </summary>
        /// <returns></returns>
        public virtual bool Init_Power(Power_Robot powerRobot)
        {
            PowerRobot = powerRobot;
            if (PowerRobot != null)
            {
                NoteUserTag = powerRobot.BindTag;
            }
            return true;
        }

    }
}
