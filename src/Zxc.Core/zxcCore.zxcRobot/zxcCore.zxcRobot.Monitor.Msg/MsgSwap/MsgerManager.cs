using System;
using System.Collections.Generic;
using System.Linq;
using zxcCore.zxcRobot.Msger;

namespace zxcCore.zxcRobot.Monitor.Msg
{
    /// <summary>消息管理类
    /// </summary>
    public class MsgerManager : MsgerHelper
    {
        #region 属性及构造

        public MsgerManager(bool isBuffer, int numsBuffer) : base(isBuffer, numsBuffer)
        {
        }
        ~MsgerManager()
        {
            // 缓存数据？
        }

        #endregion


        //public override bool NotifyMsg(dynamic msg)
        //{
        //    return true;
        //}
        //public override bool SendMsg(dynamic msg)
        //{
        //    return true;
        //}
        //public override bool LogMsg(dynamic msg)
        //{
        //    return true;
        //}
    }
}
