using System;
using System.Collections.Generic;
using System.Linq;
using zxcCore.zxcRobot.User;

namespace zpCore.zpDataCache.Memory
{
    /// <summary>机器人-基类
    /// </summary>
    public abstract class RobotBase
    {
        #region 属性及构造

        protected internal string _Title = "";
        /// <summary>说明
        /// </summary>
        public string Title
        {
            get { return _Title; }
        }
        protected internal string _Title_alias = "";
        /// <summary>说明
        /// </summary>
        public string Title_alias
        {
            get { return _Title_alias; }
        }
        protected internal string _CmdStr = "";
        /// <summary>启动命令
        /// </summary>
        public string CmdStr
        {
            get { return _CmdStr; }
        }

        protected internal IUser _User = null;
        /// <summary>归属用户
        /// </summary>
        public IUser User
        {
            get { return _User; }
        }


        /// <summary>是否后台运行
        /// </summary>
        public bool IsBackProc
        {
            get; set;
        }
        /// <summary>有效时长(分钟)
        /// </summary>
        public int MaxTime
        {
            get; set;
        }

        public RobotBase(IUser User)
        {
            _Title = "RobotBase";
            _Title_alias = "";
            _CmdStr = "@@myRobot";
            _User = User;
        }
        ~RobotBase()
        {
            // 缓存数据？
        }

        #endregion

        public virtual bool InitSetting(dynamic setting)
        {
            return true;
        }

        public virtual bool Done(dynamic msg)
        {
            return true;
        }

        //消息通知
        public virtual bool NotifyMsg(dynamic msg)
        {
            return true;
        }
    }
}
