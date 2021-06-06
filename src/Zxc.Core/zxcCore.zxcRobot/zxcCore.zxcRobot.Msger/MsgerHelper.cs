//===============================================================================
// Copyright @ 2021 Guangzhou Yijian Life Technology Co.,Ltd. All rights reserved.
// Copyright @ 2021 广州易简生活科技有限公司.  版权所有.
//===============================================================================
// 文件名称： 
// 功能描述：GModel --消息管理类
// 创建标识：zxc   2021-01-26
// 修改标识： 
// 修改描述：
//===============================================================================
using System;
using System.Collections.Generic;

namespace zxcCore.zxcRobot.Msger
{
    /// <summary>消息管理类
    /// </summary>
    public class MsgerHelper
    {
        #region 属性及构造

        /// <summary>全局消息缓存对象
        /// </summary>
        public static readonly MsgerHelper Msger = new MsgerHelper(true, -1);

        protected internal Dictionary<string, IMsger> _MsgsHandle = null;
        public Dictionary<string, IMsger> MsgsHandle
        {
            get { return _MsgsHandle; }
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
        protected internal List<IMsg> _MsgsBuffer = new List<IMsg>();
        public List<IMsg> MsgsBuffer
        {
            get { return _MsgsBuffer; }
        }

        public MsgerHelper(bool isBuffer = true, int numsBuffer = -1)
        {
            _IsBuffer = isBuffer;
            _NumsBuffer = numsBuffer;
        }
        ~MsgerHelper()
        {
            // 缓存数据？
            _MsgsBuffer.Clear();
        }

        #endregion

        /// <summary>查找消息对象（按类型）
        /// </summary>
        /// <param name="typeMsg"></param>
        /// <returns></returns>
        public virtual IMsger Find(typeMsger typeMsg)
        {
            return Find(typeMsg.ToString());
        }
        /// <summary>查找消息对象（按类型）
        /// </summary>
        /// <param name="typeMsg"></param>
        /// <returns></returns>
        public virtual IMsger Find(string typeMsg)
        {
            IMsger msger = null;
            _MsgsHandle.TryGetValue(typeMsg.ToLower(), out msger);
            return msger;
        }

        /// <summary>发送消息（多个消息类型）
        /// </summary>
        /// <param name="msg"></param>
        /// <param name="typeMsgs"></param>
        /// <returns></returns>
        public virtual bool SendMsg(dynamic msg, List<typeMsger> typeMsgs)
        {
            bool bResult = true;
            for (int i = 0; i < typeMsgs.Count; i++)
            {
                bool bRes = this.SendMsg(msg, typeMsgs[i]);
                bResult = bResult && bRes;
            }
            return bResult;
        }
        /// <summary>发送消息（指定消息类型）
        /// </summary>
        /// <param name="msg"></param>
        /// <param name="typeMsgs"></param>
        /// <returns></returns>
        public virtual bool SendMsg(dynamic msg, typeMsger typeMsg)
        {
            IMsger msger = null;
            _MsgsHandle.TryGetValue(typeMsg.ToString().ToLower(), out msger);

            if (msger != null)
            {
                bool bRes = msger.SendMsg(msg);
                if (bRes)
                {
                    this.CacheMsg(msg);
                }
                return bRes;
            }
            return false;
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
        /// <summary>查找消息
        /// </summary>
        /// <param name="match"></param>
        /// <returns></returns>
        public virtual List<IMsg> FindMsg(Predicate<IMsg> match)
        {
            return _MsgsBuffer.FindAll(match);
        }

    }
}
