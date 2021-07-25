//===============================================================================
// Copyright @ 2021 Guangzhou Yijian Life Technology Co.,Ltd. All rights reserved.
// Copyright @ 2021 广州易简生活科技有限公司.  版权所有.
//===============================================================================
// 文件名称： 
// 功能描述：zxcRobot_Point_growth --机器人-积分管理(成长)
// 创建标识：zxc   2021-06-16
// 修改标识： 
// 修改描述：
//===============================================================================
using System;
using zxcCore.Common;
using zxcCore.zxcRobot.Msger;
using zxcCore.zxcRobot.Robot.Power;
using zxcCore.zxcRobot.User;
using zxcCore.zxcStudy.Word;

namespace zxcCore.zxcRobot.Robot
{
    /// <summary>命令信息集合-成长宝贝点
    /// </summary>
    public class CmdInfos_PointsGrowth : RobotCmd_Infos
    {
        #region 属性及构造

        /// <summary>点数
        /// </summary>
        public int PointsNum
        {
            get; set;
        }


        public CmdInfos_PointsGrowth(string[] strCmds, Power_Robot powerRobot) : base(strCmds, powerRobot)
        {
        }

        #endregion

        public override bool Init(string[] strCmds)
        {
            //"@新增 5分 放学自觉读书"
            if (strCmds.Length < 3)
            {
                if (PowerRobot == null) return base.Init(strCmds);
                Power_Robot_UserSet pUserSet = this.PowerRobot.UserSets.Find(e => e.SetTag == strCmds[0]);
                if (pUserSet == null) return base.Init(strCmds);

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
            this.IsVaild = true;
            return base.Init(strCmds);
        }
    }


