//===============================================================================
// Copyright @ 2021 Guangzhou Yijian Life Technology Co.,Ltd. All rights reserved.
// Copyright @ 2021 广州易简生活科技有限公司.  版权所有.
//===============================================================================
// 文件名称： 
// 功能描述：Robot_Manager --机器人管理类
// 创建标识：zxc   2021-06-14
// 修改标识： 
// 修改描述：
//===============================================================================
using System.Collections.Generic;
using zxcCore.zxcDataCache.MemoryDB;
using zxcCore.zxcRobot.Monitor.Msg;
using zxcCore.zxcRobot.Monitor.Quote;
using zxcCore.zxcRobot.Robot.Power;

namespace zxcCore.zxcRobot.Robot
{
    /// <summary>数据缓存集管理类集中管理类
    /// </summary>
    public class Robot_Manager
    {
        public static readonly DataDB_Robot _dbRobot = new DataDB_Robot();
        public static readonly Robot_Manager _Manager = new Robot_Manager();

        #region 属性及构造

        /// <summary>消息监测交换对象
        /// </summary>
        protected internal DataMonitor_Msg _msgSwaper = new DataMonitor_Msg();
        /// <summary>消息处理对象
        /// </summary>
        protected internal MsgsHandler _msgsHandler = new MsgsHandler("zxcRobot");
        /// <summary>行情数据管理对象
        /// </summary>
        protected internal Data_Quote_Manager _managerQuote = new Data_Quote_Manager();
        /// <summary>是否初始
        /// </summary>
        protected internal bool _isInited = false;

        protected internal Robot_Manager()
        {
            this.Init();
        }
        ~Robot_Manager()
        {
            // 缓存数据？

            // 清理数据
        }

        #endregion


        /// <summary>初始 
        /// </summary>
        /// <returns></returns>
        public bool Init()
        {
            _isInited = true;
            return _isInited && this.InitMsgHandles();
        }
        /// <summary>初始消息处理对象集
        /// </summary>
        /// <returns></returns>
        public bool InitMsgHandles()
        {
            _msgsHandler.InitMsgHandle(typeof(MsgHandle_Print));
            //_MsgsHandler.InitMsgHandle(typeof(zxcRobot_Note_wx));

            zxcRobot_Note_wx pRobot_Note_wx = new zxcRobot_Note_wx(null, "");
            _msgsHandler.InitMsgHandle(pRobot_Note_wx.Tag, pRobot_Note_wx);

            zxcRobot_Point_growth pRobot_Point_growth = new zxcRobot_Point_growth(null, "");
            _msgsHandler.InitMsgHandle(pRobot_Point_growth.Tag, pRobot_Point_growth);

            zxcRobot_Quote_quantify pRobot_Quote_quantify = new zxcRobot_Quote_quantify(null, "");
            _msgsHandler.InitMsgHandle(pRobot_Quote_quantify.Tag, pRobot_Quote_quantify);

            return true;
        }


        //消息交换对象监测开始
        public bool Start()
        {
            return _msgSwaper.Start() && _managerQuote.Start(-1, 1);
        }
        //消息交换对象监测结束
        public bool Stop()
        {
            return _msgSwaper.Stop();
        }

    }
}
