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
using zxcCore.Common;

namespace zxcCore.zxcRobot.Msger
{
    /// <summary>消息管理类
    /// </summary>
    public class MsgerHelper
    {
        #region 属性及构造
        //静态Msg配置信息
        protected internal readonly static zxcConfigurationHelper _configMsgSet = new zxcConfigurationHelper("appsettings.json");
        //消息库
        protected internal static DataDB_Msg _dbMsg = null;
        /// <summary>全局消息缓存对象
        /// </summary>
        public static readonly MsgerHelper Msger = new MsgerHelper(true, -1);


        /// <summary>消息已缓存事件
        /// </summary>
        public event MsgCached_EventHandler MsgCached;


        protected internal Dictionary<string, IMsger> _MsgersObj = null;
        public Dictionary<string, IMsger> MsgersObj
        {
            get { return _MsgersObj; }
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

        protected internal string _dirMsgDB = null;
        protected internal bool _cacheDebug = true;
        public DataTable_Msg<Msg> MsgsCaches
        {
            get { return _dbMsg.Data_Msg; }
        }


        public MsgerHelper(bool isBuffer = true, int numsBuffer = -1)
        {
            _IsBuffer = isBuffer;
            _NumsBuffer = numsBuffer;
            _MsgersObj = new Dictionary<string, IMsger>();
            this.InitMsger("Wx", new Msger_Wx());
            this.InitMsger("Sys", new Msger_Sys());

            _dirMsgDB = MsgerHelper._configMsgSet.config["Msgerset:MsgDB_Path"] + "";
            _cacheDebug = Convert.ToBoolean(MsgerHelper._configMsgSet.config["Msgerset:MsgCache_Debug"]);
            if (MsgerHelper._dbMsg == null)
                MsgerHelper._dbMsg = new DataDB_Msg(_dirMsgDB);

            if (_cacheDebug)
                zxcConsoleHelper.Print(false, "消息管理器::全局 \n   >> 已启动.  -- {0}.", DateTime.Now.ToString());
        }
        ~MsgerHelper()
        {
            // 缓存数据？
            //_MsgsBuffer.Clear();
        }

        #endregion


        /// <summary>初始消息接口
        /// </summary>
        /// <param name="tagName">标识名称</param>
        /// <param name="msgHandle">消息处理对象</param>
        /// <param name="isCanCover">是否直接覆盖</param>
        /// <returns></returns>
        public virtual bool InitMsger(string tagName, IMsger msgHandle, bool isCanCover = false)
        {
            bool bResult = false;
            tagName = tagName.ToLower();
            if (isCanCover)
            {
                _MsgersObj[tagName] = msgHandle; bResult = true;
            }
            else
            {
                //不存在时添加
                if (!_MsgersObj.ContainsKey(tagName))
                {
                    _MsgersObj.Add(tagName, msgHandle); bResult = true;
                }
            }
            return bResult;
        }
        //初始数据检查对象
        public bool InitMsger(Type dest_ClassType)
        {
            var instance = this.CreateMsger(dest_ClassType);
            Msger pMsger = (Msger)instance;
            if (pMsger != null)
            {
                this.InitMsger(pMsger.Tag, pMsger);
            }
            return true;
        }
        //创建对象-泛型实现
        protected internal dynamic CreateMsger(Type dest_ClassType, bool useApi = true, bool useGet = true, bool isBuffer = false, int numsBuffer = 100)
        {
            if (dest_ClassType == null) return null;
            var instance = Activator.CreateInstance(dest_ClassType, new object[] { dest_ClassType.Name, useApi, useGet, isBuffer, numsBuffer });
            return instance;
        }


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
            _MsgersObj.TryGetValue(typeMsg.ToLower(), out msger);
            return msger;
        }


        /// <summary>发送消息（多个消息类型）
        /// </summary>
        /// <param name="msg"></param>
        /// <param name="typeMsgs"></param>
        /// <param name="useMsgServer"></param>
        /// <returns></returns>
        public virtual bool SendMsg(dynamic msg, List<typeMsger> typeMsgs, bool useMsgServer = false)
        {
            bool bResult = true;
            for (int i = 0; i < typeMsgs.Count; i++)
            {
                bool bRes = this.SendMsg(msg, typeMsgs[i], useMsgServer);
                bResult = bResult && bRes;
            }
            return bResult;
        }
        /// <summary>发送消息（指定消息类型）
        /// </summary>
        /// <param name="msg"></param>
        /// <param name="typeMsgs"></param>
        /// <param name="useMsgServer"></param>
        /// <returns></returns>
        public virtual bool SendMsg(dynamic msg, typeMsger typeMsg, bool useMsgServer = false)
        {
            IMsger msger = null;
            _MsgersObj.TryGetValue(typeMsg.ToString().ToLower(), out msger);

            if (msger != null)
            {
                bool bRes = msger.SendMsg(msg, useMsgServer);
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
            Msg pMsg = (Msg)msg;
            if (pMsg == null) return false;

            //缓存消息
            if (isFromRobot)
                pMsg.IsFromRobot = true;
            MsgsCaches.Add(pMsg);
            if (_cacheDebug)
                zxcConsoleHelper.Debug(true, "CacheMsg:: {0}({1}):: {2}", pMsg.msgTime, pMsg.msgID, pMsg.msgContent);

            //触发消息已缓存事件
            if (this.MsgCached != null)
            {
                MsgCached_Event pArgs = new MsgCached_Event(pMsg);
                this.MsgCached(this, pArgs);
            }

            //保持缓存数量
            //if (_NumsBuffer > 0 && MsgsCaches.Count > _NumsBuffer)
            //{
            //    _MsgsBuffer.RemoveRange(_MsgsBuffer.Count, _MsgsBuffer.Count - _NumsBuffer);
            //}
            return true;
        }
        /// <summary>查找消息
        /// </summary>
        /// <param name="match"></param>
        /// <returns></returns>
        public virtual List<Msg> FindMsg(Predicate<IMsg> match)
        {
            return MsgsCaches.FindAll(match);
        }

    }
}
