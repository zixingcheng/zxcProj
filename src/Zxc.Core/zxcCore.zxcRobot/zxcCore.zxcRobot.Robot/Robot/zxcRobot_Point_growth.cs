//===============================================================================
// Copyright @ 2021 Guangzhou Yijian Life Technology Co.,Ltd. All rights reserved.
// Copyright @ 2021 广州易简生活科技有限公司.  版权所有.
//===============================================================================
// 文件名称： 
// 功能描述：zxcRobot_Note_wx --机器人-积分管理(成长)
// 创建标识：zxc   2021-06-16
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
    /// <summary>命令信息集合-成长宝贝点
    /// </summary>
    public class CmdInfos_PointsGrowth : RobotCmd_Infos
    {
        #region 属性及构造

        public CmdInfos_PointsGrowth(string[] strCmds, Power_Robot powerRobot) : base(strCmds, powerRobot)
        {
        }

        #endregion

        public override bool Init(string[] strCmds)
        {
            //"@新增 5分 放学自觉读书"
            if (strCmds.Length < 3) return false;
            PointsNum = Convert.ToInt32(strCmds[1].Replace("分", ""));
            NoteInfo = strCmds[2];
            if (strCmds.Length > 3) Remark = strCmds[3];
            return base.Init(strCmds);
        }
    }


    /// <summary>机器人-消息回撤(成长)
    /// </summary>
    public class zxcRobot_Point_growth : RobotBase
    {
        #region 属性及构造

        //成长宝贝点表
        protected internal DataTable_Points_Growth<Data_Points> _growthPoints = null;
        protected internal string _pointsType = "growth";

        public zxcRobot_Point_growth(IUser User, string setting) : base(User, "zxcRobot_Point", "growth", setting)
        {
            _Title = "宝贝积分";
            _tagAlias = "宝贝积分";
            _CmdStr = "@@PointGrowth";  //启动命令
            _hasTitle = true;
            _growthPoints = Robot_Manager._dbRobot._growthPoints;

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
        ~zxcRobot_Point_growth()
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
            return new CmdInfos_PointsGrowth(strCmds, powerRobot);
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
                case "新增":
                    return _Done_Points_add(msg, pRobotCmd);
                default:
                    break;
            }
            return false;
        }

        //积分添加
        protected internal bool _Done_Points_add(Msg msg, RobotCmd pRobotCmd)
        {
            //用户权限判断
            if (!this._Check_Permission_usr(typePermission_PowerRobot.Writable, msg, pRobotCmd.CmdInfos.PowerRobot)) return false;

            //添加积分
            Data_PointsLog pDataLog = _growthPoints.Add_Points(pRobotCmd.CmdInfos);
            if (pDataLog != null)
            {
                string strPerfix = pDataLog.PointExChange > 0 ? "恭喜！" : "很遗憾！";
                string strExchange = pDataLog.PointExChange > 0 ? "新增" : "被扣除";
                string strMsg = string.Format("{0}「{1}」{2} {3} 个宝贝分.", strPerfix, pDataLog.PointsUser, strExchange, pDataLog.PointExChange);
                strMsg = string.Format("{0}\n{1}原由：{2}\n审核人：{3}\n当前分：{4} 宝贝分.", strMsg, strExchange.Replace("被", ""), pDataLog.PointsNote, pRobotCmd.CmdInfos.PowerRobot.NameUserAlias, pDataLog.PointsNow);

                ConsoleHelper.Debug(true, "宝贝积分：\n{0}", strMsg);
                this.NotifyMsg(strMsg, msg, "宝贝积分");
            }
            return pDataLog == null;
        }

    }
}
