using System;
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

        protected internal string _pathMsgSwap = "";
        protected internal string _url = "";
        protected internal bool _useApi;
        protected internal bool _useGet;
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
        protected internal List<IMsg> _MsgsBuffer = new List<IMsg>();
        public List<IMsg> MsgsBuffer
        {
            get { return _MsgsBuffer; }
        }

        //静态Msg配置信息
        protected internal static zxcConfigurationHelper _configMsgSet = new zxcConfigurationHelper("appsettings.json");

        public Msger(bool useApi = true, bool useGet = true, bool isBuffer = false, int numsBuffer = 100)
        {
            _IsBuffer = isBuffer;
            _NumsBuffer = numsBuffer;

            _Tag = "None";
            _TypeMsg = typeMsger.None;
            _useApi = useApi;
            _useGet = useGet;
        }
        ~Msger()
        {
            // 缓存数据？
            _MsgsBuffer.Clear();
        }

        #endregion

        /// <summary>发送消息（需重写）
        /// </summary>
        /// <param name="msg"></param>
        /// <returns></returns>
        public virtual bool SendMsg(dynamic msg)
        {
            //return this.CacheMsg(msg);
            return false;
        }
        /// <summary>发送消息（需重写）
        /// </summary>
        /// <param name="msg"></param>
        /// <returns></returns>
        public virtual bool SendMsg(dynamic msg, string url)
        {
            //return this.CacheMsg(msg);
            return false;
        }


        /// <summary>查找消息
        /// </summary>
        /// <param name="match"></param>
        /// <returns></returns>
        public virtual List<IMsg> FindMsg(Predicate<IMsg> match)
        {
            return _MsgsBuffer.FindAll(match);
        }
        /// <summary>缓存消息
        /// </summary>
        /// <param name="msg"></param>
        /// <returns></returns>
        public virtual bool CacheMsg(dynamic msg, bool isFromRobot = false)
        {
            if (_IsBuffer == false) return false;

            //组装消息
            IMsg pMsg = (IMsg)msg;
            if (pMsg == null) return false;

            //缓存消息
            if (isFromRobot)
                pMsg.IsFromRobot = true;
            _MsgsBuffer.Add(pMsg);

            //保持缓存数量
            if (_NumsBuffer > 0 && _MsgsBuffer.Count > _NumsBuffer)
            {
                _MsgsBuffer.RemoveRange(_MsgsBuffer.Count, _MsgsBuffer.Count - _NumsBuffer);
            }
            return true;
        }
        /// <summary>记录消息日志
        /// </summary>
        /// <param name="msg"></param>
        /// <returns></returns>
        public virtual bool LogMsg(dynamic msg)
        {
            return true;
        }

    }
}
