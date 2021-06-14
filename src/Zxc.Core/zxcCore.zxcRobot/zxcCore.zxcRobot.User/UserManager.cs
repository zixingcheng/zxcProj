//===============================================================================
// Copyright @ 2021 Guangzhou Yijian Life Technology Co.,Ltd. All rights reserved.
// Copyright @ 2021 广州易简生活科技有限公司.  版权所有.
//===============================================================================
// 文件名称： 
// 功能描述：zxcRobot --用户管理类
// 创建标识：zxc   2021-03-22
// 修改标识： 
// 修改描述：
//===============================================================================
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using zxcCore.Common;
using zxcCore.Extensions;
using zxcCore.zxcDataCache.MemoryDB;
using zxcCore.zxcRobot.User;

namespace zxcCore.zxcRobot.User
{
    /// <summary>用户管理类
    /// </summary>
    public class UserManager : Data_DB
    {
        public static readonly UserManager _Users = new UserManager("");

        #region 属性及构造

        /// <summary>库表--zxc系统
        /// </summary>
        public DataUser_zxc<User_zxc> _userZxc { get; set; }
        /// <summary>库表--wx平台
        /// </summary>
        public DataUser_wx<User_wx> _userWx { get; set; }

        protected internal UserManager(string dirBase) : base(dirBase, typePermission_DB.Normal, true, "/Datas/DB_User")
        {
            this.InitUser_system();
        }

        #endregion


        protected override void OnDBModelCreating()
        {
            base.OnDBModelCreating();

            //初始zxc用户信息
            _userZxc = new DataUser_zxc<User_zxc>(); this.InitDBModel(_userZxc);
        }

        /// <summary>初始系统用户
        /// </summary>
        protected void InitUser_system()
        {
            //初始系统账户
            User_zxc sysAdmin = _userZxc.Find(e => e.usrName == "admin");
            if (sysAdmin == null)
            {
                sysAdmin = new User_zxc()
                {
                    usrID = Guid.NewGuid().ToString(),
                    usrPW = "zxcvbnm123",
                    usrName = "admin",
                    usrNameNick = "系统管理员",
                    usrType = typeUser.sysadmin
                };
                _userZxc.Add(sysAdmin, true);
            }

            //消息平台信息初始
            ConfigurationHelper configDataCache = new ConfigurationHelper("appsettings.json");
            string usrMsger_wx = _configDataCache.config["Msgerset:Msger_Wx:UsrName_Root"] + "";
            User_Base userWx = new User_Base()
            {
                usrID = Guid.NewGuid().ToString(),
                usrName = usrMsger_wx,
                usrNameNick = "admin",
                usrPlat = typeUserPlat.wx.ToString()
            };
            this.InitUser_system(userWx);
            _userZxc.SaveChanges();
        }
        protected void InitUser_system(IUser user)
        {
            List<User_zxc> lstUsr = _userZxc.FindAll(e => e.usrName_wx == user.usrName || e.usrName_wx == user.usrNameNick || e.usrPhone == user.usrPhone || e.usrName == user.usrName || e.usrName == user.usrNameNick);

            User_zxc usrZxc = null;
            if (lstUsr.Count == 0)
            {
                //初始系统账户
                usrZxc = new User_zxc()
                {
                    usrID = Guid.NewGuid().ToString(),
                    usrPW = "666888",
                    usrName = string.IsNullOrEmpty(user.usrName) ? user.usrNameNick : user.usrName,
                    usrNameNick = user.usrNameNick
                };
            }
            else if (lstUsr.Count == 1)
            {
                usrZxc = lstUsr[0];
            }

            //设置第三方平台关联账户
            switch (user.usrPlat)
            {
                case "wx":
                    usrZxc.usrName_wx = user.usrName;
                    _userWx.Add((User_wx)user, true);
                    break;
                default:
                    break;
            }
            _userZxc.Add(usrZxc, true);
        }


        /// <summary>lambda操作（外部传入参数）
        /// </summary>
        /// <param name="source">源对象</param>
        /// <param name="predicate">lambda对象</param>
        /// <returns></returns>
        public User_zxc GetUser(Func<IEnumerable<User_zxc>, IEnumerable<User_zxc>> predicate)
        {
            return Lambda.LambdaDo<User_zxc>(_userZxc, predicate).First();
        }
        /// <summary>提取指定平台系统用户信息
        /// </summary>
        /// <param name="usrName"></param>
        /// <param name="usrNameNick"></param>
        /// <param name="usrPlat"></param>
        /// <returns></returns>
        public User_zxc GetUser(string usrName, string usrNameNick, string usrPlat)
        {
            //查询用户信息--特定
            Func<IEnumerable<User_Base>, IEnumerable<User_Base>> predicate = p => p.Where(e => e.usrName == usrName || e.usrNameNick == usrNameNick);
            User_Base usr = UserManager._Users.GetUser(predicate, usrPlat);
            if (usr == null) return null;

            //查询系统用户对应配置           
            switch (usrPlat)
            {
                case "wx":
                    return _userZxc.Find(e => e.usrName == usr.usrName || e.usrName == usr.usrNameNick || e.usrNameNick == usr.usrNameNick || e.usrName_wx == usr.usrName);
                default:
                    break;
            }
            return _userZxc.Find(e => e.usrName == usr.usrName || e.usrName == usr.usrNameNick || e.usrNameNick == usr.usrNameNick);
        }

        public User_Base GetUser(Func<IEnumerable<User_Base>, IEnumerable<User_Base>> predicate, typeUserPlat userPlat = typeUserPlat.zxc)
        {
            return GetUser(predicate, userPlat.ToString());
        }
        public User_Base GetUser(Func<IEnumerable<User_Base>, IEnumerable<User_Base>> predicate, string userPlat)
        {
            switch (userPlat)
            {
                case "wx":
                    return (Lambda.LambdaDo<User_Base>(_userWx, predicate)).Where(e => e.IsDel == false).First();
                default:
                    break;
            }
            return (Lambda.LambdaDo<User_Base>(_userZxc, predicate)).Where(e => e.IsDel == false).First();
        }


        //public void GetUser<T>(IEnumerable<T> source, Func<IEnumerable<T>, IEnumerable<T>> predicate)
        //{
        //    var aa = predicate(source);
        //    _userZxc[1].usrName = "guest";
        //    //return _userZxc.Where(predicate).First();
        //    return;
        //}
        //
        //
        //Func<IEnumerable<int>, IEnumerable<int>> expr1 =
        //       l => l.Where(n => n > 6).OrderBy(n => n % 2 == 0).Select(n => n);
        //
        //Func<IEnumerable<int>, IEnumerable<int>> expr2 =
        //               l => l.TakeWhile((n, index) => n >= index);
        //public void UseLambda<T>(IEnumerable<T> source
        //                  , Func<IEnumerable<T>, IEnumerable<T>> lambda)
        //{
        //    var items = lambda(source);
        //
        //    foreach (var item in items)
        //        Console.Writeline(item.ToString());
        //}
    }
}
