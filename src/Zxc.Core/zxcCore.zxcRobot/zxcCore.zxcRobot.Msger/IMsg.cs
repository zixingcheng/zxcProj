using System;
using System.Collections.Generic;

namespace zxcCore.zxcRobot.Msger
{    
    /// <summary>消息类型
     /// </summary>
    public enum typeMsg
    {
        TEXT = 0,
        IMAGE = 1
    }
    public interface IMsg
    {
        List<typeMsger> DestTypeMsger { get; set; }
        string MsgID { get; set; }
        string MsgInfo { get; set; }
        string MsgLink { get; set; }
        DateTime MsgTime { get; set; }
        typeMsg MsgType { get; set; }
        string UserID_Src { get; set; }
        bool IsUserGroup { get; set; }
        string UserID_To { get; set; }

        dynamic ToDict();
    }
}