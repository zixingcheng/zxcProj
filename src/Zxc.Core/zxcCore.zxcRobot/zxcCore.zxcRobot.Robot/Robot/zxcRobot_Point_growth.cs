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
using System.Collections.Generic;
using System.Globalization;
using System.IO;
using System.Xml.Linq;
using zxcCore.Common;
using zxcCore.zxcRobot.Monitor.Msg;
using zxcCore.zxcRobot.Msger;
using zxcCore.zxcRobot.Robot.Power;
using zxcCore.zxcRobot.User;

namespace zxcCore.zxcRobot.Robot
{
    /// <summary>机器人-消息回撤(成长)
    /// </summary>
    public class zxcRobot_Point_growth : RobotBase
    {
        #region 属性及构造

        public zxcRobot_Point_growth(IUser User, string setting) : base(User, "zxcRobot_Point", "growth", setting)
        {
            _Title = "成长积分";
            _tagAlias = "成长积分";
            _CmdStr = "@@PointGrowth";  //启动命令

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
        public override bool InitSetting(dynamic setting)
        {
            return true;
        }


        /// <summary>消息处理实现
        /// </summary>
        /// <returns></returns>
        public override bool HandleMsg_Do(Msg msg)
        {
            if (msg.msgType.ToString().ToUpper() != "TEXT") return false;

            //解析命令
            string strCmd = msg.msg;
            string[] strCmds = strCmd.Split("@");
            if (strCmds.Length - 1 != 1) return false;

            strCmds = strCmds[1].Split(" ");
            strCmd = strCmds[0];
            switch (strCmd)
            {
                case "新增":
                    return _Done_Points_add(msg, strCmds);
                default:
                    break;
            }
            return false;
        }

        //积分添加
        public bool _Done_Points_add(Msg msg, string[] strCmds)
        {
            //提取权限设置
            Power_Robot pPower = _Permission.Get_Permission(_tag, msg.GetNameGroup(), msg.GetNameUser(), msg.usrPlat.ToString());
            return true;
        }

    }
}
