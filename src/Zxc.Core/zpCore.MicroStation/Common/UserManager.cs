using Microsoft.EntityFrameworkCore;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Linq.Dynamic.Core;
using zpCore.MicroStation.Models;

namespace zpCore.MicroStation.Common
{
    public class UserPermission
    {
        public bool HasPermission = false;
        public UserInfo User;
        public List<string> Citys = new List<string>();
        public List<string> TownStreets = new List<string>();
        public List<string> Communitys = new List<string>();
        public List<int> DelopyIds = new List<int>();

        public UserPermission(string strPermissions)
        {
            this.Init(strPermissions);
        }
        public void Init(string strPermissions)
        {
            Citys = new List<string>();
            TownStreets = new List<string>();
            Communitys = new List<string>();
            DelopyIds = new List<int>();
            if (strPermissions == null) return;

            string[] strPermissionss = strPermissions.Split(".");
            if (strPermissionss.Length > 1)
                TownStreets = strPermissionss[1].Split(",").ToList();
            if (strPermissionss.Length > 2)
                Communitys = strPermissionss[2].Split(",").ToList();
            if (strPermissionss.Length > 3)
            {
                List<string> Delopyss = strPermissionss[3].Split(",").ToList();
                foreach (var item in Delopyss)
                {
                    DelopyIds.Add(Convert.ToInt32(item));
                }
            }
            HasPermission = true;
        }
    }

    public class UserManger
    {
        public Dictionary<string, UserInfo> UserInfos;
        public UserInfo UserDefault;

        public UserManger()
        {
            this.Init();
        }
        public void Init()
        {
            UserInfos = new Dictionary<string, UserInfo>();
            var optionsBuilder = new DbContextOptionsBuilder<db_MicroStationContext>();
            using (var context = new db_MicroStationContext(optionsBuilder.Options))
            {
                var queryAll = context.UserInfo.AsQueryable().Where("Useroid != @0", "").ToList();
                foreach (var item in queryAll)
                {
                    UserInfos.Add(item.UserInfoOid, item);
                }
            }

            UserDefault = new UserInfo()
            {
                Useroid = "863fd12b50ce401e8481ed902a59ca9-",
                Userid = "ADMIN-TEST",
                Username = "ADMIN",
                Userphone = "138272990**",
                Organizationoid = "b017665d8c6348d091c17f8e250437**",
                Groupname = "东莞市生态环境局南城分局",
                Permission = ".南城"
            };
            UserInfos.Add(UserDefault.Useroid, UserDefault);
        }
        public UserInfo GetUser(string usrName)
        {
            if (usrName + "" == "") return UserDefault;
            foreach (var item in UserInfos.Values)
            {
                if (item.Userid == usrName || item.Username == usrName || item.Userphone == usrName)
                    return item;
            }
            return UserDefault;
        }
    }

}