using System;

namespace zxcCore.zxcRobot.User
{
    public interface IUser
    {
        DateTime creatTime { get; set; }
        bool isGroup { get; set; }
        DateTime modifyTime { get; set; }
        string usrID { get; set; }
        string usrPW { get; set; }
        string usrName { get; set; }
        string usrNameNick { get; set; }
        string usrNameRemarks { get; set; }
        string usrNameLabel { get; set; }
        string usrPhone { get; set; }
        string usrDescribe { get; set; }
        string usrPlat { get; set; }
        
    }
}