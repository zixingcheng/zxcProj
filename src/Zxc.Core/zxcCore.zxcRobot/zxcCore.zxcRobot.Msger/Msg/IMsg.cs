﻿using System;
using System.Collections.Generic;

namespace zxcCore.zxcRobot.Msger
{
    /// <summary>消息类型
    /// </summary>
    public enum typeMsg
    {
        NOTE = -1,
        TEXT = 0,
        IMAGE = 1
    }
    public interface IMsg
    {
        string groupID { get; set; }
        bool IsSend { get; set; }
        bool IsUserGroup { get; set; }
        bool IsFromRobot { get; set; }
        bool IsSaved { get; set; }
        string msg { get; set; }
        string msgContent { get; set; }
        string msgID { get; set; }
        string msgLink { get; set; }
        DateTime msgTime { get; set; }
        typeMsg msgType { get; set; }
        string msgTag { get; set; }
        
        string UserName_src { get; set; }
        string usrID { get; set; }
        string usrName { get; set; }
        string usrNameNick { get; set; }
        typeMsger usrPlat { get; set; }

        string GetNameGroup();
        string GetNameUser();

        dynamic ToDict();
    }
}