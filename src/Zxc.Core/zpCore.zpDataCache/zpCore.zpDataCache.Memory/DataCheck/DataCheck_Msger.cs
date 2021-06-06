using System;
using System.Collections.Generic;
using System.Linq;

namespace zpCore.zpDataCache.Memory
{
    /// <summary>数据检查-消息管理类
    /// </summary>
    public class DataCheck_Msger : IDataCheck_Msger
    {
        #region 属性及构造

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


        public DataCheck_Msger(bool isBuffer, int numsBuffer)
        {
            _IsBuffer = isBuffer;
            _NumsBuffer = numsBuffer;
            _MsgsBuffer = new List<dynamic>();
        }
        ~DataCheck_Msger()
        {
            // 缓存数据？
            _MsgsBuffer.Clear();
        }

        #endregion


        public virtual bool NotifyMsg(dynamic msg)
        {
            return true;
        }
        public virtual bool SendMsg(dynamic msg)
        {
            return true;
        }
        public virtual bool LogMsg(dynamic msg)
        {
            return true;
        }
    }
}
