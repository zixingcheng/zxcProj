using System;
using System.Collections.Generic;
using System.Linq;
using zxcCore.zxcData.Cache.Memory;
using zxcCore.zxcRobot.Msger;

namespace zxcCore.zxcRobot.Monitor.Msger
{
    /// <summary>数据检查-消息管理类-行情
    /// </summary>
    public class DataCheck_Msger_Quote : DataCheck_Msger
    {
        #region 属性及构造

        protected internal static Msger_Wx _msger = new Msger_Wx();
        public DataCheck_Msger_Quote(bool isBuffer, int numsBuffer) : base(isBuffer, numsBuffer)
        {
            _IsBuffer = isBuffer;
            _NumsBuffer = numsBuffer;
            _MsgsBuffer = new List<dynamic>();
        }
        ~DataCheck_Msger_Quote()
        {
            // 缓存数据？
            _MsgsBuffer.Clear();
        }

        #endregion


        //消息通知
        public override bool NotifyMsg(dynamic msg)
        {
            return this.SendMsg(msg);
        }
        //消息发送
        public override bool SendMsg(dynamic msg)
        {
            return _msger.SendMsg(msg);
        }
        //消息日志
        public override bool LogMsg(dynamic msg)
        {
            return true;
        }
    }
}
