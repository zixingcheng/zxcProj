//===============================================================================
// Copyright @ 2021 Guangzhou Yijian Life Technology Co.,Ltd. All rights reserved.
// Copyright @ 2021 广州易简生活科技有限公司.  版权所有.
//===============================================================================
// 文件名称： 
// 功能描述：zxcRobot_Quote --机器人-行情量化管理
// 创建标识：zxc   2021-06-19
// 修改标识： 
// 修改描述：
//===============================================================================
using System;
using zxcCore.Common;
using zxcCore.zxcRobot.Msger;
using zxcCore.zxcRobot.Robot.Power;
using zxcCore.zxcRobot.User;

namespace zxcCore.zxcRobot.Robot
{
    /// <summary>命令信息集合-行情量化管理
    /// </summary>
    public class CmdInfos_QuoteQuantify : RobotCmd_Infos
    {
        #region 属性及构造

        public CmdInfos_QuoteQuantify(string[] strCmds, Power_Robot powerRobot) : base(strCmds, powerRobot)
        {
        }

        #endregion

        public override bool Init(string[] strCmds)
        {
            //"@新增 5分 放学自觉读书"
            if (strCmds.Length < 3)
            {
                Power_Robot_UserSet pUserSet = this.PowerRobot.UserSets.Find(e => e.SetTag == strCmds[0]);
                if (pUserSet == null) return false;

                CmdPermission = pUserSet.SetPermission;
                PointsNum = Convert.ToInt32(pUserSet.SetValue);
                NoteInfo = pUserSet.SetTag;
                NoteLabel = pUserSet.SetLabel;
                Remark = pUserSet.Remark;
                if (Remark == "" && strCmds.Length > 1)
                    Remark = strCmds[1];
                strCmds = new[] { strCmds[0], PointsNum.ToString(), NoteInfo, Remark };
            }
            else
            {
                PointsNum = Convert.ToInt32(strCmds[1].Replace("分", ""));
                NoteInfo = strCmds[2];
                if (strCmds.Length > 3)
                    NoteLabel = strCmds[3];
                else
                    if (NoteInfo.Contains("赠送"))
                    NoteLabel = "赠送";
            }
            return base.Init(strCmds);
        }
    }


    /// <summary>机器人-行情量化管理
    /// </summary>
    public class zxcRobot_Quote_quantify : RobotBase
    {
        #region 属性及构造

        //成长宝贝点表
        //protected internal DataTable_Points_Growth<Data_Points> _growthPoints = null;
        //protected internal string _pointsType = "quantify";

        public zxcRobot_Quote_quantify(IUser User, string setting) : base(User, "zxcRobot_Quote", "quantify", setting)
        {
            _Title = "量化";
            _tagAlias = "行情管理";
            _CmdStr = "@@Quantify";  //启动命令
            _hasTitle = true;
            //_growthPoints = Robot_Manager._dbRobot._growthPoints;

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
        ~zxcRobot_Quote_quantify()
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

        //初始机器人功能命令信息
        protected internal override RobotCmd_Infos _Init_CmdInfo(string[] strCmds, Power_Robot powerRobot)
        {
            return new CmdInfos_QuoteQuantify(strCmds, powerRobot);
        }


        /// <summary>消息处理实现
        /// </summary>
        /// <returns></returns>
        public override bool HandleMsg_Do(RobotCmd pRobotCmd)
        {
            Msg msg = pRobotCmd.MsgInfo;
            if (msg.msgType.ToString().ToUpper() != "TEXT") return false;

            //解析命令
            string strCmd = pRobotCmd.CmdInfos.Cmdstr;
            switch (strCmd)
            {
                case "股票":
                    return _Done_Quote_query(msg, pRobotCmd);
                default:
                    break;
            }
            return false;
        }

        //积分添加
        protected internal bool _Done_Quote_query(Msg msg, RobotCmd pRobotCmd, typePermission_PowerRobot pPermission = typePermission_PowerRobot.ReadOnly)
        {
            //用户权限判断
            Power_Robot pPowerRobot = pRobotCmd.CmdInfos.PowerRobot;
            if (!this._Check_Permission_usr(pPermission, msg, pPowerRobot))
                return false;

            //查询操作 

            return false;
        }

    }

}
