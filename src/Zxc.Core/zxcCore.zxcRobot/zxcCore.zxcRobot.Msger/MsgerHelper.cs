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
using System.Collections.Generic;

namespace zxcCore.zxcRobot.Msger
{
    /// <summary>消息管理类
    /// </summary>
    public class MsgerHelper
    {
        #region 属性及构造

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
        protected internal List<dynamic> _MsgsBuffer = null;
        public List<dynamic> MsgsBuffer
        {
            get { return _MsgsBuffer; }
        }

        public MsgerHelper(bool isBuffer, int numsBuffer)
        {
        }
        ~MsgerHelper()
        {
            // 缓存数据？
            _MsgsBuffer.Clear();
        }

        #endregion


        public virtual bool SendMsg(dynamic msg, List<typeMsger> typeMsgs)
        {
            bool bResult = true;
            for (int i = 0; i < typeMsgs.Count; i++)
            {
                bResult = bResult && this.SendMsg(msg, typeMsgs[i]);
            }
            return bResult;
        }
        public virtual bool SendMsg(dynamic msg, typeMsger typeMsg)
        {
            return true;
        }
    }
}
