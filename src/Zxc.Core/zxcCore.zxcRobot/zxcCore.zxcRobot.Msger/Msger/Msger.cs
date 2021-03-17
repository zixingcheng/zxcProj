using System.Collections.Generic;
using zxcCore.Common;

namespace zxcCore.zxcRobot.Msger
{
    /// <summary>消息管理类
    /// </summary>
    public class Msger : IMsger
    {
        #region 属性及构造

        protected internal typeMsger _TypeMsg;
        public typeMsger TypeMsg
        {
            get { return _TypeMsg; }
        }

        protected internal string _Tag = "";
        public string Tag
        {
            get { return _Tag; }
        }

        protected internal bool _IsBuffer = false;
        public bool IsBuffer
        {
            get { return _IsBuffer; }
        }
        protected internal int _NumsBuffer = 100;
        public int NumsBuffer
        {
            get { return _NumsBuffer; }
        }
        protected internal List<dynamic> _MsgsBuffer = null;
        public List<dynamic> MsgsBuffer
        {
            get { return _MsgsBuffer; }
        }

        //静态Msg配置信息
        protected internal static ConfigurationHelper _configMsgSet = new ConfigurationHelper("appsettings.json");

        public Msger(bool isBuffer = false, int numsBuffer = 100)
        {
        }
        ~Msger()
        {
            // 缓存数据？
            _MsgsBuffer.Clear();
        }

        #endregion


        public virtual bool SendMsg(dynamic msg)
        {
            return true;
        }
        public virtual bool SendMsg(dynamic msg, string url)
        {
            return true;
        }
        public virtual bool LogMsg(dynamic msg)
        {
            return true;
        }
    }
}
