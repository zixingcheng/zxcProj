using System;
using System.Collections.Generic;
using System.Linq;
using zpCore.zpDataCache.Memory;
using zxcCore.Common;

namespace zxcCore.zxcRobot.Monitor.Msg
{
    /// <summary>消息处理
    /// </summary>
    public class MsgHandle_Print : MsgHandle
    {
        #region 属性及构造

        public MsgHandle_Print(string tagName, string setting) : base("", setting)
        {
            _tag = "MsgPrint";
            _tagAlias = "实时打印";
        }
        ~MsgHandle_Print()
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

        /// <summary>消息处理实现
        /// </summary>
        /// <returns></returns>
        public override bool HandleMsg_Do(Msger.Msg msg)
        {
            //打印信息
            zxcConsoleHelper.Debug(true, "MsgHandle_Print:: {0}   ---{1}.", this.getMsg_Perfix(msg), msg.msgTime);
            //this.NotifyMsg(msg.msgContent, "@*测试群");
            return true;
        }


        protected internal override string getMsg_Perfix(Msger.Msg msg)
        {
            return string.Format("{0}", msg.msgContent);
        }

    }
}
