using System;
using System.Collections.Generic;

namespace zpCore.MicroStation.Models
{
    public partial class UserInfo
    {
        public string UserInfoOid { get; set; }
        public string Useroid { get; set; }
        public string UserPwd { get; set; }
        public string Userid { get; set; }
        public string Username { get; set; }
        public string Userphone { get; set; }
        public string Organizationoid { get; set; }
        public string Groupname { get; set; }
        public string Nodepath { get; set; }
        public ulong Isitavailable { get; set; }
        public string Permission { get; set; }
        public ulong? Permissioncreated { get; set; }
        public DateTime? Permissioncreatedt { get; set; }
    }
}
