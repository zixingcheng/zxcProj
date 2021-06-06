//===============================================================================
// Copyright @ 2021 Guangzhou Yijian Life Technology Co.,Ltd. All rights reserved.
// Copyright @ 2021 广州易简生活科技有限公司.  版权所有.
//===============================================================================
// 文件名称： 
// 功能描述：Robot_Manager --机器人管理类
// 创建标识：zxc   2021-03-24
// 修改标识： 
// 修改描述：
//===============================================================================
using System.Collections.Generic;
using zxcCore.zxcRobot.Monitor.Msg;

namespace zxcCore.zxcRobot.Robot
{
    /// <summary>数据缓存集管理类集中管理类
    /// </summary>
    public class Robot_Manager
    {
        public static readonly Robot_Manager _Manager = new Robot_Manager();

        #region 属性及构造

        /// <summary>消息监测交换对象
        /// </summary>
        protected internal DataMonitor_Msg _MsgSwaper = new DataMonitor_Msg();
        /// <summary>消息处理对象
        /// </summary>
        protected internal MsgsHandler _MsgsHandler = new MsgsHandler("zxcRobot");
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
            _MsgsHandler.InitMsgHandle(typeof(MsgHandle_Print));
            return true;
        }

        //消息交换对象监测开始
        public bool Start()
        {
            return _MsgSwaper.Start();
        }
        //消息交换对象监测结束
        public bool Stop()
        {
            return _MsgSwaper.Stop();
        }

    }
}