    /// <summary>机器人-积分管理(成长)
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
                    return _Done_Points_operation(msg, pRobotCmd);
                case "识字":
                    return _Done_Points_StudyWord(msg, pRobotCmd);
                case "识字ok":
                    return _Done_Points_StudyWord_ok(msg, pRobotCmd);
                default:
                    return _Done_Points_operation(msg, pRobotCmd, pRobotCmd.CmdInfos.CmdPermission);
            }
            return false;
        }

        //识字学习
        protected internal bool _Done_Points_StudyWord(Msg msg, RobotCmd pRobotCmd, typePermission_PowerRobot pPermission = typePermission_PowerRobot.Writable)
        {
            //用户权限判断
            Power_Robot pPowerRobot = pRobotCmd.CmdInfos.PowerRobot;
            if (!this._Check_Permission_usr(pPermission, msg, pPowerRobot))
                return false;

            //汉字识字
            Word pWord = Word_Manager._Manager.GetWord_ByUser(pRobotCmd.CmdInfos.NoteUserTag);

            //信息提示
            CmdInfos_PointsGrowth pGrowthPoints = (CmdInfos_PointsGrowth)pRobotCmd.CmdInfos;
            string strMsg = string.Format("新汉字：【{0}】\n识字奖励：{1} 宝贝分.\n发布人：{2}", pWord.WordStr, pGrowthPoints.PointsNum, pPowerRobot.NameUserAlias);
            this.NotifyMsg(strMsg, msg, "宝贝学习（识字）");


            //发送字形图片
            string strWordImg = pWord.Get_Image();
            this.NotifyMsg(strWordImg, msg, "", typeMsg.IMAGE);

            //发送字音文件
            string strWordSound = pWord.Get_Sound();
            this.NotifyMsg(strWordSound, msg, "", typeMsg.FILE);

            //发送字笔画gif
            //string strWordStrokesImg = pWord.Get_StrokesImage();
            //this.NotifyMsg(strWordStrokesImg, msg, "", typeMsg.IMAGE);
            return true;
        }
        protected internal bool _Done_Points_StudyWord_ok(Msg msg, RobotCmd pRobotCmd, typePermission_PowerRobot pPermission = typePermission_PowerRobot.Writable)
        {
            //汉字识字
            Word pWord = Word_Manager._Manager.GetWord_ByUser(pRobotCmd.CmdInfos.NoteUserTag);

            //积分变动
            if (Word_Manager._Manager.InitWord_Record(pRobotCmd.CmdInfos.NoteUserTag, pWord, zxcStudy.Record.typeWordRecord.字形, "已学"))
            {
                _Done_Points_operation(msg, pRobotCmd, pPermission, string.Format("新识【{0}】字（{1}）", pWord.WordStr, zxcStudy.Record.typeWordRecord.字形.ToString()));
            }
            if (Word_Manager._Manager.InitWord_Record(pRobotCmd.CmdInfos.NoteUserTag, pWord, zxcStudy.Record.typeWordRecord.字音, "已学"))
            {
                _Done_Points_operation(msg, pRobotCmd, pPermission, string.Format("新识【{0}】字（{1}）", pWord.WordStr, zxcStudy.Record.typeWordRecord.字音.ToString()));
            }
            return true;
        }


        //积分添加
        protected internal bool _Done_Points_operation(Msg msg, RobotCmd pRobotCmd, typePermission_PowerRobot pPermission = typePermission_PowerRobot.Writable, string strReasonDetial = "")
        {
            //用户权限判断
            Power_Robot pPowerRobot = pRobotCmd.CmdInfos.PowerRobot;
            if (!this._Check_Permission_usr(pPermission, msg, pPowerRobot))
                return false;

            //积分操作
            bool checkPoints = pRobotCmd.CmdInfos.NoteLabel == "兑换" ? true : false;
            Data_PointsLog pDataLog = _growthPoints.Add_Points((CmdInfos_PointsGrowth)pRobotCmd.CmdInfos, pPowerRobot.NameUserAlias, checkPoints);
            if (pDataLog != null)
            {
                string strPerfix = pDataLog.PointExChange > 0 ? "恭喜！" : pDataLog.PointsNote_Label != "" ? "" : "很遗憾！";
                string strMidfix = pDataLog.PointExChange > 0 ? "获得" + pDataLog.PointsNote_Label + "！" : pDataLog.PointsNote_Label == "兑换" ? "兑换成功！" : "被" + pDataLog.PointsNote_Label + "！";

                string strNumExChange = pDataLog.PointExChange > 0 ? "+" + pDataLog.PointExChange.ToString() : pDataLog.PointExChange.ToString();
                string strExchange = pDataLog.PointExChange > 0 ? "新增" : "被扣除";
                string strReason = strExchange.Replace("被", "") + "原由";
                string strRemark = string.IsNullOrEmpty(pDataLog.Remark) ? "" : string.Format("({0}).", pDataLog.Remark);
                if (pDataLog.PointsNote_Label == "兑换")
                {
                    strReason = "兑换内容";
                }
                else if (pDataLog.PointsNote_Label == "奖励")
                    strReason = "奖励原由";

                if (pDataLog.IsValid)
                {
                    string strMsg = string.Format("{0}{1}「{2}」{3} 个宝贝分.", strMidfix, strPerfix, pDataLog.PointsUser, strNumExChange);
                    strMsg = string.Format("{0}\n{1}：{2}{3}\n审核人：{4}\n当前分：{5} 宝贝分", strMsg, strReason, strReasonDetial != "" ? strReasonDetial : pDataLog.PointsNote, strRemark, pDataLog.PointsUser_OP, pDataLog.PointsNow);

                    zxcConsoleHelper.Debug(true, "宝贝分变动：\n{0}", strMsg);
                    this.NotifyMsg(strMsg, msg, "宝贝分变动");
                    return true;
                }
                else
                {
                    string strMsg = string.Format("兑换失败！{0}：{1}{2} 需要 {3} 宝贝分，当前 {4} 个宝贝分，不足以兑换.", strReason, pDataLog.PointsNote, strRemark, strNumExChange, pDataLog.PointsNow);
                    zxcConsoleHelper.Debug(true, "宝贝分提示：\n{0}", strMsg);
                    this.NotifyMsg(strMsg, msg, "宝贝分提示");
                }
            }
            return false;
        }

    }

}
