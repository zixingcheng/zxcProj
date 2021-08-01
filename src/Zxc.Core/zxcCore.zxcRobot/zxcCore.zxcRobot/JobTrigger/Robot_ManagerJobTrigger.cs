using System;
using System.IO;
using System.Linq;
using System.Threading;
using System.Collections.Generic;
using zxcCore.Common.JobTrigger;
using zxcCore.zxcRobot.Msger;
using zxcCore.zxcRobot.Robot;
using zxcCore.Common;

namespace zxcCore.zxcRobot.JobTrigger
{
    //Robot_Manager启动线程
    public class Robot_ManagerJobTrigger : BaseJobTrigger
    {
        public Robot_ManagerJobTrigger() :
            base(TimeSpan.FromSeconds(8), TimeSpan.FromMinutes(5),
                new Robot_ManagerJobExcutor(TimeSpan.FromHours(24)), true)
        {
        }
    }


    public class Robot_ManagerJobExcutor : JobExecutor
    {
        DateTime dtDay = zxcTimeHelper.checkTimeD(DateTime.Now);
        public Robot_ManagerJobExcutor(TimeSpan dueTime) :
            base(dueTime)
        {
        }


        public override void StartJob()
        {
            if (this._isInited) return;

            //执行
            this.Print();

            this.Init();
            SyncRobot_Manager();

            this.Print(false);
        }


        /// <summary>机器人管理器开始执行
        /// </summary>
        public void SyncRobot_Manager()
        {
            //机器人测试
            MsgerHelper.Msger.MsgCached += new MsgCached_EventHandler(this.MsgCached_EventHandler);
            Robot_Manager._Manager.Start();
            _isInited = true;


            //模拟长时间运算
            while (this.IsVaild())
            {
                Thread.Sleep(2000);
                DateTime dtDayNow = zxcTimeHelper.checkTimeD(DateTime.Now);
                if (dtDayNow.Day > dtDay.Day)
                {
                    dtDay = dtDayNow; break;
                }
            }

            //退出
            _isInited = false;
            MsgerHelper.Msger.MsgCached -= new MsgCached_EventHandler(this.MsgCached_EventHandler);
            Robot_Manager._Manager.Stop();
        }

        //消息缓存事件
        private void MsgCached_EventHandler(object sender, MsgCached_Event e)
        {
            //Console.WriteLine(DateTime.Now + "::");
            //Console.WriteLine("**********{0}:: {1}", e.MsgInfo.msgID, e.MsgInfo.msgContent);
        }

    }
}