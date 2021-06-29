using System;
using System.Collections.Generic;
using zxcCore.Common;
using zxcCore.zxcData.Cache.MemoryDB;

namespace zxcCore.zxcRobot.User
{
    /// <summary>用户类-微信
    /// </summary>
    public class User_wx : User_Base
    {
        #region 属性及构造

        public User_wx()
        {
            usrPlat = "wx";
        }
        ~User_wx()
        {
            // 缓存数据？
        }

        #endregion

    }
}
