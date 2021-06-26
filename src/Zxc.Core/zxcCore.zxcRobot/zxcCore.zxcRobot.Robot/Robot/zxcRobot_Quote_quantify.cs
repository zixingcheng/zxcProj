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
using Newtonsoft.Json.Linq;
using System;
using System.Collections.Generic;
using zxcCore.Common;
using zxcCore.zxcRobot.Monitor;
using zxcCore.zxcRobot.Msger;
using zxcCore.zxcRobot.Quote;
using zxcCore.zxcRobot.Robot.Power;
using zxcCore.zxcRobot.User;

namespace zxcCore.zxcRobot.Robot
{
    /// <summary>命令信息集合-行情量化管理
    /// </summary>
    public class CmdInfos_QuoteQuantify : RobotCmd_Infos
    {
        #region 属性及构造

        /// <summary>标的名称
        /// </summary>
        public string StockName
        {
            get; set;
        }

        public CmdInfos_QuoteQuantify(string[] strCmds, Power_Robot powerRobot) : base(strCmds, powerRobot)
        {
        }

        #endregion

        public override bool Init(string[] strCmds)
        {
            //"@新增 5分 放学自觉读书"
            if (strCmds.Length < 2)
            {
                Power_Robot_UserSet pUserSet = this.PowerRobot.UserSets.Find(e => e.SetTag == strCmds[0]);
                if (pUserSet == null) return false;

                //CmdPermission = pUserSet.SetPermission; 
            }
            else
            {
                StockName = strCmds[1];
            }
            this.IsVaild = true;
            return base.Init(strCmds);
        }
    }


    /// <summary>机器人-行情量化管理
    /// </summary>
    public class zxcRobot_Quote_quantify : RobotBase
    {
        #region 属性及构造

        protected internal string _urlAPI_QuoteQuery = "";          //行情实时查询接口
        protected internal string _urlAPI_QuoteQueryHistory = "";   //行情实时历史查询接口

        public zxcRobot_Quote_quantify(IUser User, string setting) : base(User, "zxcRobot_Quote", "quantify", setting)
        {
            _Title = "行情量化";
            _tagAlias = "行情量化";
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

            //提取行情API配置
            _urlAPI_QuoteQuery = _configDataCache.config["ZxcRobot.Quote:QuoteAPI:QueryAPI_Url"] + "";
            _urlAPI_QuoteQueryHistory = _configDataCache.config["ZxcRobot.Quote:QuoteAPI:QueryHistoryAPI_Url"] + "";
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

            //查询标的 
            string[] stockNames = ((CmdInfos_QuoteQuantify)pRobotCmd.CmdInfos).StockName.Split(".");
            StockInfo pStockInfo = QuoteManager.Get_StockInfo(stockNames[0], stockNames.Length > 1 ? stockNames[1] : "");
            if (pStockInfo == null)
                return false;

            //调用接口
            string statusCode;
            string result = zxcNetHelper.Get_ByHttpClient(_urlAPI_QuoteQuery, pStockInfo.StockID_TagSina, out statusCode);

            //返回解析
            JObject jsonRes = JObject.Parse(result);
            if (jsonRes["result"].ToString() == "False")
            {
                //接口失败，调用历史接口查询
                string param = pStockInfo.StockID_TagJQ + "&dataFrequency=1d&stockBars=1";
                result = zxcNetHelper.Get_ByHttpClient(_urlAPI_QuoteQueryHistory, param, out statusCode);

                //再次解析
                jsonRes = JObject.Parse(result);
                if (jsonRes["result"].ToString() == "false")
                    return false;
            }

            //循环解析文件json数据
            List<Data_Quote_Swap> lstDataQuote = new List<Data_Quote_Swap>();
            JArray jsonDatas = (JArray)jsonRes["datas"];
            if (jsonDatas != null)
            {
                //循环生成数据对象
                foreach (var jsonData in jsonDatas)
                {
                    Data_Quote_Swap pDataQuote = new Data_Quote_Swap();
                    if (pDataQuote.FromJson(jsonData))
                        lstDataQuote.Add(pDataQuote);

                    string strMsg = pDataQuote.GetMsg_Perfix();
                    zxcConsoleHelper.Debug(true, "行情信息：\n{0}", strMsg);
                    this.NotifyMsg(strMsg, msg, "行情信息");
                }
            }

            return false;
        }

    }

}
