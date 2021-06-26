using System;
using System.Collections.Generic;
using System.Linq;
using zpCore.zpDataCache.Memory;
using zxcCore.zxcRobot.Msger;

namespace zxcCore.zxcRobot.Monitor.Msg
{
    /// <summary>消息处理器
    /// </summary>
    public class MsgsHandler
    {
        #region 属性及构造

        protected internal string _tag = "";
        public string Tag
        {
            get { return _tag; }
        }

        protected internal Dictionary<string, MsgHandle> _MsgHandles = null;
        public Dictionary<string, MsgHandle> MsgHandles
        {
            get { return _MsgHandles; }
        }

        public MsgsHandler(string tagName)
        {
            _tag = tagName;
            _MsgHandles = new Dictionary<string, MsgHandle>();

            MsgerHelper.Msger.MsgCached += new MsgCached_EventHandler(MsgCached_EventHandler);
        }
        ~MsgsHandler()
        {
            // 缓存数据？
        }

        #endregion


        /// <summary>初始消息处理对象
        /// </summary>
        /// <param name="tagName">标识名称</param>
        /// <param name="msgHandle">消息处理对象</param>
        /// <param name="isCanCover">是否直接覆盖</param>
        /// <returns></returns>
        public virtual bool InitMsgHandle(string tagName, MsgHandle msgHandle, bool isCanCover = false)
        {
            bool bResult = false;
            if (isCanCover)
            {
                _MsgHandles[tagName] = msgHandle; bResult = true;
            }
            else
            {
                //不存在时添加
                if (!_MsgHandles.ContainsKey(tagName))
                {
                    _MsgHandles.Add(tagName, msgHandle); bResult = true;
                }
            }
            return bResult;
        }
        //初始数据检查对象
        public bool InitMsgHandle(Type dest_ClassType)
        {
            string setting = "";
            var instance = this.CreateMsgHandle(dest_ClassType, setting);
            MsgHandle pMsgHandle = (MsgHandle)instance;
            if (pMsgHandle != null)
            {
                this.InitMsgHandle(pMsgHandle.Tag, pMsgHandle);
            }
            return true;
        }
        //创建对象-泛型实现
        protected internal dynamic CreateMsgHandle(Type dest_ClassType, string setting)
        {
            if (dest_ClassType == null) return null;
            var instance = Activator.CreateInstance(dest_ClassType, new object[] { dest_ClassType.Name, setting });
            return instance;
        }


        /// <summary>处理消息
        /// </summary>
        /// <param name="msg"></param>
        /// <returns></returns>
        public virtual bool HandleMsg(Msger.Msg msg)
        {
            bool bResult = true;
            foreach (KeyValuePair<string, MsgHandle> msgHandle in _MsgHandles)
            {
                bResult = msgHandle.Value.HandleMsg(msg) && bResult;
            }
            return bResult;
        }


        /// <summary>消息缓存事件,触发消息处理
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        protected internal virtual void MsgCached_EventHandler(object sender, MsgCached_Event e)
        {
            this.HandleMsg(e.MsgInfo);
        }

    }
}
